from dataclasses import dataclass
from typing import Protocol

SOURCE_ROLE_APPROVED = "SOURCE_ROLE_APPROVED"
ARTIFACT_PRESENT = "ARTIFACT_PRESENT"
ARTIFACT_VERIFICATION_PENDING = "ARTIFACT_VERIFICATION_PENDING"
HASH_VERIFIED = "HASH_VERIFIED"
IMPORT_VALIDATED = "IMPORT_VALIDATED"
CANONICAL_ACTIVATION_PENDING = "CANONICAL_ACTIVATION_PENDING"
PRODUCTION_ACTIVE = "PRODUCTION_ACTIVE"


@dataclass(frozen=True)
class CorpusAdmissionRecord:
    source_id: str
    source_role_status: str
    expected_hash: str | None
    artifact_verification_status: str
    activation_status: str
    authority_reference: str


# Application enforcement of the current canonical admission records.  Neither
# source has an authority-bound artifact hash or production activation yet.
CANONICAL_CORPUS_ADMISSIONS: dict[str, CorpusAdmissionRecord] = {
    "TANZIL_QURAN_UTHMANI": CorpusAdmissionRecord(
        source_id="TANZIL_QURAN_UTHMANI",
        source_role_status=SOURCE_ROLE_APPROVED,
        expected_hash=None,
        artifact_verification_status=ARTIFACT_VERIFICATION_PENDING,
        activation_status=CANONICAL_ACTIVATION_PENDING,
        authority_reference="docs/canonical/ADMISSION_TANZIL.md",
    ),
    "QAC_MORPHOLOGY_SYNTAX": CorpusAdmissionRecord(
        source_id="QAC_MORPHOLOGY_SYNTAX",
        source_role_status=SOURCE_ROLE_APPROVED,
        expected_hash=None,
        artifact_verification_status=ARTIFACT_VERIFICATION_PENDING,
        activation_status=CANONICAL_ACTIVATION_PENDING,
        authority_reference="docs/canonical/ADMISSION_QAC.md",
    ),
}


class SnapshotLifecycle(Protocol):
    canonical_text_source: str
    canonical_text_hash: str
    source_role_status: str
    artifact_presence_status: str
    expected_canonical_text_hash: str | None
    hash_verification_status: str
    import_validation_status: str
    activation_status: str
    artifact_provenance: str | None
    fixture_only: bool
    validation_status: str


def get_canonical_admission(source_id: str) -> CorpusAdmissionRecord | None:
    return CANONICAL_CORPUS_ADMISSIONS.get(source_id)


def production_validation_failures(snapshot: SnapshotLifecycle) -> list[str]:
    """Return every failed authority boundary for production validation."""
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
    if admission.activation_status != PRODUCTION_ACTIVE:
        failures.append("canonical admission is not production-active")
    if snapshot.activation_status != PRODUCTION_ACTIVE:
        failures.append("snapshot is not production-active")
    if not snapshot.artifact_provenance:
        failures.append("artifact provenance is missing")
    if snapshot.fixture_only:
        failures.append("test fixtures cannot become production canonical artifacts")
    return failures


def is_production_validated(snapshot: SnapshotLifecycle) -> bool:
    return (
        snapshot.validation_status == "VALIDATED"
        and not production_validation_failures(snapshot)
    )
