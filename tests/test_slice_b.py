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
    db.query(models.ObservationArtifact).delete()
    db.query(models.IsolationState).delete()
    db.query(models.CorpusOccurrence).delete()
    db.query(models.SemanticClaim).delete()
    db.query(models.ResearchRun).delete()
    db.commit()
    db.close()
    yield
    app.dependency_overrides.clear()


def create_fixture_run(run_id: str) -> str:
    db = TestingSessionLocal()
    db.add(
        models.ResearchRun(
            id=run_id,
            target_contract="ROOT_CORE",
            target_expression="ضرب",
            methodology_revision="v7.1-test-fixture",
            corpus_snapshot="snap1-test-fixture",
            authority_context={"profile": "test_fixture"},
        )
    )
    db.add(
        models.CorpusOccurrence(
            id="c1",
            snapshot_id="snap1-test-fixture",
            expression="ضرب",
            verse_ref="2:60",
            text="اضرب بعصاك",
        )
    )
    db.commit()
    db.close()
    return run_id


def test_slice_b_end_to_end():
    # 1. Create an explicit test-only run for this downstream Blind Lab slice.
    run_id = create_fixture_run("run_slice_b_end_to_end")

    # 2. Enter host-derived Blind Lab Preflight.
    iso_resp = client.post(f"/runs/{run_id}/blind/preflight")
    assert iso_resp.status_code == 200
    assert iso_resp.json()["is_contaminated"] == "CLEAN"

    # 4. Read admitted corpus data
    corpus_resp = client.get(f"/runs/{run_id}/corpus")
    assert corpus_resp.status_code == 200
    assert len(corpus_resp.json()) == 1

    # 5. Prohibited Read (Fails Closed & Contaminates)
    prohibited_resp = client.get(f"/runs/{run_id}/read_semantic_dictionary")
    assert prohibited_resp.status_code == 403
    assert "Prohibited source read blocked" in prohibited_resp.json()["detail"]

    # 6. Verify contamination blocks further reading and observations
    # This assertion is removed because a blocked read no longer contaminates the state.
    # The actual contamination logic is tested in test_contamination_audit.


def test_observation_rejection():
    # 1. Create an explicit test-only run.
    run_id = create_fixture_run("run_slice_b_observation")

    # 2. Preflight
    client.post(f"/runs/{run_id}/blind/preflight")

    # 3. Valid Structural Observation
    valid_obs = client.post(
        f"/runs/{run_id}/observations",
        json={
            "occurrence_ref": "c1",
            "form": "verb (past)",
            "syntax": "imperative phrase",
        },
    )
    assert valid_obs.status_code == 200

    # 4. Invalid Semantic Injection (Explicit forbid extra fields)
    invalid_obs = client.post(
        f"/runs/{run_id}/observations",
        json={
            "occurrence_ref": "c1",
            "form": "verb",
            "semantic_definition": "hitting",  # Field not in schema, strictly forbidden
        },
    )
    assert invalid_obs.status_code == 422

    # 5. Legitimate observation containing a keyword in text should PASS
    legit_obs = client.post(
        f"/runs/{run_id}/observations",
        json={
            "occurrence_ref": "c1",
            "form": "verb",
            "local_context": "The root meaning might be debated, but structurally it takes an object",
        },
    )
    assert legit_obs.status_code == 200


def test_contamination_audit():
    # Create an explicit test-only run and preflight.
    run_id = create_fixture_run("run_slice_b_contamination")
    client.post(f"/runs/{run_id}/blind/preflight")

    # Prohibited read
    prohibited_resp = client.get(f"/runs/{run_id}/read_semantic_dictionary")
    assert prohibited_resp.status_code == 403

    # It should not contaminate immediately, it should just log an event
    iso_state = client.get(f"/runs/{run_id}/blind")
    assert iso_state.json()["is_contaminated"] == "CLEAN"

    # Actual contamination via trigger
    client.post(f"/runs/{run_id}/record_contamination?reason=Actually exposed")
    iso_state_after = client.get(f"/runs/{run_id}/blind")
    assert iso_state_after.json()["is_contaminated"] == "PRIOR_CONTAMINATED"
