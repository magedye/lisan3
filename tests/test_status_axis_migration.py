import json

import alembic.command
import alembic.config
import pytest
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError


def _config(db_path) -> alembic.config.Config:
    config = alembic.config.Config("alembic.ini")
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", f"sqlite:///{db_path.as_posix()}")
    return config


def _seed_claim(engine, *, review_state: str, publication_state: str) -> None:
    with engine.begin() as connection:
        connection.execute(
            sa.text(
                "INSERT INTO semantic_claims "
                "(id, contract_type, epistemic_state, review_state, freshness_state, "
                "publication_state, revision_id) VALUES "
                "('claim_legacy_axes', 'ROOT_CORE', 'LOCK_INTERNAL_RESULT', "
                ":review_state, 'CURRENT', :publication_state, 1)"
            ),
            {
                "review_state": review_state,
                "publication_state": publication_state,
            },
        )


def test_status_axis_migration_reconciles_with_audit_and_is_reversible(tmp_path):
    db_path = tmp_path / "legacy_axes.db"
    config = _config(db_path)
    alembic.command.upgrade(config, "c9e2a7f4b6d1")
    engine = sa.create_engine(f"sqlite:///{db_path.as_posix()}")
    _seed_claim(
        engine, review_state="PENDING_REVIEW", publication_state="UNPUBLISHED"
    )

    alembic.command.upgrade(config, "head")
    with engine.begin() as connection:
        axes = connection.execute(
            sa.text(
                "SELECT review_state, publication_state FROM semantic_claims "
                "WHERE id='claim_legacy_axes'"
            )
        ).one()
        assert axes == ("REVIEW_REQUIRED", "PRIVATE_WORKING")
        audit = connection.execute(
            sa.text(
                "SELECT action, previous_state, new_state, actor FROM audit_logs "
                "WHERE entity_id='claim_legacy_axes'"
            )
        ).one()
        assert audit.action == "RECONCILE_CANONICAL_STATUS_AXES"
        assert json.loads(audit.previous_state)["review_state"] == "PENDING_REVIEW"
        assert json.loads(audit.new_state)["publication_state"] == "PRIVATE_WORKING"
        assert audit.actor == "ALEMBIC_D4F7A2C8E901"
        with pytest.raises(IntegrityError):
            connection.execute(
                sa.text(
                    "UPDATE semantic_claims SET publication_state='UNPUBLISHED' "
                    "WHERE id='claim_legacy_axes'"
                )
            )

    alembic.command.downgrade(config, "c9e2a7f4b6d1")
    with engine.connect() as connection:
        restored = connection.execute(
            sa.text(
                "SELECT review_state, publication_state FROM semantic_claims "
                "WHERE id='claim_legacy_axes'"
            )
        ).one()
        assert restored == ("PENDING_REVIEW", "UNPUBLISHED")
        assert (
            connection.execute(
                sa.text(
                    "SELECT count(*) FROM audit_logs "
                    "WHERE entity_id='claim_legacy_axes' "
                    "AND action='RECONCILE_CANONICAL_STATUS_AXES'"
                )
            ).scalar_one()
            == 0
        )
    engine.dispose()


def test_status_axis_migration_refuses_unknown_meaning(tmp_path):
    db_path = tmp_path / "unknown_axes.db"
    config = _config(db_path)
    alembic.command.upgrade(config, "c9e2a7f4b6d1")
    engine = sa.create_engine(f"sqlite:///{db_path.as_posix()}")
    _seed_claim(engine, review_state="UNKNOWN_REVIEW", publication_state="UNPUBLISHED")

    with pytest.raises(RuntimeError, match="without inventing meaning"):
        alembic.command.upgrade(config, "head")
    engine.dispose()
