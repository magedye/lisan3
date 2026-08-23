import uuid

from sqlalchemy.orm import Session

from backend.domain.models import CorpusOccurrence, CorpusSnapshot
from backend.domain.services.corpus.alignment import CrossSourceAligner
from backend.domain.services.corpus.qac import QACAdapter
from backend.domain.services.corpus.tanzil import TanzilAdapter


class CorpusImporter:
    """
    Orchestrates the admission and mapping of canonical corpus sources into
    the Lisan relational persistence model.
    """

    @staticmethod
    def import_corpus_snapshot(
        db: Session, tanzil_raw: str, qac_raw: str, expected_tanzil_hash: str = None
    ) -> CorpusSnapshot:
        # 1. Parse Sources
        tanzil_adapter = TanzilAdapter(expected_hash=expected_tanzil_hash)
        tanzil_data = tanzil_adapter.parse_corpus(tanzil_raw)

        qac_adapter = QACAdapter()
        qac_data = qac_adapter.parse_corpus(qac_raw)

        # 2. Align Sources
        aligned_data = CrossSourceAligner.align_sources(tanzil_data, qac_data)

        # 3. Create Snapshot
        snapshot_id = f"snap_{uuid.uuid4().hex[:8]}"
        text_hash = expected_tanzil_hash or "UNKNOWN"
        val_status = "VALIDATED" if text_hash not in (None, "", "UNKNOWN", "placeholder", "synthetic", "unverified") else "UNVERIFIED"

        snapshot = CorpusSnapshot(
            id=snapshot_id,
            canonical_text_source="TANZIL_QURAN_UTHMANI",
            canonical_text_version="v1.0.2",
            canonical_text_hash=text_hash,
            structural_source="QAC_MORPHOLOGY_SYNTAX",
            structural_source_version="v0.4",
            import_revision="v1",
            validation_status=val_status,
        )
        db.add(snapshot)

        # 4. Insert Occurrences
        for verse in aligned_data:
            # We store the raw text in `CorpusOccurrence`.
            # In a full implementation, `structural_tokens` would be parsed into `ObservationArtifact` stubs or a dedicated table.
            occ = CorpusOccurrence(
                id=f"occ_{uuid.uuid4().hex[:8]}",
                snapshot_id=snapshot_id,
                verse_ref=verse["verse_ref"],
                text=verse["text"],
                # Depending on schema, we might serialize structural_tokens into a JSON column.
                # Since CorpusOccurrence schema currently only has text and verse_ref, we stop here.
            )
            db.add(occ)

        db.commit()
        db.refresh(snapshot)
        return snapshot
