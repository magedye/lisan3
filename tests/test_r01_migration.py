"""Migration round-trip coverage for the pre-analysis foundation stores.

The rest of the suite provisions schema via Base.metadata.create_all, so the
alembic migrations' server_defaults, check constraints and downgrade paths are
otherwise unexercised. This test drives migration b3d6e2f8c150 (and its parent
a2f5c1d7b940) up and down on a scratch sqlite database.
"""

import sqlite3
from pathlib import Path

from alembic.config import Config

from alembic import command

REPO_ROOT = Path(__file__).resolve().parents[1]

NEW_TABLES = {"structural_tokens", "external_hypothesis_records", "campaign_states"}


def _config(db_path: Path) -> Config:
    cfg = Config(str(REPO_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(REPO_ROOT / "alembic"))
    cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path.as_posix()}")
    return cfg


def _tables(db_path: Path) -> set[str]:
    con = sqlite3.connect(db_path)
    try:
        return {
            row[0]
            for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
    finally:
        con.close()


def test_pre_analysis_stores_migration_round_trip(tmp_path):
    db_path = tmp_path / "roundtrip.db"
    cfg = _config(db_path)

    command.upgrade(cfg, "head")
    tables = _tables(db_path)
    assert NEW_TABLES <= tables
    # origin column exists on hypotheses (parent migration a2f5c1d7b940).
    con = sqlite3.connect(db_path)
    try:
        hyp_cols = {r[1] for r in con.execute("PRAGMA table_info(hypotheses)")}
        assert "origin" in hyp_cols
        # Governed check constraint on the external register rejects a bad status.
        con.execute(
            "INSERT INTO external_hypothesis_records "
            "(id, claim_type, source, author, claim, target_scope, claim_role, status, provenance) "
            "VALUES ('x','ROOT_MEANING_CANDIDATE','s','a','c','r','RULE_CLAIM','EXTERNAL_CANDIDATE','p')"
        )
        con.commit()
        bad = False
        try:
            con.execute(
                "INSERT INTO external_hypothesis_records "
                "(id, claim_type, source, author, claim, target_scope, claim_role, status, provenance) "
                "VALUES ('y','ROOT_MEANING_CANDIDATE','s','a','c','r','RULE_CLAIM','SEMANTIC_AUTHORITY','p')"
            )
            con.commit()
        except sqlite3.IntegrityError:
            bad = True
        assert bad, "check constraint should reject an ungoverned status"
    finally:
        con.close()

    # Downgrade removes exactly the three new tables; re-upgrade restores them.
    command.downgrade(cfg, "a2f5c1d7b940")
    assert not (NEW_TABLES & _tables(db_path))
    command.upgrade(cfg, "head")
    assert NEW_TABLES <= _tables(db_path)
