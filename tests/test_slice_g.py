import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
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
with engine.begin() as connection:
    connection.execute(text("CREATE TABLE alembic_version (version_num VARCHAR(32))"))
    connection.execute(
        text("INSERT INTO alembic_version VALUES ('c9e2a7f4b6d1')")
    )

client = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    try:
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
def setup_claim(test_db):
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    run = models.ResearchRun(
        id=run_id,
        target_contract="ROOT_CORE",
        target_expression="علم",
        methodology_revision="v4.0",
        corpus_snapshot="snap_canonical_01",
        authority_context={"source": "CANONICAL"},
        status="ACTIVE",
    )
    test_db.add(run)

    claim_id = f"clm_{uuid.uuid4().hex[:8]}"
    claim = models.SemanticClaim(
        id=claim_id,
        research_run_id=run_id,
        contract_type="ROOT_CORE",
        abstract_root_core="العلم هو الإحاطة بحقيقة الشيء",
        epistemic_state="LOCK_INTERNAL_RESULT",
        review_state="NOT_REVIEWED",
        freshness_state="CURRENT",
        publication_state="PRIVATE_WORKING",
    )
    test_db.add(claim)

    audit = models.AuditLog(
        id=f"aud_{uuid.uuid4().hex[:8]}",
        entity_id=claim_id,
        entity_type="SemanticClaim",
        action="CREATE",
        actor="SYSTEM",
        new_state="LOCK_INTERNAL_RESULT",
    )
    test_db.add(audit)

    dep = models.DependencyRecord(
        id=f"dep_{uuid.uuid4().hex[:8]}",
        dependent_claim_id=claim_id,
        dependency_type="CORPUS_SNAPSHOT",
        dependency_ref="snap_canonical_01",
    )
    test_db.add(dep)

    ai_rec = models.AIExecutionRecord(
        id=f"ai_{uuid.uuid4().hex[:8]}",
        research_run_id=run_id,
        analysis_stage="HYPOTHESIS_GENERATION",
        provider="pydantic-ai",
        model="TestModel",
        skill_version="v4.0",
        prompt_revision="rev_1",
        tools_available=["corpus_search", "lexical_lookup"],
        input_artifact_refs=[run_id],
        output_artifact_refs=["hyp_1"],
        execution_status="SUCCESS",
    )
    test_db.add(ai_rec)

    test_db.commit()
    return {"claim_id": claim_id, "run_id": run_id, "ai_rec_id": ai_rec.id}


def test_knowledge_explorer(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    res = client.get(f"/knowledge/explorer/{claim_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["claim_id"] == claim_id
    assert data["target_expression"] == "علم"
    assert data["epistemic_state"] == "LOCK_INTERNAL_RESULT"
    assert data["review_state"] == "NOT_REVIEWED"
    assert data["freshness_state"] == "CURRENT"
    assert data["publication_state"] == "PRIVATE_WORKING"
    assert len(data["dependencies"]) == 1
    assert data["dependencies"][0]["dependency_ref"] == "snap_canonical_01"
    assert "snap_canonical_01" in data["affected_by"]


def test_knowledge_explorer_not_found():
    res = client.get("/knowledge/explorer/nonexistent_claim")
    assert res.status_code == 404


def test_audit_logs_read_model(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    # List all
    res = client.get("/audit")
    assert res.status_code == 200
    logs = res.json()
    assert len(logs) >= 1

    # Filter by entity_type and entity_id
    res_filtered = client.get(f"/audit?entity_type=SemanticClaim&entity_id={claim_id}")
    assert res_filtered.status_code == 200
    filtered_logs = res_filtered.json()
    assert len(filtered_logs) == 1
    assert filtered_logs[0]["action"] == "CREATE"
    assert filtered_logs[0]["actor"] == "SYSTEM"


def test_claim_history_read_model(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    # Add a review decision
    rev = models.ReviewDecision(
        id=f"rev_{uuid.uuid4().hex[:8]}",
        claim_id=claim_id,
        reviewer_identity="expert_1",
        decision="APPROVED",
        rationale="Evidence validated against canonical corpus.",
        evaluated_claim_revision=1,
    )
    test_db.add(rev)
    test_db.commit()

    res = client.get(f"/claims/{claim_id}/history")
    assert res.status_code == 200
    data = res.json()
    assert data["claim_id"] == claim_id
    assert data["current_revision"] == 1
    assert len(data["revisions"]) >= 1
    assert len(data["review_decisions"]) == 1
    assert data["review_decisions"][0]["decision"] == "APPROVED"
    assert len(data["audit_events"]) >= 1


def test_rule_history_read_model(test_db):
    rule_code = f"RULE_HIST_{uuid.uuid4().hex[:6]}"
    rule = models.GovernanceRule(
        id=f"rule_{uuid.uuid4().hex[:8]}",
        rule_code=rule_code,
        description="Historical test rule",
        active_revision=2,
    )
    test_db.add(rule)
    rev1 = models.RuleRevision(
        id=f"rev1_{uuid.uuid4().hex[:8]}",
        rule_code=rule_code,
        revision_number=1,
        changes_described="Initial version",
        approved_by="ADMIN",
    )
    rev2 = models.RuleRevision(
        id=f"rev2_{uuid.uuid4().hex[:8]}",
        rule_code=rule_code,
        revision_number=2,
        changes_described="Hardened negative boundaries",
        approved_by="ADMIN",
    )
    prop = models.ChangeProposal(
        id=f"prop_{uuid.uuid4().hex[:8]}",
        rule_code=rule_code,
        proposed_changes="Add boundary rule",
        impact_analysis={"affected_claims": []},
        status="APPROVED",
    )
    test_db.add_all([rev1, rev2, prop])
    test_db.commit()

    res = client.get(f"/governance/rules/{rule_code}/history")
    assert res.status_code == 200
    data = res.json()
    assert data["rule_code"] == rule_code
    assert data["active_revision"] == 2
    assert len(data["revisions"]) == 2
    assert len(data["proposals"]) == 1


def test_ai_traces_read_model(test_db, setup_claim):
    run_id = setup_claim["run_id"]
    ai_rec_id = setup_claim["ai_rec_id"]

    # List traces for run
    res = client.get(f"/runs/{run_id}/ai/traces")
    assert res.status_code == 200
    traces = res.json()
    assert len(traces) == 1
    assert traces[0]["id"] == ai_rec_id
    assert traces[0]["analysis_stage"] == "HYPOTHESIS_GENERATION"
    assert traces[0]["provider"] == "pydantic-ai"
    assert traces[0]["execution_status"] == "SUCCESS"
    assert "tools_available" in traces[0]

    # Get specific trace by id
    res_single = client.get(f"/ai/traces/{ai_rec_id}")
    assert res_single.status_code == 200
    single = res_single.json()
    assert single["id"] == ai_rec_id
    assert single["model"] == "TestModel"


def test_get_provenance(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    res = client.get(f"/claims/{claim_id}/provenance")
    assert res.status_code == 200
    data = res.json()
    assert data["claim"]["id"] == claim_id
    assert len(data["audit_trail"]) == 1
    assert data["audit_trail"][0]["action"] == "CREATE"
    assert len(data["dependencies"]) == 1
    assert data["dependencies"][0]["type"] == "CORPUS_SNAPSHOT"


def test_multidimensional_quality_and_purity_findings(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    res = client.get(f"/claims/{claim_id}/quality")
    assert res.status_code == 200
    data = res.json()
    assert data["claim_id"] == claim_id
    assert data["purity_score"] == 0
    assert data["purity_rating"] == "NOT_EVALUATED"
    assert len(data["purity_findings"]) == 8

    # Verify canonical 8 dimensions from UX Constitution §6.4
    dimensions = [f["dimension"] for f in data["purity_findings"]]
    expected = [
        "DICTIONARY_FIRST",
        "CONTEXTUAL_LEAKAGE",
        "HERITAGE_BIAS",
        "TAFSIR_CONTAMINATION",
        "FORCED_UNIFICATION",
        "GENERIC_OVEREXTRACTION",
        "LETTER_SEMANTICS_OVERRELIANCE",
        "CIRCULAR_CONFIRMATION",
    ]
    for exp in expected:
        assert exp in dimensions


def test_purity_contamination_detection(test_db):
    claim_id = f"clm_tafsir_{uuid.uuid4().hex[:6]}"
    claim = models.SemanticClaim(
        id=claim_id,
        contract_type="tafsir_contaminated_contract",
        abstract_root_core="معنى متأثر بتفسير متأخر",
        epistemic_state="UNRESOLVED",
        research_run_id="run_123",
    )
    test_db.add(claim)

    hyp = models.Hypothesis(
        id=f"hyp_{uuid.uuid4().hex[:8]}",
        research_run_id="run_123",
        hypothesis_type="H1",
        target_contract="tafsir_contaminated_contract",
        statement="Test hypothesis",
    )
    test_db.add(hyp)
    test_db.commit()

    res = client.get(f"/claims/{claim_id}/quality")
    assert res.status_code == 200
    data = res.json()
    assert data["purity_score"] == 0


def test_audit_api_is_read_only_and_cannot_mutate_domain_state(setup_claim, test_db):
    claim = test_db.query(models.SemanticClaim).first()
    run = test_db.query(models.ResearchRun).first()
    claim_state = claim.epistemic_state
    run_state = run.status

    resp = client.post(
        "/api/audit/log",
        json={
            "entity_id": claim.id,
            "entity_type": "SemanticClaim",
            "action": "MUTATE",
            "previous_state": claim_state,
            "new_state": "LOCK_INTERNAL_RESULT",
            "actor": "UNTRUSTED_CLIENT",
        },
    )

    assert resp.status_code == 404
    test_db.refresh(claim)
    test_db.refresh(run)
    assert claim.epistemic_state == claim_state
    assert run.status == run_state


def test_get_reproduction_manifest(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    res = client.get(f"/claims/{claim_id}/reproduction_manifest")
    assert res.status_code == 200
    data = res.json()
    assert data["claim_id"] == claim_id
    assert data["target_expression"] == "العلم هو الإحاطة بحقيقة الشيء"
    assert len(data["dependencies"]) == 1
    assert data["dependencies"][0]["type"] == "CORPUS_SNAPSHOT"
    assert len(data["ai_execution_traces"]) == 1
    assert "generated_at" in data


def test_operations_health():
    res = client.get("/operations/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert data["configuration"]["ai_governance"] == "enforced"
    assert data["database"]["status"] == "CURRENT"


def test_missing_run_semantic_dictionary_is_contractual_404():
    response = client.get("/runs/missing/read_semantic_dictionary")

    assert response.status_code == 404
    assert response.json() == {
        "status": "ERROR",
        "message": "Run not found",
        "detail": "Run not found",
    }
