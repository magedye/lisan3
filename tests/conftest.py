import pathlib

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.infrastructure.database import Base, canonical_migration_heads, get_db
from backend.main import app

# Patch TestClient to automatically include the owner token
original_request = TestClient.request

def patched_request(self, method, url, **kwargs):
    headers = kwargs.get("headers", {}) or {}
    try:
        token = pathlib.Path(".lisan_owner_token").read_text(encoding="utf-8").strip()
        headers.setdefault("X-Lisan-Owner-Token", token)
    except FileNotFoundError:
        pass
    kwargs["headers"] = headers
    return original_request(self, method, url, **kwargs)

TestClient.request = patched_request

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
