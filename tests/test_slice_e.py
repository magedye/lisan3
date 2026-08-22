import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.infrastructure.database import Base, get_db
from backend.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def test_db():
    app.dependency_overrides[get_db] = override_get_db
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def setup_governance(test_db):
    rule_id = f"rule_{uuid.uuid4().hex[:8]}"
    rule_code = f"RULE_{uuid.uuid4().hex[:4]}"

    rule = models.GovernanceRule(
        id=rule_id, rule_code=rule_code, description="Test Rule", active_revision=1
    )
    test_db.add(rule)

    rev = models.RuleRevision(
        id=f"rev_{uuid.uuid4().hex[:8]}",
        rule_code=rule_code,
        revision_number=1,
        changes_described="Initial",
        approved_by="LOCAL_USER",
    )
    test_db.add(rev)

    snapshot_id = f"snap_{uuid.uuid4().hex[:8]}"
    snap = models.CorpusSnapshot(
        id=snapshot_id,
        canonical_text_source="TANZIL",
        canonical_text_version="v1",
        canonical_text_hash="hash",
        validation_status="VALIDATED",
    )
    test_db.add(snap)

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

    dep = models.DependencyRecord(
        id=f"dep_{uuid.uuid4().hex[:8]}",
        dependent_claim_id=claim_id,
        dependency_type="GOVERNANCE_RULE",
        dependency_ref=rule_code,
        dependency_revision=1,
    )
    test_db.add(dep)

    test_db.commit()

    return {"rule_code": rule_code, "claim_id": claim_id}


def test_create_rule(test_db):
    rule_code = f"RULE_{uuid.uuid4().hex[:8]}"
    res = client.post(
        "/governance/rules",
        json={"rule_code": rule_code, "description": "Test Creation"},
    )

    assert res.status_code == 200
    assert res.json()["rule_code"] == rule_code
    assert res.json()["active_revision"] == 1


def test_transitive_invalidation(test_db, setup_governance):
    rule_code = setup_governance["rule_code"]
    claim_id = setup_governance["claim_id"]

    res = client.post(
        "/governance/proposals",
        json={"rule_code": rule_code, "proposed_changes": "Update rule"},
    )
    assert res.status_code == 200
    proposal_id = res.json()["id"]

    # Check claim is CURRENT before approval
    claim = (
        test_db.query(models.SemanticClaim)
        .filter(models.SemanticClaim.id == claim_id)
        .first()
    )
    assert claim.freshness_state == "CURRENT"

    res = client.post(f"/governance/proposals/{proposal_id}/approve")
    assert res.status_code == 200

    # Check claim is REVALIDATION_REQUIRED after approval
    test_db.refresh(claim)
    assert claim.freshness_state == "REVALIDATION_REQUIRED"

def test_rule_mutation_scope(test_db, setup_governance):
    # Rule A will be mutated.
    rule_code_a = setup_governance["rule_code"]
    
    # Rule B should remain untouched.
    rule_code_b = f"RULE_{uuid.uuid4().hex[:8]}"
    client.post("/governance/rules", json={"rule_code": rule_code_b, "description": "Unrelated Rule"})
    
    # Setup dependent claim for Rule B
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    test_db.add(models.ResearchRun(id=run_id, target_contract="t", target_expression="t", methodology_revision="1", corpus_snapshot="snap", authority_context="t", status="LOCK"))
    claim_id_b = f"clm_{uuid.uuid4().hex[:8]}"
    test_db.add(models.SemanticClaim(id=claim_id_b, research_run_id=run_id, contract_type="t", epistemic_state="LOCK_INTERNAL_RESULT", review_state="PENDING_REVIEW", freshness_state="CURRENT", publication_state="UNPUBLISHED"))
    test_db.add(models.DependencyRecord(id=f"dep_{uuid.uuid4().hex[:8]}", dependent_claim_id=claim_id_b, dependency_type="GOVERNANCE_RULE", dependency_ref=rule_code_b, dependency_revision=1))
    test_db.commit()

    # Create proposal for Rule A
    res = client.post(
        "/governance/proposals",
        json={"rule_code": rule_code_a, "proposed_changes": "Update rule A"},
    )
    proposal_id = res.json()["id"]
    
    # Approve proposal for Rule A
    client.post(f"/governance/proposals/{proposal_id}/approve")
    
    # Check that Rule B is untouched
    rule_b = test_db.query(models.GovernanceRule).filter(models.GovernanceRule.rule_code == rule_code_b).first()
    assert rule_b.active_revision == 1
    
    # Check that Claim B is still CURRENT
    claim_b = test_db.query(models.SemanticClaim).filter(models.SemanticClaim.id == claim_id_b).first()
    assert claim_b.freshness_state == "CURRENT"

