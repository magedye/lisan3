"""One explicit canonicalization boundary, separate from AI research authority."""

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.domain import models
from backend.domain.services.corpus.authority import is_production_validated
from backend.domain.services.methodology_authority import methodology_authority_failures
from backend.domain.services.research_judgment import resolve_evidence_refs


@dataclass(frozen=True)
class CanonicalizationDecision:
    accepted: bool
    reasons: tuple[str, ...]


class CanonicalizationPolicy:
    @staticmethod
    def evaluate(db: Session, claim: models.SemanticClaim) -> CanonicalizationDecision:
        reasons: list[str] = []
        if claim.research_state != models.ResearchState.PREFERRED.value:
            reasons.append("Research state is not PREFERRED")
        if claim.result_strength != models.ResultStrength.STRONG.value:
            reasons.append("Result strength is not STRONG")
        if not (claim.research_completeness or {}).get("sufficient_for_claim"):
            reasons.append("Host-derived research completeness is insufficient")
        if claim.falsification_status != models.FalsificationStatus.PASSED.value:
            reasons.append("Falsification has not passed")
        for field, message in (
            (claim.plain_explanation, "Plain explanation is missing"),
            (claim.semantic_boundary, "Semantic boundary is missing"),
            (claim.strongest_counterexample, "Strongest counterexample is missing"),
            (claim.strongest_competitor, "Strongest competitor is missing"),
        ):
            if not field:
                reasons.append(message)
        if not claim.supporting_evidence:
            reasons.append("Important evidence is missing")
        if not claim.hard_cases:
            reasons.append("Hard cases are missing")
        if not claim.reopen_conditions:
            reasons.append("Reopen conditions are missing")
        if claim.contract_type == "ROOT_CONCEPT" and not claim.root_concept:
            reasons.append("Root concept is missing")

        # Root semantic unity (INT-OWN-ROOT-002, NON_NEGOTIABLE): an accepted
        # universal root concept must show the root's contribution in EVERY
        # confirmed-attribution occurrence. Host-derived coverage proves the
        # occurrences were observed/evidenced, but observation does not equal
        # explanation: a still-unresolved (confirmed unexplained) occurrence must
        # block acceptance. No majority substitute is permitted.
        is_universal_root = (
            claim.contract_type == "ROOT_CONCEPT"
            and claim.claim_scope == models.ClaimScope.UNIVERSAL.value
        )
        if is_universal_root and (claim.unresolved_cases or []):
            reasons.append(
                "A universal root concept cannot be accepted while confirmed "
                "occurrences remain unexplained (root semantic unity)"
            )

        run = db.get(models.ResearchRun, claim.research_run_id)
        if run is None:
            reasons.append("ResearchRun is missing")
            return CanonicalizationDecision(False, tuple(reasons))
        snapshot = db.get(models.CorpusSnapshot, run.corpus_snapshot)
        if snapshot is None or not is_production_validated(snapshot):
            reasons.append("Corpus snapshot is not production-valid")
        methodology = db.get(models.MethodologyRevision, run.methodology_revision)
        if methodology is None:
            reasons.append("Methodology revision is missing")
        elif methodology_authority_failures(methodology):
            reasons.append("Methodology revision is not current and source-bound")
        isolation = (
            db.query(models.IsolationState)
            .filter(models.IsolationState.research_run_id == run.id)
            .one_or_none()
        )
        if isolation is None or isolation.is_contaminated != "CLEAN":
            reasons.append("Source isolation is absent or contaminated")
        evidence = resolve_evidence_refs(
            db,
            run,
            list(claim.supporting_evidence or []) + list(claim.counterevidence or []),
        )
        reasons.extend(evidence.reasons)

        # A confirmed occurrence recorded as counterevidence is an occurrence the
        # concept fails to explain. For a universal root concept, one such
        # occurrence in the eligible set blocks acceptance (root semantic unity).
        if is_universal_root and claim.counterevidence:
            counter = resolve_evidence_refs(db, run, list(claim.counterevidence))
            eligible_ids = {
                str(item.id)
                for item in db.query(models.CorpusOccurrence).filter(
                    models.CorpusOccurrence.snapshot_id == run.corpus_snapshot,
                    models.CorpusOccurrence.expression == run.target_expression,
                )
            }
            if counter.occurrence_ids & eligible_ids:
                reasons.append(
                    "A universal root concept cannot be accepted while a confirmed "
                    "occurrence remains a counterexample (root semantic unity)"
                )

        verification = (
            db.query(models.VerificationRecord)
            .filter(
                models.VerificationRecord.claim_id == claim.id,
                models.VerificationRecord.decision == "VERIFIED",
            )
            .order_by(models.VerificationRecord.created_at.desc())
            .first()
        )
        if claim.verification_state != models.VerificationState.VERIFIED.value:
            reasons.append("Independent verification state is not VERIFIED")
        if verification is None:
            reasons.append("Independent verification record is missing")
        elif verification.evaluated_claim_revision != claim.revision_id:
            reasons.append("Independent verification is stale for this revision")
        elif verification.verification_type != "INDEPENDENT":
            reasons.append("Verification type is not INDEPENDENT")

        corpus_dependencies = (
            db.query(models.DependencyRecord)
            .filter(
                models.DependencyRecord.dependent_claim_id == claim.id,
                models.DependencyRecord.dependency_type == "CORPUS_SNAPSHOT",
            )
            .all()
        )
        if len(corpus_dependencies) != 1 or (
            corpus_dependencies and corpus_dependencies[0].dependency_ref != run.corpus_snapshot
        ):
            reasons.append("Canonical corpus dependency is absent or ambiguous")
        if run.target_contract.startswith("test_fixture_") or (
            snapshot is not None and snapshot.fixture_only
        ):
            reasons.append("Synthetic fixtures cannot become canonical project knowledge")
        return CanonicalizationDecision(not reasons, tuple(dict.fromkeys(reasons)))

    @classmethod
    def canonicalize(
        cls,
        db: Session,
        claim: models.SemanticClaim,
        *,
        rationale: str,
        actor: str = "TRUSTED_LOCAL_OWNER",
    ) -> models.SemanticClaim:
        decision = cls.evaluate(db, claim)
        if not decision.accepted:
            raise ValueError("; ".join(decision.reasons))
        previous = claim.canonical_state
        claim.canonical_state = models.CanonicalState.ACCEPTED.value
        claim.accepted_at = datetime.now(timezone.utc).replace(tzinfo=None)
        run = db.get(models.ResearchRun, claim.research_run_id)
        if run is not None:
            run.current_stage = models.ResearchStage.CANONICALIZATION.value
            run.status = "COMPLETE"
        db.add(
            models.AuditLog(
                id=f"aud_{uuid.uuid4().hex[:8]}",
                entity_id=claim.id,
                entity_type="ResearchJudgment",
                action="CANONICALIZE",
                previous_state=previous,
                new_state=models.CanonicalState.ACCEPTED.value,
                actor=actor,
            )
        )
        db.add(
            models.AuditLog(
                id=f"aud_{uuid.uuid4().hex[:8]}",
                entity_id=claim.id,
                entity_type="CanonicalizationRationale",
                action="RECORD_RATIONALE",
                previous_state=None,
                new_state=rationale,
                actor=actor,
            )
        )
        db.commit()
        db.refresh(claim)
        return claim


def reopen_accepted_results_for_new_evidence(
    db: Session, run: models.ResearchRun, observation: models.ObservationArtifact
) -> list[str]:
    accepted = (
        db.query(models.SemanticClaim)
        .join(models.ResearchRun, models.SemanticClaim.research_run_id == models.ResearchRun.id)
        .filter(
            models.ResearchRun.target_expression == run.target_expression,
            models.SemanticClaim.canonical_state == models.CanonicalState.ACCEPTED.value,
        )
        .all()
    )
    reopened: list[str] = []
    evidence_ref = f"observation:{observation.id}"
    for claim in accepted:
        if evidence_ref in (claim.supporting_evidence or []) or evidence_ref in (
            claim.counterevidence or []
        ):
            continue
        previous = claim.canonical_state
        claim.canonical_state = models.CanonicalState.REOPEN_REQUIRED.value
        claim.verification_state = models.VerificationState.NOT_VERIFIED.value
        claim.revision_id += 1
        db.add(
            models.AuditLog(
                id=f"aud_{uuid.uuid4().hex[:8]}",
                entity_id=claim.id,
                entity_type="ResearchJudgment",
                action="REOPEN_FOR_NEW_EVIDENCE",
                previous_state=previous,
                new_state=models.CanonicalState.REOPEN_REQUIRED.value,
                actor="NEW_EVIDENCE_POLICY",
            )
        )
        reopened.append(str(claim.id))
    return reopened


def accepted_root_result(
    db: Session, expression: str
) -> models.SemanticClaim | None:
    return (
        db.query(models.SemanticClaim)
        .join(models.ResearchRun, models.SemanticClaim.research_run_id == models.ResearchRun.id)
        .filter(
            models.ResearchRun.target_expression == expression,
            models.SemanticClaim.contract_type == "ROOT_CONCEPT",
            models.SemanticClaim.canonical_state == models.CanonicalState.ACCEPTED.value,
            models.SemanticClaim.result_strength == models.ResultStrength.STRONG.value,
        )
        .order_by(models.SemanticClaim.accepted_at.desc())
        .first()
    )
