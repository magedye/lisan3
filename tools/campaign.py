"""Resumable large-scale root-research campaign runner (Owner Request: continue
autonomous semantic research to the maximum achievable extent).

Separation preserved (research MAY proceed without human canonicalization):
    AI Research Judgment -> Independent/Adversarial Verification -> Canonical Authorization
The first two stages run autonomously here; canonical_authorization stays PENDING.

Subcommands:
  bootstrap  - (re)load Tanzil + QAC into the runtime DB if empty (idempotent)
  status     - show research vs canonicalization progress
  select     - print the next N unprocessed roots (diverse across occurrence tiers)
  prep       - write FULL-coverage occurrence packets for given roots
  persist    - fold discover+verify workflow results into the ledger + CampaignState

State is durable: the committed ledger + the CampaignState row make the campaign
resumable in a fresh session without any conversation history.
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
from backend.infrastructure.database import SQLALCHEMY_DATABASE_URL

SNAP = "snap_tanzil_1_1_ac0724796cbb"
CAMPAIGN_ID = "root-research-campaign"
METHODOLOGY = "LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4"
LEDGER = Path("artifacts/semantic-campaign/CAMPAIGN_RESEARCH_LEDGER.json")
PACKET_DIR = Path("data/campaign/packets")

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
        toks = _tokens_for_root(db, root)
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
        (outdir / f"{root}.json").write_text(
            json.dumps(packet, ensure_ascii=False, indent=1), encoding="utf-8")
        manifest.append({"root": root, "arabic": buckwalter_to_arabic(root),
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


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sp = sub.add_parser("select"); sp.add_argument("--n", type=int, default=40); sp.set_defaults(func=cmd_select)
    pp = sub.add_parser("prep"); pp.add_argument("--roots", required=True); pp.add_argument("--out", required=True); pp.set_defaults(func=cmd_prep)
    ps = sub.add_parser("persist"); ps.add_argument("--results", required=True); ps.add_argument("--batch", required=True); ps.set_defaults(func=cmd_persist)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
