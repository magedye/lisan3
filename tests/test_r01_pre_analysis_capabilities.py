"""Owner Request 01 — pre-analysis capability qualification tests.

Covers the persistence and services added for full pre-analysis readiness:
 - persisted, reusable Root Descriptive Profile over StructuralToken rows;
 - four distinct knowledge levels;
 - deterministic Root Universe derivation + coverage + holdout;
 - unified external-hypothesis register (6 claim types, no authority bonus,
   RULE_CLAIM vs AUTHOR_APPLICATION);
 - durable campaign checkpoint/resume.
"""


import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.domain.services.campaign_state import CampaignStateService
from backend.domain.services.corpus.descriptive_profile import (
    ATTR_CONFIRMED,
    ATTR_DISPUTED,
    ATTR_UNRESOLVED,
    KnowledgeLevel,
    RootDescriptiveProfileService,
)
from backend.domain.services.corpus.root_universe import RootUniverseService
from backend.domain.services.corpus.structural_import import (
    DEFAULT_SLM_FIXTURE,
    StructuralFixtureLoader,
)
from backend.domain.services.external_hypothesis import ExternalHypothesisService
from backend.infrastructure.database import Base

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(engine)

SNAP = "snap_struct_fixture"


@pytest.fixture()
def db():
    session = SessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.add(
        models.CorpusSnapshot(
            id=SNAP,
            canonical_text_source="TANZIL_QURAN_UTHMANI",
            canonical_text_version="TEST_FIXTURE_STRUCT",
            canonical_text_hash="deadbeef",
            validation_status="UNVERIFIED",
            fixture_only=True,
        )
    )
    session.commit()
    yield session
    session.close()


def _add_token(session, root, word_ref, verse_ref, form, status):
    session.add(
        models.StructuralToken(
            id=f"stok_{word_ref.replace(':', '_')}_{status}",
            snapshot_id=SNAP,
            word_ref=word_ref,
            verse_ref=verse_ref,
            root=root,
            form=form,
            source_id="TEST_STRUCT",
            source_version="v0",
            extraction_version="test-v1",
            attribution_status=status,
        )
    )


# --------------------------------------------------------------------------- #
# Persisted, reusable Root Descriptive Profile.
# --------------------------------------------------------------------------- #
def test_slm_fixture_loads_and_profile_is_reusable_and_reproducible(db):
    assert DEFAULT_SLM_FIXTURE.exists(), "qualified structural fixture must be tracked"
    result = StructuralFixtureLoader.load_slm_fixture(db, SNAP)
    assert result.rows_processed > 0
    assert result.roots == ("س ل م",)
    # Persisted rows equal the fixture row count.
    persisted = db.query(models.StructuralToken).filter_by(snapshot_id=SNAP).count()
    assert persisted == result.rows_processed

    # A profile is retrieved (not recomputed by an LLM) from persisted rows.
    profile = RootDescriptiveProfileService.build_from_snapshot(db, SNAP, "س ل م")
    assert profile is not None
    assert profile.total_confirmed_occurrences == result.rows_processed
    assert profile.source_id == "QAC_MORPHOLOGY_WEB_V0_4_FIXTURE"
    assert profile.extraction_version == "slm-fixture-v1"
    assert "NO_LLM" in profile.extraction_method
    assert profile.forms  # form groups present

    # Reproducible: a fresh session over the same persisted rows is identical.
    with SessionLocal() as other:
        again = RootDescriptiveProfileService.build_from_snapshot(other, SNAP, "س ل م")
    assert again.as_dict() == profile.as_dict()

    # Idempotent re-load does not duplicate rows (deterministic ids + merge).
    StructuralFixtureLoader.load_slm_fixture(db, SNAP)
    assert (
        db.query(models.StructuralToken).filter_by(snapshot_id=SNAP).count()
        == persisted
    )


def test_four_knowledge_levels_are_distinct(db):
    _add_token(db, "ك ت ب", "2:1:1", "2:1", "FORM_I_VERB", ATTR_CONFIRMED)
    _add_token(db, "ك ت ب", "2:2:1", "2:2", "NOUN", ATTR_DISPUTED)
    _add_token(db, "ك ت ب", "2:3:1", "2:3", "NOUN", ATTR_UNRESOLVED)
    db.commit()

    profile = RootDescriptiveProfileService.build_from_snapshot(db, SNAP, "ك ت ب")
    assert profile.total_confirmed_occurrences == 1
    assert profile.total_eligible_occurrences == 3
    assert [d["word_ref"] for d in profile.disputed_annotations] == ["2:2:1"]
    assert [d["word_ref"] for d in profile.unresolved_annotations] == ["2:3:1"]
    # The four levels are defined and semantically distinct.
    assert len(set(KnowledgeLevel)) == 4
    levels = set(profile.knowledge_levels.values())
    # Confirmed root membership/counts are qualified structural annotations; the
    # two uncertainty buckets carry their own distinct levels.
    assert KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value in levels
    assert KnowledgeLevel.DISPUTED_STRUCTURAL_ANNOTATION.value in levels
    assert KnowledgeLevel.UNRESOLVED_STRUCTURAL_ANNOTATION.value in levels
    # A root-scoped profile must NOT mislabel any structural field as a direct
    # textual fact (the corrected invariant from Phase 0B review).
    assert KnowledgeLevel.DIRECT_TEXTUAL_FACT.value not in levels


def test_build_from_snapshot_does_not_double_count_across_extraction_versions(db):
    # The same word_ref under two extraction versions must not inflate the count.
    for version in ("test-v1", "test-v2"):
        db.add(
            models.StructuralToken(
                id=f"stok_dup_{version}",
                snapshot_id=SNAP,
                word_ref="9:9:9",
                verse_ref="9:9",
                root="د و ب",
                form="NOUN",
                source_id="TEST_STRUCT",
                source_version="v0",
                extraction_version=version,
                attribution_status=ATTR_CONFIRMED,
            )
        )
    db.commit()
    profile = RootDescriptiveProfileService.build_from_snapshot(db, SNAP, "د و ب")
    assert profile.total_confirmed_occurrences == 1
    assert profile.occurrence_refs == ("9:9:9",)
    assert profile.extraction_version == "test-v2"  # latest chosen deterministically


def test_holdout_guarantees_signal_for_small_roots():
    _train, hold = RootUniverseService.holdout_split(["2:1:1", "2:2:1"])
    assert len(hold) == 1  # >=2 occurrences -> at least one held out
    assert RootUniverseService.holdout_available(["2:1:1", "2:2:1"]) is True
    # A singleton cannot support a holdout.
    _train1, hold1 = RootUniverseService.holdout_split(["2:1:1"])
    assert hold1 == ()
    assert RootUniverseService.holdout_available(["2:1:1"]) is False


# --------------------------------------------------------------------------- #
# Root Universe + coverage + holdout.
# --------------------------------------------------------------------------- #
def test_root_universe_derivation_and_coverage_and_holdout(db):
    StructuralFixtureLoader.load_slm_fixture(db, SNAP)
    _add_token(db, "ع ل م", "3:1:1", "3:1", "NOUN", ATTR_CONFIRMED)
    db.commit()

    universe = RootUniverseService.derive(db, SNAP)
    roots = [e.root for e in universe]
    assert roots == sorted(roots)  # deterministic ordering
    assert {"س ل م", "ع ل م"} <= set(roots)
    slm = next(e for e in universe if e.root == "س ل م")
    assert slm.confirmed_occurrences > 1
    assert slm.distinct_forms >= 1
    assert set(slm.priority_dimensions) == {
        "occurrence_count",
        "form_diversity",
        "surah_spread",
        "structural_uncertainty",
    }
    alm = next(e for e in universe if e.root == "ع ل م")
    assert alm.is_singleton is True

    # Deterministic occurrence coverage: missing one eligible ref -> not complete.
    profile = RootDescriptiveProfileService.build_from_snapshot(db, SNAP, "س ل م")
    all_refs = set(profile.occurrence_refs)
    full = RootUniverseService.occurrence_coverage(db, SNAP, "س ل م", all_refs)
    assert full.complete is True
    partial = RootUniverseService.occurrence_coverage(
        db, SNAP, "س ل م", set(list(all_refs)[:-1])
    )
    assert partial.complete is False
    assert len(partial.missing_refs) == 1

    # Deterministic holdout split (no randomness).
    train1, hold1 = RootUniverseService.holdout_split(list(all_refs))
    train2, hold2 = RootUniverseService.holdout_split(list(all_refs))
    assert (train1, hold1) == (train2, hold2)
    assert set(train1).isdisjoint(hold1)
    assert set(train1) | set(hold1) == all_refs


# --------------------------------------------------------------------------- #
# Unified external-hypothesis register.
# --------------------------------------------------------------------------- #
def test_external_hypothesis_register_all_claim_types_no_authority_bonus(db):
    for claim_type in models.ExternalClaimType:
        rec = ExternalHypothesisService.register(
            db,
            claim_type=claim_type.value,
            source="src",
            author="auth",
            claim="c",
            target_scope="ك ت ب",
            provenance="external:auth",
        )
        assert rec.status == "EXTERNAL_CANDIDATE"
    # The register carries NO confidence/authority field at all.
    columns = {c.name for c in models.ExternalHypothesisRecord.__table__.columns}
    assert not any(
        tok in name
        for name in columns
        for tok in ("confidence", "bonus", "authority", "canonical")
    )


def test_jabal_is_high_priority_hypothesis_not_authority(db):
    rec = ExternalHypothesisService.register_jabal_root_meaning(
        db, root="س ل م", claim="المعنى المحوري: ..."
    )
    assert rec.claim_type == "ROOT_MEANING_CANDIDATE"
    assert rec.claim_role == "RULE_CLAIM"  # rule vs application kept separate
    assert rec.status == "EXTERNAL_CANDIDATE"
    assert "جبل" in rec.author
    # Jabal can be tested and even falsified — never canonized.
    tested = ExternalHypothesisService.record_test_result(
        db, rec.id, status="FALSIFIED", result="fails at one occurrence"
    )
    assert tested.status == "FALSIFIED"


def test_external_hypothesis_rejects_unknown_claim_type(db):
    with pytest.raises(ValueError, match="claim_type"):
        db.add(
            models.ExternalHypothesisRecord(
                id="exh_bad",
                claim_type="SEMANTIC_AUTHORITY",
                source="s",
                author="a",
                claim="c",
                target_scope="x",
                claim_role="RULE_CLAIM",
                status="EXTERNAL_CANDIDATE",
                provenance="p",
            )
        )
        db.flush()


# --------------------------------------------------------------------------- #
# Campaign checkpoint / resume.
# --------------------------------------------------------------------------- #
def test_campaign_state_checkpoints_and_resumes_without_context(db):
    CampaignStateService.initialize(
        db,
        campaign_id="calib-1",
        methodology_revision="method-current",
        corpus_snapshot=SNAP,
        queue=["ك ت ب", "س ل م", "ع ل م"],
    )
    CampaignStateService.checkpoint_root(db, "calib-1", "ك ت ب", findings=["F1"])

    # Simulate a fresh session/runtime: resume reads only the durable row.
    with SessionLocal() as other:
        resume = CampaignStateService.resume(other, "calib-1")
    assert resume.completed_count == 1
    assert resume.remaining_count == 2
    assert resume.next_root == "س ل م"
    assert resume.status == "IN_PROGRESS"

    CampaignStateService.checkpoint_root(db, "calib-1", "س ل م")
    CampaignStateService.checkpoint_root(db, "calib-1", "ع ل م")
    final = CampaignStateService.resume(db, "calib-1")
    assert final.status == "COMPLETE"
    assert final.remaining_count == 0
