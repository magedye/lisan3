from pathlib import Path

from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from alembic import command
from backend.domain import models  # noqa: F401
from backend.infrastructure.database import (
    DEFAULT_DATABASE_PATH,
    REPOSITORY_ROOT,
    SQLALCHEMY_DATABASE_URL,
    canonical_migration_heads,
    database_schema_status,
)


def _migrate(database_path: Path) -> None:
    config = Config(str(REPOSITORY_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(REPOSITORY_ROOT / "alembic"))
    config.set_main_option("sqlalchemy.url", f"sqlite:///{database_path.as_posix()}")
    command.upgrade(config, "head")


def test_default_database_url_is_repository_absolute():
    assert DEFAULT_DATABASE_PATH == REPOSITORY_ROOT / "lisanapp.db"
    assert SQLALCHEMY_DATABASE_URL == f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}"


def test_fresh_migrated_database_is_current(tmp_path):
    database_path = tmp_path / "fresh.db"
    _migrate(database_path)
    engine = create_engine(f"sqlite:///{database_path.as_posix()}")

    with Session(engine) as session:
        status = database_schema_status(session)

    assert status["status"] == "CURRENT"
    assert status["actual_revisions"] == list(canonical_migration_heads())
    assert status["missing_tables"] == []
    assert status["missing_columns"] == {}


def test_legacy_revision_is_reported_without_mutation(tmp_path):
    database_path = tmp_path / "legacy.db"
    engine = create_engine(f"sqlite:///{database_path.as_posix()}")
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE alembic_version (version_num VARCHAR(32))"))
        connection.execute(
            text("INSERT INTO alembic_version VALUES ('5542b3a62e23')")
        )

    with Session(engine) as session:
        status = database_schema_status(session)
        revision_after_check = session.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar_one()

    assert status["status"] == "BLOCKED_SCHEMA"
    assert status["actual_revisions"] == ["5542b3a62e23"]
    assert status["expected_revisions"] == list(canonical_migration_heads())
    assert status["missing_tables"]
    assert revision_after_check == "5542b3a62e23"
