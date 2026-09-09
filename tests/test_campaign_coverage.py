"""Owner-correction regression tests: deterministic exact-set research coverage.

Model-reported coverage counts are never sufficient; these tests pin the
word_ref-level exact-set rules:
 1 packet/coverage input contains every confirmed word_ref exactly once
 2 a missing confirmed occurrence blocks research_completeness=COMPLETE
 3 a duplicate occurrence cannot satisfy coverage
 4 a resistant confirmed occurrence blocks universal_presence_holds
 5 research progress and canonicalization progress remain independent
 6 campaign resume preserves exact processed/remaining sets
 7 repeated persistence is idempotent
 8 reprocessing preserves lineage rather than overwriting prior evidence
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.domain.services.campaign_state import CampaignStateService
from backend.domain.services.research_coverage import (
    COMPLETENESS_COMPLETE,
    COMPLETENESS_PENDING,
    confirmed_word_refs,
    finalize_root_disposition,
    fold_root_into_ledger,
    merge_reconciliation,
    upsert_coverage_batch,
    validate_root_research_coverage,
)
from backend.infrastructure.database import Base

engine = create_engine(
    "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

SNAP = "snap_cov_test"
ROOT = "ktb"
REFS = ["2:1:1:1", "2:1:3:1", "2:2:1:1", "3:5:2:1"]  # two occurrences in verse 2:1


@pytest.fixture()
def db():
    session = SessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.add(models.CorpusSnapshot(
        id=SNAP, canonical_text_source="TANZIL_QURAN_UTHMANI",
        canonical_text_version="COV_TEST", canonical_text_hash="cafe",
        validation_status="UNVERIFIED", fixture_only=True))
    for ref in REFS:
        session.add(models.StructuralToken(
            id=f"stok_{ref.replace(':', '_')}", snapshot_id=SNAP,
            word_ref=ref, verse_ref=":".join(ref.split(":")[:2]), root=ROOT,
            form="N", source_id="TEST", source_version="v0",
            extraction_version="t1",
            attribution_status=models.StructuralAttributionStatus.CONFIRMED.value))
    # One disputed member: separately visible, never part of the confirmed set.
    session.add(models.StructuralToken(
        id="stok_disp", snapshot_id=SNAP, word_ref="9:9:1:1", verse_ref="9:9",
        root=ROOT, form="N", source_id="TEST", source_version="v0",
        extraction_version="t1",
        attribution_status=models.StructuralAttributionStatus.DISPUTED.value))
    session.commit()
    yield session
    session.close()


def _judgment(result="PREFERRED", strength="STRONG"):
    return {"result": result, "result_strength": strength,
            "candidate_root_contribution": "x"}


def test_1_confirmed_set_has_every_word_ref_exactly_once(db):
    refs = confirmed_word_refs(db, SNAP, ROOT)
    assert refs == sorted(REFS)
    assert len(refs) == len(set(refs))
    # word_ref granularity: verse 2:1 contributes TWO distinct occurrences.
    assert sum(1 for r in refs if r.startswith("2:1:")) == 2


def test_2_missing_occurrence_blocks_complete(db):
    v = validate_root_research_coverage(db, SNAP, ROOT, REFS[:-1])
    assert v.exact_set_match is False
    assert v.missing_word_refs == ("3:5:2:1",)
    disp = finalize_root_disposition(_judgment(), {"verdict": "SUPPORTED"}, v, [], [], 4)
    assert disp["research_completeness"] == COMPLETENESS_PENDING
    assert disp["universal_presence_holds"] is False


def test_3_duplicate_cannot_satisfy_coverage(db):
    # 4 records, but one is a duplicate substituting for the missing ref.
    researched = [REFS[0], REFS[0], REFS[1], REFS[2]]
    v = validate_root_research_coverage(db, SNAP, ROOT, researched)
    assert v.exact_set_match is False
    assert v.duplicate_word_refs == (REFS[0],)
    assert v.missing_word_refs == ("3:5:2:1",)
    # A verse_ref can never stand in for a word_ref either.
    v2 = validate_root_research_coverage(db, SNAP, ROOT, ["2:1", *REFS[2:]])
    assert v2.exact_set_match is False
    assert "2:1" in v2.unexpected_word_refs


def test_4_resistant_confirmed_occurrence_blocks_universal(db):
    v = validate_root_research_coverage(db, SNAP, ROOT, REFS)
    assert v.exact_set_match is True
    assert v.disputed_visible == ("9:9:1:1",)  # separately visible
    disp = finalize_root_disposition(
        _judgment(), {"verdict": "SUPPORTED"}, v, ["2:2:1:1"], [], 4)
    assert disp["universal_presence_holds"] is False
    assert disp["result_strength"] == "WEAK"
    assert disp["unreconciled_occurrences"] == ["2:2:1:1"]
    # Structural uncertainty also blocks universal presence.
    disp2 = finalize_root_disposition(
        _judgment(), {"verdict": "SUPPORTED"}, v, [], ["3:5:2:1"], 4)
    assert disp2["universal_presence_holds"] is False


def test_5_research_and_canonicalization_remain_independent(db):
    v = validate_root_research_coverage(db, SNAP, ROOT, REFS)
    disp = finalize_root_disposition(_judgment(), {"verdict": "SUPPORTED"}, v, [], [], 4)
    # A maximal research result still leaves canonicalization pending.
    assert disp["research_completeness"] == COMPLETENESS_COMPLETE
    assert disp["universal_presence_holds"] is True
    assert disp["independent_verification"] == "PASSED"
    assert disp["result_strength"] == "STRONG"
    assert disp["canonical_authorization"] == "PENDING"
    assert disp["authority_level"] == "RESEARCH_JUDGMENT"


def test_6_campaign_resume_preserves_exact_sets(db):
    CampaignStateService.initialize(
        db, campaign_id="cov-test", methodology_revision="m",
        corpus_snapshot=SNAP, queue=["a", "b", "c"])
    CampaignStateService.checkpoint_root(db, "cov-test", "b")
    with SessionLocal() as fresh:
        state = (fresh.query(models.CampaignState)
                 .filter_by(campaign_id="cov-test").one())
        assert set(state.completed_roots) == {"b"}
        assert set(state.queue) == {"a", "c"}


def test_7_repeated_persistence_is_idempotent():
    ledger = {"roots": {}}
    entry = {"batch_id": "b1", "result_strength": "STRONG",
             "research_state": "PREFERRED", "research_completeness": "COMPLETE",
             "independent_verification": "PASSED", "universal_presence_holds": True,
             "adversarial_verdict": "SUPPORTED"}
    fold_root_into_ledger(ledger, ROOT, dict(entry))
    fold_root_into_ledger(ledger, ROOT, dict(entry))  # identical re-persist
    assert "lineage" not in ledger["roots"][ROOT]  # no spurious lineage entry


def test_8_reprocessing_preserves_lineage():
    ledger = {"roots": {}}
    first = {"batch_id": "b1", "result_strength": "WEAK",
             "research_state": "PREFERRED",
             "research_completeness": "PENDING_COVERAGE_EVIDENCE",
             "independent_verification": "PARTIAL", "universal_presence_holds": False,
             "adversarial_verdict": "PARTIALLY_SUPPORTED"}
    second = {"batch_id": "b2-coverage", "result_strength": "STRONG",
              "research_state": "PREFERRED", "research_completeness": "COMPLETE",
              "independent_verification": "PASSED", "universal_presence_holds": True,
              "adversarial_verdict": "SUPPORTED"}
    fold_root_into_ledger(ledger, ROOT, first)
    fold_root_into_ledger(ledger, ROOT, second)
    entry = ledger["roots"][ROOT]
    assert entry["result_strength"] == "STRONG"
    assert len(entry["lineage"]) == 1
    assert entry["lineage"][0]["result_strength"] == "WEAK"  # prior evidence kept


# --- Owner remediation: coverage provenance hardening ------------------------


def _mapper(word_ref, disposition, note):
    return {"word_ref": word_ref, "disposition": disposition, "note": note}


def test_9_reconciliation_preserves_preliminary_disposition_and_note():
    # A RESISTANT mapper flag reconciled to CONSISTENT must keep BOTH states.
    dispositions = [
        _mapper("2:1:1:1", "CONSISTENT", "plain"),
        _mapper("2:1:3:1", "RESISTANT", "mapper flagged: residue absent here"),
    ]
    reconciliation = [{"word_ref": "2:1:3:1", "final": "CONSISTENT",
                       "rationale": "bridged via form IV causation"}]
    final, lineage = merge_reconciliation(dispositions, reconciliation)
    fin = {d["word_ref"]: d for d in final}
    reconciled = fin["2:1:3:1"]
    # final disposition intact
    assert reconciled["disposition"] == "CONSISTENT"
    assert reconciled["deep_analysis"] is True
    # preliminary disposition preserved (criterion: original flagged state kept)
    assert reconciled["preliminary_disposition"] == "RESISTANT"
    # mapper note preserved verbatim
    assert reconciled["preliminary_note"] == "mapper flagged: residue absent here"
    # reconciliation rationale intact
    assert reconciled["reconciliation_rationale"] == "bridged via form IV causation"
    # untouched occurrence carries no invented lineage fields
    assert "preliminary_disposition" not in fin["2:1:1:1"]
    # durable lineage record retains all five provenance fields, not a count
    assert lineage == [{
        "word_ref": "2:1:3:1",
        "preliminary_disposition": "RESISTANT",
        "preliminary_note": "mapper flagged: residue absent here",
        "final_disposition": "CONSISTENT",
        "reconciliation_rationale": "bridged via form IV causation",
        "deep_analysis": True,
    }]


def test_10_reconciled_to_consistent_retains_flagged_state_in_lineage():
    # The exact HIGH gap: reconciled-to-CONSISTENT must remain traceable as
    # originally flagged, both in the final disposition and the lineage record.
    dispositions = [_mapper("7:1:1:1", "STRUCTURAL_UNCERTAINTY", "segmentation unclear")]
    reconciliation = [{"word_ref": "7:1:1:1", "final": "CONSISTENT",
                       "rationale": "segmentation resolved"}]
    final, lineage = merge_reconciliation(dispositions, reconciliation)
    only = final[0]
    assert only["disposition"] == "CONSISTENT"          # final intact
    assert only["preliminary_disposition"] == "STRUCTURAL_UNCERTAINTY"
    assert only["deep_analysis"] is True
    assert lineage[0]["preliminary_disposition"] == "STRUCTURAL_UNCERTAINTY"
    assert lineage[0]["final_disposition"] == "CONSISTENT"


def test_11_duplicate_word_ref_fails_exact_set_even_when_set_equality_holds(db):
    # Every confirmed ref present exactly once EXCEPT one duplicated: set equality
    # would hold, but a duplicate must still fail coverage.
    researched = [*REFS, REFS[0]]
    v = validate_root_research_coverage(db, SNAP, ROOT, researched)
    assert v.missing_word_refs == ()
    assert v.unexpected_word_refs == ()
    assert v.duplicate_word_refs == (REFS[0],)
    assert v.exact_set_match is False           # duplicate blocks exact-set
    disp = finalize_root_disposition(_judgment(), {"verdict": "SUPPORTED"}, v, [], [], 4)
    assert disp["research_completeness"] == COMPLETENESS_PENDING


def test_12_coverage_batch_log_is_idempotent_on_replay():
    ledger = {}
    upsert_coverage_batch(ledger, "b5-coverage", ["a", "b"])
    upsert_coverage_batch(ledger, "b5-coverage", ["a", "b", "c"])  # replay
    batches = ledger["coverage_batches"]
    assert len(batches) == 1                    # no duplicate append
    assert batches[0] == {"batch_id": "b5-coverage", "roots": ["a", "b", "c"]}
    # self-heals a pre-existing duplicate log
    dirty = {"coverage_batches": [
        {"batch_id": "b4-coverage", "roots": ["x"]},
        {"batch_id": "b4-coverage", "roots": ["x"]},
    ]}
    upsert_coverage_batch(dirty, "b4-coverage", ["x"])
    assert [b["batch_id"] for b in dirty["coverage_batches"]] == ["b4-coverage"]


def test_13_final_resistant_from_merge_still_blocks_universal(db):
    # A RESISTANT that survives reconciliation still blocks universal presence,
    # and COMPLETE still requires exact confirmed coverage.
    dispositions = [_mapper(r, "CONSISTENT", "") for r in REFS]
    dispositions[2] = _mapper(REFS[2], "RESISTANT", "residue absent")
    reconciliation = [{"word_ref": REFS[2], "final": "RESISTANT",
                       "rationale": "genuine anomaly; not forced"}]
    final, _lineage = merge_reconciliation(dispositions, reconciliation)
    fin = {d["word_ref"]: d for d in final}
    assert fin[REFS[2]]["disposition"] == "RESISTANT"
    assert fin[REFS[2]]["preliminary_disposition"] == "RESISTANT"
    resistant = [r for r, d in fin.items() if d["disposition"] == "RESISTANT"]
    v = validate_root_research_coverage(db, SNAP, ROOT, [d["word_ref"] for d in dispositions])
    assert v.exact_set_match is True            # exact coverage holds
    disp = finalize_root_disposition(_judgment(), {"verdict": "SUPPORTED"}, v, resistant, [], 4)
    assert disp["universal_presence_holds"] is False   # one RESISTANT blocks it
    assert disp["research_completeness"] == COMPLETENESS_COMPLETE


def test_14_reconciliation_to_consistent_lifts_universal_block(db):
    # The FLIP side of root-unity: a preliminary RESISTANT reconciled to a FINAL
    # CONSISTENT, with exact coverage + SUPPORTED, MUST lift the block. The block
    # is driven by the FINAL disposition, never the preliminary one. (Guards
    # against sourcing final_resistant/final_uncertain from the preliminary set.)
    dispositions = [_mapper(r, "CONSISTENT", "") for r in REFS]
    dispositions[1] = _mapper(REFS[1], "RESISTANT", "mapper flag")
    reconciliation = [{"word_ref": REFS[1], "final": "CONSISTENT", "rationale": "bridged"}]
    final, _lineage = merge_reconciliation(dispositions, reconciliation)
    fin = {d["word_ref"]: d for d in final}
    # finals computed exactly as cmd_persist_coverage does (from the FINAL dict)
    final_resistant = sorted(r for r, d in fin.items() if d["disposition"] == "RESISTANT")
    final_uncertain = sorted(r for r, d in fin.items()
                             if d["disposition"] == "STRUCTURAL_UNCERTAINTY")
    assert final_resistant == [] and final_uncertain == []
    v = validate_root_research_coverage(db, SNAP, ROOT, [d["word_ref"] for d in dispositions])
    disp = finalize_root_disposition(
        _judgment(), {"verdict": "SUPPORTED"}, v, final_resistant, final_uncertain, 4)
    assert disp["universal_presence_holds"] is True    # block lifted by reconciliation
    assert disp["result_strength"] == "STRONG"
    assert disp["canonical_authorization"] == "PENDING"   # research != canonical


def _run_persist_coverage(tmp_path, monkeypatch, coverage, verdict="SUPPORTED"):
    """Invoke the real cmd_persist_coverage against the in-memory fixture DB."""
    import json as _json

    import tools.campaign as camp

    monkeypatch.setattr(camp, "_Session", SessionLocal)
    monkeypatch.setattr(camp, "SNAP", SNAP)
    monkeypatch.setattr(camp, "LEDGER", tmp_path / "ledger.json")
    monkeypatch.setattr(camp, "ROOT_ARTIFACTS", tmp_path / "roots")
    research = [{"root": ROOT, "judgment": _judgment(),
                 "verdict": {"verdict": verdict}}]
    rf = tmp_path / "research.json"
    rf.write_text(_json.dumps(research), encoding="utf-8")
    cf = tmp_path / "coverage.json"
    cf.write_text(_json.dumps(coverage), encoding="utf-8")
    ns = type("Args", (), {"research": str(rf), "coverage": str(cf),
                           "batch": "b5-coverage"})()
    camp.cmd_persist_coverage(ns)
    art = _json.loads((tmp_path / "roots" / "ktb.json").read_text(encoding="utf-8"))
    ledger = _json.loads((tmp_path / "ledger.json").read_text(encoding="utf-8"))
    return camp, ns, art, ledger


def test_15_persist_coverage_persists_preliminary_and_lifts_block(tmp_path, monkeypatch, db):
    # End-to-end through the actual command: a preliminary RESISTANT reconciled to
    # CONSISTENT must (a) be persisted with its preliminary state in the artifact,
    # and (b) have its universal-presence block lifted.
    coverage = [{"root": ROOT, "dispositions": [
        _mapper("2:1:1:1", "CONSISTENT", "a"),
        _mapper("2:1:3:1", "RESISTANT", "mapper flagged: absent"),
        _mapper("2:2:1:1", "CONSISTENT", "c"),
        _mapper("3:5:2:1", "CONSISTENT", "d"),
    ], "reconciliation": [
        {"word_ref": "2:1:3:1", "final": "CONSISTENT", "rationale": "bridged via causation"},
    ]}]
    camp, ns, art, _ledger = _run_persist_coverage(tmp_path, monkeypatch, coverage)
    recon = {d["word_ref"]: d for d in art["occurrence_dispositions"]}["2:1:3:1"]
    # (a) preliminary preserved in the PERSISTED artifact (not just the helper)
    assert recon["disposition"] == "CONSISTENT"
    assert recon["preliminary_disposition"] == "RESISTANT"
    assert recon["preliminary_note"] == "mapper flagged: absent"
    assert recon["reconciliation_rationale"] == "bridged via causation"
    lin = art["resistant_deep_analysis"]
    assert lin[0]["preliminary_disposition"] == "RESISTANT"
    assert lin[0]["final_disposition"] == "CONSISTENT"        # lineage, not a count
    # (b) block lifted; exact coverage; canonical still pending
    assert art["coverage_validation"]["exact_set_match"] is True
    assert art["universal_presence_holds"] is True
    assert art["research_completeness"] == COMPLETENESS_COMPLETE
    assert art["canonical_authorization"] == "PENDING"
    # replay is idempotent at the batch-log level (no duplicate coverage_batches)
    camp.cmd_persist_coverage(ns)
    import json as _json
    replayed = _json.loads((tmp_path / "ledger.json").read_text(encoding="utf-8"))
    assert [b["batch_id"] for b in replayed["coverage_batches"]] == ["b5-coverage"]


def test_16_persist_coverage_duplicate_researched_ref_blocks_complete(tmp_path, monkeypatch, db):
    # The command must validate on the PRE-merge researched list: a duplicated
    # researched ref (which merge_reconciliation's dict-collapse would hide) must
    # still fail exact-set and block COMPLETE.
    coverage = [{"root": ROOT, "dispositions": [
        _mapper("2:1:1:1", "CONSISTENT", "a"),
        _mapper("2:1:1:1", "CONSISTENT", "dup"),   # duplicate of a confirmed ref
        _mapper("2:1:3:1", "CONSISTENT", "b"),
        _mapper("2:2:1:1", "CONSISTENT", "c"),
        _mapper("3:5:2:1", "CONSISTENT", "d"),
    ], "reconciliation": []}]
    _camp, _ns, art, _ledger = _run_persist_coverage(tmp_path, monkeypatch, coverage)
    assert art["coverage_validation"]["duplicate_word_refs"] == ["2:1:1:1"]
    assert art["coverage_validation"]["exact_set_match"] is False
    assert art["research_completeness"] == COMPLETENESS_PENDING
    assert art["universal_presence_holds"] is False


# --- Owner remediation: cross-lens root unity (Window 03 integrity fix) -------


def test_17_unresolved_discovery_blocks_universal_presence(db):
    # A root whose single unifying contribution was never established (discovery
    # result UNRESOLVED) cannot be universal-present, even with a SUPPORTED
    # adversarial verdict, exact coverage, and zero coverage-mapped RESISTANT.
    # Guards the contradiction that surfaced on root Anf: research_state=UNRESOLVED
    # must NEVER coexist with universal_presence_holds=True / verification=PASSED.
    v = validate_root_research_coverage(db, SNAP, ROOT, REFS)
    assert v.exact_set_match is True
    disp = finalize_root_disposition(
        _judgment(result="UNRESOLVED", strength="UNRESOLVED"),
        {"verdict": "SUPPORTED"}, v, [], [], 4)
    assert disp["research_state"] == "UNRESOLVED"
    assert disp["universal_presence_holds"] is False
    assert disp["independent_verification"] != "PASSED"


def test_18_discovery_inconsistent_ref_blocks_universal_and_is_reported(db):
    # ROOT_SEMANTIC_UNITY is cross-lens: an occurrence the internal discoverer
    # could not reconcile (presence.inconsistent_refs) blocks universal presence
    # AND surfaces in unreconciled_occurrences — even when the coverage mapper
    # marked it CONSISTENT (0 final_resistant) and the verdict is SUPPORTED.
    v = validate_root_research_coverage(db, SNAP, ROOT, REFS)
    judgment = {"result": "PREFERRED", "result_strength": "STRONG",
                "candidate_root_contribution": "x",
                "presence": {"inconsistent_refs": ["3:5:2:1"]}}
    disp = finalize_root_disposition(judgment, {"verdict": "SUPPORTED"}, v, [], [], 4)
    assert disp["universal_presence_holds"] is False
    assert "3:5:2:1" in disp["unreconciled_occurrences"]
    assert disp["unreconciled_count"] == 1
