"""Deterministic validation and persistence of AI/user Research Judgments."""

import uuid
from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from backend.domain import models, schemas
from backend.domain.services.research_coverage import confirmed_word_refs

# Contract types whose governed occurrence unit is the word-level root occurrence
# (StructuralToken word_ref), not the verse/lexeme-level CorpusOccurrence.
WORD_LEVEL_CONTRACTS = frozenset({"ROOT_CONCEPT"})


@dataclass(frozen=True)
class EvidenceResolution:
    valid: bool
    reasons: tuple[str, ...]
    occurrence_ids: frozenset[str]
    # Word-level root occurrence identities (StructuralToken word_refs) resolved
    # from `token:`/token-referencing-observation evidence for word-level contracts.
    token_word_refs: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class JudgmentDecision:
    accepted: bool
    reasons: tuple[str, ...]
    completeness: dict[str, object]


def _token_reject_reason(
    db: Session, run: models.ResearchRun, ref: str, word_ref: str
) -> str:
    """Precise reason a word-level token evidence ref is inadmissible.

    Validity is defined as membership in the run's confirmed occurrence set; this
    helper only explains WHY a non-member failed (wrong snapshot/absent, wrong
    root, or non-CONFIRMED attribution) so negative controls get exact messages.
    """
    rows = (
        db.query(models.StructuralToken)
        .filter(
            models.StructuralToken.snapshot_id == run.corpus_snapshot,
            models.StructuralToken.word_ref == word_ref,
        )
        .all()
    )
    if not rows:
        return f"Evidence reference '{ref}' is absent or outside the run corpus"
    latest = max(r.extraction_version for r in rows)
    current = [r for r in rows if r.extraction_version == latest]
    roots = sorted({str(r.root) for r in current})
    if run.target_expression not in roots:
        return (
            f"Evidence reference '{ref}' resolves to root(s) {roots}, "
            f"not the run target root '{run.target_expression}'"
        )
    if not any(
        r.root == run.target_expression
        and r.attribution_status == models.StructuralAttributionStatus.CONFIRMED.value
        for r in current
    ):
        return (
            f"Evidence reference '{ref}' is not a CONFIRMED structural occurrence "
            "for the run target root"
        )
    return f"Evidence reference '{ref}' is not in the confirmed occurrence set"


def resolve_evidence_refs(
    db: Session, run: models.ResearchRun, refs: list[str]
) -> EvidenceResolution:
    reasons: list[str] = []
    occurrence_ids: set[str] = set()
    token_word_refs: set[str] = set()
    _confirmed_cache: set[str] | None = None

    def confirmed() -> set[str]:
        nonlocal _confirmed_cache
        if _confirmed_cache is None:
            _confirmed_cache = set(
                confirmed_word_refs(db, run.corpus_snapshot, run.target_expression)
            )
        return _confirmed_cache

    for ref in refs:
        if ":" not in ref:
            reasons.append(f"Evidence reference '{ref}' has no supported type prefix")
            continue
        kind, entity_id = ref.split(":", 1)
        if not entity_id:
            reasons.append(f"Evidence reference '{ref}' has an empty identity")
            continue
        if kind == "occurrence":
            item = db.get(models.CorpusOccurrence, entity_id)
            if item is None or item.snapshot_id != run.corpus_snapshot:
                reasons.append(f"Evidence reference '{ref}' is absent or outside the run corpus")
            else:
                occurrence_ids.add(str(item.id))
        elif kind == "token":
            # Word-level root occurrence bridge: Quranic word_ref -> the run's
            # confirmed StructuralToken occurrence set (snapshot + root scoped).
            if entity_id in confirmed():
                token_word_refs.add(entity_id)
            else:
                reasons.append(_token_reject_reason(db, run, ref, entity_id))
        elif kind == "observation":
            item = db.get(models.ObservationArtifact, entity_id)
            if item is None or item.research_run_id != run.id:
                reasons.append(f"Evidence reference '{ref}' is absent or cross-run")
            else:
                occurrence = db.get(models.CorpusOccurrence, item.occurrence_ref)
                if occurrence is not None and occurrence.snapshot_id == run.corpus_snapshot:
                    occurrence_ids.add(str(occurrence.id))
                elif str(item.occurrence_ref) in confirmed():
                    # A word-level observation references a confirmed token word_ref.
                    token_word_refs.add(str(item.occurrence_ref))
                else:
                    reasons.append(f"Observation evidence '{ref}' has invalid occurrence lineage")
        elif kind == "hypothesis":
            item = db.get(models.Hypothesis, entity_id)
            if item is None or item.research_run_id != run.id:
                reasons.append(f"Evidence reference '{ref}' is absent or cross-run")
        elif kind == "neighbor":
            item = db.get(models.EssentialNeighbor, entity_id)
            hypothesis = db.get(models.Hypothesis, item.hypothesis_id) if item else None
            if item is None or hypothesis is None or hypothesis.research_run_id != run.id:
                reasons.append(f"Evidence reference '{ref}' is absent or cross-run")
        else:
            reasons.append(f"Evidence reference type '{kind}' is not admissible")
    return EvidenceResolution(
        not reasons,
        tuple(reasons),
        frozenset(occurrence_ids),
        frozenset(token_word_refs),
    )


def derive_completeness(
    db: Session,
    run: models.ResearchRun,
    scope: str,
    sampling_basis: str | None,
    evidence_occurrence_ids: frozenset[str],
    evidence_token_word_refs: frozenset[str] = frozenset(),
    contract_type: str | None = None,
) -> dict[str, object]:
    """Host-derive coverage. The occurrence UNIT depends on the contract type:

    * ROOT_CONCEPT (word-level): the eligible set is the root's CONFIRMED
      StructuralToken word_refs (from admitted QAC morphology). This is the only
      honest universe for a claim about "every occurrence of a root"; the
      verse-level CorpusOccurrence store (one row per verse, expression='') can
      never represent it. Supported = word-level observations + `token:` evidence
      that land in the eligible set.
    * All other contracts: the existing verse/lexeme-level CorpusOccurrence set
      keyed by (snapshot, expression).

    Coverage is never self-certified: it is derived here from persisted rows only.
    """
    word_level = contract_type in WORD_LEVEL_CONTRACTS
    if word_level:
        eligible_ids = set(
            confirmed_word_refs(db, run.corpus_snapshot, run.target_expression)
        )
        observed_ids = {
            str(item.occurrence_ref)
            for item in db.query(models.ObservationArtifact)
            .filter(models.ObservationArtifact.research_run_id == run.id)
            .all()
            if str(item.occurrence_ref) in eligible_ids
        }
        supported_ids = observed_ids | (set(evidence_token_word_refs) & eligible_ids)
    else:
        eligible = (
            db.query(models.CorpusOccurrence)
            .filter(
                models.CorpusOccurrence.snapshot_id == run.corpus_snapshot,
                models.CorpusOccurrence.expression == run.target_expression,
            )
            .order_by(models.CorpusOccurrence.id)
            .all()
        )
        eligible_ids = {str(item.id) for item in eligible}
        observed_ids = {
            str(item.occurrence_ref)
            for item in db.query(models.ObservationArtifact)
            .filter(models.ObservationArtifact.research_run_id == run.id)
            .all()
            if str(item.occurrence_ref) in eligible_ids
        }
        supported_ids = observed_ids | (set(evidence_occurrence_ids) & eligible_ids)
    index_complete = bool(eligible_ids)
    if scope == models.ClaimScope.UNIVERSAL.value:
        sufficient = index_complete and supported_ids == eligible_ids
    elif scope == models.ClaimScope.REPRESENTATIVE.value:
        sufficient = index_complete and bool(supported_ids) and bool(sampling_basis)
    else:
        sufficient = bool(supported_ids)
    return {
        "claim_scope": scope,
        "occurrence_unit": "word_ref" if word_level else "occurrence",
        "eligible_occurrence_count": len(eligible_ids),
        "evidenced_occurrence_count": len(supported_ids),
        "index_complete": index_complete,
        "deep_analysis_complete": bool(eligible_ids) and observed_ids == eligible_ids,
        "sampling_basis_recorded": bool(sampling_basis),
        "sufficient_for_claim": sufficient,
        "derived_by": "ResearchJudgmentService",
    }


def _required_layers(contract_type: str) -> set[str]:
    return {
        "ROOT_CONCEPT": {"root"},
        "LEXEME": {"root", "lexeme"},
        "LOCAL_MEANING": {
            "root",
            "lexeme",
            "form",
            "construction",
            "context",
            "local_meaning",
        },
        "VERSE_MEANING": {"construction", "context", "final_statement"},
        "SEMANTIC_DIFFERENCE": {"lexeme", "semantic_boundary"},
    }[contract_type]


def evaluate_judgment(
    db: Session, run: models.ResearchRun, judgment: schemas.ResearchJudgmentCreate
) -> JudgmentDecision:
    refs = list(dict.fromkeys(
        judgment.supporting_evidence_refs + judgment.counterevidence_refs
    ))
    evidence = resolve_evidence_refs(db, run, refs)
    # Coverage is derived from SUPPORTING evidence only. A counterevidence
    # occurrence is an occurrence the concept fails to explain; it must never
    # count toward universal coverage (root semantic unity, NON_NEGOTIABLE).
    supporting = resolve_evidence_refs(db, run, judgment.supporting_evidence_refs)
    completeness = derive_completeness(
        db,
        run,
        judgment.claim_scope.value,
        judgment.sampling_basis,
        supporting.occurrence_ids,
        supporting.token_word_refs,
        judgment.contract_type,
    )
    reasons = list(evidence.reasons)
    isolation = (
        db.query(models.IsolationState)
        .filter(models.IsolationState.research_run_id == run.id)
        .one_or_none()
    )
    if isolation is None:
        reasons.append("Source isolation is not initialized")
    elif isolation.is_contaminated != "CLEAN":
        reasons.append("Actual prohibited-source contamination is recorded")

    if judgment.research_state == models.ResearchState.PREFERRED:
        if not judgment.preferred_conclusion:
            reasons.append("A preferred judgment requires preferred_conclusion")
        if not judgment.supporting_evidence_refs:
            reasons.append("A preferred judgment requires supporting evidence")
        if not completeness["sufficient_for_claim"]:
            reasons.append("Host-derived coverage is insufficient for the claim scope")
        if judgment.rejection_condition is None:
            reasons.append("A preferred judgment requires a structured rejection condition")
        if judgment.falsification_status != models.FalsificationStatus.PASSED:
            reasons.append("A preferred judgment requires passed falsification")
        if not judgment.strongest_competitor:
            reasons.append("A preferred judgment requires the strongest competitor")
        present_layers = {
            key for key, value in judgment.layer_attribution.items() if value.strip()
        }
        missing_layers = _required_layers(judgment.contract_type) - present_layers
        if missing_layers:
            reasons.append(
                "Missing material semantic layer attribution: "
                + ", ".join(sorted(missing_layers))
            )
    if judgment.research_state == models.ResearchState.UNRESOLVED:
        if judgment.result_strength != models.ResultStrength.UNRESOLVED:
            reasons.append("UNRESOLVED research state requires UNRESOLVED strength")
    elif judgment.result_strength == models.ResultStrength.UNRESOLVED:
        reasons.append("Resolved research states cannot use UNRESOLVED strength")
    return JudgmentDecision(not reasons, tuple(reasons), completeness)


class ResearchJudgmentService:
    @staticmethod
    def create(
        db: Session,
        run: models.ResearchRun,
        judgment: schemas.ResearchJudgmentCreate,
        *,
        actor: str,
    ) -> models.SemanticClaim:
        decision = evaluate_judgment(db, run, judgment)
        if not decision.accepted:
            raise ValueError("; ".join(decision.reasons))
        claim = models.SemanticClaim(
            id=f"jud_{uuid.uuid4().hex[:8]}",
            research_run_id=run.id,
            contract_type=judgment.contract_type,
            research_state=judgment.research_state.value,
            canonical_state=models.CanonicalState.NOT_CANONICAL.value,
            result_strength=judgment.result_strength.value,
            verification_state=models.VerificationState.NOT_REQUIRED.value,
            falsification_status=judgment.falsification_status.value,
            claim_scope=judgment.claim_scope.value,
            sampling_basis=judgment.sampling_basis,
            research_completeness=decision.completeness,
            preferred_conclusion=judgment.preferred_conclusion,
            root_concept=judgment.root_concept,
            plain_explanation=judgment.plain_explanation,
            semantic_boundary=judgment.semantic_boundary,
            layer_attribution=judgment.layer_attribution,
            rejection_condition=(
                judgment.rejection_condition.model_dump()
                if judgment.rejection_condition
                else None
            ),
            supporting_evidence=judgment.supporting_evidence_refs,
            counterevidence=judgment.counterevidence_refs,
            unresolved_cases=judgment.unresolved_cases,
            hard_cases=judgment.hard_cases,
            strongest_counterexample=judgment.strongest_counterexample,
            strongest_competitor=judgment.strongest_competitor,
            reopen_conditions=judgment.reopen_conditions,
        )
        db.add(claim)
        db.flush()
        db.add(
            models.DependencyRecord(
                id=f"dep_{uuid.uuid4().hex[:8]}",
                dependent_claim_id=claim.id,
                dependency_type="CORPUS_SNAPSHOT",
                dependency_ref=run.corpus_snapshot,
            )
        )
        for ref in list(dict.fromkeys(
            judgment.supporting_evidence_refs + judgment.counterevidence_refs
        )):
            db.add(
                models.DependencyRecord(
                    id=f"dep_{uuid.uuid4().hex[:8]}",
                    dependent_claim_id=claim.id,
                    dependency_type="EVIDENCE",
                    dependency_ref=ref,
                )
            )
        db.add(
            models.AuditLog(
                id=f"aud_{uuid.uuid4().hex[:8]}",
                entity_id=claim.id,
                entity_type="ResearchJudgment",
                action="CREATE_RESEARCH_JUDGMENT",
                previous_state=None,
                new_state=claim.research_state,
                actor=actor,
            )
        )
        run.current_stage = models.ResearchStage.JUDGMENT.value
        run.status = "ACTIVE"
        db.commit()
        db.refresh(claim)
        return claim
