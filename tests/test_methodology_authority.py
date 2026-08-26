import hashlib

import alembic.command
import alembic.config
import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.domain.services.corpus import authority as corpus_authority
from backend.domain.services.methodology_authority import (
    methodology_authority_failures,
)
from backend.infrastructure.database import REPOSITORY_ROOT, Base, get_db
from backend.main import app

SOURCE_REFERENCE = "skills/lisan-semantic-extraction/SKILL.md"
SOURCE_SHA256 = hashlib.sha256(
    (REPOSITORY_ROOT / SOURCE_REFERENCE).read_bytes()
).hexdigest()

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(engine)
client = TestClient(app)


def override_get_db():
    with SessionLocal() as db:
        yield db


@pytest.fixture(autouse=True)
def test_db():
    app.dependency_overrides[get_db] = override_get_db
    with SessionLocal() as db:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
        yield db
    app.dependency_overrides.pop(get_db, None)


def _methodology(**overrides) -> models.MethodologyRevision:
    values = {
        "id": "LISAN_QURANIC_SEMANTIC_EXTRACTION@test",
        "methodology_id": "LISAN_QURANIC_SEMANTIC_EXTRACTION",
        "revision": "test-source-bound-revision",
        "lifecycle_state": "CURRENT",
        "authority_reference": "canonical:test",
        "source_reference": SOURCE_REFERENCE,
        "source_sha256": SOURCE_SHA256,
        "allowed_use": "QURAN_INTERNAL_CUMULATIVE_RUN",
        "research_run_eligible": True,
    }
    values.update(overrides)
    return models.MethodologyRevision(**values)


def _active_snapshot(test_db, monkeypatch) -> models.CorpusSnapshot:
    expected_hash = "b" * 64
    source_id = "TANZIL_QURAN_UTHMANI"
    monkeypatch.setitem(
        corpus_authority.CANONICAL_CORPUS_ADMISSIONS,
        source_id,
        corpus_authority.CorpusAdmissionRecord(
            source_id=source_id,
            source_role_status=corpus_authority.SOURCE_ROLE_APPROVED,
            expected_hash=expected_hash,
            artifact_verification_status=corpus_authority.HASH_VERIFIED,
            activation_status=corpus_authority.PRODUCTION_ACTIVE,
            authority_reference="canonical:test",
        ),
    )
    snapshot = models.CorpusSnapshot(
        id="snapshot-active-test",
        canonical_text_source=source_id,
        canonical_text_version="test-version",
        canonical_text_hash=expected_hash,
        validation_status="VALIDATED",
        source_role_status=corpus_authority.SOURCE_ROLE_APPROVED,
        artifact_presence_status=corpus_authority.ARTIFACT_PRESENT,
        expected_canonical_text_hash=expected_hash,
        hash_verification_status=corpus_authority.HASH_VERIFIED,
        import_validation_status=corpus_authority.IMPORT_VALIDATED,
        activation_status=corpus_authority.PRODUCTION_ACTIVE,
        artifact_provenance="canonical:test",
        fixture_only=False,
    )
    test_db.add(snapshot)
    test_db.commit()
    return snapshot


def _payload(snapshot_id: str, methodology_id: str) -> dict:
    return {
        "target_contract": "ROOT_CORE",
        "target_expression": "test",
        "methodology_revision": methodology_id,
        "corpus_snapshot": snapshot_id,
        "authority_context": {"profile": "methodology-authority-test"},
    }


def test_methodology_revision_is_source_bound_and_current():
    assert methodology_authority_failures(_methodology()) == []
    assert any(
        "hash does not match" in reason
        for reason in methodology_authority_failures(
            _methodology(source_sha256="0" * 64)
        )
    )
    retired = methodology_authority_failures(
        _methodology(lifecycle_state="RETIRED", research_run_eligible=False)
    )
    assert any("lifecycle" in reason for reason in retired)
    assert any("not eligible" in reason for reason in retired)
    assert any(
        "not approved" in reason
        for reason in methodology_authority_failures(
            _methodology(allowed_use="UNRELATED_USE")
        )
    )
    assert any(
        "escapes the repository" in reason
        for reason in methodology_authority_failures(
            _methodology(source_reference="../outside-repository.md")
        )
    )


def test_methodology_revision_provenance_cannot_be_mutated_in_place(test_db):
    methodology = _methodology()
    test_db.add(methodology)
    test_db.commit()

    methodology.source_sha256 = "0" * 64
    with pytest.raises(ValueError, match="provenance is immutable"):
        test_db.commit()
    test_db.rollback()


def test_registry_read_model_and_active_authorities_admit_run(test_db, monkeypatch):
    methodology = _methodology()
    test_db.add(methodology)
    snapshot = _active_snapshot(test_db, monkeypatch)

    registry = client.get("/methodologies")
    assert registry.status_code == 200
    assert registry.json() == [
        {
            "id": methodology.id,
            "methodology_id": methodology.methodology_id,
            "revision": methodology.revision,
            "lifecycle_state": "CURRENT",
            "authority_reference": methodology.authority_reference,
            "source_reference": SOURCE_REFERENCE,
            "source_sha256": SOURCE_SHA256,
            "allowed_use": "QURAN_INTERNAL_CUMULATIVE_RUN",
            "research_run_eligible": True,
            "created_at": registry.json()[0]["created_at"],
        }
    ]

    admitted = client.post("/runs", json=_payload(snapshot.id, methodology.id))
    assert admitted.status_code == 200
    assert test_db.query(models.ResearchRun).count() == 1


def test_unknown_retired_and_hash_drift_reject_future_admission(
    test_db, monkeypatch
):
    methodology = _methodology()
    test_db.add(methodology)
    snapshot = _active_snapshot(test_db, monkeypatch)

    unknown = client.post("/runs", json=_payload(snapshot.id, "UNKNOWN_METHOD"))
    assert unknown.status_code == 422
    assert "does not exist" in unknown.json()["detail"]
    assert test_db.query(models.ResearchRun).count() == 0

    methodology.lifecycle_state = "RETIRED"
    methodology.research_run_eligible = False
    test_db.commit()
    retired = client.post("/runs", json=_payload(snapshot.id, methodology.id))
    assert retired.status_code == 503
    assert test_db.query(models.ResearchRun).count() == 0

    test_db.delete(methodology)
    test_db.commit()
    drifted_methodology = _methodology(source_sha256="0" * 64)
    test_db.add(drifted_methodology)
    test_db.commit()
    drifted = client.post(
        "/runs", json=_payload(snapshot.id, drifted_methodology.id)
    )
    assert drifted.status_code == 503
    assert "hash does not match" in drifted.json()["detail"]
    assert test_db.query(models.ResearchRun).count() == 0


def test_methodology_migration_seeds_source_bound_revision_and_is_reversible(
    tmp_path,
):
    db_path = tmp_path / "methodology_registry.db"
    config = alembic.config.Config("alembic.ini")
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", f"sqlite:///{db_path.as_posix()}")

    alembic.command.upgrade(config, "head")
    engine = sa.create_engine(f"sqlite:///{db_path.as_posix()}")
    with engine.connect() as connection:
        record = connection.execute(
            sa.text(
                "SELECT id, lifecycle_state, source_reference, source_sha256, "
                "allowed_use, research_run_eligible FROM methodology_revisions"
            )
        ).one()
        assert record.id == "LISAN_QURANIC_SEMANTIC_EXTRACTION@6bb1c10a0f9a"
        assert record.lifecycle_state == "CURRENT"
        assert record.source_reference == SOURCE_REFERENCE
        assert record.source_sha256 == SOURCE_SHA256
        assert record.allowed_use == "QURAN_INTERNAL_CUMULATIVE_RUN"
        assert record.research_run_eligible == 1

    alembic.command.downgrade(config, "d4f7a2c8e901")
    with engine.connect() as connection:
        assert "methodology_revisions" not in sa.inspect(connection).get_table_names()

    alembic.command.upgrade(config, "head")
    with engine.connect() as connection:
        assert connection.execute(
            sa.text("SELECT count(*) FROM methodology_revisions")
        ).scalar_one() == 1
    engine.dispose()
