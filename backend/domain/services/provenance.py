from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.domain import models
from backend.domain.services.orchestrator import CampaignOrchestrator, OrchestratorState

class ProvenanceService:
    @staticmethod
    def get_run_provenance(db: Session, run_id: str) -> Dict[str, Any]:
        provenance = {
            "run_id": run_id,
            "state": CampaignOrchestrator.derive_root_state(db, run_id).value,
            "isolation": None,
            "observations": [],
            "claims": []
        }
        
        run = db.query(models.ResearchRun).filter_by(id=run_id).first()
        if not run:
            return provenance
            
        isolation = db.query(models.IsolationState).filter_by(research_run_id=run_id).first()
        if isolation:
            provenance["isolation"] = {
                "id": isolation.id,
                "status": isolation.establishment_status,
                "snapshot": isolation.corpus_snapshot,
                "audit_ref": isolation.audit_ref
            }
            
        obs = db.query(models.ObservationArtifact).filter_by(research_run_id=run_id).all()
        for o in obs:
            provenance["observations"].append({
                "id": o.id,
                "occurrence_ref": o.occurrence_ref,
                "form": o.form
            })
            
        claims = db.query(models.SemanticClaim).filter_by(research_run_id=run_id).all()
        for c in claims:
            claim_data = {
                "id": c.id,
                "canonical_state": c.canonical_state,
                "research_state": c.research_state,
                "verification_state": c.verification_state,
                "reviews": [],
                "audits": []
            }
            
            reviews = db.query(models.IndependentReview).filter_by(claim_id=c.id).all()
            for r in reviews:
                claim_data["reviews"].append({
                    "id": r.id,
                    "reviewer": r.reviewer_identity,
                    "status": r.review_status,
                    "verdict": r.verdict
                })
                
            audits = db.query(models.AuditLog).filter_by(entity_id=c.id).all()
            for a in audits:
                claim_data["audits"].append({
                    "id": a.id,
                    "action": a.action,
                    "actor": a.actor,
                    "new_state": a.new_state
                })
            
            provenance["claims"].append(claim_data)
            
        return provenance
