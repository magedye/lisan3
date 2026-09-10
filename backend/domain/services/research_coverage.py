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
        # COMPLETE requires BOTH exact confirmed-set equality AND zero duplicate
        # researched refs: a duplicate must fail coverage even when set equality
        # would otherwise hold (a repeated ref never counts as full "exactly once"
        # coverage). verse_ref substitution stays impossible via word_ref
        # granularity (a verse-level ref lands in ``unexpected``).
        exact_set_match=bool(expected) and not missing and not unexpected and not duplicates,
        disputed_visible=tuple(visible["DISPUTED"]),
        unresolved_visible=tuple(visible["UNRESOLVED"]),
    )


def merge_reconciliation(
    dispositions: list[dict], reconciliation: list[dict]
) -> tuple[list[dict], list[dict]]:
    """Fold reconciliation finals over preliminary mapper dispositions WITHOUT
    discarding the preliminary evidence (owner provenance-hardening).

    Returns ``(final_dispositions, reconciliation_lineage)``:

    - ``final_dispositions``: one entry per word_ref, sorted by word_ref. A
      reconciled occurrence keeps its final disposition/note AND carries the
      preserved ``preliminary_disposition`` / ``preliminary_note`` so its
      original flagged state is never lost — even when reconciled to CONSISTENT.
    - ``reconciliation_lineage``: durable per-reconciled-occurrence provenance
      record (never a count): ``word_ref``, ``preliminary_disposition``,
      ``preliminary_note``, ``final_disposition``, ``reconciliation_rationale``,
      ``deep_analysis=True``.

    A reconciliation entry is applied only when its word_ref is already a mapped
    disposition and it carries a ``final`` (never invents an occurrence).
    """
    preliminary = {d["word_ref"]: dict(d) for d in dispositions}
    final = {d["word_ref"]: dict(d) for d in dispositions}
    lineage: list[dict] = []
    for r in reconciliation:
        ref = r.get("word_ref")
        if ref not in final or not r.get("final"):
            continue
        if r["final"] not in VALID_DISPOSITIONS:
            raise ValueError(
                f"Invalid final reconciliation disposition for {ref}: {r['final']!r}"
            )
        if not r.get("rationale"):
            raise ValueError(
                f"Reconciliation for {ref} requires a non-empty rationale"
            )
        prev = preliminary[ref]
        lineage_entry = {
            "word_ref": ref,
            "preliminary_disposition": prev.get("disposition"),
            "preliminary_note": prev.get("note"),
            "final_disposition": r["final"],
            "reconciliation_rationale": r.get("rationale"),
            "deep_analysis": True,
        }
        final[ref] = {
            **prev,
            "disposition": r["final"],
            "final_disposition": r["final"],
            "note": r["rationale"],
            "deep_analysis": True,
            "preliminary_disposition": prev.get("disposition"),
            "preliminary_note": prev.get("note"),
            "reconciliation_rationale": r.get("rationale"),
            "reconciliation_lineage": [lineage_entry],
        }
        lineage.append(lineage_entry)
    final_list = sorted(final.values(), key=lambda d: d["word_ref"])
    return final_list, lineage


def upsert_coverage_batch(ledger: dict, batch_id: str, roots: list[str]) -> dict:
    """Idempotent coverage-batch log: replaying the same ``batch_id`` replaces the
    existing entry instead of appending a duplicate (also self-heals any prior
    duplicate entries for that id). Root-level idempotency is unaffected."""
    batches = ledger.setdefault("coverage_batches", [])
    batches[:] = [b for b in batches if b.get("batch_id") != batch_id]
    batches.append({"batch_id": batch_id, "roots": list(roots)})
    return ledger


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
    # Root semantic unity is NON-NEGOTIABLE and cross-lens: an occurrence held
    # unreconciled by ANY lens blocks universal presence. Besides coverage-mapping
    # RESISTANT/STRUCTURAL_UNCERTAINTY, this includes the discovery pass's own
    # inconsistent_refs — occurrences the internal discoverer could not reconcile
    # to the candidate. An UNRESOLVED discovery result likewise cannot yield
    # universal presence: a root whose single unifying contribution was never
    # established is not "present, reconciled, in every occurrence". (Without this
    # a root could be simultaneously research_state=UNRESOLVED and
    # universal_presence_holds=True — a contradiction that violated root unity.)
    discover_inconsistent = list((j.get("presence") or {}).get("inconsistent_refs") or [])
    unreconciled = sorted(set(final_resistant) | set(final_uncertain) | set(discover_inconsistent))
    universal = (
        coverage.exact_set_match
        and not unreconciled
        and verdict_val == "SUPPORTED"
        and discover_result != "UNRESOLVED"
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
