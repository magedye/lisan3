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
        validation_status="UNVERIFIED",
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
        review_state="REVIEW_REQUIRED",
        freshness_state="CURRENT",
        publication_state="PRIVATE_WORKING",
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
        "Claim review state is 'REVIEW_REQUIRED', expected 'APPROVED'"
        in res.json()["detail"]
    )


def test_review_approval_cannot_bypass_corpus_and_gate_authority(setup_claim):
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

    assert res.status_code == 403
    detail = res.json()["detail"]
    assert "validation_status is 'UNVERIFIED'" in detail
    assert "Missing PASSED GateReport for 'INTERNAL_LOCK'" in detail
    assert "Missing required PASSED GateReport for 'PURITY_CHECK'" in detail


def test_client_passed_gate_status_is_ignored_and_derived(test_db, setup_claim):
    run_id = setup_claim["run_id"]

    purity_response = client.post(
        f"/runs/{run_id}/gates",
        json={
            "gate_code": "PURITY_CHECK",
            "status": "PASSED",
            "evidence_refs": ["client:forged"],
            "evaluated_revision": "forged",
        },
    )
    assert purity_response.status_code == 200
    assert purity_response.json()["status"] == "FAILED"
    assert purity_response.json()["evidence_refs"] == []

    lock_response = client.post(
        f"/runs/{run_id}/gates",
        json={
            "gate_code": "INTERNAL_LOCK",
            "status": "PASSED",
            "evidence_refs": ["client:forged"],
            "evaluated_revision": "forged",
        },
    )
    assert lock_response.status_code == 200
    assert lock_response.json()["status"] == "FAILED"
    run = test_db.get(models.ResearchRun, run_id)
    assert run.status == "LOCK_BLOCKED"


def test_forged_passed_gates_do_not_authorize_claim_creation(setup_claim):
    run_id = setup_claim["run_id"]

    response = client.post(
        f"/runs/{run_id}/claims",
        json={"contract_type": "ROOT_CORE", "research_run_id": run_id},
    )

    assert response.status_code == 403
    assert "valid INTERNAL_LOCK gate not passed" in response.json()["detail"]


def test_dependency_on_another_claim_does_not_satisfy_traceability(
    test_db, setup_claim
):
    claim = test_db.get(models.SemanticClaim, setup_claim["claim_id"])
    claim.review_state = "APPROVED"
    other_claim = models.SemanticClaim(
        id="clm_other_entity",
        research_run_id=setup_claim["run_id"],
        contract_type="ROOT_CORE",
    )
    test_db.add(other_claim)
    test_db.add(
        models.DependencyRecord(
            id="dep_other_entity",
            dependent_claim_id=other_claim.id,
            dependency_type="CORPUS_SNAPSHOT",
            dependency_ref=setup_claim["snapshot_id"],
        )
    )
    test_db.commit()

    response = client.post(
        f"/claims/{claim.id}/publish",
        json={"publisher_identity": "admin", "target_registry": "public"},
    )

    assert response.status_code == 403
    assert (
        "Claim must have exactly one CORPUS_SNAPSHOT dependency"
        in response.json()["detail"]
    )


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
    assert claim.publication_state == "PRIVATE_WORKING"

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
    claim = (
        test_db.query(models.SemanticClaim)
        .filter(models.SemanticClaim.id == claim_id)
        .first()
    )
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
    claim = (
        test_db.query(models.SemanticClaim)
        .filter(models.SemanticClaim.id == claim_id)
        .first()
    )
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
    claim = (
        test_db.query(models.SemanticClaim)
        .filter(models.SemanticClaim.id == claim_id)
        .first()
    )
    claim.review_state = "APPROVED"

    # Add a mismatching dependency
    dep = models.DependencyRecord(
        id="dep_mismatch",
        dependent_claim_id=claim_id,
        dependency_type="CORPUS_SNAPSHOT",
        dependency_ref="wrong_snapshot_id",
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
    snap = (
        test_db.query(models.CorpusSnapshot)
        .filter(models.CorpusSnapshot.id == snap_id)
        .first()
    )
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
    test_db.query(models.GateReport).filter(
        models.GateReport.research_run_id == run_id
    ).delete()
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
    run = (
        test_db.query(models.ResearchRun)
        .filter(models.ResearchRun.id == run_id)
        .first()
    )
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
    assert (
        "Synthetic fixtures and tests cannot be admitted to production registry"
        in res.json()["detail"]
    )
