import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

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


def test_execute_steward_command(test_db):
    res = client.post(
        "/steward/commands",
        json={
            "command_type": "CREATE_CLAIM",
            "intent": "I want to create a new semantic claim for Alif",
            "parameters": {"target_contract": "test"},
        },
    )

    assert res.status_code == 200
    data = res.json()
    assert data["command_type"] == "CREATE_CLAIM"
    assert data["execution_status"] == "SUCCESS"
    assert "RULE_CORE_1" in data["evaluated_rules"]["applied_rules"]
    assert "SUCCESS" in data["execution_status"]


def test_execute_steward_command_invalid(test_db):
    res = client.post(
        "/steward/commands",
        json={
            "command_type": "CREATE_CLAIM",
            "intent": "ROOT_CORE",
            "parameters": {},
        },
    )

    assert res.status_code == 403
    assert "Intent violates immutable domain constraints" in res.json()["detail"]
