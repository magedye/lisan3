import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.infrastructure.database import Base, get_db
from backend.main import app

# Setup mock DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


@pytest.fixture
def test_db():
    app.dependency_overrides[get_db] = override_get_db
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture
def setup_claim(test_db):
    # Setup Corpus Snapshot
    snapshot_id = f"snap_{uuid.uuid4().hex[:8]}"
    snap = models.CorpusSnapshot(
        id=snapshot_id,
        canonical_text_source="TANZIL",
        canonical_text_version="v1",
        canonical_text_hash="hash",
        validation_status="VALIDATED",
    )
    test_db.add(snap)

    # Setup Run
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    run = models.ResearchRun(
        id=run_id,
        target_contract="test",
        target_expression="test",
        methodology_revision="v1",
        corpus_snapshot=snapshot_id,
        authority_context="test",
        status="LOCK_INTERNAL_RESULT",
    )
    test_db.add(run)

    # Setup Gate Report
    gate1 = models.GateReport(
        id=f"gate_{uuid.uuid4().hex[:8]}",
        research_run_id=run_id,
        gate_code="INTERNAL_LOCK",
        status="PASSED",
    )
    test_db.add(gate1)
    
    gate2 = models.GateReport(
        id=f"gate_{uuid.uuid4().hex[:8]}",
        research_run_id=run_id,
        gate_code="PURITY_CHECK",
        status="PASSED",
    )
    test_db.add(gate2)

    # Setup Claim
    claim_id = f"clm_{uuid.uuid4().hex[:8]}"
    claim = models.SemanticClaim(
        id=claim_id,
        research_run_id=run_id,
        contract_type="test",
        epistemic_state="LOCK_INTERNAL_RESULT",
        review_state="PENDING_REVIEW",
        freshness_state="CURRENT",
        publication_state="UNPUBLISHED",
    )
    test_db.add(claim)
    test_db.commit()

    return {"run_id": run_id, "claim_id": claim_id, "snapshot_id": snapshot_id}


def test_publish_unapproved_claim_fails(setup_claim):
    claim_id = setup_claim["claim_id"]

    # Try to publish
    res = client.post(
        f"/claims/{claim_id}/publish",
        json={"publisher_identity": "admin", "target_registry": "public"},
    )

    assert res.status_code == 403
    assert (
        "Claim review state is 'PENDING_REVIEW', expected 'APPROVED'"
        in res.json()["detail"]
    )


def test_approve_and_publish_claim(setup_claim):
    claim_id = setup_claim["claim_id"]

    # Review
    res = client.post(
        f"/claims/{claim_id}/reviews",
        json={
            "reviewer_identity": "reviewer_1",
            "decision": "APPROVED",
            "rationale": "Looks good",
        },
    )
    assert res.status_code == 200

    # Publish
    res = client.post(
        f"/claims/{claim_id}/publish",
        json={"publisher_identity": "admin", "target_registry": "public"},
    )

    assert res.status_code == 200
    assert res.json()["publication_state"] == "PUBLISHED"


def test_reject_claim_blocks_publication(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]

    # Review
    res = client.post(
        f"/claims/{claim_id}/reviews",
        json={
            "reviewer_identity": "reviewer_1",
            "decision": "REJECTED",
            "rationale": "Needs work",
        },
    )
    assert res.status_code == 200

    claim = (
        test_db.query(models.SemanticClaim)
        .filter(models.SemanticClaim.id == claim_id)
        .first()
    )
    assert claim.review_state == "REJECTED"
    assert claim.publication_state == "BLOCKED"

    # Publish
    res = client.post(
        f"/claims/{claim_id}/publish",
        json={"publisher_identity": "admin", "target_registry": "public"},
    )

    assert res.status_code == 403


def test_stale_review_blocks_publication(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]

    # 1. Approve claim at revision 1
    res = client.post(
        f"/claims/{claim_id}/reviews",
        json={
            "reviewer_identity": "reviewer_1",
            "decision": "APPROVED",
            "rationale": "Looks good",
        },
    )
    assert res.status_code == 200

    # 2. Update claim to revision 2
    claim = (
        test_db.query(models.SemanticClaim)
        .filter(models.SemanticClaim.id == claim_id)
        .first()
    )
    claim.revision_id = 2
    test_db.commit()

    # 3. Try to publish
    res = client.post(
        f"/claims/{claim_id}/publish",
        json={"publisher_identity": "admin", "target_registry": "public"},
    )

    assert res.status_code == 403
    assert "Latest APPROVED review is for revision 1" in res.json()["detail"]


def test_unlocked_epistemic_state_blocks_publication(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    claim = test_db.query(models.SemanticClaim).filter(models.SemanticClaim.id == claim_id).first()
    claim.epistemic_state = "HYPOTHESIS"
    claim.review_state = "APPROVED"
    test_db.commit()

    res = client.post(
        f"/claims/{claim_id}/publish",
        json={"publisher_identity": "admin", "target_registry": "public"},
    )
    assert res.status_code == 403
    assert "Claim epistemic state is 'HYPOTHESIS'" in res.json()["detail"]


def test_non_current_freshness_blocks_publication(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    claim = test_db.query(models.SemanticClaim).filter(models.SemanticClaim.id == claim_id).first()
    claim.freshness_state = "STALE"
    claim.review_state = "APPROVED"
    test_db.commit()

    res = client.post(
        f"/claims/{claim_id}/publish",
        json={"publisher_identity": "admin", "target_registry": "public"},
    )
    assert res.status_code == 403
    assert "Claim freshness state is 'STALE'" in res.json()["detail"]


def test_corpus_snapshot_mismatch_blocks_publication(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    claim = test_db.query(models.SemanticClaim).filter(models.SemanticClaim.id == claim_id).first()
    claim.review_state = "APPROVED"
    
    # Add a mismatching dependency
    dep = models.DependencyRecord(
        id="dep_mismatch",
        dependent_claim_id=claim_id,
        dependency_type="CORPUS_SNAPSHOT",
        dependency_ref="wrong_snapshot_id"
    )
    test_db.add(dep)
    test_db.commit()

    res = client.post(
        f"/claims/{claim_id}/publish",
        json={"publisher_identity": "admin", "target_registry": "public"},
    )
    assert res.status_code == 403
    assert "does not match ResearchRun snapshot" in res.json()["detail"]


def test_unvalidated_corpus_snapshot_blocks_publication(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    snap_id = setup_claim["snapshot_id"]
    snap = test_db.query(models.CorpusSnapshot).filter(models.CorpusSnapshot.id == snap_id).first()
    snap.validation_status = "PENDING"
    test_db.commit()
    
    # Approve review
    res_rev = client.post(
        f"/claims/{claim_id}/reviews",
        json={"reviewer_identity": "rev1", "decision": "APPROVED"},
    )
    assert res_rev.status_code == 200

    res = client.post(
        f"/claims/{claim_id}/publish",
        json={"publisher_identity": "admin", "target_registry": "public"},
    )
    assert res.status_code == 403
    assert "CorpusSnapshot validation_status is 'PENDING'" in res.json()["detail"]


def test_missing_internal_lock_gate_blocks_publication(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    run_id = setup_claim["run_id"]
    
    # Delete gate report
    test_db.query(models.GateReport).filter(models.GateReport.research_run_id == run_id).delete()
    test_db.commit()

    # Approve review
    client.post(
        f"/claims/{claim_id}/reviews",
        json={"reviewer_identity": "rev1", "decision": "APPROVED"},
    )

    res = client.post(
        f"/claims/{claim_id}/publish",
        json={"publisher_identity": "admin", "target_registry": "public"},
    )
    assert res.status_code == 403
    assert "Missing PASSED GateReport for 'INTERNAL_LOCK'" in res.json()["detail"]


def test_synthetic_fixture_blocks_publication(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    run_id = setup_claim["run_id"]
    run = test_db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()
    run.target_contract = "test_fixture_synthetic"
    test_db.commit()

    client.post(
        f"/claims/{claim_id}/reviews",
        json={"reviewer_identity": "rev1", "decision": "APPROVED"},
    )

    res = client.post(
        f"/claims/{claim_id}/publish",
        json={"publisher_identity": "admin", "target_registry": "public"},
    )
    assert res.status_code == 403
    assert "Synthetic fixtures and tests cannot be admitted to production registry" in res.json()["detail"]

