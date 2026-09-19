import uuid

from sqlalchemy.orm import Session

from backend.domain import models
from backend.domain.services.actor_context import ActorContext, ActorRole
from backend.domain.services.research_judgment import resolve_evidence_refs


class VerificationService:
    @staticmethod
    def create_record(
        db: Session,
        claim_id: str,
        verification_type: str,
        decision: str,
        rationale: str,
        evidence_refs: list[str],
        actor_context: ActorContext,
    ) -> models.VerificationRecord:
        ActorContext.require_role(actor_context, ActorRole.VERIFIER)

        claim = db.get(models.SemanticClaim, claim_id)
        if not claim:
            raise LookupError("Research Judgment not found")
        if decision == "VERIFIED" and verification_type != "INDEPENDENT":
            raise ValueError(
                "A VERIFIED decision requires verification_type=INDEPENDENT"
            )

        run = db.get(models.ResearchRun, claim.research_run_id)
        if run is None:
            raise LookupError("ResearchRun not found")

        evidence = resolve_evidence_refs(db, run, evidence_refs)
        if not evidence.valid:
            raise ValueError("; ".join(evidence.reasons))

        record = models.VerificationRecord(
            id=f"ver_{uuid.uuid4().hex[:8]}",
            claim_id=claim_id,
            verifier_identity=actor_context.identity,
            verification_type=verification_type,
            decision=decision,
            rationale=rationale,
            evidence_refs=evidence_refs,
            evaluated_claim_revision=claim.revision_id,
        )
        db.add(record)

        claim.verification_state = (
            models.VerificationState.VERIFIED.value
            if decision == "VERIFIED"
            else models.VerificationState.NOT_VERIFIED.value
        )
        db.add(
            models.AuditLog(
                id=f"aud_{uuid.uuid4().hex[:8]}",
                entity_id=claim.id,
                entity_type="ResearchJudgment",
                action="RECORD_INDEPENDENT_VERIFICATION",
                previous_state=None,
                new_state=claim.verification_state,
                actor=actor_context.identity,
            )
        )
        db.flush()
        return record
