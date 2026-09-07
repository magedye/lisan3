"""Deterministic exact-set research-coverage validation (owner correction).

Model-reported ``occurrences_checked == total`` is NOT sufficient evidence of full
coverage. Research completeness requires occurrence-level evidence keyed by
``word_ref`` whose set EXACTLY equals the confirmed StructuralToken word_refs:

    confirmed StructuralToken word_refs  ==  researched occurrence evidence

- no missing confirmed word_ref;
- no duplicate substituting for a missing one;
- no verse-level ref standing in for multiple word occurrences;
- no majority/percentage shortcut.

One missing confirmed occurrence prevents ``research_completeness=COMPLETE``.
One unreconciled confirmed occurrence prevents ``universal_presence_holds=true``.
Research progress and canonicalization progress remain independent
(``canonical_authorization`` stays PENDING regardless of research strength).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from backend.domain import models

# Occurrence-level research dispositions (research evidence, not a status axis).
DISP_CONSISTENT = "CONSISTENT"
DISP_RESISTANT = "RESISTANT"
DISP_STRUCTURAL_UNCERTAINTY = "STRUCTURAL_UNCERTAINTY"
VALID_DISPOSITIONS = {DISP_CONSISTENT, DISP_RESISTANT, DISP_STRUCTURAL_UNCERTAINTY}

COMPLETENESS_COMPLETE = "COMPLETE"
COMPLETENESS_PENDING = "PENDING_COVERAGE_EVIDENCE"


def confirmed_word_refs(db: Session, snapshot_id: str, root: str) -> list[str]:
    """Single source of truth for a root's confirmed occurrence identity.

    Mirrors RootDescriptiveProfileService: latest extraction version only, and
    only CONFIRMED attributions. Ordered deterministically by word_ref.
    """
    rows = (
        db.query(models.StructuralToken)
        .filter(
            models.StructuralToken.snapshot_id == snapshot_id,
            models.StructuralToken.root == root,
        )
        .order_by(models.StructuralToken.word_ref)
        .all()
    )
    if not rows:
        return []
    latest = max(r.extraction_version for r in rows)
    return [
        r.word_ref
        for r in rows
        if r.extraction_version == latest
        and r.attribution_status == models.StructuralAttributionStatus.CONFIRMED.value
    ]


def non_confirmed_word_refs(db: Session, snapshot_id: str, root: str) -> dict[str, list[str]]:
    """Disputed/unresolved structural membership, kept separately visible."""
    rows = (
        db.query(models.StructuralToken)
        .filter(
            models.StructuralToken.snapshot_id == snapshot_id,
            models.StructuralToken.root == root,
        )
        .order_by(models.StructuralToken.word_ref)
        .all()
    )
    out: dict[str, list[str]] = {"DISPUTED": [], "UNRESOLVED": []}
    if not rows:
        return out
    latest = max(r.extraction_version for r in rows)
    for r in rows:
        if r.extraction_version != latest:
            continue
        if r.attribution_status == models.StructuralAttributionStatus.DISPUTED.value:
            out["DISPUTED"].append(r.word_ref)
        elif r.attribution_status == models.StructuralAttributionStatus.UNRESOLVED.value:
            out["UNRESOLVED"].append(r.word_ref)
    return out


@dataclass(frozen=True)
class CoverageValidation:
    root: str
    expected_count: int
    researched_count: int
    missing_word_refs: tuple[str, ...]
    unexpected_word_refs: tuple[str, ...]
    duplicate_word_refs: tuple[str, ...]
    exact_set_match: bool
    disputed_visible: tuple[str, ...] = field(default=())
    unresolved_visible: tuple[str, ...] = field(default=())

    def as_dict(self) -> dict:
        return {
            "root": self.root,
            "expected_count": self.expected_count,
            "researched_count": self.researched_count,
            "missing_word_refs": list(self.missing_word_refs),
            "unexpected_word_refs": list(self.unexpected_word_refs),
            "duplicate_word_refs": list(self.duplicate_word_refs),
            "exact_set_match": self.exact_set_match,
            "disputed_visible": list(self.disputed_visible),
            "unresolved_visible": list(self.unresolved_visible),
        }


def validate_root_research_coverage(
    db: Session, snapshot_id: str, root: str, researched_word_refs: list[str]
) -> CoverageValidation:
    """Exact-set validation: researched occurrence evidence vs confirmed store.

    - A duplicate never substitutes for a missing ref (set equality + dup list).
    - word_ref granularity: multiple root occurrences in one verse stay distinct.
    """
    expected = confirmed_word_refs(db, snapshot_id, root)
    expected_set = set(expected)
    seen: set[str] = set()
    duplicates: list[str] = []
    for ref in researched_word_refs:
        if ref in seen:
            duplicates.append(ref)
        seen.add(ref)
    missing = tuple(sorted(expected_set - seen))
    unexpected = tuple(sorted(seen - expected_set))
    visible = non_confirmed_word_refs(db, snapshot_id, root)
    return CoverageValidation(
        root=root,
        expected_count=len(expected),
        researched_count=len(seen),
        missing_word_refs=missing,
        unexpected_word_refs=unexpected,
        duplicate_word_refs=tuple(sorted(set(duplicates))),
        exact_set_match=bool(expected) and not missing and not unexpected,
        disputed_visible=tuple(visible["DISPUTED"]),
        unresolved_visible=tuple(visible["UNRESOLVED"]),
    )


def finalize_root_disposition(
    judgment: dict,
    verdict: dict,
    coverage: CoverageValidation,
    final_resistant: list[str],
    final_uncertain: list[str],
    occurrences: int,
) -> dict:
    """Fold discovery + adversarial verdict + exact-set coverage into research
    fields. Root semantic unity is NON-NEGOTIABLE: one unreconciled confirmed
    occurrence (resistant or structurally uncertain) blocks universal presence.
    Canonical authorization is ALWAYS pending here (research != canonical)."""
    j = judgment or {}
    v = verdict or {}
    verdict_val = v.get("verdict")
    discover_result = j.get("result")

    completeness = COMPLETENESS_COMPLETE if coverage.exact_set_match else COMPLETENESS_PENDING
    unreconciled = sorted(set(final_resistant) | set(final_uncertain))
    universal = (
        coverage.exact_set_match
        and not unreconciled
        and verdict_val == "SUPPORTED"
    )
    independent_verification = "PASSED" if universal else (
        "FAILED" if verdict_val == "REFUTED" else "PARTIAL"
    )
    if discover_result == "UNRESOLVED" or verdict_val == "REFUTED":
        research_state, strength = "UNRESOLVED", "UNRESOLVED"
    elif universal:
        research_state = "PREFERRED"
        strength = j.get("result_strength", "MODERATE")
        if occurrences <= 2 and strength == "STRONG":
            strength = "MODERATE"
    else:
        research_state, strength = "PREFERRED", "WEAK"
    return {
        "authority_level": "RESEARCH_JUDGMENT",
        "research_state": research_state,
        "result_strength": strength,
        "research_completeness": completeness,
        "independent_verification": independent_verification,
        "canonical_authorization": "PENDING",
        "universal_presence_holds": universal,
        "unreconciled_occurrences": unreconciled,
        "unreconciled_count": len(unreconciled),
        "resistant_occurrences": sorted(set(final_resistant)),
        "structural_uncertainty_occurrences": sorted(set(final_uncertain)),
    }


def fold_root_into_ledger(ledger: dict, root: str, entry: dict) -> dict:
    """Idempotent, lineage-preserving ledger update (pure function).

    Re-persisting identical content is a no-op. Reprocessing appends the prior
    summary to ``lineage`` instead of silently overwriting it.
    """
    roots = ledger.setdefault("roots", {})
    prior = roots.get(root)
    if prior is not None:
        prior_summary = {
            k: prior.get(k)
            for k in (
                "batch_id",
                "result_strength",
                "research_state",
                "research_completeness",
                "independent_verification",
                "universal_presence_holds",
                "adversarial_verdict",
            )
        }
        current_summary = {k: entry.get(k) for k in prior_summary}
        if prior_summary == current_summary:
            return ledger  # idempotent re-persist
        lineage = list(prior.get("lineage") or [])
        prior_compact = {k: v for k, v in prior.items() if k != "lineage"}
        lineage.append(prior_compact)
        entry = {**entry, "lineage": lineage}
    roots[root] = entry
    return ledger
