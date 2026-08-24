import hashlib
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from backend.domain.vector_contracts import (
    EmbeddingModelManifest,
    EmbeddingSpace,
    GovernedModelArtifactManifest,
    GovernedModelArtifactRequirements,
    GovernedModelManifestRequired,
    QuranCorpusBinding,
    RetrievalCandidate,
    require_governed_model_manifest,
    verify_artifact_sha256,
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


def corpus_binding() -> QuranCorpusBinding:
    return QuranCorpusBinding(
        snapshot_id="quran-snapshot-fixture",
        version="fixture-v1",
        sha256="c" * 64,
    )


def governed_manifest(**overrides) -> GovernedModelArtifactManifest:
    governance_decision_override = overrides.pop("governance_decision_ref", None)
    base = manifest(
        **{
            field: overrides[field]
            for field in (
                "model_id",
                "revision",
                "dimensions",
                "preprocessing_config",
                "allowed_spaces",
            )
            if field in overrides
        }
    )
    artifact_bytes = b"immutable-exported-model-artifact"
    base_values = base.model_dump()
    base_values.pop("governance_decision_ref")
    values = {
        **base_values,
        "artifact_location": "artifact://lisan-models/fixture-r1",
        "artifact_sha256": hashlib.sha256(artifact_bytes).hexdigest(),
        "tokenizer_sha256": "a" * 64,
        "configuration_sha256": base.config_hash,
        "normalization": "l2",
        "quran_corpus": corpus_binding(),
        "blind_lab_eligible": True,
        "blind_lab_eligibility_classification": "fixture-approved",
        "training_data_provenance": "fixture-governed-provenance",
        "tafsir_heritage_islamic_qa_exposure": "fixture-reviewed-exposure",
        "provenance_approved": True,
        "benchmark_version": "fixture-benchmark-v1",
        "metrics_by_space": {EmbeddingSpace.CLAIM: {"ndcg_at_3": 0.9}},
        "known_limitations": ("Synthetic contract fixture only.",),
        "license": "fixture-license",
        "reproducibility_evidence_ref": "evidence:fixture-reproducibility",
        "independent_model_review_evidence_ref": "review:fixture-independent",
        "issued_at": datetime(2026, 8, 24, tzinfo=timezone.utc),
        "expires_at": datetime(2026, 9, 24, tzinfo=timezone.utc),
        "governance_decision_ref": "decision:fixture-model-r1",
    }
    values.update(overrides)
    if governance_decision_override is not None:
        values["governance_decision_ref"] = governance_decision_override
    if "configuration_sha256" not in overrides:
        values["configuration_sha256"] = base.config_hash
    return GovernedModelArtifactManifest(**values)


def requirements(**overrides) -> GovernedModelArtifactRequirements:
    production_manifest = governed_manifest()
    values = {
        "governance_decision_ref": production_manifest.governance_decision_ref,
        "model_id": production_manifest.model_id,
        "revision": production_manifest.revision,
        "artifact_sha256": production_manifest.artifact_sha256,
        "tokenizer_sha256": production_manifest.tokenizer_sha256,
        "configuration_sha256": production_manifest.configuration_sha256,
        "dimensions": production_manifest.dimensions,
        "normalization": production_manifest.normalization,
        "quran_corpus": production_manifest.quran_corpus,
        "authorized_spaces": production_manifest.allowed_spaces,
        "blind_lab_eligibility_classification": (
            production_manifest.blind_lab_eligibility_classification
        ),
        "approved_training_data_provenance": (
            production_manifest.training_data_provenance,
        ),
        "approved_exposure_classifications": (
            production_manifest.tafsir_heritage_islamic_qa_exposure,
        ),
    }
    values.update(overrides)
    return GovernedModelArtifactRequirements(**values)


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
    with pytest.raises(GovernedModelManifestRequired, match="artifact manifest"):
        require_governed_model_manifest(
            None, space=EmbeddingSpace.CLAIM, requirements=requirements()
        )
    with pytest.raises(GovernedModelManifestRequired, match="Evaluation-only"):
        require_governed_model_manifest(
            manifest(),  # type: ignore[arg-type]
            space=EmbeddingSpace.CLAIM,
            requirements=requirements(),
        )


def test_production_handoff_rejects_an_unauthorized_space():
    with pytest.raises(GovernedModelManifestRequired, match="VERSE_CONTEXT"):
        require_governed_model_manifest(
            governed_manifest(),
            space=EmbeddingSpace.VERSE_CONTEXT,
            requirements=requirements(),
        )


def test_production_handoff_accepts_only_the_exact_governed_artifact():
    artifact = governed_manifest()
    require_governed_model_manifest(
        artifact,
        space=EmbeddingSpace.CLAIM,
        requirements=requirements(),
        now=datetime(2026, 8, 25, tzinfo=timezone.utc),
    )
    verify_artifact_sha256(artifact, b"immutable-exported-model-artifact")


@pytest.mark.parametrize(
    ("manifest_overrides", "requirements_overrides", "message"),
    [
        ({"revision": "unsupported-r2"}, {}, "Model revision"),
        ({"dimensions": 8}, {}, "Embedding dimension"),
        ({"normalization": "none"}, {}, "normalization"),
        ({"blind_lab_eligible": False}, {}, "Blind Lab"),
        ({"provenance_approved": False}, {}, "provenance"),
        (
            {"training_data_provenance": "unknown-provenance"},
            {},
            "unknown or prohibited",
        ),
        (
            {"tafsir_heritage_islamic_qa_exposure": "prohibited-exposure"},
            {},
            "unknown or prohibited",
        ),
        ({"quran_corpus": corpus_binding().model_copy(update={"version": "other"})}, {}, "Quran corpus"),
    ],
)
def test_production_handoff_rejects_mismatched_governed_metadata(
    manifest_overrides, requirements_overrides, message
):
    candidate = governed_manifest(**manifest_overrides)
    with pytest.raises(GovernedModelManifestRequired, match=message):
        require_governed_model_manifest(
            candidate,
            space=EmbeddingSpace.CLAIM,
            requirements=requirements(**requirements_overrides),
            now=datetime(2026, 8, 25, tzinfo=timezone.utc),
        )


def test_production_handoff_rejects_a_stale_manifest_and_artifact_hash_mismatch():
    stale = governed_manifest(expires_at=datetime(2026, 8, 24, 1, tzinfo=timezone.utc))
    with pytest.raises(GovernedModelManifestRequired, match="stale"):
        require_governed_model_manifest(
            stale,
            space=EmbeddingSpace.CLAIM,
            requirements=requirements(),
            now=datetime(2026, 8, 25, tzinfo=timezone.utc),
        )
    with pytest.raises(GovernedModelManifestRequired, match="hash verification"):
        verify_artifact_sha256(governed_manifest(), b"different-exported-artifact")


def test_handoff_contract_rejects_invalid_hashes_and_checkout_paths():
    with pytest.raises(ValidationError, match="SHA-256"):
        governed_manifest(artifact_sha256="g" * 64)
    with pytest.raises(ValidationError, match="immutable artifact reference"):
        governed_manifest(artifact_location="D:/external-checkout/exports/model")


def test_handoff_contract_requires_metrics_for_every_supported_space():
    base = manifest(allowed_spaces=(EmbeddingSpace.CLAIM, EmbeddingSpace.HYPOTHESIS))
    with pytest.raises(ValidationError, match="Metrics must cover"):
        governed_manifest(
            **base.model_dump(),
            configuration_sha256=base.config_hash,
            metrics_by_space={EmbeddingSpace.CLAIM: {"ndcg_at_3": 0.9}},
        )


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
        RetrievalCandidate.model_validate(
            {
                "candidate_id": "candidate-1",
                "candidate_type": "SEMANTIC_NEIGHBOR",
                "entity_ref": "SEMANTIC_CLAIM:claim-1",
                "source_revision": "1",
                "embedding_space": "CLAIM",
                "embedding_model": "synthetic-evaluation-adapter",
                "embedding_model_revision": "fixture-r1",
                "distance": 0.1,
                "similarity_score": 0.9,
                "retrieval_reason": "synthetic evaluation",
                "provenance": {"class": "SYNTHETIC_EVALUATION"},
                "confidence": 0.9,
            }
        )
