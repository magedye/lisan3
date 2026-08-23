from typing import Any

from sqlalchemy.orm import Session

from backend.domain.models import (
    CorpusSnapshot,
    DependencyRecord,
    ResearchRun,
    ReviewDecision,
    SemanticClaim,
)
from backend.domain.services.corpus.authority import is_production_validated
from backend.domain.services.gates import INTERNAL_LOCK, PURITY_CHECK, has_valid_gate


class SemanticRegistryAdmissionPolicy:
    """
    Evaluates all applicable canonical prerequisites for publishing a claim to the registry.
    """

    @staticmethod
    def evaluate(db: Session, claim: SemanticClaim) -> dict[str, Any]:
        reasons: list[str] = []

        # 1. Epistemic State
        if claim.epistemic_state != "LOCK_INTERNAL_RESULT":
            reasons.append(
                f"Claim epistemic state is '{claim.epistemic_state}', expected 'LOCK_INTERNAL_RESULT'"
            )

        # 2. Review Decision
        if claim.review_state != "APPROVED":
            reasons.append(
                f"Claim review state is '{claim.review_state}', expected 'APPROVED'"
            )
        else:
            latest_review = (
                db.query(ReviewDecision)
                .filter(
                    ReviewDecision.claim_id == claim.id,
                    ReviewDecision.decision == "APPROVED",
                )
                .order_by(ReviewDecision.created_at.desc())
                .first()
            )
            if not latest_review:
                reasons.append("No APPROVED ReviewDecision record found")
            elif latest_review.evaluated_claim_revision != claim.revision_id:
                reasons.append(
                    f"Latest APPROVED review is for revision {latest_review.evaluated_claim_revision}, but current claim revision is {claim.revision_id}"
                )

        # 3. Freshness State
        if claim.freshness_state != "CURRENT":
            reasons.append(
                f"Claim freshness state is '{claim.freshness_state}', expected 'CURRENT'"
            )

        # 4. Admitted & Activated Corpus Snapshot
        run = (
            db.query(ResearchRun)
            .filter(ResearchRun.id == claim.research_run_id)
            .first()
        )
        snapshot = None
        if not run:
            reasons.append("Claim is not linked to a valid ResearchRun")
        else:
            snapshot = (
                db.query(CorpusSnapshot)
                .filter(CorpusSnapshot.id == run.corpus_snapshot)
                .first()
            )
            if not snapshot:
                reasons.append("ResearchRun has no CorpusSnapshot")
            elif snapshot.validation_status != "VALIDATED":
                reasons.append(
                    f"CorpusSnapshot validation_status is '{snapshot.validation_status}', expected 'VALIDATED'"
                )
            elif not is_production_validated(snapshot):
                reasons.append(
                    "CorpusSnapshot is not authority-verified and production-active"
                )

            claim_snapshot_dependencies = (
                db.query(DependencyRecord)
                .filter(
                    DependencyRecord.dependent_claim_id == claim.id,
                    DependencyRecord.dependency_type == "CORPUS_SNAPSHOT",
                )
                .all()
            )
            if len(claim_snapshot_dependencies) != 1:
                reasons.append("Claim must have exactly one CORPUS_SNAPSHOT dependency")
            elif claim_snapshot_dependencies[0].dependency_ref != run.corpus_snapshot:
                reasons.append(
                    f"Claim CORPUS_SNAPSHOT dependency '{claim_snapshot_dependencies[0].dependency_ref}' does not match ResearchRun snapshot '{run.corpus_snapshot}'"
                )

            # 5. Blind Lab Contamination
            # We assume contamination sets status to LOCK_BLOCKED earlier, but checking here adds defense-in-depth.
            # 6. Required GateReport results
            if not has_valid_gate(db, run.id, INTERNAL_LOCK):
                reasons.append("Missing PASSED GateReport for 'INTERNAL_LOCK'")
            if not has_valid_gate(db, run.id, PURITY_CHECK):
                reasons.append("Missing required PASSED GateReport for 'PURITY_CHECK'")

        # Fixture/Test Registry invariant
        if (run and run.target_contract.startswith("test_fixture_")) or (
            snapshot and snapshot.fixture_only
        ):
            reasons.append(
                "Synthetic fixtures and tests cannot be admitted to production registry"
            )

        if reasons:
            return {"status": "NOT_ELIGIBLE", "reasons": reasons}

        return {"status": "ELIGIBLE", "reasons": []}
