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

    # Create run
    response = client.post(
        "/runs",
        json={
            "target_contract": "ROOT_CORE",
            "target_expression": "ن ش ز",
            "methodology_revision": "v7.1",
            "corpus_snapshot": "snap1",
            "authority_context": {"initiator": "local_user"},
        },
    )
    run_id = response.json()["id"]

    # Enter preflight
    client.post(
        f"/runs/{run_id}/blind/preflight",
        json={
            "target_contract": "ROOT_CORE",
            "corpus_snapshot": "snap1",
            "methodology_reference": "ref_v1",
            "allowed_sources": ["QURAN_CORPUS"],
        },
    )

    db = TestingSessionLocal()
    context = AIContextBuilder.build_research_context(db, run_id)
    db.close()

    # Internal lock not passed, semantic knowledge must be restricted
    assert context["semantic_knowledge_access"] == "BLIND_LAB_RESTRICTED"
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
