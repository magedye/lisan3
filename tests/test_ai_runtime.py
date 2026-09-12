import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.infrastructure.database import Base, get_db
from backend.main import app
from tests.governed_baseline import (
    AUTHORIZED_TANZIL_SNAPSHOT,
    CURRENT_METHODOLOGY_ID,
    seed_current_methodology,
    seed_production_valid_tanzil_snapshot,
)

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
    db.query(models.AIExecutionRecord).delete()
    db.query(models.IsolationState).delete()
    db.query(models.ResearchRun).delete()
    db.commit()
    db.close()
    yield
    app.dependency_overrides.clear()


def test_ai_provider_boundary():
    from pydantic_ai.models.test import TestModel

    from backend.domain.services.ai_provider import get_ai_model, get_provider_name

    model = get_ai_model()
    # In tests without OPENAI_API_KEY, it should default to TestModel
    assert isinstance(model, TestModel)
    assert get_provider_name() == "pydantic_ai:test"


def test_ai_context_builder_blind_lab_enforcement():
    from backend.domain.services.ai_context import AIContextBuilder

    # This downstream test uses an explicit fixture run; arbitrary identifiers
    # are intentionally rejected by the production POST /runs admission boundary.
    run_id = "run_ai_context_fixture"
    db = TestingSessionLocal()
    seed_production_valid_tanzil_snapshot(db)
    seed_current_methodology(db)
    db.add(
        models.ResearchRun(
            id=run_id,
            target_contract="ROOT_CORE",
            target_expression="ن ش ز",
            methodology_revision=CURRENT_METHODOLOGY_ID,
            corpus_snapshot=AUTHORIZED_TANZIL_SNAPSHOT,
            authority_context={"profile": "test_fixture"},
        )
    )
    db.commit()
    db.close()

    # Enter preflight
    client.post(f"/runs/{run_id}/blind/preflight")

    db = TestingSessionLocal()
    context = AIContextBuilder.build_research_context(db, run_id)
    db.close()

    assert context["source_policy"]["evidence_sources"] == [
        "ADMITTED_CANONICAL_QURAN",
        "SAME_RUN_ARTIFACTS",
    ]
    assert context["accepted_project_knowledge"] is None
    assert "prior_semantics" not in context


def test_ask_lisan_ai_fallback():
    # Ask Lisan for something not in the DB
    resp = client.post(
        "/ask", json={"expression": "unknown", "contract_type": "ROOT_CORE"}
    )

    # Should fallback cleanly without blowing up
    assert resp.status_code == 200
    assert resp.json()["status"] == "INSUFFICIENT_EVIDENCE"
    assert resp.json()["claim"] is None
