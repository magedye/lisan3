import hashlib
import json
from collections.abc import Sequence
from enum import Enum
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, FiniteFloat, field_validator


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


def require_governed_model_manifest(
    manifest: EmbeddingModelManifest, space: EmbeddingSpace
) -> None:
    if not manifest.governance_decision_ref:
        raise GovernedModelManifestRequired(
            "A governed embedding-model decision reference is required"
        )
    if space not in manifest.allowed_spaces:
        raise GovernedModelManifestRequired(
            f"Governed embedding manifest does not authorize {space.value}"
        )


class EmbeddingModelAdapter(Protocol):
    @property
    def manifest(self) -> EmbeddingModelManifest: ...

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
