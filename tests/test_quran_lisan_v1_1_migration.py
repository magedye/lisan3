import sqlite3
import subprocess
import sys


def test_migration_fresh_base_to_head(tmp_path):
    """Proves that a fresh empty database upgrades cleanly to alembic head."""
    db_file = tmp_path / "fresh_test.db"
    db_url = f"sqlite:///{db_file.as_posix()}"

    res = subprocess.run(
        [sys.executable, "-m", "alembic", "-x", f"db_url={db_url}", "upgrade", "head"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.returncode == 0, f"Alembic upgrade head failed on fresh DB: {res.stderr}"

    # Verify tables exist
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    tables = [
        r[0]
        for r in c.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    ]
    assert "semantic_memory" in tables
    assert "essential_neighbors" in tables
    assert "semantic_claims" in tables

    # Verify semantic_memory columns
    cols = [r[1] for r in c.execute("PRAGMA table_info(semantic_memory)").fetchall()]
    for col in [
        "id",
        "claim_id",
        "target_type",
        "target_expression",
        "reliability",
        "scope",
        "conflict_state",
        "lifecycle",
        "result_strength",
        "research_completeness",
        "independent_verification",
        "evidence_refs",
        "counterevidence_refs",
        "dependencies",
        "reopen_if",
        "parent_revision",
        "revision_reason",
    ]:
        assert col in cols, f"Missing column {col} in semantic_memory"

    conn.close()


def test_migration_upgrade_from_previous_head_with_legacy_data(tmp_path):
    """Proves that upgrading from previous head (50ccdbbf2a2e) to new head (bac8ad155a7c)
    preserves all legacy data without information loss and migrates fields forward."""
    db_file = tmp_path / "upgrade_test.db"
    db_url = f"sqlite:///{db_file.as_posix()}"

    # 1. Upgrade to previous head 50ccdbbf2a2e
    res_prev = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-x",
            f"db_url={db_url}",
            "upgrade",
            "50ccdbbf2a2e",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert res_prev.returncode == 0, (
        f"Upgrade to 50ccdbbf2a2e failed: {res_prev.stderr}"
    )

    # 2. Insert legacy data into essential_neighbors using pre-v1.1 schema
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(
        "INSERT INTO hypotheses (id, origin, hypothesis_type, target_contract, scope, statement) "
        "VALUES ('hyp_legacy_1', 'INDEPENDENT_INTERNAL_DERIVATION', 'ROOT_CORE', 'ROOT_CONCEPT', 'UNIVERSAL', 'statement 1')"
    )
    c.execute(
        "INSERT INTO essential_neighbors (id, hypothesis_id, shared_domain, positive_distinguishing_candidate, "
        "supporting_evidence, unresolved_distinction, substitution_probe) "
        "VALUES ('nbr_legacy_1', 'hyp_legacy_1', 'movement', 'ن ه ض', '[\"token:1:1\"]', 'unresolved axis', 'probe_1')"
    )
    conn.commit()
    conn.close()

    # 3. Upgrade to new head bac8ad155a7c
    res_head = subprocess.run(
        [sys.executable, "-m", "alembic", "-x", f"db_url={db_url}", "upgrade", "head"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert res_head.returncode == 0, f"Upgrade to head failed: {res_head.stderr}"

    # 4. Verify that legacy data is intact AND forward-migrated
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(
        "SELECT id, distinctive_difference, discriminating_evidence, status, "
        "positive_distinguishing_candidate, supporting_evidence, unresolved_distinction, substitution_probe "
        "FROM essential_neighbors WHERE id = 'nbr_legacy_1'"
    )
    row = c.fetchone()
    assert row is not None
    # Forward-migrated fields:
    assert (
        row[1] == "ن ه ض"
    )  # distinctive_difference migrated from positive_distinguishing_candidate
    assert (
        row[2] == '["token:1:1"]'
    )  # discriminating_evidence migrated from supporting_evidence
    assert row[3] == "UNRESOLVED"  # status derived from unresolved_distinction
    # Legacy fields preserved (ZERO INFORMATION LOSS):
    assert row[4] == "ن ه ض"
    assert row[5] == '["token:1:1"]'
    assert row[6] == "unresolved axis"
    assert row[7] == "probe_1"

    conn.close()

    # 5. Test downgrade to previous head
    res_down = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-x",
            f"db_url={db_url}",
            "downgrade",
            "50ccdbbf2a2e",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert res_down.returncode == 0, (
        f"Downgrade to 50ccdbbf2a2e failed: {res_down.stderr}"
    )
