import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.infrastructure.database import Base, canonical_migration_heads, get_db
from backend.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        connection.execute(
            text("CREATE TABLE IF NOT EXISTS alembic_version (version_num VARCHAR(32))")
        )
        connection.execute(text("DELETE FROM alembic_version"))
        for head in canonical_migration_heads():
            connection.execute(
                text("INSERT INTO alembic_version VALUES (:head)"), {"head": head}
            )
    app.dependency_overrides[get_db] = override_get_db
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def setup_claim(test_db):
    # A Research Judgment on a clean-isolation run is released by the source
    # boundary alone; no lock/gate/review is required to read it.
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

    test_db.add(
        models.IsolationState(
            id=f"iso_{uuid.uuid4().hex[:8]}",
            research_run_id=run_id,
            target_contract=run.target_contract,
            corpus_snapshot=run.corpus_snapshot,
            methodology_reference=run.methodology_revision,
            allowed_sources=["QURAN_CORPUS"],
            is_contaminated="CLEAN",
        )
    )

    claim_id = f"jud_{uuid.uuid4().hex[:8]}"
    claim = models.SemanticClaim(
        id=claim_id,
        research_run_id=run_id,
        contract_type="ROOT_CORE",
        research_state="PREFERRED",
        canonical_state="NOT_CANONICAL",
        result_strength="STRONG",
        verification_state="NOT_VERIFIED",
        preferred_conclusion="العلم هو الإحاطة بحقيقة الشيء",
        plain_explanation="العلم هو الإحاطة بحقيقة الشيء",
    )
    test_db.add(claim)

    audit = models.AuditLog(
        id=f"aud_{uuid.uuid4().hex[:8]}",
        entity_id=claim_id,
        entity_type="ResearchJudgment",
        action="CREATE",
        actor="SYSTEM",
        new_state="PREFERRED",
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
        analysis_stage="RESEARCH_JUDGMENT",
        provider="pydantic-ai",
        model="TestModel",
        skill_version="v4.0",
        prompt_revision="rev_1",
        tools_available=["corpus_search", "lexical_lookup"],
        input_artifact_refs=[run_id],
        output_artifact_refs=["judgment:1"],
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
    assert data["research_state"] == "PREFERRED"
    assert data["canonical_state"] == "NOT_CANONICAL"
    assert data["result_strength"] == "STRONG"
    assert data["verification_state"] == "NOT_VERIFIED"
    assert len(data["dependencies"]) == 1
    assert data["dependencies"][0]["dependency_ref"] == "snap_canonical_01"
    assert "snap_canonical_01" in data["affected_by"]


def test_knowledge_explorer_not_found(test_db):
    res = client.get("/knowledge/explorer/nonexistent_claim")
    assert res.status_code == 404


def test_audit_logs_read_model(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    res = client.get("/audit")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    res_filtered = client.get(
        f"/audit?entity_type=ResearchJudgment&entity_id={claim_id}"
    )
    assert res_filtered.status_code == 200
    filtered_logs = res_filtered.json()
    assert len(filtered_logs) == 1
    assert filtered_logs[0]["action"] == "CREATE"
    assert filtered_logs[0]["actor"] == "SYSTEM"


def test_judgment_history_read_model(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    record = models.VerificationRecord(
        id=f"ver_{uuid.uuid4().hex[:8]}",
        claim_id=claim_id,
        verifier_identity="expert_1",
        verification_type="INDEPENDENT",
        decision="VERIFIED",
        rationale="Independently reproduced against the admitted corpus.",
        evidence_refs=[],
        evaluated_claim_revision=1,
    )
    test_db.add(record)
    test_db.commit()

    res = client.get(f"/judgments/{claim_id}/history")
    assert res.status_code == 200
    data = res.json()
    assert data["claim_id"] == claim_id
    assert data["current_revision"] == 1
    assert len(data["revisions"]) >= 1
    assert len(data["verification_records"]) == 1
    assert data["verification_records"][0]["decision"] == "VERIFIED"
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

    res = client.get(f"/runs/{run_id}/ai/traces")
    assert res.status_code == 200
    traces = res.json()
    assert len(traces) == 1
    assert traces[0]["id"] == ai_rec_id
    assert traces[0]["analysis_stage"] == "RESEARCH_JUDGMENT"
    assert traces[0]["provider"] == "pydantic-ai"
    assert traces[0]["execution_status"] == "SUCCESS"
    assert "tools_available" in traces[0]

    res_single = client.get(f"/ai/traces/{ai_rec_id}")
    assert res_single.status_code == 200
    single = res_single.json()
    assert single["id"] == ai_rec_id
    assert single["model"] == "TestModel"


def test_get_provenance(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    res = client.get(f"/judgments/{claim_id}/provenance")
    assert res.status_code == 200
    data = res.json()
    assert data["claim"]["id"] == claim_id
    assert data["claim"]["research_state"] == "PREFERRED"
    assert len(data["audit_trail"]) == 1
    assert data["audit_trail"][0]["action"] == "CREATE"
    assert len(data["dependencies"]) == 1
    assert data["dependencies"][0]["type"] == "CORPUS_SNAPSHOT"


def test_methodology_diagnostics_expose_all_named_dimensions(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    res = client.get(f"/judgments/{claim_id}/diagnostics")
    assert res.status_code == 200
    data = res.json()
    assert data["claim_id"] == claim_id

    dimensions = [finding["dimension"] for finding in data["findings"]]
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

    # Diagnostics guide challenge/review; on a clean run none is a hard failure,
    # and no QualityProfile metrics are manufactured.
    assert data["hard_blockers"] == []
    assert all(finding["hard_blocker"] is False for finding in data["findings"])
    assert (
        test_db.query(models.QualityProfile)
        .filter(models.QualityProfile.claim_id == claim_id)
        .count()
        == 0
    )


def test_diagnostics_hidden_for_contaminated_source_boundary(test_db):
    run = models.ResearchRun(
        id="run_contaminated",
        target_contract="ROOT_CORE",
        target_expression="test",
        methodology_revision="v4.0",
        corpus_snapshot="snapshot_test",
        authority_context={"source": "test"},
    )
    isolation = models.IsolationState(
        id="isolation_run_contaminated",
        research_run_id=run.id,
        target_contract=run.target_contract,
        corpus_snapshot=run.corpus_snapshot,
        methodology_reference=run.methodology_revision,
        allowed_sources=["QURAN_CORPUS"],
        is_contaminated="PRIOR_CONTAMINATED",
        contamination_reason="actual prohibited-source read",
    )
    test_db.add_all([run, isolation])
    claim_id = f"jud_tafsir_{uuid.uuid4().hex[:6]}"
    claim = models.SemanticClaim(
        id=claim_id,
        contract_type="ROOT_CORE",
        research_state="UNRESOLVED",
        result_strength="UNRESOLVED",
        research_run_id=run.id,
    )
    test_db.add(claim)
    test_db.commit()

    # A contaminated source boundary hides the judgment from all read APIs.
    res = client.get(f"/judgments/{claim_id}/diagnostics")
    assert res.status_code == 403


def test_audit_api_is_read_only_and_cannot_mutate_domain_state(setup_claim, test_db):
    claim = test_db.query(models.SemanticClaim).first()
    run = test_db.query(models.ResearchRun).first()
    claim_state = claim.research_state
    run_state = run.status

    resp = client.post(
        "/api/audit/log",
        json={
            "entity_id": claim.id,
            "entity_type": "ResearchJudgment",
            "action": "MUTATE",
            "previous_state": claim_state,
            "new_state": "PREFERRED",
            "actor": "UNTRUSTED_CLIENT",
        },
    )

    assert resp.status_code == 404
    test_db.refresh(claim)
    test_db.refresh(run)
    assert claim.research_state == claim_state
    assert run.status == run_state


def test_get_reproduction_manifest(test_db, setup_claim):
    claim_id = setup_claim["claim_id"]
    res = client.get(f"/judgments/{claim_id}/reproduction-manifest")
    assert res.status_code == 200
    data = res.json()
    assert data["claim_id"] == claim_id
    assert data["target_expression"] == "علم"
    assert len(data["dependencies"]) == 1
    assert data["dependencies"][0]["type"] == "CORPUS_SNAPSHOT"
    assert len(data["ai_execution_traces"]) == 1
    assert "generated_at" in data


def test_operations_health(test_db):
    res = client.get("/operations/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert data["configuration"]["ai_governance"] == "enforced"
    assert data["database"]["status"] == "CURRENT"


def test_missing_run_semantic_dictionary_is_contractual_404(test_db):
    response = client.get("/runs/missing/read_semantic_dictionary")

    assert response.status_code == 404
    assert response.json() == {
        "status": "ERROR",
        "message": "Run not found",
        "detail": "Run not found",
    }
