"""Deterministic validation and persistence of AI/user Research Judgments."""

import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session

from backend.domain import models, schemas


@dataclass(frozen=True)
class EvidenceResolution:
    valid: bool
    reasons: tuple[str, ...]
    occurrence_ids: frozenset[str]


@dataclass(frozen=True)
class JudgmentDecision:
    accepted: bool
    reasons: tuple[str, ...]
    completeness: dict[str, object]


def resolve_evidence_refs(
    db: Session, run: models.ResearchRun, refs: list[str]
) -> EvidenceResolution:
    reasons: list[str] = []
    occurrence_ids: set[str] = set()
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
        elif kind == "observation":
            item = db.get(models.ObservationArtifact, entity_id)
            if item is None or item.research_run_id != run.id:
                reasons.append(f"Evidence reference '{ref}' is absent or cross-run")
            else:
                occurrence = db.get(models.CorpusOccurrence, item.occurrence_ref)
                if occurrence is None or occurrence.snapshot_id != run.corpus_snapshot:
                    reasons.append(f"Observation evidence '{ref}' has invalid occurrence lineage")
                else:
                    occurrence_ids.add(str(occurrence.id))
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
    return EvidenceResolution(not reasons, tuple(reasons), frozenset(occurrence_ids))


def derive_completeness(
    db: Session,
    run: models.ResearchRun,
    scope: str,
    sampling_basis: str | None,
    evidence_occurrence_ids: frozenset[str],
) -> dict[str, object]:
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
