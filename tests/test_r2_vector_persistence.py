import struct

import alembic.command
import alembic.config
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from backend.domain import models
from backend.infrastructure.database import Base


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    session.add(
        models.ResearchRun(
            id="run-r2-evaluation",
            target_contract="ROOT_CORE",
            target_expression="synthetic",
            methodology_revision="fixture-method",
            corpus_snapshot="fixture-snapshot",
            authority_context={"mode": "SYNTHETIC_EVALUATION"},
        )
    )
    session.commit()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def embedding(**overrides) -> models.SemanticEmbedding:
    values = {
        "id": "embedding-1",
        "research_run_id": "run-r2-evaluation",
        "entity_type": "SYNTHETIC_FIXTURE",
        "entity_id": "fixture-1",
        "embedding_space": "CLAIM",
        "embedding_model": "synthetic-evaluation-adapter",
        "embedding_model_revision": "fixture-r1",
        "model_config_hash": "config-hash",
        "source_revision": "source-r1",
        "source_hash": "source-hash",
        "vector": struct.pack("<4f", 1.0, 0.0, 0.0, 0.0),
        "dimensions": 4,
        "provenance_class": "SYNTHETIC_EVALUATION",
        "production_eligible": False,
        "source_eligible": True,
        "index_revision": "index-r1",
        "lifecycle_state": "CURRENT",
    }
    values.update(overrides)
    return models.SemanticEmbedding(**values)


def test_evaluation_embedding_persists_with_explicit_provenance(db):
    db.add(embedding())
    db.commit()
    stored = db.get(models.SemanticEmbedding, "embedding-1")
    assert stored.provenance_class == "SYNTHETIC_EVALUATION"
    assert stored.production_eligible is False
    assert stored.embedding_space == "CLAIM"


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"production_eligible": True}, "cannot store production vectors"),
        ({"embedding_space": "UNIVERSAL"}, "Unsupported embedding space"),
        ({"source_eligible": False}, "eligible source"),
        ({"vector": b"short"}, "exactly dimensions float32"),
        ({"lifecycle_state": "STALE"}, "invalidation reason"),
    ],
)
def test_evaluation_boundary_fails_closed(db, overrides, message):
    db.add(embedding(**overrides))
    with pytest.raises(ValueError, match=message):
        db.flush()
    db.rollback()


def test_stale_record_requires_and_retains_reason(db):
    db.add(
        embedding(
            lifecycle_state="STALE",
            source_eligible=False,
            invalidated_reason="SOURCE_BECAME_INELIGIBLE",
        )
    )
    db.commit()
    stored = db.get(models.SemanticEmbedding, "embedding-1")
    assert stored.lifecycle_state == "STALE"
    assert stored.invalidated_reason == "SOURCE_BECAME_INELIGIBLE"


def test_r2_migration_is_reversible_and_matches_metadata(tmp_path):
    database_url = f"sqlite:///{(tmp_path / 'r2-migration.db').as_posix()}"
    config = alembic.config.Config("alembic.ini")
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", database_url)
    engine = create_engine(database_url)
    try:
        alembic.command.upgrade(config, "head")
        assert "semantic_embeddings" in inspect(engine).get_table_names()
        alembic.command.check(config)

        alembic.command.downgrade(config, "b7e4c1d9a5f2")
        assert "semantic_embeddings" not in inspect(engine).get_table_names()

        alembic.command.upgrade(config, "head")
        assert "semantic_embeddings" in inspect(engine).get_table_names()
    finally:
        engine.dispose()
