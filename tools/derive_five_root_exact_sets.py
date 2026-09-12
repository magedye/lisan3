"""Read-only exact-set STRUCTURAL derivation for the five campaign roots.

Canonical Runtime Qualification — occurrence negative control. This is NOT
semantic research: it counts the confirmed word-level occurrences of each root
directly from the admitted QAC-derived StructuralToken store (host-derived,
deterministic), then compares AFTERWARDS to the frozen Batch 07 artifact counts
as a cross-check. The derivation is never tuned to force agreement; a difference
is reported, not reconciled away.

Five roots (Buckwalter): ESw, dnw, flH, fwh, glm.

Run (against the authoritative converged lisanapp.db):
    python -m tools.derive_five_root_exact_sets
    python -m tools.derive_five_root_exact_sets --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from backend.domain.services.research_coverage import (
    confirmed_word_refs,
    non_confirmed_word_refs,
)
from backend.infrastructure.database import SessionLocal

AUTHORIZED_SNAPSHOT = "snap_tanzil_1_1_ac0724796cbb"
# Buckwalter root -> frozen Batch 07 artifact file (artifacts/semantic-campaign/roots/).
ROOT_ARTIFACTS = {
    "ESw": "E_53_w.json",
    "dnw": "dnw.json",
    "flH": "fl_48_.json",
    "fwh": "fwh.json",
    "glm": "glm.json",
}
ARTIFACT_DIR = Path("artifacts/semantic-campaign/roots")


def _batch07_expected_count(artifact_name: str) -> int | None:
    path = ARTIFACT_DIR / artifact_name
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    coverage = data.get("coverage_validation") or {}
    if "expected_count" in coverage:
        return int(coverage["expected_count"])
    if isinstance(data.get("occurrences"), int):
        return int(data["occurrences"])
    return None


def derive(db) -> dict:
    results = {}
    all_match = True
    for root, artifact in ROOT_ARTIFACTS.items():
        confirmed = confirmed_word_refs(db, AUTHORIZED_SNAPSHOT, root)
        non_confirmed = non_confirmed_word_refs(db, AUTHORIZED_SNAPSHOT, root)
        batch07 = _batch07_expected_count(artifact)
        match = batch07 is not None and batch07 == len(confirmed)
        all_match &= bool(match)
        results[root] = {
            "artifact": artifact,
            "derived_confirmed_occurrences": len(confirmed),
            "confirmed_word_refs": confirmed,
            "disputed": non_confirmed["DISPUTED"],
            "unresolved": non_confirmed["UNRESOLVED"],
            "batch07_expected_count": batch07,
            "exact_count_match": match,
        }
    return {
        "snapshot": AUTHORIZED_SNAPSHOT,
        "source": "QAC_MORPHOLOGY v0.4 -> StructuralToken (CONFIRMED, latest extraction)",
        "note": (
            "Structural occurrence counting only; NOT semantic research. Batch 07 "
            "counts used solely as a post-derivation cross-check, never as the source."
        ),
        "roots": results,
        "all_counts_match_batch07": all_match,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    with SessionLocal() as db:
        report = derive(db)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Five-root exact-set structural derivation (snapshot {report['snapshot']})")
        for root, r in report["roots"].items():
            flag = "OK" if r["exact_count_match"] else "DIFF"
            print(
                f"  [{flag}] {root:5s} derived={r['derived_confirmed_occurrences']:4d} "
                f"batch07={r['batch07_expected_count']}  "
                f"(disputed={len(r['disputed'])} unresolved={len(r['unresolved'])})"
            )
        print(f"  all_counts_match_batch07: {report['all_counts_match_batch07']}")
    return 0 if report["all_counts_match_batch07"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
