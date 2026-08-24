import argparse
import hashlib
import json
import math
import platform
import sqlite3
import statistics
import tempfile
import time
from contextlib import ExitStack, closing
from pathlib import Path

import sqlite_vec

VECTOR_COUNT = 5_000
DIMENSIONS = 32
QUERY_RUNS = 100
TOP_K = 10
MAX_BUILD_SECONDS = 5.0
MAX_QUERY_P95_MILLISECONDS = 100.0
SPACES = (
    "VERSE_CONTEXT",
    "STRUCTURAL_PROFILE",
    "HYPOTHESIS",
    "CLAIM",
    "ROOT_CANDIDATE",
    "EXTERNAL_RESEARCH",
)
RUN_IDS = ("run-a", "run-b", "run-c", "run-d")
QUERY_SPACE = "VERSE_CONTEXT"


def load_extension(db: sqlite3.Connection) -> str:
    db.enable_load_extension(True)
    try:
        sqlite_vec.load(db)
    finally:
        db.enable_load_extension(False)
    return str(db.execute("select vec_version()").fetchone()[0])


def synthetic_vector(index: int, dimensions: int = DIMENSIONS) -> list[float]:
    values = [
        float(((index + 3) * (offset + 5)) % 97 + 1) for offset in range(dimensions)
    ]
    magnitude = math.sqrt(sum(value * value for value in values))
    return [value / magnitude for value in values]


def create_index(db: sqlite3.Connection, dimensions: int = DIMENSIONS) -> None:
    db.execute(
        f"""
        CREATE VIRTUAL TABLE evaluation_vectors USING vec0(
            embedding_id INTEGER PRIMARY KEY,
            run_id TEXT,
            embedding_space TEXT,
            provenance_class TEXT,
            model_revision TEXT,
            config_hash TEXT,
            source_eligible BOOLEAN,
            vector FLOAT[{dimensions}],
            +source_ref TEXT
        )
        """
    )


def rows_for(
    *,
    vector_count: int,
    dimensions: int,
    model_revision: str,
    config_hash: str,
):
    for index in range(vector_count):
        yield (
            index + 1,
            RUN_IDS[index % len(RUN_IDS)],
            SPACES[index % len(SPACES)],
            "SYNTHETIC_EVALUATION",
            model_revision,
            config_hash,
            True,
            sqlite_vec.serialize_float32(synthetic_vector(index, dimensions)),
            f"synthetic:{index + 1}",
        )


def populate(
    db: sqlite3.Connection,
    *,
    vector_count: int,
    dimensions: int,
    model_revision: str,
    config_hash: str,
) -> None:
    db.executemany(
        """
        INSERT INTO evaluation_vectors(
            embedding_id, run_id, embedding_space, provenance_class,
            model_revision, config_hash, source_eligible, vector, source_ref
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows_for(
            vector_count=vector_count,
            dimensions=dimensions,
            model_revision=model_revision,
            config_hash=config_hash,
        ),
    )
    db.commit()


def query(
    db: sqlite3.Connection,
    *,
    query_vector: list[float],
    model_revision: str,
    config_hash: str,
    top_k: int,
) -> list[tuple[int, str, str, str, str, float]]:
    return db.execute(
        """
        SELECT embedding_id, run_id, embedding_space, provenance_class,
               source_ref, distance
        FROM evaluation_vectors
        WHERE vector MATCH ?
          AND k = ?
          AND run_id = 'run-a'
          AND embedding_space = 'VERSE_CONTEXT'
          AND provenance_class = 'SYNTHETIC_EVALUATION'
          AND model_revision = ?
          AND config_hash = ?
          AND source_eligible = 1
        ORDER BY distance ASC
        """,
        (
            sqlite_vec.serialize_float32(query_vector),
            top_k,
            model_revision,
            config_hash,
        ),
    ).fetchall()


def run_spike() -> dict:
    model_revision = "synthetic-evaluation-r1"
    config_hash = hashlib.sha256(b"l2-normalized-32d-synthetic-r1").hexdigest()
    changed_revision = "synthetic-evaluation-r2"
    changed_config_hash = hashlib.sha256(b"l2-normalized-32d-synthetic-r2").hexdigest()
    query_vector = synthetic_vector(9)
    runner_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    with (
        tempfile.TemporaryDirectory(prefix="lisan-r2-sqlite-vec-") as directory,
        ExitStack() as cleanup,
    ):
        database_path = Path(directory) / "spike.db"
        db = cleanup.enter_context(closing(sqlite3.connect(database_path)))
        vec_version = load_extension(db)
        create_index(db)
        build_started = time.perf_counter()
        populate(
            db,
            vector_count=VECTOR_COUNT,
            dimensions=DIMENSIONS,
            model_revision=model_revision,
            config_hash=config_hash,
        )
        build_seconds = time.perf_counter() - build_started
        initial_count = int(
            db.execute("SELECT count(*) FROM evaluation_vectors").fetchone()[0]
        )
        baseline = query(
            db,
            query_vector=query_vector,
            model_revision=model_revision,
            config_hash=config_hash,
            top_k=TOP_K,
        )
        repeat = query(
            db,
            query_vector=query_vector,
            model_revision=model_revision,
            config_hash=config_hash,
            top_k=TOP_K,
        )
        db.close()

        reopened = cleanup.enter_context(closing(sqlite3.connect(database_path)))
        load_extension(reopened)
        reopened_result = query(
            reopened,
            query_vector=query_vector,
            model_revision=model_revision,
            config_hash=config_hash,
            top_k=TOP_K,
        )
        filtered = all(
            row[1] == "run-a"
            and row[2] == QUERY_SPACE
            and row[3] == "SYNTHETIC_EVALUATION"
            for row in reopened_result
        )
        provenance_linked = all(
            row[4].startswith("synthetic:") for row in reopened_result
        )

        query_durations = []
        for _ in range(QUERY_RUNS):
            started = time.perf_counter()
            query(
                reopened,
                query_vector=query_vector,
                model_revision=model_revision,
                config_hash=config_hash,
                top_k=TOP_K,
            )
            query_durations.append((time.perf_counter() - started) * 1_000)

        deleted_id = int(reopened_result[0][0])
        reopened.execute(
            "DELETE FROM evaluation_vectors WHERE embedding_id = ?", (deleted_id,)
        )
        reopened.commit()
        deletion_count = int(
            reopened.execute("SELECT count(*) FROM evaluation_vectors").fetchone()[0]
        )
        after_deletion = query(
            reopened,
            query_vector=query_vector,
            model_revision=model_revision,
            config_hash=config_hash,
            top_k=TOP_K,
        )

        reopened.execute("DROP TABLE evaluation_vectors")
        create_index(reopened)
        populate(
            reopened,
            vector_count=VECTOR_COUNT,
            dimensions=DIMENSIONS,
            model_revision=model_revision,
            config_hash=config_hash,
        )
        rebuilt_result = query(
            reopened,
            query_vector=query_vector,
            model_revision=model_revision,
            config_hash=config_hash,
            top_k=TOP_K,
        )

        stale_filter_result = query(
            reopened,
            query_vector=query_vector,
            model_revision=changed_revision,
            config_hash=changed_config_hash,
            top_k=TOP_K,
        )
        reopened.execute("DROP TABLE evaluation_vectors")
        create_index(reopened)
        populate(
            reopened,
            vector_count=VECTOR_COUNT,
            dimensions=DIMENSIONS,
            model_revision=changed_revision,
            config_hash=changed_config_hash,
        )
        old_profile_after_rebuild = query(
            reopened,
            query_vector=query_vector,
            model_revision=model_revision,
            config_hash=config_hash,
            top_k=TOP_K,
        )
        changed_profile_result = query(
            reopened,
            query_vector=query_vector,
            model_revision=changed_revision,
            config_hash=changed_config_hash,
            top_k=TOP_K,
        )

        count_before_failure = int(
            reopened.execute("SELECT count(*) FROM evaluation_vectors").fetchone()[0]
        )
        failure_rejected = False
        try:
            reopened.execute(
                """
                INSERT INTO evaluation_vectors(
                    embedding_id, run_id, embedding_space, provenance_class,
                    model_revision, config_hash, source_eligible, vector, source_ref
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    VECTOR_COUNT + 1,
                    "run-a",
                    QUERY_SPACE,
                    "SYNTHETIC_EVALUATION",
                    changed_revision,
                    changed_config_hash,
                    True,
                    sqlite_vec.serialize_float32([1.0, 0.0]),
                    "synthetic:invalid-dimension",
                ),
            )
            reopened.commit()
        except sqlite3.OperationalError:
            failure_rejected = True
            reopened.rollback()
        count_after_failure = int(
            reopened.execute("SELECT count(*) FROM evaluation_vectors").fetchone()[0]
        )
        reopened.close()

    p95_index = max(0, math.ceil(len(query_durations) * 0.95) - 1)
    query_p95_ms = sorted(query_durations)[p95_index]
    checks = {
        "deletion": deletion_count == VECTOR_COUNT - 1
        and all(row[0] != deleted_id for row in after_deletion),
        "deterministic_query": baseline == repeat,
        "failure_recovery": failure_rejected
        and count_before_failure == count_after_failure == VECTOR_COUNT,
        "filtered_run_space": filtered,
        "model_config_invalidation": not stale_filter_result
        and not old_profile_after_rebuild
        and bool(changed_profile_result),
        "persistence_after_reopen": baseline == reopened_result,
        "provenance_linkage": provenance_linked,
        "rebuild_equivalence": baseline == rebuilt_result,
        "vector_count": initial_count == VECTOR_COUNT,
    }
    performance_passed = (
        build_seconds <= MAX_BUILD_SECONDS
        and query_p95_ms <= MAX_QUERY_P95_MILLISECONDS
    )
    passed = all(checks.values()) and performance_passed
    return {
        "status": (
            "SQLITE_VEC_EVALUATION_PASSED" if passed else "SQLITE_VEC_EVALUATION_FAILED"
        ),
        "canonical_adoption_status": "APPROVED_FOR_EVALUATION",
        "embedding_model_selection": "EMBEDDING_MODEL_SELECTION_BLOCKED",
        "production_vector_state": "NOT_CREATED",
        "provenance_class": "SYNTHETIC_EVALUATION",
        "runner_sha256": runner_hash,
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "sqlite": sqlite3.sqlite_version,
            "sqlite_vec": vec_version,
        },
        "profile": {
            "dimensions": DIMENSIONS,
            "query_runs": QUERY_RUNS,
            "top_k": TOP_K,
            "vector_count": VECTOR_COUNT,
        },
        "predeclared_performance_thresholds": {
            "max_build_seconds": MAX_BUILD_SECONDS,
            "max_query_p95_milliseconds": MAX_QUERY_P95_MILLISECONDS,
        },
        "observed_performance": {
            "build_seconds": round(build_seconds, 6),
            "query_mean_milliseconds": round(statistics.mean(query_durations), 6),
            "query_p95_milliseconds": round(query_p95_ms, 6),
        },
        "checks": checks,
        "performance_passed": performance_passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=Path(__file__).with_name("results.json")
    )
    args = parser.parse_args()
    result = run_spike()
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "SQLITE_VEC_EVALUATION_PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
