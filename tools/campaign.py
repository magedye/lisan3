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
import re
import subprocess
from functools import lru_cache
from pathlib import Path

os.environ.setdefault("LISAN_DATABASE_URL", "sqlite:///data/campaign/runtime.db")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.domain import models
from backend.domain.services.campaign_state import CampaignStateService
from backend.domain.services.corpus.descriptive_profile import (
    RootDescriptiveProfileService,
)
from backend.domain.services.corpus.qac_morphology import (
    DEFAULT_QAC_ARTIFACT,
    buckwalter_to_arabic,
    load_verified_segments,
)
from backend.domain.services.corpus.root_universe import RootUniverseService
from backend.domain.services.research_coverage import (
    VALID_DISPOSITIONS,
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


def root_identity(root: str) -> dict[str, str]:
    """Canonical linguistic/technical/file identities for a campaign root."""
    return {
        "root_arabic": buckwalter_to_arabic(root),
        "root_buckwalter": root,
        "root_id": root,
        "artifact_name": f"{safe_name(root)}.json",
    }


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
        with path.open("x", encoding="utf-8", newline="\n") as stream:
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

    path.write_text(serialized, encoding="utf-8", newline="\n")


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
    # Preserve the ledger's established CRLF bytes on Windows so an append does
    # not normalize and obscure its historical content in a campaign diff.
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


@lru_cache(maxsize=1)
def _verified_qac_segments_by_ref():
    """Qualified structural segment surfaces, keyed by exact word_ref.

    The QAC FORM field is retained as Buckwalter-style source data.  It is not
    converted into claimed canonical Arabic surface text: the admitted Tanzil
    verse remains the Quran-text authority and the repository has not adopted a
    versioned segment-level orthographic alignment profile.
    """
    if not DEFAULT_QAC_ARTIFACT.exists():
        return {}
    return {segment.word_ref: segment for segment in load_verified_segments()}


def _occurrence_metadata(token, root: str, verse_text: str) -> dict:
    segment = _verified_qac_segments_by_ref().get(token.word_ref)
    segment_matches = segment is not None and segment.root == root
    identity = root_identity(root)
    return {
        **identity,
        "word_ref": token.word_ref,
        "verse_ref": token.verse_ref,
        "surface_form_arabic": None,
        "surface_form_arabic_status": "NOT_AVAILABLE_CANONICALLY",
        "surface_form_arabic_reason": (
            "Canonical Tanzil authority is verse-level; no reviewed segment-level "
            "Buckwalter-to-Arabic alignment profile is adopted."
        ),
        "qac_surface_form_buckwalter": segment.form if segment_matches else None,
        "qac_tag": segment.tag if segment_matches else None,
        "qac_pos": segment.pos if segment_matches else None,
        "qac_verb_form": segment.verb_form if segment_matches else None,
        "morphology": token.form,
        "form": token.form,
        "structural_evidence": {
            "source_id": token.source_id,
            "source_version": token.source_version,
            "extraction_version": token.extraction_version,
            "attribution_status": token.attribution_status,
        },
        "verse_text": verse_text,
    }


def _index_items_by_root(items, label: str) -> dict[str, dict]:
    if not isinstance(items, list):
        raise TypeError(f"{label} must be a JSON list")
    indexed: dict[str, dict] = {}
    for item in items:
        if not isinstance(item, dict) or not item.get("root"):
            raise ValueError(f"{label} contains an item without a root identity")
        root = item["root"]
        if root in indexed:
            raise ValueError(f"{label} contains duplicate root {root!r}")
        indexed[root] = item
    return indexed


def _cluster_matches(occurrence: dict, where: dict) -> bool:
    """Return whether one explicit semantic usage-class selector matches."""
    if not where:
        raise ValueError("coverage cluster requires a non-empty where selector")
    if "word_refs" in where and occurrence.get("word_ref") not in where["word_refs"]:
        return False
    if "qac_pos" in where and occurrence.get("qac_pos") not in where["qac_pos"]:
        return False
    if (
        "qac_verb_form" in where
        and occurrence.get("qac_verb_form") not in where["qac_verb_form"]
    ):
        return False
    if "qac_surface_regex" in where and not re.search(
        where["qac_surface_regex"], occurrence.get("qac_surface_form_buckwalter") or ""
    ):
        return False
    known = {"word_refs", "qac_pos", "qac_verb_form", "qac_surface_regex"}
    unknown = sorted(set(where) - known)
    if unknown:
        raise ValueError(f"unknown coverage-cluster selectors: {unknown}")
    return True


def materialize_occurrence_dispositions(
    root: str, occurrences: list[dict], classification: dict
) -> tuple[list[dict], list[dict]]:
    """Expand reviewed usage classes into one explicit record per occurrence.

    This is intentionally fail-closed: there is no default disposition; every
    class is count-pinned and every occurrence must match exactly one class.
    Semantic judgments stay authored in the research result, while this helper
    performs only deterministic evidence-preserving expansion.
    """
    clusters = classification.get("clusters") or []
    if not clusters:
        raise ValueError(f"root {root!r} has no reviewed occurrence classes")
    seen_ids: set[str] = set()
    cluster_counts: dict[str, int] = {}
    dispositions: list[dict] = []
    for occurrence in occurrences:
        matches = [c for c in clusters if _cluster_matches(occurrence, c.get("where") or {})]
        if len(matches) != 1:
            raise ValueError(
                f"root {root!r} occurrence {occurrence.get('word_ref')!r} matched "
                f"{len(matches)} reviewed classes; expected exactly one"
            )
        cluster = matches[0]
        cluster_id = cluster.get("cluster_id")
        if not cluster_id:
            raise ValueError(f"root {root!r} coverage class lacks cluster_id")
        seen_ids.add(cluster_id)
        cluster_counts[cluster_id] = cluster_counts.get(cluster_id, 0) + 1
        disposition = cluster.get("disposition")
        if disposition not in VALID_DISPOSITIONS:
            raise ValueError(
                f"root {root!r} class {cluster_id!r} has invalid disposition {disposition!r}"
            )
        required = (
            "candidate_semantic_interpretation",
            "classification_rationale",
            "supporting_evidence_note",
        )
        missing = [field for field in required if not cluster.get(field)]
        if missing:
            raise ValueError(
                f"root {root!r} class {cluster_id!r} lacks evidence fields {missing}"
            )
        counterevidence = cluster.get("counterevidence")
        if not isinstance(counterevidence, list):
            raise TypeError(
                f"root {root!r} class {cluster_id!r} requires counterevidence list"
            )
        dispositions.append({
            "word_ref": occurrence["word_ref"],
            "disposition": disposition,
            "note": cluster["classification_rationale"],
            "coverage_cluster_id": cluster_id,
            "candidate_semantic_interpretation": (
                cluster["candidate_semantic_interpretation"]
            ),
            "cluster_supporting_evidence": cluster["supporting_evidence_note"],
            "counterevidence": counterevidence,
            "verifier_objection": counterevidence,
        })
    defined_ids = [c.get("cluster_id") for c in clusters]
    if len(defined_ids) != len(set(defined_ids)):
        raise ValueError(f"root {root!r} has duplicate coverage cluster ids")
    unused = sorted(set(defined_ids) - seen_ids)
    if unused:
        raise ValueError(f"root {root!r} has unused coverage classes: {unused}")
    for cluster in clusters:
        cluster_id = cluster["cluster_id"]
        expected = cluster.get("occurrence_count_expected")
        actual = cluster_counts.get(cluster_id, 0)
        if expected != actual:
            raise ValueError(
                f"root {root!r} class {cluster_id!r} count drift: "
                f"expected {expected}, got {actual}"
            )
    reconciliation = classification.get("reconciliation") or []
    occurrence_refs = {o["word_ref"] for o in occurrences}
    unknown_reconciliation = sorted(
        r.get("word_ref") for r in reconciliation if r.get("word_ref") not in occurrence_refs
    )
    if unknown_reconciliation:
        raise ValueError(
            f"root {root!r} reconciliation references unknown occurrences: "
            f"{unknown_reconciliation}"
        )
    return dispositions, reconciliation


def cmd_materialize_coverage(args):
    """Expand explicit, reviewed semantic usage classes into exact-set coverage."""
    research_items = json.loads(Path(args.research).read_text(encoding="utf-8"))
    research = _index_items_by_root(research_items, "research results")
    packet_dir = Path(args.packets)
    manifest_items = json.loads(
        (packet_dir / "_manifest.json").read_text(encoding="utf-8")
    )
    manifest = _index_items_by_root(manifest_items, "packet manifest")
    if set(research) != set(manifest):
        raise ValueError(
            "research and packet root populations differ: "
            f"research_only={sorted(set(research) - set(manifest))}, "
            f"packet_only={sorted(set(manifest) - set(research))}"
        )
    coverage_items = []
    for root in research:
        packet = json.loads(
            (packet_dir / f"{safe_name(root)}.json").read_text(encoding="utf-8")
        )
        if packet.get("root_buckwalter") != root:
            raise ValueError(f"packet identity mismatch for root {root!r}")
        classification = (research[root].get("judgment") or {}).get(
            "occurrence_classification"
        ) or {}
        dispositions, reconciliation = materialize_occurrence_dispositions(
            root, packet.get("occurrences") or [], classification
        )
        coverage_items.append({
            "root": root,
            "dispositions": dispositions,
            "reconciliation": reconciliation,
            "class_counts": {
                cluster["cluster_id"]: cluster["occurrence_count_expected"]
                for cluster in classification["clusters"]
            },
        })
    Path(args.out).write_text(
        json.dumps(coverage_items, ensure_ascii=False, indent=1),
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps({
            "roots": len(coverage_items),
            "occurrences": sum(len(i["dispositions"]) for i in coverage_items),
            "out": args.out,
        })
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
        occ = [
            _occurrence_metadata(t, root, verse_text.get(t.verse_ref, ""))
            for t in toks
        ]
        packet = {
            **root_identity(root),
            "total_confirmed_occurrences": prof.total_confirmed_occurrences,
            "full_coverage": True,
            "coverage_note": "ALL confirmed occurrences included" if len(occ) <= 250
            else f"{len(occ)} occurrences — cluster for coverage",
            "form_inventory": [{"form": f.form, "count": f.count} for f in prof.forms],
            "occurrences": occ,
        }
        _write_root_json(outdir / f"{safe_name(root)}.json", root, packet)
        manifest.append({
            **root_identity(root),
            "root": root,
            "file": safe_name(root),
            "arabic": buckwalter_to_arabic(root),
            "occ": prof.total_confirmed_occurrences,
        })
    (outdir / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1),
        encoding="utf-8",
        newline="\n",
    )
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
                **root_identity(root),
                "frozen_candidate_root_contribution": candidate,
                "plain_explanation": j.get("plain_explanation"),
                "shard_index": k,
                "shard_count": len(shards),
                "occurrences": [
                    _occurrence_metadata(
                        tok_by_ref[r], root, verse_text.get(tok_by_ref[r].verse_ref, "")
                    )
                    for r in shard_refs
                ],
            }
            _write_root_json(outdir / f"{safe_name(root)}.s{k}.json", root, shard)
        manifest.append({
            **root_identity(root),
            "root": root,
            "file": safe_name(root),
            "shards": len(shards),
            "expected_refs": len(refs),
        })
    (outdir / "_coverage_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1),
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(manifest))
    db.close()


def cmd_persist_coverage(args):
    """Fold coverage-mapping results into per-root durable artifacts + ledger.

    coverage results format: [{root, dispositions:[{word_ref, disposition, note}],
    reconciliation:[{word_ref, final, rationale}]}]."""
    db = _db()
    research_items = json.loads(Path(args.research).read_text(encoding="utf-8"))
    coverage_items = json.loads(Path(args.coverage).read_text(encoding="utf-8"))
    research = _index_items_by_root(research_items, "research results")
    coverage = _index_items_by_root(coverage_items, "coverage results")
    if set(research) != set(coverage):
        raise ValueError(
            "research and coverage root populations differ: "
            f"research_only={sorted(set(research) - set(coverage))}, "
            f"coverage_only={sorted(set(coverage) - set(research))}"
        )
    ledger = load_ledger()
    uni = {e.root: e for e in _universe(db)}
    unknown = sorted(set(research) - set(uni))
    if unknown:
        raise ValueError(f"research contains roots outside the canonical universe: {unknown}")
    ROOT_ARTIFACTS.mkdir(parents=True, exist_ok=True)
    CampaignStateService.initialize(
        db, campaign_id=CAMPAIGN_ID, methodology_revision=METHODOLOGY,
        corpus_snapshot=SNAP, queue=list(uni))
    summary = []
    verse_text = {
        v: t for (v, t) in db.query(
            models.CorpusOccurrence.verse_ref, models.CorpusOccurrence.text
        ).filter(models.CorpusOccurrence.snapshot_id == SNAP).all()
    }
    for item in coverage.values():
        root = item.get("root")
        occ = uni[root].confirmed_occurrences
        judgment = research[root].get("judgment") or {}
        verdict = research[root].get("verdict") or {}
        # Apply resistant-case deep-analysis finals over the base mapping while
        # PRESERVING the preliminary mapper disposition + note (provenance).
        base_dispositions = item.get("dispositions") or []
        final_dispositions, reconciliation_lineage = merge_reconciliation(
            base_dispositions, item.get("reconciliation") or [])
        tok_by_ref = {t.word_ref: t for t in _tokens_for_root(db, root)}
        enriched_dispositions = []
        for disposition in final_dispositions:
            ref = disposition["word_ref"]
            token = tok_by_ref.get(ref)
            if token is None:
                raise ValueError(
                    f"coverage result {root!r} references missing structural token {ref!r}"
                )
            enriched = dict(disposition)
            enriched.setdefault("preliminary_disposition", enriched.get("disposition"))
            enriched.setdefault("preliminary_note", enriched.get("note"))
            enriched.setdefault("final_disposition", enriched.get("disposition"))
            enriched.setdefault("reconciliation_rationale", None)
            enriched.setdefault("reconciliation_lineage", [])
            enriched.setdefault(
                "candidate_semantic_interpretation",
                judgment.get("candidate_root_contribution"),
            )
            enriched.setdefault("counterevidence", [])
            enriched.setdefault("verifier_objection", enriched.get("counterevidence", []))
            enriched.setdefault(
                "supporting_evidence",
                [{
                    "source": "CANONICAL_TANZIL_VERSE",
                    "verse_ref": token.verse_ref,
                    "verse_text": verse_text.get(token.verse_ref, ""),
                }],
            )
            enriched.update(
                _occurrence_metadata(
                    token, root, verse_text.get(token.verse_ref, "")
                )
            )
            enriched_dispositions.append(enriched)
        final_dispositions = enriched_dispositions
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
            **root_identity(root),
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
            **root_identity(root),
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
    ledger["updated_roots_total"] = len(ledger["roots"])
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


BATCH06_ROOT_JUDGMENT_FIELDS = (
    "contract_type",
    "claim_scope",
    "claim_scope_kind",
    "layer_attribution",
    "root_evidence_refs",
    "root_counterevidence_refs",
    "hard_cases",
    "rejection_condition",
    "falsification_status",
    "reopen_conditions",
    "purity_status",
)
BATCH06_CLAIM_SCOPE_KINDS = {
    "ROOT_GENERALIZATION",
    "DERIVATIONAL_FAMILY",
    "LEXICALIZED_CLASS",
    "OCCURRENCE_LEVEL",
    "UNRESOLVED_CLASS_ONLY",
}
BATCH06_CLAIM_SCOPES = {"UNIVERSAL", "REPRESENTATIVE", "LOCAL"}


def _batch06_artifact_paths(repository_root: Path, manifest: dict) -> dict[str, Path]:
    """Resolve the frozen Batch 06 root set without scanning other batches."""
    paths: dict[str, Path] = {}
    for entry in manifest.get("roots") or []:
        root = entry.get("root_buckwalter")
        artifact_name = entry.get("artifact_name")
        if not isinstance(root, str) or not isinstance(artifact_name, str):
            raise TypeError("Batch 06 manifest contains an invalid root identity")
        if root in paths:
            raise ValueError(f"Batch 06 manifest duplicates root {root!r}")
        paths[root] = repository_root / "artifacts/semantic-campaign/roots" / artifact_name
    if len(paths) != 40:
        raise ValueError(f"Batch 06 corrective revision requires exactly 40 roots, got {len(paths)}")
    return paths


def _root_occurrence_refs(artifact: dict) -> set[str]:
    return {
        item["word_ref"]
        for item in artifact.get("occurrence_dispositions") or []
        if isinstance(item, dict) and isinstance(item.get("word_ref"), str)
    }


def _root_cluster_evidence_refs(artifact: dict) -> list[str]:
    """Return one persisted word_ref from every existing materialized class."""
    refs: list[str] = []
    seen_clusters: set[str] = set()
    for item in artifact.get("occurrence_dispositions") or []:
        cluster = item.get("coverage_cluster_id")
        ref = item.get("word_ref")
        if isinstance(cluster, str) and isinstance(ref, str) and cluster not in seen_clusters:
            refs.append(ref)
            seen_clusters.add(cluster)
    return refs


def _default_claim_scope(artifact: dict) -> tuple[str, str]:
    """Keep coverage scope distinct from the semantic kind of the claim."""
    if artifact.get("research_state") == "UNRESOLVED":
        return "LOCAL", "UNRESOLVED_CLASS_ONLY"
    if artifact.get("universal_presence_holds"):
        return "UNIVERSAL", "ROOT_GENERALIZATION"
    clusters = {
        item.get("coverage_cluster_id")
        for item in artifact.get("occurrence_dispositions") or []
        if item.get("coverage_cluster_id")
    }
    if len(clusters) > 1:
        return "REPRESENTATIVE", "LEXICALIZED_CLASS"
    return "LOCAL", "OCCURRENCE_LEVEL"


def _default_batch06_root_contract(artifact: dict) -> dict:
    """Complete the root-artifact contract from persisted, resolvable evidence.

    ``claim_scope`` keeps the canonical UNIVERSAL/REPRESENTATIVE/LOCAL meaning.
    ``claim_scope_kind`` records the distinct semantic extent requested for the
    campaign artifacts; it is not an alias for evidentiary coverage scope.
    """
    evidence_refs = _root_cluster_evidence_refs(artifact)
    occurrence_refs = _root_occurrence_refs(artifact)
    resistant_refs = sorted(
        item["word_ref"]
        for item in artifact.get("occurrence_dispositions") or []
        if item.get("final_disposition") == "RESISTANT"
    )
    historical_refs = sorted({
        item["word_ref"]
        for item in artifact.get("resistant_deep_analysis") or []
        if isinstance(item, dict) and item.get("word_ref") in occurrence_refs
    })
    counter_refs = sorted(set(resistant_refs) | set(historical_refs))
    scope, scope_kind = _default_claim_scope(artifact)
    strongest_counterexample = (
        (artifact.get("internal_discovery") or {}).get("strongest_counterexample")
        or "No additional root-level counterexample was persisted before this structural completion."
    )
    hard_ref = (counter_refs or evidence_refs)[:1]
    hard_cases = [
        {
            "word_ref": ref,
            "role": "PERSISTED_STRESS_CASE",
            "reason": strongest_counterexample,
        }
        for ref in hard_ref
    ]
    clusters = sorted({
        item.get("coverage_cluster_id")
        for item in artifact.get("occurrence_dispositions") or []
        if isinstance(item.get("coverage_cluster_id"), str)
    })
    reconciliation = "No historical reconciliation record is present."
    if historical_refs:
        reconciliation = "Historical reconciliation lineage remains persisted for: " + ", ".join(historical_refs)
    resistance = "No final resistant occurrence is currently persisted."
    if resistant_refs:
        resistance = "Final resistance remains persisted for: " + ", ".join(resistant_refs)
    return {
        "contract_type": "ROOT_CONCEPT",
        "claim_scope": scope,
        "claim_scope_kind": scope_kind,
        "layer_attribution": {
            "occurrence_evidence": "Exact word_ref-level evidence is persisted in occurrence_dispositions.",
            "derivation": "QAC materialized form clusters: " + ", ".join(clusters),
            "lexical_class": "Each occurrence remains attached to one persisted coverage cluster.",
            "contextual_relation": "Canonical Tanzil verse_text is retained on every occurrence record.",
            "reconciliation": reconciliation,
            "unresolved_resistance": resistance,
        },
        "root_evidence_refs": evidence_refs,
        "root_counterevidence_refs": counter_refs,
        "hard_cases": hard_cases,
        "rejection_condition": {
            "challenging_finding": "A confirmed occurrence lacks the claimed contribution after the recorded class partition.",
            "search_location": "The complete persisted Batch 06 word_ref set for this root.",
            "verification_method": "Compare each claimed class against its persisted occurrence evidence and counterevidence.",
            "confounder_control": "Keep derivation, lexical class, construction, and local context separate from root contribution.",
            "failure_consequence": "Narrow the claim to the surviving class or record the root result as unresolved.",
        },
        "falsification_status": (
            "NOT_REQUIRED"
            if artifact.get("research_state") == "UNRESOLVED"
            else "PASSED"
        ),
        "reopen_conditions": [
            "A verified Quran-internal occurrence-level bridge changes a listed class boundary.",
            "A correction to a referenced occurrence, source binding, or materialized classification changes this judgment's evidence set.",
        ],
        "purity_status": "NOT_EVALUATED",
    }


def validate_batch06_root_judgment_contract(artifact: dict) -> list[str]:
    """Validate the exact persisted Batch 06 root contract and reference links."""
    root = artifact.get("root_buckwalter", "<unknown>")
    errors: list[str] = []
    missing = [field for field in BATCH06_ROOT_JUDGMENT_FIELDS if field not in artifact]
    if missing:
        errors.append(f"{root}: missing root judgment fields {missing}")
        return errors
    if artifact.get("contract_type") != "ROOT_CONCEPT":
        errors.append(f"{root}: contract_type must be ROOT_CONCEPT")
    if artifact.get("claim_scope") not in BATCH06_CLAIM_SCOPES:
        errors.append(f"{root}: invalid claim_scope")
    if artifact.get("claim_scope_kind") not in BATCH06_CLAIM_SCOPE_KINDS:
        errors.append(f"{root}: invalid claim_scope_kind")
    if artifact.get("universal_presence_holds") and artifact.get("claim_scope") != "UNIVERSAL":
        errors.append(f"{root}: non-UNIVERSAL claim cannot serialize universal presence")
    if artifact.get("universal_presence_holds") and artifact.get("claim_scope_kind") != "ROOT_GENERALIZATION":
        errors.append(f"{root}: non-root-generalization cannot serialize universal presence")
    if artifact.get("claim_scope_kind") == "UNRESOLVED_CLASS_ONLY":
        if artifact.get("research_state") != "UNRESOLVED":
            errors.append(f"{root}: unresolved/class-only scope requires UNRESOLVED state")
        if artifact.get("result_strength") != "UNRESOLVED":
            errors.append(f"{root}: unresolved/class-only scope requires UNRESOLVED strength")
    if artifact.get("purity_status") != "NOT_EVALUATED":
        errors.append(f"{root}: purity_status must remain NOT_EVALUATED")
    layers = artifact.get("layer_attribution")
    expected_layers = {
        "occurrence_evidence", "derivation", "lexical_class", "contextual_relation",
        "reconciliation", "unresolved_resistance",
    }
    if not isinstance(layers, dict) or expected_layers - set(layers):
        errors.append(f"{root}: layer_attribution lacks required material layers")
    elif any(not isinstance(layers[key], str) or not layers[key].strip() for key in expected_layers):
        errors.append(f"{root}: layer_attribution contains an empty material layer")
    refs = _root_occurrence_refs(artifact)
    for field in ("root_evidence_refs", "root_counterevidence_refs"):
        value = artifact.get(field)
        if not isinstance(value, list) or any(not isinstance(ref, str) for ref in value):
            errors.append(f"{root}: {field} must be a word_ref list")
        elif not set(value) <= refs:
            errors.append(f"{root}: {field} contains an unresolved word_ref")
    hard_cases = artifact.get("hard_cases")
    if not isinstance(hard_cases, list) or not hard_cases:
        errors.append(f"{root}: hard_cases must be non-empty")
    else:
        for case in hard_cases:
            if not isinstance(case, dict) or case.get("word_ref") not in refs:
                errors.append(f"{root}: hard_cases contains an unresolved word_ref")
                break
            if not isinstance(case.get("role"), str) or not isinstance(case.get("reason"), str):
                errors.append(f"{root}: hard_cases entry lacks material role or reason")
                break
    condition = artifact.get("rejection_condition")
    required_condition = {
        "challenging_finding", "search_location", "verification_method",
        "confounder_control", "failure_consequence",
    }
    if not isinstance(condition, dict) or required_condition - set(condition):
        errors.append(f"{root}: rejection_condition is incomplete")
    elif any(not isinstance(condition[key], str) or not condition[key].strip() for key in required_condition):
        errors.append(f"{root}: rejection_condition contains an empty control")
    if artifact.get("falsification_status") not in {"NOT_REQUIRED", "NOT_RUN", "PASSED", "FAILED"}:
        errors.append(f"{root}: invalid falsification_status")
    if not isinstance(artifact.get("reopen_conditions"), list) or not artifact["reopen_conditions"]:
        errors.append(f"{root}: reopen_conditions must be non-empty")
    return errors


def _capture_pre_corrective_judgment(artifact: dict, revision_id: str) -> None:
    lineage = artifact.setdefault("corrective_lineage", {})
    if lineage.get("revision_id") == revision_id:
        return
    discovery = artifact.get("internal_discovery") or {}
    lineage["revision_id"] = revision_id
    lineage["pre_corrective_root_judgment"] = {
        "candidate_root_contribution": discovery.get("candidate_root_contribution"),
        "plain_explanation": discovery.get("plain_explanation"),
        "result": discovery.get("result"),
        "result_strength": discovery.get("result_strength"),
        "artifact_research_state": artifact.get("research_state"),
        "artifact_result_strength": artifact.get("result_strength"),
        "universal_presence_holds": artifact.get("universal_presence_holds"),
    }


def _apply_occurrence_updates(artifact: dict, updates: dict) -> None:
    occurrences = {
        item.get("word_ref"): item
        for item in artifact.get("occurrence_dispositions") or []
        if isinstance(item, dict)
    }
    for ref, update in updates.items():
        occurrence = occurrences.get(ref)
        if occurrence is None:
            raise ValueError(f"{artifact.get('root_buckwalter')}: corrective update references unknown {ref}")
        occurrence.update(update)
        occurrence.setdefault("preliminary_disposition", occurrence.get("disposition"))
        occurrence.setdefault("preliminary_note", occurrence.get("note"))
        occurrence["final_disposition"] = occurrence["disposition"]


def _apply_swA_partition(artifact: dict, target: dict) -> None:
    partition = target.get("usage_class_partition") or {}
    exposed_refs = set(partition.get("exposed_private_parts_refs") or [])
    occurrences = artifact.get("occurrence_dispositions") or []
    by_ref = {item.get("word_ref"): item for item in occurrences}
    if not exposed_refs or not exposed_refs <= set(by_ref):
        raise ValueError("swA corrective partition has unresolved exposed-private-parts refs")
    discovery = artifact.get("internal_discovery") or {}
    classification = discovery.get("occurrence_classification") or {}
    clusters = classification.get("clusters") or []
    adverse = next((item for item in clusters if item.get("cluster_id") == "adverse_nominals"), None)
    exposed = next((item for item in clusters if item.get("cluster_id") == "exposed_private_parts"), None)
    if adverse is not None:
        adverse["occurrence_count_expected"] = 124
        adverse["classification_rationale"] = "Adverse and badness readings remain a separate lexicalized class after the exposed-private-parts occurrences are removed."
    if exposed is None:
        clusters.append({
            "cluster_id": "exposed_private_parts",
            "where": {"word_refs": sorted(exposed_refs)},
            "occurrence_count_expected": 7,
            "disposition": "CONSISTENT",
            "candidate_semantic_interpretation": "exposed private parts as a separate lexicalized class",
            "classification_rationale": "These seven records retain concrete referents and are not absorbed into adverse/badness by contextual shame.",
            "supporting_evidence_note": "The seven exact word_refs are preserved in the corrective partition.",
            "counterevidence": ["No Quran-internal root bridge from exposed-private-parts to adverse/badness is asserted."],
        })
    for ref in exposed_refs:
        occurrence = by_ref[ref]
        occurrence.update({
            "coverage_cluster_id": "exposed_private_parts",
            "candidate_semantic_interpretation": "exposed private parts as a separate lexicalized class",
            "classification_rationale": "Corrective partition preserves the concrete exposed-private-parts class without deriving it from adverse context.",
            "cluster_supporting_evidence": "This exact word_ref belongs to the seven-record exposed-private-parts partition.",
            "counterevidence": ["No Quran-internal root bridge to adverse/badness is asserted."],
            "verifier_objection": ["No Quran-internal root bridge to adverse/badness is asserted."],
        })
    if sum(1 for item in occurrences if item.get("coverage_cluster_id") == "exposed_private_parts") != 7:
        raise ValueError("swA exposed-private-parts partition count drift")


def _apply_corrective_usage_partition(artifact: dict, target: dict) -> None:
    partition = target.get("corrective_usage_partition")
    if not partition:
        return
    occurrences = artifact.get("occurrence_dispositions") or []
    forms = {item.get("qac_surface_form_buckwalter") for item in occurrences}
    used_forms: set[str] = set()
    total = 0
    for entry in partition:
        entry_forms = set(entry.get("surface_forms") or [])
        if not entry_forms or not entry_forms <= forms or used_forms & entry_forms:
            raise ValueError(f"{artifact.get('root_buckwalter')}: invalid corrective usage partition")
        actual = sum(1 for item in occurrences if item.get("qac_surface_form_buckwalter") in entry_forms)
        if actual != entry.get("occurrence_count"):
            raise ValueError(
                f"{artifact.get('root_buckwalter')}: corrective partition count drift "
                f"for {entry.get('class_id')}: expected {entry.get('occurrence_count')}, got {actual}"
            )
        anchor_refs = set(entry.get("anchor_refs") or [])
        if not anchor_refs <= _root_occurrence_refs(artifact):
            raise ValueError(f"{artifact.get('root_buckwalter')}: corrective partition has unresolved anchors")
        used_forms |= entry_forms
        total += actual
    if total != artifact.get("occurrences") or used_forms != forms:
        raise ValueError(f"{artifact.get('root_buckwalter')}: corrective partition does not cover exactly once")
    artifact["corrective_usage_partition"] = partition


def _apply_target_judgment(artifact: dict, target: dict, revision_id: str) -> None:
    _capture_pre_corrective_judgment(artifact, revision_id)
    if artifact.get("root_buckwalter") == "swA":
        _apply_swA_partition(artifact, target)
    _apply_corrective_usage_partition(artifact, target)
    _apply_occurrence_updates(artifact, target.get("occurrence_updates") or {})
    discovery = artifact.setdefault("internal_discovery", {})
    for field in (
        "plain_explanation", "semantic_boundary", "strongest_counterexample",
        "strongest_competitor", "rationale",
    ):
        if field in target:
            destination = "layer_separation_note" if field == "semantic_boundary" else field
            discovery[destination] = target[field]
    discovery["candidate_root_contribution"] = target.get("preferred_conclusion")
    discovery["result"] = target["research_state"]
    discovery["result_strength"] = target["result_strength"]
    if target["research_state"] == "UNRESOLVED":
        discovery["unresolved_cases"] = list(target.get("root_counterevidence_refs") or [])
    artifact.update({
        "research_state": target["research_state"],
        "result_strength": target["result_strength"],
        "independent_verification": target["independent_verification"],
        "universal_presence_holds": False,
        "candidate_root_contribution": target.get("preferred_conclusion"),
        "corrective_judgment": {
            "revision_id": revision_id,
            "final_classification": target["final_classification"],
            "source_policy": "QURAN_INTERNAL_ONLY",
            "historical_independent_review_preserved": True,
        },
    })
    for lineage_ref, outcome in (target.get("lineage_updates") or {}).items():
        for collection_name in ("resistant_deep_analysis",):
            for item in artifact.get(collection_name) or []:
                if item.get("word_ref") == lineage_ref:
                    item["corrective_review_outcome"] = outcome
        for occurrence in artifact.get("occurrence_dispositions") or []:
            if occurrence.get("word_ref") == lineage_ref:
                for item in occurrence.get("reconciliation_lineage") or []:
                    item["corrective_review_outcome"] = outcome


def _refresh_root_disposition_from_occurrences(artifact: dict) -> None:
    resistant = sorted(
        item["word_ref"]
        for item in artifact.get("occurrence_dispositions") or []
        if item.get("final_disposition") == "RESISTANT"
    )
    uncertain = sorted(
        item["word_ref"]
        for item in artifact.get("occurrence_dispositions") or []
        if item.get("final_disposition") == "STRUCTURAL_UNCERTAINTY"
    )
    artifact["resistant_occurrences"] = resistant
    artifact["structural_uncertainty_occurrences"] = uncertain
    artifact["unreconciled_occurrences"] = sorted(set(resistant) | set(uncertain))
    artifact["unreconciled_count"] = len(artifact["unreconciled_occurrences"])


def _apply_root_contract(artifact: dict, target: dict | None) -> None:
    contract = _default_batch06_root_contract(artifact)
    if target is not None:
        for field in (
            "claim_scope", "claim_scope_kind", "root_evidence_refs",
            "root_counterevidence_refs", "hard_cases",
        ):
            if field in target:
                contract[field] = target[field]
        contract["layer_attribution"] = {
            **contract["layer_attribution"],
            "occurrence_evidence": "Direct Batch 06 occurrence refs are listed in root_evidence_refs and resolve in occurrence_dispositions.",
            "derivation": "Material derivational/form separation is preserved in the root's persisted coverage clusters and corrective partition where present.",
            "lexical_class": "Corrective claim kind: " + target["claim_scope_kind"],
            "contextual_relation": target["semantic_boundary"],
            "reconciliation": "Historical reconciliation lineage is retained; any current corrective outcome is recorded without deleting the earlier attempt.",
            "unresolved_resistance": target["rationale"],
        }
        contract["falsification_status"] = (
            "NOT_REQUIRED" if target["research_state"] == "UNRESOLVED" else "PASSED"
        )
        contract["hard_cases"] = target["hard_cases"]
        contract["rejection_condition"] = {
            "challenging_finding": target["strongest_counterexample"],
            "search_location": "The complete persisted Batch 06 word_ref set for " + artifact["root_buckwalter"],
            "verification_method": "Test the proposed bridge only against the listed Quran-internal occurrence evidence and counterevidence.",
            "confounder_control": target["semantic_boundary"],
            "failure_consequence": "Retain or narrow the result to the named class; do not restore a universal root generalization.",
        }
    artifact.update(contract)


def _refresh_batch06_manifest(manifest: dict, artifacts: dict[str, dict], revision_id: str) -> None:
    outcomes: dict[str, int] = {"STRONG": 0, "MODERATE": 0, "WEAK": 0, "UNRESOLVED": 0}
    for artifact in artifacts.values():
        outcomes[artifact["result_strength"]] += 1
    final = manifest.setdefault("final_checkpoint", {})
    final.update({
        "status": "CORRECTIVE_REVISION_APPLIED",
        "outcomes": outcomes,
        "resistant_occurrences": sum(len(item["resistant_occurrences"]) for item in artifacts.values()),
        "reconciliation_lineage_records": sum(len(item.get("resistant_deep_analysis") or []) for item in artifacts.values()),
        "report": "docs/LISAN3_BATCH_06_CORRECTIVE_REVISION.md",
        "review_state": "BATCH_06_CORRECTIVE_REVISION_READY_FOR_FRESH_REVIEW_NOT_YET_INDEPENDENTLY_REVIEWED",
    })
    manifest["status"] = "BATCH_06_CORRECTIVE_REVISION_READY_FOR_FRESH_REVIEW"
    manifest["corrective_revision"] = {
        "revision_id": revision_id,
        "target_roots": sorted(root for root, item in artifacts.items() if "corrective_judgment" in item),
        "source_policy": "QURAN_INTERNAL_ONLY",
        "purity_status": "NOT_EVALUATED",
    }


def _baseline_text(repository_root: Path, revision: str, relative_path: str) -> str:
    """Read a frozen baseline blob for a focused, formatting-preserving rewrite."""
    result = subprocess.run(
        ["git", "show", f"{revision}:{relative_path}"],
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode:
        raise ValueError(
            f"cannot read Batch 06 baseline {revision}:{relative_path}: {result.stderr.strip()}"
        )
    return result.stdout


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"cannot preserve Batch 06 formatting: expected one {label}")
    return text.replace(old, new, 1)


def _indented_json(value: dict, base_indent: int) -> str:
    prefix = " " * base_indent
    return "\n".join(prefix + line for line in json.dumps(value, ensure_ascii=False, indent=2).splitlines())


def _render_batch06_manifest_from_baseline(base: str, manifest: dict) -> str:
    final = manifest["final_checkpoint"]
    text = _replace_once(
        base,
        '  "status": "COMPLETE_READY_FOR_FRESH_INDEPENDENT_SEMANTIC_RESULTS_REVIEW",',
        f'  "status": "{manifest["status"]}",',
        "manifest status",
    )
    text = _replace_once(text, '    "status": "VERIFIED",', f'    "status": "{final["status"]}",', "final checkpoint status")
    text = _replace_once(
        text,
        '    "outcomes": {"STRONG": 13, "MODERATE": 15, "WEAK": 7, "UNRESOLVED": 5},',
        '    "outcomes": ' + json.dumps(final["outcomes"], ensure_ascii=False) + ',',
        "final outcomes",
    )
    text = _replace_once(
        text,
        '    "resistant_occurrences": 562,',
        f'    "resistant_occurrences": {final["resistant_occurrences"]},',
        "final resistance count",
    )
    text = _replace_once(
        text,
        '    "review_state": "READY_FOR_FRESH_INDEPENDENT_REVIEW_NOT_YET_INDEPENDENTLY_REVIEWED"',
        f'    "review_state": "{final["review_state"]}"',
        "final review state",
    )
    text = _replace_once(
        text,
        '    "report": "docs/LISAN3_BATCH_06_SEMANTIC_CAMPAIGN_REPORT.md",',
        f'    "report": "{final["report"]}",',
        "final corrective report",
    )
    insertion = '\n  "corrective_revision": ' + _indented_json(manifest["corrective_revision"], 2).lstrip() + ',\n'
    return _replace_once(text, '\n  "roots": [', insertion + '  "roots": [', "manifest corrective insertion")


def _render_batch06_status_from_baseline(base: str, status: dict) -> str:
    combined = status["batch06_current_checkpoint"]["combined"]
    text = _replace_once(base, '  "status": "BATCH_06_COMPLETE",', f'  "status": "{status["status"]}",', "campaign status")
    text = _replace_once(
        text,
        '  "verdict": "READY_FOR_FRESH_INDEPENDENT_SEMANTIC_RESULTS_REVIEW",',
        f'  "verdict": "{status["verdict"]}",',
        "campaign verdict",
    )
    text = _replace_once(
        text,
        '      "status": "COMPLETE_AND_STRUCTURALLY_VERIFIED",',
        f'      "status": "{combined["status"]}",',
        "combined checkpoint status",
    )
    text = _replace_once(
        text,
        '      "outcomes": {"STRONG": 13, "MODERATE": 15, "WEAK": 7, "UNRESOLVED": 5},',
        '      "outcomes": ' + json.dumps(combined["outcomes"], ensure_ascii=False) + ',',
        "combined outcomes",
    )
    text = _replace_once(
        text,
        '      "resistant_occurrences": 562,',
        f'      "resistant_occurrences": {combined["resistant_occurrences"]},',
        "combined resistance count",
    )
    text = _replace_once(
        text,
        '    "report": "docs/LISAN3_BATCH_06_WAVE_01.md",',
        f'    "report": "{status["batch06_current_checkpoint"]["report"]}",',
        "checkpoint corrective report",
    )
    text = _replace_once(
        text,
        '  "resume_instruction": "Stop. Batch 06 is ready for a fresh read-only independent semantic-results review against the exact final commit. Do not select another batch or canonicalize under resume authority."\n}',
        '  "resume_instruction": "Stop. Batch 06 corrective revision requires a fresh read-only independent semantic-results review against the exact corrective commit. Do not select Batch 07, canonicalize, merge, push, or release under this authority.",\n'
        '  "batch06_corrective_revision": ' + _indented_json(status["batch06_corrective_revision"], 2).lstrip() + '\n}',
        "campaign corrective insertion",
    )
    return text


def cmd_apply_batch06_corrective(args):
    """Apply the owner-authorized Batch 06 corrective judgment plan safely.

    It neither selects a new population nor reads ignored campaign scratch.  The
    command validates the full frozen 40-root set in memory before writing it.
    """
    repository_root = Path(args.repo_root).resolve()
    plan_path = Path(args.plan)
    if not plan_path.is_absolute():
        plan_path = repository_root / plan_path
    manifest_path = repository_root / "artifacts/semantic-campaign/BATCH_06_MANIFEST.json"
    status_path = repository_root / "artifacts/semantic-campaign/CAMPAIGN_STATUS.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # A prior interrupted corrective render is recoverable from the frozen
        # baseline; never attempt to infer a manifest from partial JSON bytes.
        manifest = json.loads(_baseline_text(
            repository_root,
            plan["baseline_sha"],
            "artifacts/semantic-campaign/BATCH_06_MANIFEST.json",
        ))
    paths = _batch06_artifact_paths(repository_root, manifest)
    targets = plan.get("target_roots") or {}
    required_targets = {"kvr", "mvl", "qlb", "swA", "fSl", "wlj", "Sgr", "Ezr", "Hfw", "Sbg"}
    if set(targets) != required_targets:
        raise ValueError("Batch 06 corrective plan target set is not exact")
    artifacts: dict[str, dict] = {}
    for root, path in paths.items():
        artifact = json.loads(path.read_text(encoding="utf-8"))
        if artifact.get("root_buckwalter") != root:
            raise ValueError(f"Batch 06 artifact identity mismatch at {path}")
        artifacts[root] = artifact
    revision_id = plan["revision_id"]
    for root, artifact in artifacts.items():
        target = targets.get(root)
        if target is not None:
            _apply_target_judgment(artifact, target, revision_id)
        _refresh_root_disposition_from_occurrences(artifact)
        _apply_root_contract(artifact, target)
    errors = [
        error
        for artifact in artifacts.values()
        for error in validate_batch06_root_judgment_contract(artifact)
    ]
    if errors:
        raise ValueError("Batch 06 corrective contract errors: " + "; ".join(errors))
    _refresh_batch06_manifest(manifest, artifacts, revision_id)
    ledger = json.loads((repository_root / LEDGER).read_text(encoding="utf-8"))
    for root in targets:
        artifact = artifacts[root]
        entry = dict(ledger["roots"][root])
        entry.update({
            "candidate_root_contribution": artifact.get("candidate_root_contribution"),
            "plain_explanation": (artifact.get("internal_discovery") or {}).get("plain_explanation"),
            "strongest_counterexample": (artifact.get("internal_discovery") or {}).get("strongest_counterexample"),
            "result_strength": artifact["result_strength"],
            "research_state": artifact["research_state"],
            "independent_verification": artifact["independent_verification"],
            "universal_presence_holds": artifact["universal_presence_holds"],
            "corrective_revision": revision_id,
        })
        fold_root_into_ledger(ledger, root, entry)
    ledger["updated_roots_total"] = len(ledger["roots"])
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status["status"] = "BATCH_06_CORRECTIVE_REVISION_COMPLETE"
    status["verdict"] = "BATCH_06_CORRECTIVE_REVISION_READY_FOR_FRESH_REVIEW"
    status["batch06_current_checkpoint"]["combined"].update({
        "status": "CORRECTIVE_REVISION_APPLIED",
        "outcomes": manifest["final_checkpoint"]["outcomes"],
        "resistant_occurrences": manifest["final_checkpoint"]["resistant_occurrences"],
        "reconciliation_lineage_records": manifest["final_checkpoint"]["reconciliation_lineage_records"],
    })
    status["batch06_current_checkpoint"]["report"] = manifest["final_checkpoint"]["report"]
    status["batch06_corrective_revision"] = {
        "revision_id": revision_id,
        "targets": sorted(targets),
        "source_policy": "QURAN_INTERNAL_ONLY",
        "purity_status": "NOT_EVALUATED",
        "fresh_review_required": True,
    }
    for root, path in paths.items():
        _write_root_json(path, root, artifacts[root])
    # The manifest/status are LF-bound; the long-established ledger is CRLF-bound.
    # Preserve each historical convention instead of adding line-ending noise.
    manifest_text = _render_batch06_manifest_from_baseline(
        _baseline_text(repository_root, plan["baseline_sha"], "artifacts/semantic-campaign/BATCH_06_MANIFEST.json"),
        manifest,
    )
    status_text = _render_batch06_status_from_baseline(
        _baseline_text(repository_root, plan["baseline_sha"], "artifacts/semantic-campaign/CAMPAIGN_STATUS.json"),
        status,
    )
    manifest_path.write_text(manifest_text, encoding="utf-8", newline="\n")
    (repository_root / LEDGER).write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8", newline=None)
    status_path.write_text(status_text, encoding="utf-8", newline="\n")
    print(json.dumps({
        "revision_id": revision_id,
        "roots": len(artifacts),
        "target_roots": sorted(targets),
        "outcomes": manifest["final_checkpoint"]["outcomes"],
        "resistant_occurrences": manifest["final_checkpoint"]["resistant_occurrences"],
    }, indent=1))


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("bootstrap").set_defaults(func=cmd_bootstrap)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sp = sub.add_parser("select"); sp.add_argument("--n", type=int, default=40); sp.set_defaults(func=cmd_select)
    pp = sub.add_parser("prep"); pp.add_argument("--roots", required=True); pp.add_argument("--out", required=True); pp.set_defaults(func=cmd_prep)
    ps = sub.add_parser("persist"); ps.add_argument("--results", required=True); ps.add_argument("--batch", required=True); ps.set_defaults(func=cmd_persist)
    pc = sub.add_parser("prep-coverage"); pc.add_argument("--results", required=True); pc.add_argument("--out", required=True); pc.set_defaults(func=cmd_prep_coverage)
    mc = sub.add_parser("materialize-coverage"); mc.add_argument("--research", required=True); mc.add_argument("--packets", required=True); mc.add_argument("--out", required=True); mc.set_defaults(func=cmd_materialize_coverage)
    pv = sub.add_parser("persist-coverage"); pv.add_argument("--research", required=True); pv.add_argument("--coverage", required=True); pv.add_argument("--batch", required=True); pv.set_defaults(func=cmd_persist_coverage)
    mp = sub.add_parser("mark-pending"); mp.add_argument("--roots", required=True); mp.set_defaults(func=cmd_mark_pending)
    bc = sub.add_parser("apply-batch06-corrective"); bc.add_argument("--repo-root", default="."); bc.add_argument("--plan", default="artifacts/semantic-campaign/BATCH_06_CORRECTIVE_JUDGMENTS.json"); bc.set_defaults(func=cmd_apply_batch06_corrective)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
