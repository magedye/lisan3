"""Bounded operational guards for the canonical runtime convergence command."""

from __future__ import annotations

import pytest
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from alembic import command
from backend.infrastructure.database import DEFAULT_DATABASE_PATH, REPOSITORY_ROOT
from tools.converge_runtime import (
    ConvergenceError,
    ConvergenceEvidence,
    authoritative_target_failure,
    converge,
    main,
)


def _database_url(database_path) -> str:
    return f"sqlite:///{database_path.as_posix()}"


def _evidence(database_path) -> ConvergenceEvidence:
    return ConvergenceEvidence(
        database_url=_database_url(database_path),
        schema_status="UNKNOWN",
        schema_expected_revisions=[],
        schema_actual_revisions=[],
    )


def _migrate(database_path) -> None:
    config = Config(str(REPOSITORY_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(REPOSITORY_ROOT / "alembic"))
    config.set_main_option("sqlalchemy.url", _database_url(database_path))
    command.upgrade(config, "head")


def test_authoritative_lisanapp_target_is_accepted():
    assert authoritative_target_failure(_database_url(DEFAULT_DATABASE_PATH)) is None


def test_campaign_side_store_is_rejected_by_database_identity():
    campaign_db = REPOSITORY_ROOT / "data" / "campaign" / "runtime.db"
    reason = authoritative_target_failure(_database_url(campaign_db))
    assert reason is not None
    assert "not the authoritative lisanapp.db path" in reason


def test_renamed_side_store_is_rejected_by_database_identity(tmp_path):
    reason = authoritative_target_failure(_database_url(tmp_path / "innocuous.db"))
    assert reason is not None
    assert "renamed copy" in reason


def test_wrong_schema_is_rejected_before_any_convergence_mutation(tmp_path):
    database_path = tmp_path / "wrong-schema.db"
    engine = create_engine(_database_url(database_path))
    try:
        with Session(engine) as db, pytest.raises(
            ConvergenceError, match="schema is not CURRENT"
        ):
            converge(db, evidence=_evidence(database_path))
    finally:
        engine.dispose()


def test_repeat_convergence_is_idempotent_in_a_disposable_governed_db(tmp_path):
    database_path = tmp_path / "governed-replay.db"
    _migrate(database_path)
    engine = create_engine(_database_url(database_path))
    try:
        with Session(engine) as db:
            first = converge(db, evidence=_evidence(database_path))
            assert first.tanzil_import_created is True
            first_tokens = first.qac_tokens_persisted
        with Session(engine) as db:
            second = converge(db, evidence=_evidence(database_path))
            assert second.tanzil_import_created is False
            assert second.qac_tokens_persisted == first_tokens
            assert any("idempotent" in note for note in second.notes)
    finally:
        engine.dispose()


def test_side_store_override_flag_is_not_an_available_escape_hatch():
    with pytest.raises(SystemExit) as exit_info:
        main(["--allow-side-store"])
    assert exit_info.value.code == 2
