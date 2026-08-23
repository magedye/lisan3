import uuid

from sqlalchemy.orm import Session

from ..models import IsolationEvent, IsolationState
from .gates import INTERNAL_LOCK, has_valid_gate


class IsolationContaminationException(Exception):
    def __init__(self, message: str, run_id: str):
        self.message = message
        self.run_id = run_id
        super().__init__(self.message)


class BlindLabIsolationService:
    @staticmethod
    def enforce_semantic_isolation(db: Session, run_id: str):
        """
        Enforce that semantic dictionaries/prior knowledge cannot be accessed
        until the authoritative internal-lock condition has actually been reached.
        """
        if not has_valid_gate(db, run_id, INTERNAL_LOCK):
            # Create an auditable isolation event for the blocked read attempt
            event = IsolationEvent(
                id=f"evt_{uuid.uuid4().hex[:8]}",
                research_run_id=run_id,
                attempted_action="READ_PRIOR_SEMANTIC_KNOWLEDGE",
                was_blocked=True,
            )
            db.add(event)
            db.commit()

            raise IsolationContaminationException(
                message="Prohibited read: Semantic knowledge cannot be accessed before authoritative internal lock.",
                run_id=run_id,
            )
        return True

    @staticmethod
    def record_actual_contamination(db: Session, run_id: str, reason: str):
        """
        Records actual prior exposure/injection affecting the analysis,
        not merely a successfully blocked request.
        """
        state = (
            db.query(IsolationState)
            .filter(IsolationState.research_run_id == run_id)
            .first()
        )
        if state and state.is_contaminated != "PRIOR_CONTAMINATED":
            state.is_contaminated = "PRIOR_CONTAMINATED"
            state.contamination_reason = reason
            db.commit()
