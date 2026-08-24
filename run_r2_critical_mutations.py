r"""Run the reproducible authority-critical R2 vector mutation profile.

From the repository root:

    .venv\Scripts\python.exe run_r2_critical_mutations.py
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "cosmic-ray-vector-config.toml"
MODULE = "backend/domain/services/vector_discovery.py"
EXPECTED_SOURCE_SHA256 = (
    "3382eed7668bfcaa05c8c9ec77d57881987faab8f205aef80b14e3719edb2799"
)
CRITICAL_FINGERPRINTS = {
    ("_require_evaluation_manifest", 37, "AddNot"),
    ("_require_evaluation_manifest", 41, "AddNot"),
    ("_require_run_access", 49, "AddNot"),
    ("_require_run_access", 56, "ReplaceComparisonOperator_NotEq_Eq"),
    ("_require_run_access", 56, "ReplaceOrWithAnd"),
    ("_require_run_access", 60, "AddNot"),
    ("_serialize", 68, "ReplaceComparisonOperator_NotEq_Eq"),
    ("_index_revision", 82, "ZeroIterationForLoop"),
    ("rebuild_evaluation", 134, "AddNot"),
    ("rebuild_evaluation", 154, "ReplaceFalseWithTrue"),
    ("rebuild_evaluation", 155, "ReplaceTrueWithFalse"),
    ("rebuild_evaluation", 163, "ReplaceComparisonOperator_Eq_NotEq"),
    ("rebuild_evaluation", 164, "ReplaceComparisonOperator_Eq_NotEq"),
    ("invalidate_mismatched", 188, "ZeroIterationForLoop"),
    ("invalidate_mismatched", 191, "ReplaceComparisonOperator_NotEq_Eq"),
    ("invalidate_mismatched", 192, "ReplaceOrWithAnd"),
    ("invalidate_mismatched", 195, "ReplaceComparisonOperator_NotEq_Eq"),
    ("invalidate_mismatched", 197, "AddNot"),
    ("delete_derived_state", 210, "ReplaceComparisonOperator_Eq_NotEq"),
    ("delete_derived_state", 212, "AddNot"),
    ("delete_derived_state", 214, "ReplaceComparisonOperator_Eq_NotEq"),
    ("discover", 233, "ReplaceOrWithAnd"),
    ("discover", 239, "ReplaceComparisonOperator_Eq_NotEq"),
    ("discover", 240, "ReplaceComparisonOperator_Eq_NotEq"),
    ("discover", 241, "ReplaceComparisonOperator_Eq_NotEq"),
    ("discover", 243, "ReplaceComparisonOperator_NotEq_Eq"),
    ("discover", 246, "ReplaceComparisonOperator_NotEq_Eq"),
    ("discover", 250, "ReplaceComparisonOperator_NotEq_Eq"),
    ("discover", 256, "AddNot"),
}


def short_operator(mutation: dict[str, object]) -> str:
    return str(mutation["operator_name"]).removeprefix("core/")


def fingerprint(mutation: dict[str, object]) -> tuple[str, int, str]:
    start_pos = mutation["start_pos"]
    assert isinstance(start_pos, list)
    return (
        str(mutation["definition_name"]),
        int(start_pos[0]),
        short_operator(mutation),
    )


def completed(
    command: list[str], environment: dict[str, str]
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def main() -> int:
    suffix = ".exe" if os.name == "nt" else ""
    cosmic_ray = Path(sys.executable).with_name(f"cosmic-ray{suffix}")
    if not cosmic_ray.is_file():
        print(f"Cosmic Ray executable not found: {cosmic_ray}", file=sys.stderr)
        return 1

    source = ROOT / MODULE
    original_source = source.read_bytes()
    source_hash = hashlib.sha256(original_source).hexdigest()
    if source_hash != EXPECTED_SOURCE_SHA256:
        print(
            f"R2 mutation source drifted: expected={EXPECTED_SOURCE_SHA256} "
            f"actual={source_hash}",
            file=sys.stderr,
        )
        return 1

    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
        }
    )
    with tempfile.TemporaryDirectory(prefix="lisan-r2-critical-") as temporary:
        temporary_path = Path(temporary)
        environment["HYPOTHESIS_STORAGE_DIRECTORY"] = str(temporary_path / "hypothesis")
        test_arguments = [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_r2_vector_contracts.py",
            "tests/test_r2_vector_persistence.py",
            "tests/test_r2_vector_lifecycle.py",
            "-q",
            "-p",
            "no:cacheprovider",
            "--basetemp",
            str(temporary_path / "pytest"),
        ]
        baseline = completed(test_arguments, environment)
        if baseline.returncode != 0:
            print(baseline.stdout, baseline.stderr, file=sys.stderr)
            return 1
        print("BASELINE=passed", flush=True)

        session = temporary_path / "r2-critical.sqlite"
        initialized = completed(
            [str(cosmic_ray), "init", str(CONFIG), str(session)], environment
        )
        if initialized.returncode != 0:
            print(initialized.stderr, file=sys.stderr)
            return 1
        dumped = completed([str(cosmic_ray), "dump", str(session)], environment)
        if dumped.returncode != 0:
            print(dumped.stderr, file=sys.stderr)
            return 1
        universe = [
            json.loads(line)[0]["mutations"][0]
            for line in dumped.stdout.splitlines()
            if line.strip()
        ]
        selected = sorted(
            (
                mutation
                for mutation in universe
                if fingerprint(mutation) in CRITICAL_FINGERPRINTS
            ),
            key=lambda mutation: (fingerprint(mutation), int(mutation["occurrence"])),
        )
        selected_fingerprints = {fingerprint(mutation) for mutation in selected}
        if (
            len(selected) != len(CRITICAL_FINGERPRINTS)
            or selected_fingerprints != CRITICAL_FINGERPRINTS
        ):
            missing = sorted(CRITICAL_FINGERPRINTS - selected_fingerprints)
            extra = sorted(selected_fingerprints - CRITICAL_FINGERPRINTS)
            print(
                f"Mutation selection drifted: universe={len(universe)} "
                f"selected={len(selected)} missing={missing} extra={extra}",
                file=sys.stderr,
            )
            return 1
        print(f"MUTATION_UNIVERSE={len(universe)} SELECTED={len(selected)}", flush=True)

        test_command = subprocess.list2cmdline(
            [argument.replace("\\", "/") for argument in test_arguments]
        )
        results = []
        for index, mutation in enumerate(selected, start=1):
            worker = completed(
                [
                    str(cosmic_ray),
                    "mutate-and-test",
                    MODULE,
                    str(mutation["operator_name"]),
                    str(mutation["occurrence"]),
                    test_command,
                ],
                environment,
            )
            if source.read_bytes() != original_source:
                print("Cosmic Ray did not restore the R2 source", file=sys.stderr)
                return 1
            if worker.returncode != 0:
                print(worker.stdout, worker.stderr, file=sys.stderr)
                return 1
            result = json.loads(worker.stdout)
            results.append((fingerprint(mutation), result))
            print(
                f"MUTANT {index:02d}/{len(selected)} "
                f"{fingerprint(mutation)} => {result['test_outcome']}",
                flush=True,
            )

    survivors = [
        (key, result) for key, result in results if result["test_outcome"] == "survived"
    ]
    abnormal = [
        result
        for _, result in results
        if result["test_outcome"] not in {"killed", "survived"}
        or result["worker_outcome"] != "normal"
    ]
    for key, result in survivors:
        print(
            "SURVIVOR="
            + json.dumps(
                {
                    "definition": key[0],
                    "line": key[1],
                    "operator": key[2],
                    "diff": result["diff"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    summary = {
        "source_sha256": source_hash,
        "universe": len(universe),
        "selected": len(results),
        "killed": sum(result["test_outcome"] == "killed" for _, result in results),
        "survived": len(survivors),
        "non_equivalent_critical_survivors": len(survivors),
    }
    print("MUTATION_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    return 1 if abnormal or survivors else 0


if __name__ == "__main__":
    raise SystemExit(main())
