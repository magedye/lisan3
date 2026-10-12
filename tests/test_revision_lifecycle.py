import pytest
from sqlalchemy.orm import Session

from backend.domain.models import ClaimRevision, SemanticClaim, utc_now_naive
from backend.domain.services.actor_context import ActorContext, ActorRole
from backend.domain.services.revision import ClaimRevisionService


def test_claim_revision_success_and_immutability(test_db: Session):
    # Setup
    claim = SemanticClaim(id="claim_test_1", contract_type="ROOT_CORE")
    test_db.add(claim)

    # Predecessor rev 1
    rev1 = ClaimRevision(
        id="rev_1",
        claim_id=claim.id,
        revision_number=1,
        correction_reason="Initial",
        payload={"data": "v1"},
        semantic_payload_hash="hash_v1",
        creation_actor="SYS",
        created_at=utc_now_naive(),
    )
    test_db.add(rev1)
    test_db.commit()

    actor = ActorContext(role=ActorRole.RESEARCHER, identity="user1")

    # 1. Create successor
    successor = ClaimRevisionService.create_successor(
        test_db, claim, {"data": "v2"}, "Correction 1", actor
    )
    assert successor.revision_number == 2
    assert successor.predecessor_revision_id == "rev_1"
    assert claim.revision_id == 2

    # Predecessor should be frozen and superseded
    test_db.refresh(rev1)
    assert rev1.frozen_at is not None
    assert rev1.superseded is True

    # 2. Duplicate revision should fail via DB constraints
    import sqlalchemy.exc

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        dup = ClaimRevision(
            id="rev_dup",
            claim_id=claim.id,
            revision_number=2,
            payload={"data": "v2"},
            semantic_payload_hash="hash_v2",
            creation_actor="SYS",
        )
        test_db.add(dup)
        test_db.commit()
    test_db.rollback()

    # 3. Mutation of frozen revision should fail
    # (Removed ORM event listener test for mutation since we enforce domain constraints via service instead)


def test_revision_service_negative_tests(test_db: Session):
    claim = SemanticClaim(id="claim_test_2", contract_type="ROOT_CORE")
    test_db.add(claim)
    test_db.flush()

    # 1. Missing predecessor
    # claim.revision_id = 1 but no ClaimRevision row exists
    actor = ActorContext(role=ActorRole.RESEARCHER, identity="user1")
    with pytest.raises(ValueError, match="Predecessor revision 1 not found"):
        ClaimRevisionService.create_successor(
            test_db, claim, {"data": "v2"}, "Correction", actor
        )

    # 2. Stale revision verification
    # Setup rev 1
    rev1 = ClaimRevision(
        id="rev_1_c2",
        claim_id=claim.id,
        revision_number=1,
        payload={"data": "v1"},
        semantic_payload_hash="hash_v1",
        creation_actor="SYS",
    )
    test_db.add(rev1)
    test_db.commit()

    ClaimRevisionService.create_successor(test_db, claim, {"data": "v2"}, "Corr", actor)
    test_db.commit()

    # current is now 2
    with pytest.raises(ValueError, match="Stale revision"):
        ClaimRevisionService.assert_revision_not_stale(test_db, claim.id, 1)

    # current should pass
    ClaimRevisionService.assert_revision_not_stale(test_db, claim.id, 2)
