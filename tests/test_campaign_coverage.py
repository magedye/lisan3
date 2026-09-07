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
