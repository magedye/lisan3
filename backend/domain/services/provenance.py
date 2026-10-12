from typing import Any

from sqlalchemy.orm import Session

from backend.domain import models
from backend.domain.services.orchestrator import CampaignOrchestrator


class ProvenanceService:
    @staticmethod
    def get_run_provenance(db: Session, run_id: str) -> dict[str, Any]:
        provenance = {
            "run_id": run_id,
            "state": CampaignOrchestrator.derive_root_state(db, run_id).value,
            "snapshot": None,
            "tokens": [],
            "isolation": None,
            "observations": [],
            "claims": [],
        }

        run = db.query(models.ResearchRun).filter_by(id=run_id).first()
        if not run:
            return provenance

        snapshot = (
            db.query(models.CorpusSnapshot).filter_by(id=run.corpus_snapshot).first()
        )
        if snapshot:
            provenance["snapshot"] = {
                "id": snapshot.id,
                "text_hash": snapshot.canonical_text_hash,
                "activation": snapshot.activation_status,
            }

            # Fetch occurrences linked to the run's target_expression
            occurrences = (
                db.query(models.CorpusOccurrence)
                .filter_by(snapshot_id=snapshot.id, expression=run.target_expression)
                .all()
            )
            for occ in occurrences:
                provenance["tokens"].append(
                    {"id": occ.id, "verse": occ.verse_ref, "text": occ.text}
                )

        isolation = (
            db.query(models.IsolationState).filter_by(research_run_id=run_id).first()
        )
        if isolation:
            provenance["isolation"] = {
                "id": isolation.id,
                "status": isolation.establishment_status,
                "snapshot": isolation.corpus_snapshot,
                "audit_ref": isolation.audit_ref,
                "contamination": isolation.is_contaminated,
            }

        obs = (
            db.query(models.ObservationArtifact).filter_by(research_run_id=run_id).all()
        )
        for o in obs:
            provenance["observations"].append(
                {"id": o.id, "occurrence_ref": o.occurrence_ref, "form": o.form}
            )

        claims = db.query(models.SemanticClaim).filter_by(research_run_id=run_id).all()
        for c in claims:
            claim_data = {
                "id": c.id,
                "canonical_state": c.canonical_state,
                "research_state": c.research_state,
                "verification_state": c.verification_state,
                "revisions": [],
                "reviews": [],
                "verifications": [],
                "audits": [],
            }

            # Revisions
            revisions = db.query(models.ClaimRevision).filter_by(claim_id=c.id).all()
            for rev in revisions:
                claim_data["revisions"].append(
                    {
                        "id": rev.id,
                        "revision_number": rev.revision_number,
                        "correction_reason": rev.correction_reason,
                    }
                )

            # Reviews
            reviews = db.query(models.IndependentReview).filter_by(claim_id=c.id).all()
            for r in reviews:
                claim_data["reviews"].append(
                    {
                        "id": r.id,
                        "reviewer": r.reviewer_identity,
                        "status": r.review_status,
                        "verdict": r.verdict,
                        "revision_id": r.revision_id,
                    }
                )

            # Verifications
            verifications = (
                db.query(models.VerificationRecord).filter_by(claim_id=c.id).all()
            )
            for v in verifications:
                claim_data["verifications"].append(
                    {
                        "id": v.id,
                        "verifier": v.verifier_identity,
                        "decision": v.decision,
                        "revision": v.evaluated_claim_revision,
                    }
                )

            # Canonicalization Audit
            audits = db.query(models.AuditLog).filter_by(entity_id=c.id).all()
            for a in audits:
                claim_data["audits"].append(
                    {
                        "id": a.id,
                        "action": a.action,
                        "actor": a.actor,
                        "new_state": a.new_state,
                    }
                )

            provenance["claims"].append(claim_data)

        return provenance
