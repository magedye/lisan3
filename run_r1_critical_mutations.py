r"""Run the reproducible authority-critical R1 mutation profile.

From the repository root:

    .venv\Scripts\python.exe run_r1_critical_mutations.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "cosmic-ray-knowledge-graph-config.toml"
MODULE = "backend/domain/services/knowledge_graph.py"
EXPECTED_SELECTED = 32
REACHABILITY = ("read", 351, "AddNot")
EQUIVALENT = ("_is_projection_eligible", 58, "ReplaceComparisonOperator_Eq_LtE")
EXACT_CLEAN_GATE_GUARD = (
    'if isolation is None or isolation.is_contaminated != "CLEAN":'
)


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


def is_critical(mutation: dict[str, object]) -> bool:
    definition, line, operator = fingerprint(mutation)
    if definition == "_is_projection_eligible":
        return (
            line == 58
            or (line == 53 and operator == "ReplaceComparisonOperator_Eq_NotEq")
            or (line == 59 and operator == "ReplaceAndWithOr")
        )
    if definition == "rebuild":
        return line in {150, 151, 154, 155, 158, 163, 193, 204, 215} or (
            line in {229, 246}
            and operator == "ReplaceComparisonOperator_Eq_NotEq"
        )
    if definition == "_scoped_node_ids":
        return (
            (line in {269, 275, 291} and operator == "ZeroIterationForLoop")
            or (
                line in {277, 283}
                and operator == "ReplaceComparisonOperator_Eq_NotEq"
            )
            or (line == 281 and operator == "AddNot")
        )
    if definition == "read":
        return line in {332, 344, 351} and operator == "AddNot"
    if definition == "presentation_label":
        return line in {362, 364} and operator == "ReplaceComparisonOperator_Eq_NotEq"
    return False


def completed(command: list[str], environment: dict[str, str]) -> subprocess.CompletedProcess[str]:
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

    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
        }
    )
    source = ROOT / MODULE
    original_source = source.read_bytes()
    gates_source = (ROOT / "backend/domain/services/gates.py").read_text(
        encoding="utf-8"
    )
    equivalent_allowed = EXACT_CLEAN_GATE_GUARD in gates_source

    with tempfile.TemporaryDirectory(prefix="lisan-r1-critical-") as temporary:
        temporary_path = Path(temporary)
        environment["HYPOTHESIS_STORAGE_DIRECTORY"] = str(
            temporary_path / "hypothesis"
        )
        test_arguments = [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_r1_knowledge_graph.py",
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

        session = temporary_path / "r1-critical.sqlite"
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
            (mutation for mutation in universe if is_critical(mutation)),
            key=lambda mutation: (
                fingerprint(mutation),
                int(mutation["occurrence"]),
            ),
        )
        if len(selected) != EXPECTED_SELECTED or sum(
            fingerprint(mutation) == REACHABILITY for mutation in selected
        ) != 1:
            print(
                f"Mutation selection drifted: universe={len(universe)} "
                f"selected={len(selected)}",
                file=sys.stderr,
            )
            return 1
        print(
            f"MUTATION_UNIVERSE={len(universe)} SELECTED={len(selected)}", flush=True
        )

        test_command = subprocess.list2cmdline(
            [argument.replace("\\", "/") for argument in test_arguments]
        )
        results: list[tuple[tuple[str, int, str], dict[str, object]]] = []
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
                print("Cosmic Ray did not restore the production source", file=sys.stderr)
                return 1
            if worker.returncode != 0:
                print(worker.stdout, worker.stderr, file=sys.stderr)
                return 1
            result = json.loads(worker.stdout)
            key = fingerprint(mutation)
            results.append((key, result))
            print(
                f"MUTANT {index:02d}/{EXPECTED_SELECTED} {key[0]}:{key[1]} "
                f"{key[2]} => {result['test_outcome']}",
                flush=True,
            )

    survivors = [(key, result) for key, result in results if result["test_outcome"] == "survived"]
    equivalent = [
        (key, result)
        for key, result in survivors
        if key == EQUIVALENT and equivalent_allowed
    ]
    critical = [item for item in survivors if item not in equivalent]
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
                    "classification": "equivalent"
                    if (key, result) in equivalent
                    else "non_equivalent_critical",
                    "diff": result["diff"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    reachability_outcome = dict(results)[REACHABILITY]["test_outcome"]
    summary = {
        "selected": len(results),
        "killed": sum(result["test_outcome"] == "killed" for _, result in results),
        "survived": len(survivors),
        "equivalent_survivors": len(equivalent),
        "non_equivalent_critical_survivors": len(critical),
        "reachability_mutant": reachability_outcome,
    }
    print("MUTATION_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    return 1 if abnormal or critical or reachability_outcome != "killed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
