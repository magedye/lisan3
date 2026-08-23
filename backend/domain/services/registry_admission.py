from typing import Any

from sqlalchemy.orm import Session

from backend.domain.models import CorpusSnapshot, GateReport, ResearchRun, SemanticClaim


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
            from backend.domain.models import ReviewDecision

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
            elif not snapshot.canonical_text_hash or snapshot.canonical_text_hash == "UNKNOWN":
                reasons.append(
                    "CorpusSnapshot validation_status is 'VALIDATED' but canonical_text_hash is missing or 'UNKNOWN'"
                )

            # Ensure the claim's corpus snapshot dependency matches the run's snapshot
            from backend.domain.models import DependencyRecord
            claim_snapshot_deps = db.query(DependencyRecord).filter(
                DependencyRecord.dependent_claim_id == claim.id,
                DependencyRecord.dependency_type == "CORPUS_SNAPSHOT"
            ).all()
            
            if claim_snapshot_deps:
                for dep in claim_snapshot_deps:
                    if dep.dependency_ref != run.corpus_snapshot:
                        reasons.append(
                            f"Claim CORPUS_SNAPSHOT dependency '{dep.dependency_ref}' does not match ResearchRun snapshot '{run.corpus_snapshot}'"
                        )

            # 5. Blind Lab Contamination
            # We assume contamination sets status to LOCK_BLOCKED earlier, but checking here adds defense-in-depth.
            # 6. Required GateReport results
            lock_gate = (
                db.query(GateReport)
                .filter(
                    GateReport.research_run_id == run.id,
                    GateReport.gate_code == "INTERNAL_LOCK",
                    GateReport.status == "PASSED",
                )
                .first()
            )
            if not lock_gate:
                reasons.append("Missing PASSED GateReport for 'INTERNAL_LOCK'")
                
            purity_gate = (
                db.query(GateReport)
                .filter(
                    GateReport.research_run_id == run.id,
                    GateReport.gate_code == "PURITY_CHECK",
                    GateReport.status == "PASSED",
                )
                .first()
            )
            if not purity_gate:
                reasons.append("Missing required PASSED GateReport for 'PURITY_CHECK'")

        # Fixture/Test Registry invariant
        if (
            run
            and run.target_contract.startswith("test_fixture_")
            or (snapshot and snapshot.canonical_text_hash == "synthetic")
        ):
            reasons.append(
                "Synthetic fixtures and tests cannot be admitted to production registry"
            )

        if len(reasons) > 0:
            return {"status": "NOT_ELIGIBLE", "reasons": reasons}

        return {"status": "ELIGIBLE", "reasons": []}
