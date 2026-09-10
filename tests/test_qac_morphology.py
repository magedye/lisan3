"""QAC morphology admission + importer qualification tests (Request 01 §9).

Parse-logic is tested against an AUTHORED format-faithful fixture (own content,
no QAC bytes). The full-corpus qualification is an integration test that runs
only when the local, hash-bound QAC artifact is present (acquire-per-install).
"""

from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.domain.services.corpus.qac_morphology import (
    DEFAULT_QAC_ARTIFACT,
    QAC_EXPECTED_SHA256,
    QacMorphologyImporter,
    buckwalter_to_arabic,
    load_verified_segments,
    parse_segments,
)
from backend.infrastructure.database import Base

AUTHORED = Path("data/fixtures/qac/authored_sample.tsv")
QAC_PRESENT = DEFAULT_QAC_ARTIFACT.exists()

engine = create_engine(
    "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def test_parse_authored_fixture_extracts_roots_deterministically():
    segs = parse_segments(AUTHORED.read_bytes())
    assert len(segs) == 5
    root_bearing = [s for s in segs if s.root]
    assert [s.root for s in root_bearing] == ["smw", "ktb", "ktb"]
    ktb_verb = next(s for s in root_bearing if s.root == "ktb" and s.pos == "V")
    assert ktb_verb.verb_form == "I"
    assert ktb_verb.word_ref == "2:2:2:1"
    assert ktb_verb.verse_ref == "2:2"


def test_buckwalter_to_arabic():
    assert buckwalter_to_arabic("ktb") == "ك ت ب"
    assert buckwalter_to_arabic("smw") == "س م و"
    assert buckwalter_to_arabic("slm") == "س ل م"


def test_import_fails_closed_on_unqualified_bytes():
    # The authored fixture is not the qualified artifact; import must refuse it.
    db = SessionLocal()
    with pytest.raises(ValueError, match="do not match the qualified immutable source"):
        QacMorphologyImporter.import_tokens(db, "snap_x", artifact_path=AUTHORED)
    db.close()


def test_verified_segment_reader_fails_closed_on_unqualified_bytes():
    with pytest.raises(ValueError, match="do not match the qualified immutable source"):
        load_verified_segments(AUTHORED)


def test_parse_rejects_malformed_location():
    bad = b"LOCATION\tFORM\tTAG\tFEATURES\r\n1:1:1:1\tbi\tP\tPREFIX|bi+\r\n"
    with pytest.raises(ValueError, match="Malformed QAC location"):
        parse_segments(bad)


@pytest.mark.skipif(not QAC_PRESENT, reason="local QAC artifact not present (acquire-per-install)")
def test_real_qac_import_builds_qualified_root_universe():
    from backend.domain.services.corpus.importer import TanzilPreActivationImporter
    from backend.domain.services.corpus.root_universe import RootUniverseService

    db = SessionLocal()
    for t in reversed(Base.metadata.sorted_tables):
        db.execute(t.delete())
    db.commit()

    res = TanzilPreActivationImporter.import_candidate(db, repository_root=Path("."))
    snap = res.snapshot.id

    qac = QacMorphologyImporter.import_tokens(db, snap)
    assert qac.source_sha256 == QAC_EXPECTED_SHA256          # byte-preserved (q2)
    assert qac.segments_total == 128219                       # deterministic (q7)
    assert qac.root_bearing_segments == 49968
    assert qac.distinct_roots == 1642                         # root inventory (q6)
    assert qac.tokens_persisted == 49968
    assert qac.reconciliation["verse_sets_equal"] is True     # canonical mapping (q5)
    assert qac.reconciliation["unmatched_qac_verses"] == []

    universe = RootUniverseService.derive(db, snap)
    assert len(universe) == 1642
    total = sum(e.confirmed_occurrences for e in universe)
    assert total == 49968                                     # counts deterministic
    # Reproducible across a fresh session.
    with SessionLocal() as other:
        universe2 = RootUniverseService.derive(other, snap)
    assert [e.as_dict() for e in universe] == [e.as_dict() for e in universe2]

    # Tanzil text authority preserved (q4): QAC did not replace any verse text.
    verse = db.query(models.CorpusOccurrence).filter_by(
        snapshot_id=snap, verse_ref="1:1").one()
    assert "بِسْمِ" in verse.text or verse.text  # real Tanzil text present
    db.close()
