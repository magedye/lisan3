"""Canonical release boundary for SemanticClaim-derived reads."""

from dataclasses import dataclass

from sqlalchemy.orm import Session

from backend.domain import models
from backend.domain.services.gates import INTERNAL_LOCK, has_valid_gate


@dataclass(frozen=True)
class ClaimReleaseDecision:
    released: bool
    reason: str | None = None


class ClaimReleasePolicy:
    """Derive claim visibility from current run, isolation, and Gate authority."""

    @staticmethod
    def evaluate_run(db: Session, run_id: str | None) -> ClaimReleaseDecision:
        if not run_id:
            return ClaimReleaseDecision(False, "Claim is not linked to a ResearchRun")
        run = db.get(models.ResearchRun, run_id)
        if run is None:
            return ClaimReleaseDecision(False, "Claim ResearchRun does not exist")
        isolation = (
            db.query(models.IsolationState)
            .filter(models.IsolationState.research_run_id == run_id)
            .one_or_none()
        )
        if isolation is None:
            return ClaimReleaseDecision(
                False, "Blind Lab isolation is absent"
            )
        if isolation.is_contaminated != "CLEAN":
            return ClaimReleaseDecision(False, "Blind Lab run is contaminated")
        try:
            locked = has_valid_gate(db, run_id, INTERNAL_LOCK)
        except (LookupError, ValueError):
            locked = False
        if not locked:
            return ClaimReleaseDecision(False, "Current Internal Lock is not valid")
        return ClaimReleaseDecision(True)

    @classmethod
    def evaluate_claim(
        cls, db: Session, claim: models.SemanticClaim
    ) -> ClaimReleaseDecision:
        return cls.evaluate_run(db, claim.research_run_id)

    @classmethod
    def is_claim_released(cls, db: Session, claim: models.SemanticClaim) -> bool:
        return cls.evaluate_claim(db, claim).released

    @classmethod
    def filter_released_claims(
        cls, db: Session, claims: list[models.SemanticClaim]
    ) -> list[models.SemanticClaim]:
        decisions: dict[str | None, bool] = {}
        released: list[models.SemanticClaim] = []
        for claim in claims:
            run_id = claim.research_run_id
            if run_id not in decisions:
                decisions[run_id] = cls.evaluate_run(db, run_id).released
            if decisions[run_id]:
                released.append(claim)
        return released

    @classmethod
    def filter_released_audit_logs(
        cls, db: Session, logs: list[models.AuditLog]
    ) -> list[models.AuditLog]:
        entity_ids = {str(log.entity_id) for log in logs if log.entity_id}
        claims = (
            db.query(models.SemanticClaim)
            .filter(models.SemanticClaim.id.in_(entity_ids))
            .all()
            if entity_ids
            else []
        )
        claims_by_id = {claim.id: claim for claim in claims}
        visible: list[models.AuditLog] = []
        for log in logs:
            claim = claims_by_id.get(str(log.entity_id))
            is_claim_log = log.entity_type == "SemanticClaim" or claim is not None
            if not is_claim_log or (
                claim is not None and cls.is_claim_released(db, claim)
            ):
                visible.append(log)
        return visible
