import hashlib

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain.models import CorpusOccurrence
from backend.domain.services.corpus.importer import CorpusImporter
from backend.domain.services.corpus.qac import QACAdapter
from backend.domain.services.corpus.tanzil import TanzilAdapter
from backend.infrastructure.database import Base

# Setup mock DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def test_tanzil_adapter_hash_validation():
    raw = "1|1|بِسْمِ اللَّهِ\n"
    # Expected hash of `raw`
    expected_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    # Should succeed
    adapter = TanzilAdapter(expected_hash=expected_hash)
    data = adapter.parse_corpus(raw)
    assert len(data) == 1
    assert data[0]["verse_ref"] == "1:1"

    # Should fail
    adapter = TanzilAdapter(expected_hash="wronghash")
    with pytest.raises(ValueError):
        adapter.parse_corpus(raw)


def test_qac_adapter_semantic_quarantine():
    # Example QAC line with both morphological and semantic fields
    # QAC uses 4 parts. The last part is a colon-separated feature list.
    raw = "(1:1:1:1)|bis'mi|N|POS:N|ROOT:smw|LEM:ism|SEM:NAME|ONTOLOGY:Concept"
    adapter = QACAdapter()
    data = adapter.parse_corpus(raw)

    assert len(data) == 1
    features = data[0]["features"].split(":")
    assert any(f.startswith("POS") for f in features)
    assert any(f.startswith("ROOT") for f in features)
    assert any(f.startswith("LEM") for f in features)
    # Semantic tags MUST be stripped
    assert not any(f.startswith("SEM") for f in features)
    assert not any(f.startswith("ONTOLOGY") for f in features)


def test_corpus_importer_integration():
    db = TestingSessionLocal()
    tanzil_raw = "1|1|بِسْمِ اللَّهِ\n"
    qac_raw = "(1:1:1:1)|bis'mi|N|POS:N|ROOT:smw"

    snapshot = CorpusImporter.import_corpus_snapshot(db, tanzil_raw, qac_raw)

    assert snapshot.canonical_text_source == "TANZIL_QURAN_UTHMANI"
    assert snapshot.structural_source == "QAC_MORPHOLOGY_SYNTAX"

    occurrences = db.query(CorpusOccurrence).filter_by(snapshot_id=snapshot.id).all()
    assert len(occurrences) == 1
    assert occurrences[0].verse_ref == "1:1"
    assert occurrences[0].text == "بِسْمِ اللَّهِ"

    db.close()
