import hashlib
import json
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker

from backend.domain import models
from backend.domain.services.corpus import authority as corpus_authority
from backend.domain.services.corpus.activation import (
    ACTIVATION_ACTION,
    ACTIVATION_ACTOR,
    AUTHORIZED_METHODOLOGY_ID,
    AUTHORIZED_SNAPSHOT_ID,
    CorpusActivationRejected,
    TanzilProductionActivationService,
)
from backend.domain.services.corpus.importer import TanzilPreActivationImporter
from backend.infrastructure.database import REPOSITORY_ROOT, Base, get_db
from backend.main import app


@pytest.fixture(scope="module")
def pre_activation_database(tmp_path_factory) -> Path:
    database_path = tmp_path_factory.mktemp("tanzil-activation") / "baseline.db"
    engine = create_engine(f"sqlite:///{database_path.as_posix()}")
    Base.metadata.create_all(engine)
    methodology_source = REPOSITORY_ROOT / "skills/lisan-semantic-extraction/SKILL.md"
    with Session(engine) as db:
        db.add(
            models.MethodologyRevision(
                id=AUTHORIZED_METHODOLOGY_ID,
                methodology_id="LISAN_QURANIC_SEMANTIC_EXTRACTION",
                revision="git-blob:6bb1c10a0f9a09bf9a59c29c45e2252efc9832fb",
                lifecycle_state="CURRENT",
                authority_reference=(
                    "docs/canonical/"
                    "LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md"
                    "#methodology-revision-authority"
                ),
                source_reference="skills/lisan-semantic-extraction/SKILL.md",
                source_sha256=hashlib.sha256(
                    methodology_source.read_bytes()
                ).hexdigest(),
                allowed_use="QURAN_INTERNAL_CUMULATIVE_RUN",
                research_run_eligible=True,
            )
        )
        db.commit()
        TanzilPreActivationImporter.import_candidate(db)
    engine.dispose()
    return database_path


@pytest.fixture
def activation_db(pre_activation_database, tmp_path):
    database_path = tmp_path / "activation.db"
    shutil.copyfile(pre_activation_database, database_path)
    engine = create_engine(
        f"sqlite:///{database_path.as_posix()}",
        connect_args={"check_same_thread": False},
    )
    session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    with session_factory() as db:
        yield db, session_factory
    engine.dispose()


def _payload(
    snapshot_id=AUTHORIZED_SNAPSHOT_ID, methodology_id=AUTHORIZED_METHODOLOGY_ID
):
    return {
        "target_contract": "ROOT_CORE",
        "target_expression": "كتب",
        "methodology_revision": methodology_id,
        "corpus_snapshot": snapshot_id,
        "authority_context": {"source": "production-activation-test"},
    }


def test_exact_snapshot_activation_audit_and_run_admission(activation_db, monkeypatch):
    db, session_factory = activation_db
    result = TanzilProductionActivationService.activate(db)
    snapshot = result.snapshot
    assert snapshot.id == AUTHORIZED_SNAPSHOT_ID
    assert snapshot.validation_status == "VALIDATED"
    assert snapshot.activation_status == corpus_authority.PRODUCTION_ACTIVE
    assert result.audit_log.entity_id == AUTHORIZED_SNAPSHOT_ID
    assert result.audit_log.entity_type == "CorpusSnapshot"
    assert result.audit_log.action == ACTIVATION_ACTION
    assert result.audit_log.actor == ACTIVATION_ACTOR
    assert json.loads(result.audit_log.previous_state) == {
        "activation_status": corpus_authority.CANONICAL_ACTIVATION_PENDING,
        "validation_status": "PENDING",
    }
    audit_state = json.loads(result.audit_log.new_state)
    assert audit_state["snapshot_id"] == AUTHORIZED_SNAPSHOT_ID
    assert audit_state["artifact_path"] == ("data/corpus/tanzil/tanzil-uthmani-1.1.txt")
    assert audit_state["artifact_bytes"] == 1_334_737
    assert audit_state["artifact_sha256"] == snapshot.canonical_text_hash
    assert audit_state["artifact_version"] == "1.1"
    assert audit_state["import_validation_status"] == "IMPORT_VALIDATED"
    assert audit_state["surah_count"] == 114
    assert audit_state["verse_count"] == 6_236
    assert audit_state["authority_decision_reference"].endswith(
        "#owner-production-activation-decision"
    )

    with pytest.raises(CorpusActivationRejected, match="not in CANONICAL"):
        TanzilProductionActivationService.activate(db)

    def override_db():
        with session_factory() as request_db:
            yield request_db

    app.dependency_overrides[get_db] = override_db
    try:
        client = TestClient(app)
        # POST /runs now auto-resolves the active corpus + methodology instead of
        # having the client re-declare them; the host binds the exact authorized
        # ids it derived (simplified AUTHORITY_PREFLIGHT auto-resolve).
        run_payload = {"target_contract": "ROOT_CORE", "target_expression": "كتب"}
        admitted = client.post("/runs", json=run_payload)
        assert admitted.status_code == 200
        assert admitted.json()["corpus_snapshot"] == AUTHORIZED_SNAPSHOT_ID
        assert admitted.json()["methodology_revision"] == AUTHORIZED_METHODOLOGY_ID

        # Retiring the sole eligible methodology makes governed run authority
        # unavailable and fails closed (503), creating no run.
        methodology = db.get(models.MethodologyRevision, AUTHORIZED_METHODOLOGY_ID)
        assert methodology is not None
        methodology.lifecycle_state = "RETIRED"
        methodology.research_run_eligible = False
        db.commit()
        retired = client.post("/runs", json=run_payload)
        assert retired.status_code == 503
        assert "Methodology" in retired.json()["detail"]

        methodology.lifecycle_state = "CURRENT"
        methodology.research_run_eligible = True
        db.commit()
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert db.scalar(select(func.count()).select_from(models.ResearchRun)) == 1


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("canonical_text_hash", "0" * 64, "canonical_text_hash"),
        ("fixture_only", True, "fixture_only"),
        ("import_validation_status", "IMPORT_PENDING", "import_validation_status"),
        ("canonical_text_source", "WRONG_SOURCE", "canonical_text_source"),
        ("canonical_text_version", "0.0", "canonical_text_version"),
    ],
    ids=("wrong-hash", "fixture", "incomplete-import", "wrong-source", "wrong-version"),
)
def test_activation_rejects_corrupt_snapshot_identity(
    activation_db, field, value, message
):
    db, _ = activation_db
    db.execute(
        models.CorpusSnapshot.__table__.update()
        .where(models.CorpusSnapshot.id == AUTHORIZED_SNAPSHOT_ID)
        .values({field: value})
    )
    db.commit()
    with pytest.raises(ValueError, match=message):
        TanzilProductionActivationService.activate(db)
    assert db.query(models.AuditLog).count() == 0


def test_activation_rejects_missing_artifact(activation_db, tmp_path):
    db, _ = activation_db
    with pytest.raises(ValueError, match="artifact is missing"):
        TanzilProductionActivationService.activate(db, repository_root=tmp_path)
    assert db.query(models.AuditLog).count() == 0


def test_activation_rejects_stale_occurrence_rows(activation_db):
    db, _ = activation_db
    occurrence = db.get(models.CorpusOccurrence, "occ_tanzil_1_1_114_006")
    assert occurrence is not None
    db.delete(occurrence)
    db.commit()
    with pytest.raises(ValueError, match="do not exactly match"):
        TanzilProductionActivationService.activate(db)
    assert db.query(models.AuditLog).count() == 0


def test_activation_rejects_competing_active_snapshot(activation_db):
    db, _ = activation_db
    db.execute(
        models.CorpusSnapshot.__table__.insert().values(
            id="competing-active-corpus",
            canonical_text_source="OTHER_QURAN_CORPUS",
            canonical_text_version="1",
            canonical_text_hash="competing-hash",
            validation_status="VALIDATED",
            activation_status=corpus_authority.PRODUCTION_ACTIVE,
        )
    )
    db.commit()
    with pytest.raises(CorpusActivationRejected, match="competing production-active"):
        TanzilProductionActivationService.activate(db)
    assert db.query(models.AuditLog).count() == 0


def test_activation_rejects_invalid_lifecycle_and_ineligible_methodology(
    activation_db,
):
    db, _ = activation_db
    db.execute(
        models.CorpusSnapshot.__table__.update()
        .where(models.CorpusSnapshot.id == AUTHORIZED_SNAPSHOT_ID)
        .values(validation_status="UNVERIFIED")
    )
    db.commit()
    with pytest.raises(CorpusActivationRejected, match="pre-activation PENDING"):
        TanzilProductionActivationService.activate(db)

    db.execute(
        models.CorpusSnapshot.__table__.update()
        .where(models.CorpusSnapshot.id == AUTHORIZED_SNAPSHOT_ID)
        .values(validation_status="PENDING")
    )
    db.execute(
        models.MethodologyRevision.__table__.update()
        .where(models.MethodologyRevision.id == AUTHORIZED_METHODOLOGY_ID)
        .values(lifecycle_state="RETIRED", research_run_eligible=False)
    )
    db.commit()
    with pytest.raises(CorpusActivationRejected, match="Methodology revision"):
        TanzilProductionActivationService.activate(db)
    assert db.query(models.AuditLog).count() == 0
