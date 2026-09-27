import pytest
from sqlalchemy.orm import Session

from backend.domain.models import SemanticClaim
from backend.domain.services.actor_context import ActorContext, ActorRole
from backend.domain.services.independent_review import IndependentReviewService


def test_independent_review_negative_tests(test_db: Session):
    claim = SemanticClaim(id="claim_rev_1", contract_type="ROOT_CONCEPT", revision_id=1)
    test_db.add(claim)
    test_db.commit()

    reviewer = ActorContext(role=ActorRole.REVIEWER, identity="reviewer1")

    # Assign review
    review = IndependentReviewService.assign_review_context(test_db, claim, reviewer)
    assert review.review_status == "PENDING"

    # 1. Asserting independence metadata is present
    with pytest.raises(ValueError, match="Independence metadata is strictly required"):
        IndependentReviewService.record_verdict(
            test_db,
            review_id=review.id,
            verdict="VERIFIED",
            scope_disposition="FULL",
            evidence_package_ref="pkg1",
            independence_metadata={},
        )

    # 2. Invalidating pending reviews when a claim is revised
    # Simulate claim revision
    claim.revision_id = 2
    test_db.add(claim)
    test_db.commit()

    IndependentReviewService.invalidate_pending_reviews(test_db, claim.id)

    test_db.refresh(review)
    assert review.review_status == "INVALIDATED"
    assert review.superseded_by == "REVISION"

    # Try recording verdict on invalidated review
    with pytest.raises(ValueError, match="is not PENDING"):
        IndependentReviewService.record_verdict(
            test_db,
            review_id=review.id,
            verdict="VERIFIED",
            scope_disposition="FULL",
            evidence_package_ref="pkg1",
            independence_metadata={"check": "passed"},
        )
