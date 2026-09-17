
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

class CampaignOrchestrator:
    @staticmethod
    def derive_root_state(db: Session, run_id: str) -> OrchestratorState:
        run = db.query(models.ResearchRun).filter_by(id=run_id).first()
        if not run:
            return OrchestratorState.PLANNED
            
        isolation = db.query(models.IsolationState).filter_by(research_run_id=run_id).first()
        if not isolation or isolation.establishment_status != "ESTABLISHED":
            return OrchestratorState.RUN_CREATED
            
        if isolation.is_contaminated == "PRIOR_CONTAMINATED":
            return OrchestratorState.BLOCKED
            
        claim = db.query(models.SemanticClaim).filter_by(research_run_id=run_id).order_by(models.SemanticClaim.created_at.desc()).first()
        if not claim:
            return OrchestratorState.OBSERVATIONS_COMPLETE # Simplifying observation check for now
            
        if claim.canonical_state == "ACCEPTED":
            return OrchestratorState.CANONICALIZED
            
        if claim.canonical_state == "REOPEN_REQUIRED":
            return OrchestratorState.CORRECTION_REQUIRED
            
        if claim.verification_state == "VERIFIED":
            return OrchestratorState.CANONICALIZATION_ELIGIBLE
            
        if claim.research_state == "UNRESOLVED":
            return OrchestratorState.UNRESOLVED
            
        reviews = db.query(models.IndependentReview).filter_by(claim_id=claim.id).all()
        if not reviews:
            return OrchestratorState.CLAIM_FROZEN
            
        pending = [r for r in reviews if r.review_status == "PENDING"]
        if pending:
            return OrchestratorState.INDEPENDENT_REVIEW_PENDING
            
        return OrchestratorState.CLOSED
