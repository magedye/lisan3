import datetime
import hashlib
import uuid
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.orm import Session

from backend.domain.models import CorpusOccurrence, CorpusSnapshot
from backend.domain.services.corpus.alignment import CrossSourceAligner
from backend.domain.services.corpus.authority import (
    ARTIFACT_PRESENT,
    ARTIFACT_VERIFICATION_PENDING,
    CANON_001_ARTIFACT_IDENTITY_MATCH_CONFIRMED,
    CANONICAL_ACTIVATION_PENDING,
    HASH_VERIFIED,
    IMPORT_VALIDATED,
    get_canonical_admission,
)
from backend.domain.services.corpus.qac import QACAdapter
from backend.domain.services.corpus.tanzil import TanzilAdapter, TanzilArtifactParser

TANZIL_IMPORT_REVISION = "tanzil-one-verse-per-line-v1"
TANZIL_PROVENANCE = (
    "docs/canonical/ADMISSION_TANZIL.md#artifact-provenance"
)


@dataclass(frozen=True)
class TanzilImportResult:
    snapshot: CorpusSnapshot
    occurrence_count: int
    created: bool


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
        actual_text_hash = hashlib.sha256(tanzil_raw.encode("utf-8")).hexdigest()
        admission = get_canonical_admission("TANZIL_QURAN_UTHMANI")
        if admission is None:
            raise ValueError("Tanzil has no canonical admission record")

        snapshot = CorpusSnapshot(
            id=snapshot_id,
            canonical_text_source="TANZIL_QURAN_UTHMANI",
            canonical_text_version=f"TEST_FIXTURE_{snapshot_id}",
            canonical_text_hash=actual_text_hash,
            structural_source="QAC_MORPHOLOGY_SYNTAX",
            structural_source_version="v0.4",
            import_revision="v1",
            validation_status="UNVERIFIED",
            source_role_status=admission.source_role_status,
            artifact_presence_status=ARTIFACT_PRESENT,
            expected_canonical_text_hash=None,
            hash_verification_status=ARTIFACT_VERIFICATION_PENDING,
            import_validation_status="IMPORT_PENDING",
            activation_status=CANONICAL_ACTIVATION_PENDING,
            artifact_provenance="TEST_FIXTURE_INPUT",
            fixture_only=True,
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


class TanzilPreActivationImporter:
    """Persist the authority-bound Tanzil artifact without activating it."""

    @staticmethod
    def _repository_root() -> Path:
        return Path(__file__).resolve().parents[4]

    @staticmethod
    def _authority_path(repository_root: Path, reference: str | None) -> Path:
        if not reference:
            raise ValueError("Tanzil authority is missing an artifact reference")
        root = repository_root.resolve()
        path = (root / Path(reference)).resolve()
        if path != root and root not in path.parents:
            raise ValueError("Tanzil authority reference escapes the repository root")
        return path

    @staticmethod
    def _read_required(path: Path, label: str) -> bytes:
        try:
            return path.read_bytes()
        except FileNotFoundError as exc:
            raise ValueError(f"Required Tanzil {label} is missing: {path}") from exc

    @staticmethod
    def _snapshot_id(version: str, artifact_hash: str) -> str:
        normalized_version = version.replace(".", "_")
        return f"snap_tanzil_{normalized_version}_{artifact_hash[:12]}"

    @classmethod
    def import_candidate(
        cls,
        db: Session,
        *,
        repository_root: Path | None = None,
    ) -> TanzilImportResult:
        admission = get_canonical_admission("TANZIL_QURAN_UTHMANI")
        if admission is None:
            raise ValueError("Tanzil has no canonical admission record")
        if admission.canonical_text_version is None or admission.expected_hash is None:
            raise ValueError("Tanzil authority has no bound version/hash")

        root = (repository_root or cls._repository_root()).resolve()
        artifact_path = cls._authority_path(root, admission.artifact_reference)
        index_path = cls._authority_path(root, admission.identity_index_reference)
        raw_bytes = cls._read_required(artifact_path, "artifact")
        index_bytes = cls._read_required(index_path, "identity index")
        parsed = TanzilArtifactParser(admission).parse(raw_bytes, index_bytes)
        snapshot_id = cls._snapshot_id(
            admission.canonical_text_version, parsed.actual_sha256
        )

        existing = db.get(CorpusSnapshot, snapshot_id)
        if existing is not None:
            cls._verify_existing(db, existing, parsed.verses)
            return TanzilImportResult(existing, len(parsed.verses), False)

        conflicting = (
            db.query(CorpusSnapshot)
            .filter(
                CorpusSnapshot.canonical_text_source == admission.source_id,
                CorpusSnapshot.canonical_text_version
                == admission.canonical_text_version,
                CorpusSnapshot.canonical_text_hash == parsed.actual_sha256,
            )
            .first()
        )
        if conflicting is not None:
            raise ValueError(
                "Authority-bound Tanzil artifact already has a competing snapshot identity"
            )

        verified_at = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        snapshot = CorpusSnapshot(
            id=snapshot_id,
            canonical_text_source=admission.source_id,
            canonical_text_version=admission.canonical_text_version,
            canonical_text_hash=parsed.actual_sha256,
            structural_source=None,
            structural_source_version=None,
            import_revision=TANZIL_IMPORT_REVISION,
            validation_status="PENDING",
            source_role_status=admission.source_role_status,
            artifact_presence_status=ARTIFACT_PRESENT,
            expected_canonical_text_hash=admission.expected_hash,
            hash_verification_status=HASH_VERIFIED,
            import_validation_status=IMPORT_VALIDATED,
            activation_status=CANONICAL_ACTIVATION_PENDING,
            artifact_provenance=TANZIL_PROVENANCE,
            artifact_reference=admission.artifact_reference,
            artifact_size_bytes=parsed.artifact_size_bytes,
            artifact_format=admission.artifact_format,
            artifact_verified_at=verified_at,
            artifact_verification_revision=admission.verification_revision,
            identity_index_reference=admission.identity_index_reference,
            identity_index_sha256=parsed.identity_index_sha256,
            verse_count=len(parsed.verses),
            canon_001_reconciliation=(
                CANON_001_ARTIFACT_IDENTITY_MATCH_CONFIRMED
            ),
            fixture_only=False,
            created_at=verified_at,
        )
        db.add(snapshot)
        for verse in parsed.verses:
            db.add(
                CorpusOccurrence(
                    id=(
                        f"occ_tanzil_{admission.canonical_text_version.replace('.', '_')}"
                        f"_{verse.surah:03d}_{verse.ayah:03d}"
                    ),
                    snapshot_id=snapshot_id,
                    expression="",
                    verse_ref=verse.verse_ref,
                    text=verse.text,
                    created_at=verified_at,
                )
            )
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
        db.refresh(snapshot)
        return TanzilImportResult(snapshot, len(parsed.verses), True)

    @classmethod
    def _verify_existing(cls, db: Session, snapshot, verses) -> None:
        admission = get_canonical_admission("TANZIL_QURAN_UTHMANI")
        assert admission is not None
        version = admission.canonical_text_version
        if version is None:
            raise ValueError("Tanzil authority has no bound version")
        expected_snapshot = {
            "canonical_text_source": admission.source_id,
            "canonical_text_version": admission.canonical_text_version,
            "canonical_text_hash": admission.expected_hash,
            "source_role_status": admission.source_role_status,
            "artifact_presence_status": ARTIFACT_PRESENT,
            "expected_canonical_text_hash": admission.expected_hash,
            "hash_verification_status": HASH_VERIFIED,
            "import_validation_status": IMPORT_VALIDATED,
            "activation_status": CANONICAL_ACTIVATION_PENDING,
            "artifact_provenance": TANZIL_PROVENANCE,
            "artifact_reference": admission.artifact_reference,
            "artifact_size_bytes": admission.expected_bytes,
            "artifact_format": admission.artifact_format,
            "artifact_verification_revision": admission.verification_revision,
            "identity_index_reference": admission.identity_index_reference,
            "identity_index_sha256": admission.identity_index_sha256,
            "verse_count": admission.expected_verse_count,
            "canon_001_reconciliation": (
                CANON_001_ARTIFACT_IDENTITY_MATCH_CONFIRMED
            ),
            "fixture_only": False,
            "validation_status": "PENDING",
        }
        mismatches = [
            field
            for field, expected in expected_snapshot.items()
            if getattr(snapshot, field) != expected
        ]
        if snapshot.artifact_verified_at is None:
            mismatches.append("artifact_verified_at")
        if mismatches:
            raise ValueError(
                "Existing Tanzil snapshot conflicts with governed provenance: "
                + ", ".join(mismatches)
            )

        occurrences = (
            db.query(CorpusOccurrence)
            .filter(CorpusOccurrence.snapshot_id == snapshot.id)
            .order_by(CorpusOccurrence.id)
            .all()
        )
        expected = [
            (
                (
                    f"occ_tanzil_{version.replace('.', '_')}"
                    f"_{verse.surah:03d}_{verse.ayah:03d}"
                ),
                verse.verse_ref,
                verse.text,
            )
            for verse in verses
        ]
        actual = [(item.id, item.verse_ref, item.text) for item in occurrences]
        if actual != expected:
            raise ValueError(
                "Existing Tanzil occurrences do not exactly match the governed artifact"
            )
