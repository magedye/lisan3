import hashlib
import json
import re
from collections.abc import Sequence
from datetime import datetime, timezone
from enum import Enum
from typing import Literal, Protocol

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FiniteFloat,
    field_validator,
    model_validator,
)

_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$", re.IGNORECASE)
_IMMUTABLE_ARTIFACT_REFERENCE_PREFIX = "artifact://"


class EmbeddingSpace(str, Enum):
    VERSE_CONTEXT = "VERSE_CONTEXT"
    STRUCTURAL_PROFILE = "STRUCTURAL_PROFILE"
    HYPOTHESIS = "HYPOTHESIS"
    CLAIM = "CLAIM"
    ROOT_CANDIDATE = "ROOT_CANDIDATE"
    EXTERNAL_RESEARCH = "EXTERNAL_RESEARCH"


class ExperimentalVectorProvenance(str, Enum):
    BENCHMARK_ONLY = "BENCHMARK_ONLY"
    SYNTHETIC_EVALUATION = "SYNTHETIC_EVALUATION"


class CandidateType(str, Enum):
    SEMANTIC_NEIGHBOR = "SEMANTIC_NEIGHBOR"
    COUNTEREVIDENCE = "COUNTEREVIDENCE"


class GovernedModelManifestRequired(ValueError):
    pass


class VectorContract(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class EmbeddingModelManifest(VectorContract):
    model_id: str = Field(min_length=1)
    revision: str = Field(min_length=1)
    dimensions: int = Field(gt=0)
    preprocessing_config: dict[str, str | int | float | bool]
    allowed_spaces: tuple[EmbeddingSpace, ...] = Field(min_length=1)
    governance_decision_ref: str | None = None

    @field_validator("allowed_spaces")
    @classmethod
    def reject_duplicate_spaces(
        cls, spaces: tuple[EmbeddingSpace, ...]
    ) -> tuple[EmbeddingSpace, ...]:
        if len(spaces) != len(set(spaces)):
            raise ValueError("Embedding manifest spaces must be unique")
        return spaces

    @property
    def config_hash(self) -> str:
        payload = {
            "allowed_spaces": sorted(space.value for space in self.allowed_spaces),
            "dimensions": self.dimensions,
            "model_id": self.model_id,
            "preprocessing_config": self.preprocessing_config,
            "revision": self.revision,
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode()
        return hashlib.sha256(encoded).hexdigest()


class QuranCorpusBinding(VectorContract):
    snapshot_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    sha256: str = Field(min_length=64, max_length=64)

    @field_validator("sha256")
    @classmethod
    def require_sha256(cls, value: str) -> str:
        if not _SHA256_PATTERN.fullmatch(value):
            raise ValueError("Quran corpus hash must be a SHA-256 digest")
        return value.lower()


class GovernedModelArtifactManifest(EmbeddingModelManifest):
    """Immutable, repository-independent production model handoff metadata."""

    artifact_location: str = Field(min_length=1)
    artifact_sha256: str = Field(min_length=64, max_length=64)
    tokenizer_sha256: str = Field(min_length=64, max_length=64)
    configuration_sha256: str = Field(min_length=64, max_length=64)
    normalization: str = Field(min_length=1)
    quran_corpus: QuranCorpusBinding
    blind_lab_eligible: bool
    blind_lab_eligibility_classification: str = Field(min_length=1)
    training_data_provenance: str = Field(min_length=1)
    tafsir_heritage_islamic_qa_exposure: str = Field(min_length=1)
    provenance_approved: bool
    benchmark_version: str = Field(min_length=1)
    metrics_by_space: dict[EmbeddingSpace, dict[str, FiniteFloat]]
    known_limitations: tuple[str, ...] = Field(min_length=1)
    license: str = Field(min_length=1)
    reproducibility_evidence_ref: str = Field(min_length=1)
    independent_model_review_evidence_ref: str = Field(min_length=1)
    issued_at: datetime
    expires_at: datetime

    @field_validator(
        "artifact_sha256", "tokenizer_sha256", "configuration_sha256"
    )
    @classmethod
    def require_sha256(cls, value: str) -> str:
        if not _SHA256_PATTERN.fullmatch(value):
            raise ValueError("Artifact, tokenizer, and configuration hashes must be SHA-256")
        return value.lower()

    @field_validator("artifact_location")
    @classmethod
    def require_immutable_artifact_reference(cls, value: str) -> str:
        if not value.startswith(_IMMUTABLE_ARTIFACT_REFERENCE_PREFIX):
            raise ValueError("Artifact location must be an immutable artifact reference")
        return value

    @model_validator(mode="after")
    def validate_handoff_completeness(self) -> "GovernedModelArtifactManifest":
        if not self.governance_decision_ref:
            raise ValueError("Governed model artifact manifest requires a decision reference")
        if self.configuration_sha256 != self.config_hash:
            raise ValueError("Configuration hash does not match the declared model configuration")
        if set(self.metrics_by_space) != set(self.allowed_spaces):
            raise ValueError("Metrics must cover exactly the supported embedding spaces")
        if any(not metrics for metrics in self.metrics_by_space.values()):
            raise ValueError("Each supported embedding space requires benchmark metrics")
        issued_at = _as_utc(self.issued_at)
        expires_at = _as_utc(self.expires_at)
        if expires_at <= issued_at:
            raise ValueError("Model manifest expiry must be after issuance")
        return self


class GovernedModelArtifactRequirements(VectorContract):
    """Decision-bound expectations supplied by future governed integration."""

    governance_decision_ref: str = Field(min_length=1)
    model_id: str = Field(min_length=1)
    revision: str = Field(min_length=1)
    artifact_sha256: str = Field(min_length=64, max_length=64)
    tokenizer_sha256: str = Field(min_length=64, max_length=64)
    configuration_sha256: str = Field(min_length=64, max_length=64)
    dimensions: int = Field(gt=0)
    normalization: str = Field(min_length=1)
    quran_corpus: QuranCorpusBinding
    authorized_spaces: tuple[EmbeddingSpace, ...] = Field(min_length=1)
    blind_lab_eligibility_classification: str = Field(min_length=1)
    approved_training_data_provenance: tuple[str, ...] = Field(min_length=1)
    approved_exposure_classifications: tuple[str, ...] = Field(min_length=1)

    @field_validator(
        "artifact_sha256", "tokenizer_sha256", "configuration_sha256"
    )
    @classmethod
    def require_sha256(cls, value: str) -> str:
        if not _SHA256_PATTERN.fullmatch(value):
            raise ValueError("Governed artifact requirements require SHA-256 digests")
        return value.lower()

    @field_validator("authorized_spaces")
    @classmethod
    def reject_duplicate_spaces(
        cls, spaces: tuple[EmbeddingSpace, ...]
    ) -> tuple[EmbeddingSpace, ...]:
        if len(spaces) != len(set(spaces)):
            raise ValueError("Authorized embedding spaces must be unique")
        return spaces


def require_governed_model_manifest(
    manifest: GovernedModelArtifactManifest | None,
    *,
    space: EmbeddingSpace,
    requirements: GovernedModelArtifactRequirements,
    now: datetime | None = None,
) -> None:
    if manifest is None:
        raise GovernedModelManifestRequired(
            "An immutable governed embedding-model artifact manifest is required"
        )
    if not isinstance(manifest, GovernedModelArtifactManifest):
        raise GovernedModelManifestRequired(
            "Evaluation-only manifests cannot activate a governed model artifact"
        )
    if manifest.governance_decision_ref != requirements.governance_decision_ref:
        raise GovernedModelManifestRequired("Manifest decision reference is not accepted")
    if manifest.model_id != requirements.model_id or manifest.revision != requirements.revision:
        raise GovernedModelManifestRequired("Model revision is not supported by the governed decision")
    if manifest.artifact_sha256 != requirements.artifact_sha256:
        raise GovernedModelManifestRequired("Artifact hash is not accepted by the governed decision")
    if manifest.dimensions != requirements.dimensions:
        raise GovernedModelManifestRequired("Embedding dimension is not supported")
    if manifest.tokenizer_sha256 != requirements.tokenizer_sha256:
        raise GovernedModelManifestRequired("Tokenizer hash is not accepted by the governed decision")
    if manifest.configuration_sha256 != requirements.configuration_sha256:
        raise GovernedModelManifestRequired("Configuration hash is not accepted by the governed decision")
    if manifest.normalization != requirements.normalization:
        raise GovernedModelManifestRequired("Embedding normalization is not compatible")
    if manifest.quran_corpus != requirements.quran_corpus:
        raise GovernedModelManifestRequired("Quran corpus snapshot does not match the governed decision")
    if space not in manifest.allowed_spaces or space not in requirements.authorized_spaces:
        raise GovernedModelManifestRequired(
            f"Governed embedding manifest does not authorize {space.value}"
        )
    if not manifest.blind_lab_eligible or (
        manifest.blind_lab_eligibility_classification
        != requirements.blind_lab_eligibility_classification
    ):
        raise GovernedModelManifestRequired("Blind Lab eligibility is not approved")
    if not manifest.provenance_approved:
        raise GovernedModelManifestRequired("Model provenance is not approved")
    if manifest.training_data_provenance not in requirements.approved_training_data_provenance:
        raise GovernedModelManifestRequired("Training-data provenance is unknown or prohibited")
    if (
        manifest.tafsir_heritage_islamic_qa_exposure
        not in requirements.approved_exposure_classifications
    ):
        raise GovernedModelManifestRequired(
            "Tafsir, heritage, or Islamic-QA exposure is unknown or prohibited"
        )
    current_time = _as_utc(now or datetime.now(timezone.utc))
    if current_time < _as_utc(manifest.issued_at) or current_time >= _as_utc(
        manifest.expires_at
    ):
        raise GovernedModelManifestRequired("Model manifest is stale or not yet valid")


def verify_artifact_sha256(
    manifest: GovernedModelArtifactManifest, artifact_bytes: bytes
) -> None:
    """Verify exported artifact bytes without loading a model or provider."""

    actual_hash = hashlib.sha256(artifact_bytes).hexdigest()
    if actual_hash != manifest.artifact_sha256:
        raise GovernedModelManifestRequired("Artifact hash verification failed")


def _as_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)


class EmbeddingModelAdapter(Protocol):
    @property
    def manifest(self) -> GovernedModelArtifactManifest: ...

    def embed(
        self, texts: Sequence[str], *, space: EmbeddingSpace
    ) -> Sequence[Sequence[float]]: ...


class EvaluationVectorInput(VectorContract):
    embedding_id: str = Field(min_length=1)
    entity_type: str = Field(min_length=1)
    entity_id: str = Field(min_length=1)
    source_revision: str = Field(min_length=1)
    source_hash: str = Field(min_length=1)
    vector: tuple[FiniteFloat, ...] = Field(min_length=1)
    provenance_class: ExperimentalVectorProvenance
    source_eligible: bool = True


class RetrievalCandidate(VectorContract):
    candidate_id: str
    candidate_type: CandidateType
    source_layer: Literal["VECTOR"] = "VECTOR"
    entity_ref: str
    source_revision: str
    embedding_space: EmbeddingSpace
    embedding_model: str
    embedding_model_revision: str
    distance: FiniteFloat = Field(ge=0)
    similarity_score: FiniteFloat
    retrieval_reason: str
    provenance: dict[str, str]
    status: Literal["CANDIDATE"] = "CANDIDATE"
    authority_notice: Literal["DERIVED_DISCOVERY_NON_AUTHORITATIVE"] = (
        "DERIVED_DISCOVERY_NON_AUTHORITATIVE"
    )
