import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy.orm import Session

from backend.domain import models


class OrchestratorState(Enum):
    PLANNED = "PLANNED"
    AUTHORIZED = "AUTHORIZED"
    RUN_CREATED = "RUN_CREATED"
    ISOLATION_ESTABLISHED = "ISOLATION_ESTABLISHED"
    OBSERVATIONS_COMPLETE = "OBSERVATIONS_COMPLETE"
    RESEARCH_IN_PROGRESS = "RESEARCH_IN_PROGRESS"
    CLAIM_FROZEN = "CLAIM_FROZEN"
    INDEPENDENT_REVIEW_PENDING = "INDEPENDENT_REVIEW_PENDING"
    CORRECTION_REQUIRED = "CORRECTION_REQUIRED"
    VERIFIED = "VERIFIED"
    CANONICALIZATION_ELIGIBLE = "CANONICALIZATION_ELIGIBLE"
    CANONICALIZED = "CANONICALIZED"
    UNRESOLVED = "UNRESOLVED"
    CLOSED = "CLOSED"
    BLOCKED = "BLOCKED"


class IllegalTransitionError(ValueError):
    pass


class CampaignOrchestrator:
    @staticmethod
    def _utc_now():
        return datetime.now(timezone.utc).replace(tzinfo=None)

    @staticmethod
    def derive_root_state(db: Session, run_id: str) -> OrchestratorState:
        run = db.query(models.ResearchRun).filter_by(id=run_id).first()
        if not run:
            return OrchestratorState.PLANNED

        isolation = (
            db.query(models.IsolationState).filter_by(research_run_id=run_id).first()
        )
        if not isolation or isolation.establishment_status != "ESTABLISHED":
            return OrchestratorState.RUN_CREATED

        if isolation.is_contaminated == "PRIOR_CONTAMINATED":
            return OrchestratorState.BLOCKED

        claim = (
            db.query(models.SemanticClaim)
            .filter_by(research_run_id=run_id)
            .order_by(models.SemanticClaim.created_at.desc())
            .first()
        )
        if not claim:
            obs = (
                db.query(models.ObservationArtifact)
                .filter_by(research_run_id=run_id)
                .first()
            )
            if obs:
                return OrchestratorState.OBSERVATIONS_COMPLETE
            return OrchestratorState.ISOLATION_ESTABLISHED

        if claim.canonical_state == "ACCEPTED":
            return OrchestratorState.CANONICALIZED

        if claim.canonical_state == "REOPEN_REQUIRED":
            return OrchestratorState.CORRECTION_REQUIRED

        if claim.verification_state == "VERIFIED":
            return OrchestratorState.CANONICALIZATION_ELIGIBLE

        if claim.research_state == "UNRESOLVED":
            return OrchestratorState.UNRESOLVED

        reviews = db.query(models.IndependentReview).filter_by(claim_id=claim.id).all()
        current_reviews = [r for r in reviews if r.revision_id == claim.revision_id]
        if not current_reviews:
            return OrchestratorState.CLAIM_FROZEN

        pending = [r for r in current_reviews if r.review_status == "PENDING"]
        if pending:
            return OrchestratorState.INDEPENDENT_REVIEW_PENDING

        # Check if the claim has completed reviews on current revision
        return OrchestratorState.CLOSED

    @staticmethod
    def _record_transition(
        db: Session,
        entity_id: str,
        entity_type: str,
        previous_state: str,
        new_state: str,
        actor: str,
    ):
        audit = models.AuditLog(
            id=f"aud_{uuid.uuid4().hex[:8]}",
            entity_id=entity_id,
            entity_type=entity_type,
            action="STATE_TRANSITION",
            previous_state=previous_state,
            new_state=new_state,
            actor=actor,
            created_at=CampaignOrchestrator._utc_now(),
        )
        db.add(audit)

    @staticmethod
    def transition(
        db: Session,
        run_id: str,
        target_state: OrchestratorState,
        actor: str,
        force: bool = False,
    ):
        """
        Idempotent transition enforcer. Validates prerequisites before advancing state.
        """
        current_state = CampaignOrchestrator.derive_root_state(db, run_id)
        if current_state == target_state:
            return current_state

        if target_state == OrchestratorState.CLAIM_FROZEN and current_state not in [
            OrchestratorState.OBSERVATIONS_COMPLETE,
            OrchestratorState.RESEARCH_IN_PROGRESS,
        ]:
            raise IllegalTransitionError(
                f"Cannot freeze claim from {current_state.value}"
            )
        elif (
            target_state == OrchestratorState.CANONICALIZED
            and current_state != OrchestratorState.CANONICALIZATION_ELIGIBLE
        ):
            raise IllegalTransitionError(
                f"Cannot canonicalize from {current_state.value}. Requires VERIFIED state."
            )
        elif target_state == OrchestratorState.VERIFIED and current_state not in [
            OrchestratorState.INDEPENDENT_REVIEW_PENDING,
            OrchestratorState.CLAIM_FROZEN,
        ]:
            raise IllegalTransitionError(f"Cannot verify from {current_state.value}")

        CampaignOrchestrator._record_transition(
            db, run_id, "ResearchRun", current_state.value, target_state.value, actor
        )
        db.commit()
        return target_state
