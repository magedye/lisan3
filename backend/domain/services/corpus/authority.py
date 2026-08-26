from dataclasses import dataclass
from typing import Protocol

SOURCE_ROLE_APPROVED = "SOURCE_ROLE_APPROVED"
SOURCE_ROLE_PENDING = "SOURCE_ROLE_PENDING"
ARTIFACT_PRESENT = "ARTIFACT_PRESENT"
ARTIFACT_VERIFICATION_PENDING = "ARTIFACT_VERIFICATION_PENDING"
HASH_VERIFIED = "HASH_VERIFIED"
IMPORT_VALIDATED = "IMPORT_VALIDATED"
CANONICAL_ACTIVATION_PENDING = "CANONICAL_ACTIVATION_PENDING"
PRODUCTION_ACTIVE = "PRODUCTION_ACTIVE"
CANON_001_ARTIFACT_IDENTITY_MATCH_CONFIRMED = (
    "CANON_001_ARTIFACT_IDENTITY_MATCH_CONFIRMED"
)


@dataclass(frozen=True)
class CorpusAdmissionRecord:
    source_id: str
    source_role_status: str
    expected_hash: str | None
    artifact_verification_status: str
    activation_status: str
    authority_reference: str
    source_name: str | None = None
    canonical_text_version: str | None = None
    artifact_reference: str | None = None
    expected_bytes: int | None = None
    artifact_format: str | None = None
    identity_index_reference: str | None = None
    identity_index_sha256: str | None = None
    expected_verse_count: int | None = None
    expected_surah_count: int | None = None
    verification_revision: str | None = None
    provenance_reference: str | None = None
    canon_001_reconciliation: str | None = None
    authorized_snapshot_id: str | None = None
    activation_decision_reference: str | None = None


# Application enforcement of the current canonical admission records. Tanzil
# production activation is owner-authorized only for the exact bound snapshot.
# QAC remains pending source-role admission, artifact/provenance verification,
# real-format import, and activation. It is not required for Tanzil
# canonical-text admission.
CANONICAL_CORPUS_ADMISSIONS: dict[str, CorpusAdmissionRecord] = {
    "TANZIL_QURAN_UTHMANI": CorpusAdmissionRecord(
        source_id="TANZIL_QURAN_UTHMANI",
        source_role_status=SOURCE_ROLE_APPROVED,
        expected_hash=(
            "ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af"
        ),
        artifact_verification_status=HASH_VERIFIED,
        activation_status=PRODUCTION_ACTIVE,
        authority_reference="docs/canonical/ADMISSION_TANZIL.md",
        source_name="Tanzil Quran Text (Uthmani)",
        canonical_text_version="1.1",
        artifact_reference="data/corpus/tanzil/tanzil-uthmani-1.1.txt",
        expected_bytes=1_334_737,
        artifact_format="TANZIL_UTHMANI_1_1_ONE_VERSE_PER_LINE_UTF8_LF",
        identity_index_reference=("data/corpus/tanzil/quran-verse-index-v1.0.json"),
        identity_index_sha256=(
            "0d0a2273e82ebb0d9848ccbf831f1bb297c0fb255413c5aeb299bbfaf2bbc967"
        ),
        expected_verse_count=6_236,
        expected_surah_count=114,
        verification_revision="LISAN3_TANZIL_ADMISSION_V1_2026_08_26",
        provenance_reference="docs/canonical/ADMISSION_TANZIL.md#artifact-provenance",
        canon_001_reconciliation=CANON_001_ARTIFACT_IDENTITY_MATCH_CONFIRMED,
        authorized_snapshot_id="snap_tanzil_1_1_ac0724796cbb",
        activation_decision_reference=(
            "docs/canonical/ADMISSION_TANZIL.md#owner-production-activation-decision"
        ),
    ),
    "QAC_MORPHOLOGY_SYNTAX": CorpusAdmissionRecord(
        source_id="QAC_MORPHOLOGY_SYNTAX",
        source_role_status=SOURCE_ROLE_PENDING,
        expected_hash=None,
        artifact_verification_status=ARTIFACT_VERIFICATION_PENDING,
        activation_status=CANONICAL_ACTIVATION_PENDING,
        authority_reference="docs/canonical/ADMISSION_QAC.md",
    ),
}


class SnapshotLifecycle(Protocol):
    id: str
    canonical_text_source: str
    canonical_text_hash: str
    source_role_status: str
    artifact_presence_status: str
    expected_canonical_text_hash: str | None
    hash_verification_status: str
    import_validation_status: str
    activation_status: str
    artifact_provenance: str | None
    artifact_reference: str | None
    artifact_size_bytes: int | None
    artifact_format: str | None
    artifact_verified_at: object | None
    artifact_verification_revision: str | None
    identity_index_reference: str | None
    identity_index_sha256: str | None
    verse_count: int | None
    canon_001_reconciliation: str | None
    fixture_only: bool
    validation_status: str


def get_canonical_admission(source_id: str) -> CorpusAdmissionRecord | None:
    return CANONICAL_CORPUS_ADMISSIONS.get(source_id)


def import_validation_failures(snapshot: SnapshotLifecycle) -> list[str]:
    """Return every failed boundary for authority-bound import validation."""
    failures: list[str] = []
    admission = get_canonical_admission(snapshot.canonical_text_source)

    if admission is None:
        failures.append("canonical source has no admission record")
        return failures
    if admission.source_role_status != SOURCE_ROLE_APPROVED:
        failures.append("source role is not approved")
    if snapshot.source_role_status != SOURCE_ROLE_APPROVED:
        failures.append("snapshot does not record source-role approval")
    if snapshot.artifact_presence_status != ARTIFACT_PRESENT:
        failures.append("physical artifact presence is not established")
    if admission.expected_hash is None:
        failures.append("canonical admission has no authority-bound expected hash")
    elif snapshot.expected_canonical_text_hash != admission.expected_hash:
        failures.append("snapshot expected hash is not authority-bound")
    elif snapshot.canonical_text_hash != admission.expected_hash:
        failures.append("artifact hash does not match the canonical expected hash")
    if snapshot.hash_verification_status != HASH_VERIFIED:
        failures.append("artifact hash is not verified")
    if snapshot.import_validation_status != IMPORT_VALIDATED:
        failures.append("import validation has not passed")
    if not snapshot.artifact_provenance:
        failures.append("artifact provenance is missing")
    if snapshot.fixture_only:
        failures.append("test fixtures cannot become production canonical artifacts")
    metadata_checks = (
        (
            "canonical_text_version",
            admission.canonical_text_version,
            "canonical text version is not authority-bound",
        ),
        (
            "artifact_reference",
            admission.artifact_reference,
            "artifact reference is not authority-bound",
        ),
        (
            "artifact_size_bytes",
            admission.expected_bytes,
            "artifact byte size is not authority-bound",
        ),
        (
            "artifact_format",
            admission.artifact_format,
            "artifact format is not authority-bound",
        ),
        (
            "artifact_verification_revision",
            admission.verification_revision,
            "artifact verification revision is not authority-bound",
        ),
        (
            "identity_index_reference",
            admission.identity_index_reference,
            "identity index reference is not authority-bound",
        ),
        (
            "identity_index_sha256",
            admission.identity_index_sha256,
            "identity index hash is not authority-bound",
        ),
        (
            "verse_count",
            admission.expected_verse_count,
            "verse count is not authority-bound",
        ),
        (
            "canon_001_reconciliation",
            admission.canon_001_reconciliation,
            "CANON-001 reconciliation is not the recorded factual match",
        ),
    )
    for field, expected, message in metadata_checks:
        if expected is not None and getattr(snapshot, field, None) != expected:
            failures.append(message)
    if (
        admission.verification_revision is not None
        and getattr(snapshot, "artifact_verified_at", None) is None
    ):
        failures.append("artifact verification timestamp is missing")
    return failures


def production_validation_failures(snapshot: SnapshotLifecycle) -> list[str]:
    """Return every failed authority boundary for production validation."""
    failures = import_validation_failures(snapshot)
    admission = get_canonical_admission(snapshot.canonical_text_source)
    if admission is None:
        return failures
    if admission.activation_status != PRODUCTION_ACTIVE:
        failures.append("canonical admission is not production-active")
    if (
        admission.authorized_snapshot_id is not None
        and snapshot.id != admission.authorized_snapshot_id
    ):
        failures.append("snapshot identity is not owner-authorized for production")
    if snapshot.activation_status != PRODUCTION_ACTIVE:
        failures.append("snapshot is not production-active")
    return failures


def is_production_validated(snapshot: SnapshotLifecycle) -> bool:
    return (
        snapshot.validation_status == "VALIDATED"
        and not production_validation_failures(snapshot)
    )
