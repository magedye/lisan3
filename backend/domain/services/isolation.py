import uuid

from sqlalchemy.orm import Session

from ..models import IsolationEvent, IsolationState, ResearchRun


class IsolationContaminationException(Exception):
    def __init__(self, message: str, run_id: str):
        self.message = message
        self.run_id = run_id
        super().__init__(self.message)


class BlindLabIsolationService:
    @staticmethod
    def enforce_semantic_isolation(db: Session, run_id: str):
        """
        Enforce the permanent source boundary for internal Quranic induction.

        Accepted project memory has a separate traceable read path. This method
        represents prohibited external semantic content entering evidence context.
        """
        run = db.get(ResearchRun, run_id)
        if run is None:
            raise LookupError(f"ResearchRun {run_id} not found")
        state = (
            db.query(IsolationState)
            .filter(IsolationState.research_run_id == run_id)
            .one_or_none()
        )
        if state is None:
            raise IsolationContaminationException(
                message="Source isolation has not been initialized.", run_id=run_id
            )
        event = IsolationEvent(
            id=f"evt_{uuid.uuid4().hex[:8]}",
            research_run_id=run_id,
            attempted_action="READ_PROHIBITED_EXTERNAL_SEMANTIC_SOURCE",
            was_blocked=True,
        )
        db.add(event)
        db.commit()
        raise IsolationContaminationException(
            message=(
                "Prohibited source read blocked: external semantic content cannot "
                "enter internal Quranic induction."
            ),
            run_id=run_id,
        )

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
