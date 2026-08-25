import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = REPOSITORY_ROOT / "lisanapp.db"
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "LISAN_DATABASE_URL", f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


@lru_cache(maxsize=1)
def canonical_migration_heads() -> tuple[str, ...]:
    """Return the repository's canonical Alembic heads without mutating a DB."""
    config = Config(str(REPOSITORY_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(REPOSITORY_ROOT / "alembic"))
    return tuple(sorted(ScriptDirectory.from_config(config).get_heads()))


def database_schema_status(db: Session) -> dict[str, Any]:
    """Inspect runtime schema compatibility without creating or stamping tables."""
    bind = db.get_bind()
    inspector = inspect(bind)
    actual_tables = set(inspector.get_table_names())
    expected_tables = set(Base.metadata.tables)

    actual_revisions: tuple[str, ...] = ()
    if "alembic_version" in actual_tables:
        actual_revisions = tuple(
            sorted(
                str(row[0])
                for row in db.execute(text("SELECT version_num FROM alembic_version"))
            )
        )

    missing_tables = sorted(expected_tables - actual_tables)
    missing_columns: dict[str, list[str]] = {}
    for table_name in sorted(expected_tables & actual_tables):
        actual_columns = {
            column["name"] for column in inspector.get_columns(table_name)
        }
        expected_columns = set(Base.metadata.tables[table_name].columns.keys())
        missing = sorted(expected_columns - actual_columns)
        if missing:
            missing_columns[table_name] = missing

    expected_heads = canonical_migration_heads()
    current = (
        actual_revisions == expected_heads
        and not missing_tables
        and not missing_columns
    )
    return {
        "status": "CURRENT" if current else "BLOCKED_SCHEMA",
        "database_url": bind.url.render_as_string(hide_password=True),
        "expected_revisions": list(expected_heads),
        "actual_revisions": list(actual_revisions),
        "missing_tables": missing_tables,
        "missing_columns": missing_columns,
    }


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
