import json

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


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    db = TestingSessionLocal()
    db.query(models.GateReport).delete()
    db.query(models.EssentialNeighbor).delete()
    db.query(models.Hypothesis).delete()
    db.query(models.ObservationArtifact).delete()
    db.query(models.IsolationEvent).delete()
    db.query(models.IsolationState).delete()
    db.query(models.AIExecutionRecord).delete()
    db.query(models.ResearchRun).delete()
    db.commit()
    db.close()

    yield
    app.dependency_overrides.clear()


def test_ai_slice_c_integrated_flow():
    # 1. Setup an explicit fixture Run and Blind Lab. Production run admission
    # intentionally rejects arbitrary methodology and Corpus identifiers.
    run_id = "run_slice_c_ai_fixture"
    db = TestingSessionLocal()
    db.add(
        models.ResearchRun(
            id=run_id,
            target_contract="ROOT_CORE",
            target_expression="ن ش ز",
            methodology_revision="v7.1-test-fixture",
            corpus_snapshot="snap1-test-fixture",
            authority_context={"profile": "test_fixture"},
        )
    )
    db.commit()
    db.close()
    client.post(
        f"/runs/{run_id}/blind/preflight",
        json={
            "target_contract": "ROOT_CORE",
            "corpus_snapshot": "snap1-test-fixture",
            "methodology_reference": "ref_v1",
            "allowed_sources": ["QURAN_CORPUS"],
        },
    )

    # 2. Ask AI to propose a Hypothesis (Fake model returns structured response)
    ai_resp = client.post(f"/runs/{run_id}/ai/propose_hypothesis")
    assert ai_resp.status_code == 200

    # Verify AIExecutionRecord is returned and SUCCESS
    record = ai_resp.json()
    if record["execution_status"] != "SUCCESS":
        print(f"FAILED: {record['error_message']}")
    assert record["execution_status"] == "SUCCESS"
    assert record["analysis_stage"] == "HYPOTHESIS_GENERATION"

    # 3. Read the generated HypothesisProposal from the output artifacts
    output_refs = record["output_artifact_refs"]
    assert len(output_refs) > 0
    proposal_json = json.loads(output_refs[0])

    assert isinstance(proposal_json["statement"], str)

    # 4. Prove that the AI proposal is NOT directly admitted as a domain Hypothesis.
    # The application/researcher must explicitly submit it to the domain endpoint.
    domain_hyp_resp = client.post(
        f"/runs/{run_id}/hypotheses",
        json={
            "hypothesis_type": proposal_json["hypothesis_type"],
            "target_contract": proposal_json["target_contract"],
            "scope": proposal_json["scope"],
            "statement": proposal_json["statement"],
            "supporting_evidence_refs": proposal_json.get(
                "supporting_evidence_refs", []
            ),
            "counterevidence_refs": [],
            "unresolved_cases": proposal_json.get("unresolved_cases", []),
            "rejection_condition": proposal_json["rejection_condition"],
            "provenance": f"Derived from AIExecutionRecord {record['id']}",
        },
    )

    assert domain_hyp_resp.status_code == 200
    assert domain_hyp_resp.json()["statement"] == proposal_json["statement"]
