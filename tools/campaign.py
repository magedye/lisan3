"""Resumable large-scale root-research campaign runner (Owner Request: continue
autonomous semantic research to the maximum achievable extent).

Separation preserved (research MAY proceed without human canonicalization):
    AI Research Judgment -> Independent/Adversarial Verification -> Canonical Authorization
The first two stages run autonomously here; canonical_authorization stays PENDING.

Subcommands:
  bootstrap       - (re)load Tanzil + QAC into the runtime DB if empty (idempotent)
  status          - show research vs canonicalization progress
  select          - print the next N unprocessed roots (diverse across occurrence tiers)
  prep            - write FULL-coverage occurrence packets for given roots
  persist         - fold discover+verify workflow results into the ledger + CampaignState
  prep-coverage   - shard confirmed occurrences per root (frozen candidate embedded)
                    for word_ref-level coverage mapping
  persist-coverage- fold shard dispositions + reconciliation into per-root durable
                    artifacts, run exact-set validation, update ledger + CampaignState

Exact-set coverage rule (owner correction): research_completeness=COMPLETE only
when the researched word_ref set EXACTLY equals the confirmed StructuralToken
word_refs (no missing, no duplicate substitution, word_ref granularity).

State is durable: the committed ledger + per-root artifacts + the CampaignState
row make the campaign resumable in a fresh session without conversation history.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("LISAN_DATABASE_URL", "sqlite:///data/campaign/runtime.db")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.domain import models
from backend.domain.services.campaign_state import CampaignStateService
from backend.domain.services.corpus.descriptive_profile import (
    RootDescriptiveProfileService,
)
from backend.domain.services.corpus.qac_morphology import buckwalter_to_arabic
from backend.domain.services.corpus.root_universe import RootUniverseService
from backend.domain.services.research_coverage import (
    confirmed_word_refs,
    finalize_root_disposition,
    fold_root_into_ledger,
    merge_reconciliation,
    upsert_coverage_batch,
    validate_root_research_coverage,
)
from backend.infrastructure.database import SQLALCHEMY_DATABASE_URL, Base

SNAP = "snap_tanzil_1_1_ac0724796cbb"
CAMPAIGN_ID = "root-research-campaign"
METHODOLOGY = "LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4"
LEDGER = Path("artifacts/semantic-campaign/CAMPAIGN_RESEARCH_LEDGER.json")
ROOT_ARTIFACTS = Path("artifacts/semantic-campaign/roots")
PACKET_DIR = Path("data/campaign/packets")
SHARD_SIZE = 50

# Buckwalter root symbols that are illegal in Windows filenames.
_FS_ILLEGAL = '*<>|":?\\/'
# Uppercase Buckwalter letters whose lowercase form is ALSO a Buckwalter letter:
# H/h (ح/ه), S/s (ص/س), D/d (ض/د), T/t (ط/ت), Z/z (ظ/ز). On a case-insensitive
# filesystem (Windows/macOS) these collide with their lowercase twin — e.g.
# Swm (ص و م) and swm (س و م) both map to "swm.json", so one silently overwrites
# the other's durable artifact. The QAC root universe has 137 such case-fold
# pairs, so this WILL corrupt data at scale. Escape them with the same reversible
# hex scheme. (A/E never collide — 'a'/'e' are not Buckwalter letters — so they
# stay legible.)
_CASE_COLLIDING = "HSDTZ"
_ESCAPE = set(_FS_ILLEGAL) | set(_CASE_COLLIDING)


def safe_name(root: str) -> str:
    """Deterministic, case-insensitive-collision-safe encoding of a Buckwalter root.

    Encodes filesystem-illegal characters (e.g. '*' dhal -> _2A_) AND the
    uppercase homograph letters H/S/D/T/Z (e.g. 'S' -> _53_) so a root never
    shares an artifact filename with its case-twin. Legal, non-colliding symbols
    like '$' and letters like 'A'/'E' stay as-is.
    """
    return "".join(f"_{ord(c):02X}_" if c in _ESCAPE else c for c in root)


class ArtifactIdentityCollisionError(RuntimeError):
    """Raised before a root artifact could overwrite another root's bytes."""


def _write_root_json(path: Path, root: str, artifact: dict) -> None:
    """Write one root-owned JSON artifact, failing closed on identity mismatch."""
    payload_root = artifact.get("root_buckwalter")
    if payload_root != root:
        raise ArtifactIdentityCollisionError(
            f"artifact payload canonical root {payload_root!r} != requested "
            f"canonical root {root!r}"
        )

    serialized = json.dumps(artifact, ensure_ascii=False, indent=1)
    try:
        # Exclusive creation closes the first-writer race when a path is absent.
        with path.open("x", encoding="utf-8") as stream:
            stream.write(serialized)
        return
    except FileExistsError:
        pass

    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ArtifactIdentityCollisionError(
            f"cannot verify existing artifact identity at {path} before "
            f"writing canonical root {root!r}"
        ) from exc
    existing_root = existing.get("root_buckwalter") if isinstance(existing, dict) else None
    if existing_root != root:
        raise ArtifactIdentityCollisionError(
            f"artifact identity collision at {path}: existing canonical root "
            f"{existing_root!r} != requested canonical root {root!r}"
        )

    path.write_text(serialized, encoding="utf-8")


_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
_Session = sessionmaker(bind=_engine)


def _db():
    return _Session()


def load_ledger() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    return {"campaign_id": CAMPAIGN_ID, "methodology_revision": METHODOLOGY,
            "corpus_snapshot": SNAP, "roots": {}, "batches": []}


def save_ledger(ledger: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8")


def _universe(db):
    return RootUniverseService.derive(db, SNAP)


def cmd_status(_args):
    db = _db()
    uni = _universe(db)
    ledger = load_ledger()
    done = ledger["roots"]
    strengths = {}
    canon_pending = 0
    research_complete = 0
    for r in done.values():
        strengths[r["result_strength"]] = strengths.get(r["result_strength"], 0) + 1
        if r["research_completeness"] == "COMPLETE":
            research_complete += 1
        if r["canonical_authorization"] == "PENDING":
            canon_pending += 1
    print(json.dumps({
        "total_roots": len(uni),
        "processed_roots": len(done),
        "remaining_roots": len(uni) - len(done),
        "result_strength": strengths,
        "research_complete": research_complete,
        "canonicalization_pending": canon_pending,
    }, indent=1))
    db.close()


def _tokens_for_root(db, root):
    return (
        db.query(models.StructuralToken)
        .filter_by(snapshot_id=SNAP, root=root)
        .order_by(models.StructuralToken.word_ref)
        .all()
    )


def cmd_select(args):
    db = _db()
    uni = _universe(db)
    done = set(load_ledger()["roots"])
    remaining = [e for e in uni if e.root not in done]
    # Diverse selection across occurrence tiers (not only easy/frequent roots).
    tiers = {"xs": [], "s": [], "m": [], "l": [], "xl": []}
    for e in remaining:
        c = e.confirmed_occurrences
        key = ("xs" if c <= 3 else "s" if c <= 15 else "m" if c <= 50
               else "l" if c <= 200 else "xl")
        tiers[key].append(e)
    for bucket in tiers.values():
        bucket.sort(key=lambda e: (-e.confirmed_occurrences, e.root))
    n = args.n
    # proportional-ish diverse mix, capped by availability
    mix = {"xl": max(1, n // 12), "l": max(1, n // 6), "m": max(1, n // 4),
           "s": max(1, n // 4), "xs": n}  # xs fills remainder
    picked: list = []
    for k in ("xl", "l", "m", "s", "xs"):
        take = tiers[k][: mix[k]]
        picked.extend(take)
        if len(picked) >= n:
            break
    picked = picked[:n]
    print(" ".join(e.root for e in picked))
    db.close()


def cmd_prep(args):
    db = _db()
    roots = args.roots.split()
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    verse_text = {
        v: t for (v, t) in db.query(
            models.CorpusOccurrence.verse_ref, models.CorpusOccurrence.text
        ).filter(models.CorpusOccurrence.snapshot_id == SNAP).all()
    }
    manifest = []
    for root in roots:
        prof = RootDescriptiveProfileService.build_from_snapshot(db, SNAP, root)
        if prof is None:
            continue
        confirmed = set(confirmed_word_refs(db, SNAP, root))
        toks = [t for t in _tokens_for_root(db, root) if t.word_ref in confirmed]
        occ = [{
            "word_ref": t.word_ref, "verse_ref": t.verse_ref, "form": t.form,
            "verse_text": verse_text.get(t.verse_ref, ""),
        } for t in toks]
        packet = {
            "root_buckwalter": root,
            "root_arabic": buckwalter_to_arabic(root),
            "total_confirmed_occurrences": prof.total_confirmed_occurrences,
            "full_coverage": True,
            "coverage_note": "ALL confirmed occurrences included" if len(occ) <= 250
            else f"{len(occ)} occurrences — cluster for coverage",
            "form_inventory": [{"form": f.form, "count": f.count} for f in prof.forms],
            "occurrences": occ,
        }
        _write_root_json(outdir / f"{safe_name(root)}.json", root, packet)
        manifest.append({"root": root, "file": safe_name(root),
                         "arabic": buckwalter_to_arabic(root),
                         "occ": prof.total_confirmed_occurrences})
    (outdir / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"prepped {len(manifest)} packets -> {outdir}")
    db.close()


def _disposition(judgment: dict, verdict: dict, occ: int) -> dict:
    """Map discover+verify into research-level fields (canonicalization PENDING)."""
    j = judgment or {}
    v = verdict or {}
    presence = j.get("presence") or {}
    inconsistent = presence.get("inconsistent_refs") or []
    failing = v.get("failing_occurrences") or []
    unreconciled = sorted(set(inconsistent) | set(failing))
    verdict_val = v.get("verdict")
    discover_result = j.get("result")  # PREFERRED | UNRESOLVED
    universal_presence = (not unreconciled) and verdict_val == "SUPPORTED"
    # Independent (adversarial) verification passes only if SUPPORTED w/ no failures.
    independent_verification = "PASSED" if universal_presence else (
        "FAILED" if verdict_val == "REFUTED" else "PARTIAL")
    # Research completeness = full coverage was analyzed.
    research_completeness = "COMPLETE" if presence.get("occurrences_checked", 0) >= occ else "PARTIAL"
    # Result: honor the more conservative of discoverer/verifier. A confirmed
    # unreconciled occurrence blocks universal presence (root unity NON-NEGOTIABLE).
    if discover_result == "UNRESOLVED" or verdict_val == "REFUTED":
        research_state, strength = "UNRESOLVED", "UNRESOLVED"
    elif universal_presence:
        research_state = "PREFERRED"
        strength = j.get("result_strength", "MODERATE")
        if occ <= 2 and strength == "STRONG":
            strength = "MODERATE"  # too few occurrences for a STRONG universal claim
    else:  # PARTIALLY_SUPPORTED: a preferred candidate that is not yet universal
        research_state, strength = "PREFERRED", "WEAK"
    return {
        "authority_level": "RESEARCH_JUDGMENT",
        "research_state": research_state,
        "result_strength": strength,
        "research_completeness": research_completeness,
        "independent_verification": independent_verification,
        "canonical_authorization": "PENDING",
        "universal_presence_holds": universal_presence,
        "unreconciled_occurrences": unreconciled,
        "unreconciled_count": len(unreconciled),
        "candidate_root_contribution": j.get("candidate_root_contribution"),
        "plain_explanation": j.get("plain_explanation"),
        "strongest_counterexample": j.get("strongest_counterexample"),
        "distinctiveness_ok": v.get("distinctiveness_ok"),
        "falsifiable": v.get("falsifiable"),
        "adversarial_verdict": verdict_val,
    }


def cmd_persist(args):
    db = _db()
    results = json.loads(Path(args.results).read_text(encoding="utf-8"))
    ledger = load_ledger()
    uni = {e.root: e for e in _universe(db)}
    CampaignStateService.initialize(
        db, campaign_id=CAMPAIGN_ID, methodology_revision=METHODOLOGY,
        corpus_snapshot=SNAP, queue=[e for e in uni])
    batch_roots = []
    for item in results:
        root = item.get("root")
        if root not in uni:
            continue
        occ = uni[root].confirmed_occurrences
        disp = _disposition(item.get("judgment"), item.get("verdict"), occ)
        disp.update({
            "root_arabic": buckwalter_to_arabic(root),
            "occurrences": occ,
            "batch_id": args.batch,
            "methodology_revision": METHODOLOGY,
            "corpus_snapshot": SNAP,
            "source": "QAC_MORPHOLOGY v0.4",
        })
        # Preserve lineage: keep prior disposition history.
        prior = ledger["roots"].get(root)
        if prior:
            disp["previous"] = {k: prior.get(k) for k in
                                ("batch_id", "result_strength", "adversarial_verdict",
                                 "research_completeness")}
        ledger["roots"][root] = disp
        batch_roots.append(root)
        CampaignStateService.checkpoint_root(db, CAMPAIGN_ID, root)
    # Batch metrics.
    strengths: dict = {}
    for r in batch_roots:
        s = ledger["roots"][r]["result_strength"]
        strengths[s] = strengths.get(s, 0) + 1
    ledger["batches"].append({
        "batch_id": args.batch, "roots": batch_roots,
        "count": len(batch_roots), "result_strength": strengths,
    })
    ledger["updated_roots_total"] = len(ledger["roots"])
    save_ledger(ledger)
    print(json.dumps({"batch": args.batch, "persisted": len(batch_roots),
                      "result_strength": strengths,
                      "total_processed": len(ledger["roots"]),
                      "remaining": len(uni) - len(ledger["roots"])}, indent=1))
    db.close()


def cmd_bootstrap(_args):
    """Idempotent runtime bootstrap: Tanzil + QAC into the local DB if empty."""
    Base.metadata.create_all(_engine)
    db = _db()
    tokens = db.query(models.StructuralToken).filter_by(snapshot_id=SNAP).count()
    if tokens:
        print(json.dumps({"bootstrapped": False, "existing_tokens": tokens}))
        db.close()
        return
    from backend.domain.services.corpus.importer import TanzilPreActivationImporter
    from backend.domain.services.corpus.qac_morphology import QacMorphologyImporter

    res = TanzilPreActivationImporter.import_candidate(db, repository_root=Path("."))
    qac = QacMorphologyImporter.import_tokens(db, res.snapshot.id)
    print(json.dumps({
        "bootstrapped": True, "snapshot": res.snapshot.id,
        "verses": res.occurrence_count, "tokens": qac.tokens_persisted,
        "distinct_roots": qac.distinct_roots,
    }))
    db.close()


def cmd_prep_coverage(args):
    """Shard confirmed occurrences per root for word_ref-level coverage mapping.

    The frozen candidate contribution is read from research results (judgment
    stays frozen; coverage mapping never re-opens discovery)."""
    db = _db()
    results = json.loads(Path(args.results).read_text(encoding="utf-8"))
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    verse_text = {
        v: t for (v, t) in db.query(
            models.CorpusOccurrence.verse_ref, models.CorpusOccurrence.text
        ).filter(models.CorpusOccurrence.snapshot_id == SNAP).all()
    }
    manifest = []
    for item in results:
        root = item.get("root")
        j = item.get("judgment") or {}
        candidate = j.get("candidate_root_contribution")
        if not root or not candidate:
            continue
        refs = confirmed_word_refs(db, SNAP, root)
        tok_by_ref = {t.word_ref: t for t in _tokens_for_root(db, root)}
        shards = [refs[i:i + SHARD_SIZE] for i in range(0, len(refs), SHARD_SIZE)]
        for k, shard_refs in enumerate(shards):
            shard = {
                "root_buckwalter": root,
                "root_arabic": buckwalter_to_arabic(root),
                "frozen_candidate_root_contribution": candidate,
                "plain_explanation": j.get("plain_explanation"),
                "shard_index": k,
                "shard_count": len(shards),
                "occurrences": [{
                    "word_ref": r,
                    "verse_ref": tok_by_ref[r].verse_ref,
                    "form": tok_by_ref[r].form,
                    "verse_text": verse_text.get(tok_by_ref[r].verse_ref, ""),
                } for r in shard_refs],
            }
            _write_root_json(outdir / f"{safe_name(root)}.s{k}.json", root, shard)
        manifest.append({"root": root, "file": safe_name(root),
                         "shards": len(shards), "expected_refs": len(refs)})
    (outdir / "_coverage_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(manifest))
    db.close()


def cmd_persist_coverage(args):
    """Fold coverage-mapping results into per-root durable artifacts + ledger.

    coverage results format: [{root, dispositions:[{word_ref, disposition, note}],
    reconciliation:[{word_ref, final, rationale}]}]."""
    db = _db()
    research = {i["root"]: i for i in json.loads(Path(args.research).read_text(encoding="utf-8"))}
    coverage_items = json.loads(Path(args.coverage).read_text(encoding="utf-8"))
    ledger = load_ledger()
    uni = {e.root: e for e in _universe(db)}
    ROOT_ARTIFACTS.mkdir(parents=True, exist_ok=True)
    CampaignStateService.initialize(
        db, campaign_id=CAMPAIGN_ID, methodology_revision=METHODOLOGY,
        corpus_snapshot=SNAP, queue=list(uni))
    summary = []
    for item in coverage_items:
        root = item.get("root")
        if root not in uni or root not in research:
            continue
        occ = uni[root].confirmed_occurrences
        judgment = research[root].get("judgment") or {}
        verdict = research[root].get("verdict") or {}
        # Apply resistant-case deep-analysis finals over the base mapping while
        # PRESERVING the preliminary mapper disposition + note (provenance).
        base_dispositions = item.get("dispositions") or []
        final_dispositions, reconciliation_lineage = merge_reconciliation(
            base_dispositions, item.get("reconciliation") or [])
        dispositions = {d["word_ref"]: d for d in final_dispositions}
        # Exact-set validation runs on the mapped word_refs (pre-merge list so a
        # duplicated researched ref is still caught by the validator).
        researched_refs = [d["word_ref"] for d in base_dispositions]
        validation = validate_root_research_coverage(db, SNAP, root, researched_refs)
        final_resistant = sorted(r for r, d in dispositions.items()
                                 if d.get("disposition") == "RESISTANT")
        final_uncertain = sorted(r for r, d in dispositions.items()
                                 if d.get("disposition") == "STRUCTURAL_UNCERTAINTY")
        disp = finalize_root_disposition(
            judgment, verdict, validation, final_resistant, final_uncertain, occ)
        artifact = {
            "root_buckwalter": root,
            "root_arabic": buckwalter_to_arabic(root),
            "corpus_snapshot": SNAP,
            "morphology_source": "QAC_MORPHOLOGY v0.4 (sha256 a1d12923...)",
            "methodology_revision": METHODOLOGY,
            "batch_id": args.batch,
            "occurrences": occ,
            "frozen_candidate_root_contribution": judgment.get("candidate_root_contribution"),
            "internal_discovery": judgment,
            "adversarial_verification": verdict,
            "coverage_validation": validation.as_dict(),
            "occurrence_dispositions": final_dispositions,
            "resistant_deep_analysis": reconciliation_lineage,
            **disp,
        }
        _write_root_json(ROOT_ARTIFACTS / f"{safe_name(root)}.json", root, artifact)
        ledger_entry = {
            "root_arabic": buckwalter_to_arabic(root),
            "occurrences": occ,
            "batch_id": args.batch,
            "methodology_revision": METHODOLOGY,
            "corpus_snapshot": SNAP,
            "source": "QAC_MORPHOLOGY v0.4",
            "artifact": f"artifacts/semantic-campaign/roots/{safe_name(root)}.json",
            "candidate_root_contribution": judgment.get("candidate_root_contribution"),
            "plain_explanation": judgment.get("plain_explanation"),
            "strongest_counterexample": judgment.get("strongest_counterexample"),
            "adversarial_verdict": verdict.get("verdict"),
            "distinctiveness_ok": verdict.get("distinctiveness_ok"),
            "falsifiable": verdict.get("falsifiable"),
            "coverage_exact_set_match": validation.exact_set_match,
            **disp,
        }
        fold_root_into_ledger(ledger, root, ledger_entry)
        CampaignStateService.checkpoint_root(db, CAMPAIGN_ID, root)
        summary.append({"root": root, "exact_set": validation.exact_set_match,
                        "strength": disp["result_strength"],
                        "completeness": disp["research_completeness"],
                        "universal": disp["universal_presence_holds"],
                        "resistant": len(final_resistant)})
    upsert_coverage_batch(ledger, args.batch, [s["root"] for s in summary])
    save_ledger(ledger)
    print(json.dumps(summary, indent=1))
    db.close()


def cmd_mark_pending(args):
    """Classify roots whose coverage evidence is not yet exact-set validated."""
    ledger = load_ledger()
    changed = []
    for root in args.roots.split():
        entry = ledger["roots"].get(root)
        if entry and not entry.get("coverage_exact_set_match"):
            entry["research_completeness"] = "PENDING_COVERAGE_EVIDENCE"
            changed.append(root)
    save_ledger(ledger)
    print(json.dumps({"marked_pending_coverage_evidence": changed}))


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("bootstrap").set_defaults(func=cmd_bootstrap)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sp = sub.add_parser("select"); sp.add_argument("--n", type=int, default=40); sp.set_defaults(func=cmd_select)
    pp = sub.add_parser("prep"); pp.add_argument("--roots", required=True); pp.add_argument("--out", required=True); pp.set_defaults(func=cmd_prep)
    ps = sub.add_parser("persist"); ps.add_argument("--results", required=True); ps.add_argument("--batch", required=True); ps.set_defaults(func=cmd_persist)
    pc = sub.add_parser("prep-coverage"); pc.add_argument("--results", required=True); pc.add_argument("--out", required=True); pc.set_defaults(func=cmd_prep_coverage)
    pv = sub.add_parser("persist-coverage"); pv.add_argument("--research", required=True); pv.add_argument("--coverage", required=True); pv.add_argument("--batch", required=True); pv.set_defaults(func=cmd_persist_coverage)
    mp = sub.add_parser("mark-pending"); mp.add_argument("--roots", required=True); mp.set_defaults(func=cmd_mark_pending)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
