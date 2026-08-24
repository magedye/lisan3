import pytest
from pydantic import ValidationError

from backend.domain.vector_contracts import (
    EmbeddingModelManifest,
    EmbeddingSpace,
    GovernedModelManifestRequired,
    RetrievalCandidate,
    require_governed_model_manifest,
)


def manifest(**overrides) -> EmbeddingModelManifest:
    values = {
        "model_id": "synthetic-evaluation-adapter",
        "revision": "fixture-r1",
        "dimensions": 4,
        "preprocessing_config": {"normalization": "l2"},
        "allowed_spaces": (EmbeddingSpace.CLAIM,),
    }
    values.update(overrides)
    return EmbeddingModelManifest(**values)


def test_embedding_spaces_are_exactly_the_canonical_six():
    assert {space.value for space in EmbeddingSpace} == {
        "VERSE_CONTEXT",
        "STRUCTURAL_PROFILE",
        "HYPOTHESIS",
        "CLAIM",
        "ROOT_CANDIDATE",
        "EXTERNAL_RESEARCH",
    }


def test_production_handoff_fails_closed_without_governed_decision():
    with pytest.raises(GovernedModelManifestRequired, match="decision reference"):
        require_governed_model_manifest(manifest(), EmbeddingSpace.CLAIM)


def test_production_handoff_rejects_an_unauthorized_space():
    governed = manifest(governance_decision_ref="decision:future-governed-model")
    with pytest.raises(GovernedModelManifestRequired, match="VERSE_CONTEXT"):
        require_governed_model_manifest(governed, EmbeddingSpace.VERSE_CONTEXT)


def test_manifest_fingerprint_is_stable_and_configuration_sensitive():
    first = manifest()
    reordered = manifest(preprocessing_config={"normalization": "l2"})
    changed = manifest(preprocessing_config={"normalization": "none"})
    assert first.config_hash == reordered.config_hash
    assert first.config_hash != changed.config_hash


def test_candidate_contract_has_no_epistemic_confidence_or_mutation_fields():
    forbidden = {
        "confidence",
        "epistemic_state",
        "gate_status",
        "review_state",
        "publication_state",
        "knowledge_edge",
    }
    assert forbidden.isdisjoint(RetrievalCandidate.model_fields)
    with pytest.raises(ValidationError):
        RetrievalCandidate(
            candidate_id="candidate-1",
            candidate_type="SEMANTIC_NEIGHBOR",
            entity_ref="SEMANTIC_CLAIM:claim-1",
            source_revision="1",
            embedding_space="CLAIM",
            embedding_model="synthetic-evaluation-adapter",
            embedding_model_revision="fixture-r1",
            distance=0.1,
            similarity_score=0.9,
            retrieval_reason="synthetic evaluation",
            provenance={"class": "SYNTHETIC_EVALUATION"},
            confidence=0.9,
        )
