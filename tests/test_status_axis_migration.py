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

    # Upgrading to head first reconciles the legacy four axes (d4f7a2c8e901)
    # and then collapses them into the simplified two-state model
    # (research_state + canonical_state) via f1a6c3d9e204.
    alembic.command.upgrade(config, "head")
    with engine.begin() as connection:
        states = connection.execute(
            sa.text(
                "SELECT research_state, canonical_state, result_strength "
                "FROM semantic_claims WHERE id='claim_legacy_axes'"
            )
        ).one()
        assert states.research_state == "PREFERRED"
        assert states.canonical_state == "NOT_CANONICAL"
        assert states.result_strength == "MODERATE"
        audit = connection.execute(
            sa.text(
                "SELECT action, previous_state, new_state, actor FROM audit_logs "
                "WHERE entity_id='claim_legacy_axes' "
                "AND action='SIMPLIFY_AI_GOVERNANCE_STATUS'"
            )
        ).one()
        assert audit.actor == "ALEMBIC_F1A6C3D9E204"
        assert (
            json.loads(audit.previous_state)["epistemic_state"]
            == "LOCK_INTERNAL_RESULT"
        )
        assert json.loads(audit.new_state)["research_state"] == "PREFERRED"
        with pytest.raises(IntegrityError):
            connection.execute(
                sa.text(
                    "UPDATE semantic_claims SET research_state='UNPUBLISHED' "
                    "WHERE id='claim_legacy_axes'"
                )
            )

    # Reversing only the simplification restores the pre-simplification axes.
    alembic.command.downgrade(config, "c4d8b7e2a913")
    with engine.connect() as connection:
        restored = connection.execute(
            sa.text(
                "SELECT epistemic_state FROM semantic_claims "
                "WHERE id='claim_legacy_axes'"
            )
        ).one()
        assert restored.epistemic_state == "LOCK_INTERNAL_RESULT"
        assert (
            connection.execute(
                sa.text(
                    "SELECT count(*) FROM audit_logs "
                    "WHERE entity_id='claim_legacy_axes' "
                    "AND action='SIMPLIFY_AI_GOVERNANCE_STATUS'"
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
