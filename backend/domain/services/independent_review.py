import uuid

from sqlalchemy.orm import Session

from backend.domain.models import (
    IndependentReview,
    SemanticClaim,
    InternalResultSnapshotRecord,
    utc_now_naive,
)
from backend.domain.services.actor_context import ActorContext
from backend.domain.services.tool_reality import ToolRealityService


class IndependentReviewService:
    @staticmethod
    def assign_review_context(
        db: Session,
        claim: SemanticClaim,
        reviewer: ActorContext,
    ) -> IndependentReview:
        """Assigns a review context to a revision, rendering it PENDING."""
        # Assert independence
        # (A real implementation would check that reviewer != claim.creation_actor etc.)

        review = IndependentReview(
            id=f"ir_{uuid.uuid4().hex[:8]}",
            claim_id=claim.id,
            revision_id=claim.revision_id,
            reviewer_identity=reviewer.identity,
            review_status="PENDING",
            created_at=utc_now_naive(),
        )
        db.add(review)
        db.flush()
        return review

    @staticmethod
    def record_verdict(
        db: Session,
        review_id: str,
        verdict: str,
        scope_disposition: str,
        evidence_package_ref: str,
        independence_metadata: dict,
    ) -> IndependentReview:
        review = (
            db.query(IndependentReview)
            .filter(IndependentReview.id == review_id)
            .first()
        )
        if not review:
            raise ValueError(f"Review {review_id} not found")

        if review.review_status != "PENDING":
            raise ValueError(f"Review {review_id} is not PENDING")

        if not independence_metadata:
            raise ValueError(
                "Independence metadata is strictly required for an independent review"
            )

        claim = db.query(SemanticClaim).filter(SemanticClaim.id == review.claim_id).first()
        if not claim:
            raise ValueError(f"Claim {review.claim_id} not found")

        # Runtime Integration of Slice H (Tool Reality) & Track 4 (Internal Snapshot)
        if verdict == "VERIFIED":
            snapshot = db.query(InternalResultSnapshotRecord).filter(InternalResultSnapshotRecord.claim_id == claim.id).first()
            if not snapshot:
                raise ValueError("External comparison requires a valid frozen internal snapshot")
            
            if claim.research_run_id:
                # Assuming generic required_tools for now, or fetch from claim metadata
                # Just checking that ToolReality validate passes if any tools were required
                required_tools = claim.falsification_plan.get("required_tools", []) if claim.falsification_plan else []
                if required_tools:
                    ToolRealityService.validate_tool_reality_for_claim(db, claim.research_run_id, required_tools)

        # Invalidate pending reviews if claim was revised
        if claim.revision_id != review.revision_id:
            review.review_status = "INVALIDATED"
            db.add(review)
            raise ValueError(f"Claim {claim.id} was revised. Review is obsolete.")

        review.review_status = "COMPLETED"
        review.verdict = verdict
        review.scope_disposition = scope_disposition
        review.evidence_package_ref = evidence_package_ref
        review.independence_metadata = independence_metadata
        review.completed_at = utc_now_naive()

        db.add(review)

        db.flush()
        return review

    @staticmethod
    def invalidate_pending_reviews(db: Session, claim_id: str):
        """When a claim is revised, any pending reviews on older revisions are invalidated/superseded."""
        pending = (
            db.query(IndependentReview)
            .filter(
                IndependentReview.claim_id == claim_id,
                IndependentReview.review_status == "PENDING",
            )
            .all()
        )
        for rev in pending:
            rev.review_status = "INVALIDATED"
            rev.superseded_by = "REVISION"
            db.add(rev)
        db.flush()
