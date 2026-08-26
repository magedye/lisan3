import shutil
from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from alembic import command
from backend.domain.models import CorpusOccurrence, CorpusSnapshot
from backend.domain.services.corpus.authority import (
    ARTIFACT_PRESENT,
    CANON_001_ARTIFACT_IDENTITY_MATCH_CONFIRMED,
    CANONICAL_ACTIVATION_PENDING,
    HASH_VERIFIED,
    IMPORT_VALIDATED,
    PRODUCTION_ACTIVE,
    get_canonical_admission,
)
from backend.domain.services.corpus.importer import TanzilPreActivationImporter
from backend.domain.services.corpus.tanzil import TanzilArtifactParser
from backend.domain.services.run_admission import ResearchRunAdmissionPolicy
from backend.infrastructure.database import Base

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


def _copy_authority_artifacts(destination_root: Path) -> None:
    admission = get_canonical_admission("TANZIL_QURAN_UTHMANI")
    assert admission is not None
    for reference in (
        admission.artifact_reference,
        admission.identity_index_reference,
    ):
        assert reference is not None
        destination = destination_root / reference
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPOSITORY_ROOT / reference, destination)


def test_real_tanzil_import_persists_exact_pre_activation_snapshot(db, tmp_path):
    _copy_authority_artifacts(tmp_path)
    admission = get_canonical_admission("TANZIL_QURAN_UTHMANI")
    assert admission is not None
    raw = (tmp_path / str(admission.artifact_reference)).read_bytes()
    index = (tmp_path / str(admission.identity_index_reference)).read_bytes()
    parsed = TanzilArtifactParser(admission).parse(raw, index)

    result = TanzilPreActivationImporter.import_candidate(
        db, repository_root=tmp_path
    )

    assert result.created is True
    assert result.occurrence_count == 6_236
    snapshot = result.snapshot
    assert snapshot.id == "snap_tanzil_1_1_ac0724796cbb"
    assert snapshot.canonical_text_version == "1.1"
    assert snapshot.canonical_text_hash == admission.expected_hash
    assert snapshot.expected_canonical_text_hash == admission.expected_hash
    assert snapshot.artifact_size_bytes == 1_334_737
    assert snapshot.hash_verification_status == HASH_VERIFIED
    assert snapshot.import_validation_status == IMPORT_VALIDATED
    assert snapshot.validation_status == "PENDING"
    assert snapshot.activation_status == CANONICAL_ACTIVATION_PENDING
    assert snapshot.verse_count == 6_236
    assert snapshot.fixture_only is False
    assert snapshot.structural_source is None
    assert (
        snapshot.canon_001_reconciliation
        == CANON_001_ARTIFACT_IDENTITY_MATCH_CONFIRMED
    )

    occurrences = (
        db.query(CorpusOccurrence)
        .filter(CorpusOccurrence.snapshot_id == snapshot.id)
        .order_by(CorpusOccurrence.id)
        .all()
    )
    assert len(occurrences) == 6_236
    assert [(row.verse_ref, row.text) for row in occurrences] == [
        (verse.verse_ref, verse.text) for verse in parsed.verses
    ]
    assert occurrences[0].id == "occ_tanzil_1_1_001_001"
    assert occurrences[-1].id == "occ_tanzil_1_1_114_006"

    state = ResearchRunAdmissionPolicy.current_state(db)
    assert state["available"] is False
    assert state["corpus_snapshot_ids"] == []
    assert any("production-active" in blocker for blocker in state["blockers"])


def test_exact_reimport_is_idempotent_and_partial_existing_import_fails_closed(
    db, tmp_path
):
    _copy_authority_artifacts(tmp_path)
    first = TanzilPreActivationImporter.import_candidate(
        db, repository_root=tmp_path
    )
    second = TanzilPreActivationImporter.import_candidate(
        db, repository_root=tmp_path
    )
    assert second.created is False
    assert second.snapshot.id == first.snapshot.id
    assert db.query(CorpusSnapshot).count() == 1
    assert db.query(CorpusOccurrence).count() == 6_236

    missing = db.get(CorpusOccurrence, "occ_tanzil_1_1_114_006")
    assert missing is not None
    db.delete(missing)
    db.commit()
    with pytest.raises(ValueError, match="do not exactly match"):
        TanzilPreActivationImporter.import_candidate(db, repository_root=tmp_path)
    assert db.query(CorpusSnapshot).count() == 1
    assert db.query(CorpusOccurrence).count() == 6_235


def test_missing_artifact_fails_before_persistence(db, tmp_path):
    admission = get_canonical_admission("TANZIL_QURAN_UTHMANI")
    assert admission is not None
    assert admission.identity_index_reference is not None
    index_path = tmp_path / admission.identity_index_reference
    index_path.parent.mkdir(parents=True)
    shutil.copyfile(REPOSITORY_ROOT / admission.identity_index_reference, index_path)

    with pytest.raises(ValueError, match="artifact is missing"):
        TanzilPreActivationImporter.import_candidate(db, repository_root=tmp_path)
    assert db.query(CorpusSnapshot).count() == 0
    assert db.query(CorpusOccurrence).count() == 0


def test_lifecycle_rejects_import_before_hash_and_fixture_impersonation(db):
    admission = get_canonical_admission("TANZIL_QURAN_UTHMANI")
    assert admission is not None
    common = {
        "canonical_text_source": admission.source_id,
        "canonical_text_version": admission.canonical_text_version,
        "canonical_text_hash": admission.expected_hash,
        "source_role_status": admission.source_role_status,
        "artifact_presence_status": ARTIFACT_PRESENT,
        "expected_canonical_text_hash": admission.expected_hash,
        "import_validation_status": IMPORT_VALIDATED,
        "activation_status": CANONICAL_ACTIVATION_PENDING,
        "artifact_provenance": "governed-test-provenance",
        "artifact_reference": admission.artifact_reference,
        "artifact_size_bytes": admission.expected_bytes,
        "artifact_format": admission.artifact_format,
        "artifact_verified_at": sa.func.now(),
        "artifact_verification_revision": admission.verification_revision,
        "identity_index_reference": admission.identity_index_reference,
        "identity_index_sha256": admission.identity_index_sha256,
        "verse_count": admission.expected_verse_count,
        "canon_001_reconciliation": admission.canon_001_reconciliation,
        "validation_status": "PENDING",
    }
    db.add(
        CorpusSnapshot(
            id="snap_hash_not_verified",
            hash_verification_status="HASH_UNVERIFIED",
            fixture_only=False,
            **common,
        )
    )
    with pytest.raises(ValueError, match="artifact hash is not verified"):
        db.flush()
    db.rollback()

    db.add(
        CorpusSnapshot(
            id="snap_fixture_impersonation",
            hash_verification_status=HASH_VERIFIED,
            fixture_only=True,
            **common,
        )
    )
    with pytest.raises(ValueError, match="test fixtures cannot become production"):
        db.flush()
    db.rollback()


def test_production_activation_and_imported_provenance_mutation_fail_closed(
    db, tmp_path
):
    _copy_authority_artifacts(tmp_path)
    snapshot = TanzilPreActivationImporter.import_candidate(
        db, repository_root=tmp_path
    ).snapshot

    snapshot.activation_status = PRODUCTION_ACTIVE
    with pytest.raises(ValueError, match="production-active snapshot must be VALIDATED"):
        db.flush()
    db.rollback()

    snapshot = db.get(CorpusSnapshot, snapshot.id)
    assert snapshot is not None
    snapshot.artifact_reference = "data/corpus/tanzil/forged.txt"
    with pytest.raises(ValueError, match="artifact reference is not authority-bound"):
        db.flush()
    db.rollback()


def test_tanzil_provenance_migration_is_reversible_and_matches_models(tmp_path):
    database_path = tmp_path / "tanzil-migration.db"
    config = Config("alembic.ini")
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", f"sqlite:///{database_path.as_posix()}")

    command.upgrade(config, "head")
    engine = create_engine(f"sqlite:///{database_path.as_posix()}")
    inspector = sa.inspect(engine)
    snapshot_columns = {item["name"] for item in inspector.get_columns("corpus_snapshots")}
    assert {column.name for column in CorpusSnapshot.__table__.columns}.issubset(
        snapshot_columns
    )
    occurrence_columns = inspector.get_columns("corpus_occurrences")
    nullable = {item["name"]: item["nullable"] for item in occurrence_columns}
    assert nullable["snapshot_id"] is False
    assert nullable["verse_ref"] is False
    assert nullable["text"] is False
    assert {
        constraint["name"] for constraint in inspector.get_unique_constraints("corpus_snapshots")
    } >= {"uq_corpus_snapshot_artifact_identity"}
    assert {
        constraint["name"] for constraint in inspector.get_unique_constraints("corpus_occurrences")
    } >= {"uq_corpus_occurrence_snapshot_verse"}

    command.downgrade(config, "e8b3f6a1c204")
    inspector = sa.inspect(engine)
    snapshot_columns = {item["name"] for item in inspector.get_columns("corpus_snapshots")}
    assert "artifact_reference" not in snapshot_columns

    command.upgrade(config, "head")
    inspector = sa.inspect(engine)
    assert "artifact_reference" in {
        item["name"] for item in inspector.get_columns("corpus_snapshots")
    }
    engine.dispose()


def test_tanzil_migration_rejects_legacy_duplicates_before_schema_changes(tmp_path):
    database_path = tmp_path / "duplicate-legacy-corpus.db"
    config = Config("alembic.ini")
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", f"sqlite:///{database_path.as_posix()}")
    command.upgrade(config, "e8b3f6a1c204")
    engine = create_engine(f"sqlite:///{database_path.as_posix()}")
    with engine.begin() as connection:
        for snapshot_id in ("legacy_duplicate_a", "legacy_duplicate_b"):
            connection.execute(
                sa.text(
                    "INSERT INTO corpus_snapshots "
                    "(id, canonical_text_source, canonical_text_version, "
                    "canonical_text_hash) VALUES "
                    "(:id, 'LEGACY', '1', 'same-hash')"
                ),
                {"id": snapshot_id},
            )

    with pytest.raises(RuntimeError, match="duplicate snapshot artifact identities"):
        command.upgrade(config, "head")

    inspector = sa.inspect(engine)
    assert "artifact_reference" not in {
        item["name"] for item in inspector.get_columns("corpus_snapshots")
    }
    engine.dispose()
