from unittest.mock import patch

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.domain import models
from backend.domain.services import vector_discovery
from backend.domain.vector_contracts import (
    CandidateType,
    EmbeddingModelManifest,
    EmbeddingSpace,
    EvaluationVectorInput,
    ExperimentalVectorProvenance,
)
from backend.infrastructure.database import Base


def create_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine, sessionmaker(bind=engine)()


def add_run(db, run_id: str, *, contamination: str = "CLEAN"):
    db.add_all(
        [
            models.ResearchRun(
                id=run_id,
                target_contract="ROOT_CORE",
                target_expression="synthetic",
                methodology_revision="fixture-method",
                corpus_snapshot=f"fixture-snapshot-{run_id}",
                authority_context={"mode": "SYNTHETIC_EVALUATION"},
            ),
            models.IsolationState(
                id=f"isolation-{run_id}",
                research_run_id=run_id,
                target_contract="ROOT_CORE",
                corpus_snapshot=f"fixture-snapshot-{run_id}",
                methodology_reference="fixture-method",
                allowed_sources=["SYNTHETIC_EVALUATION"],
                is_contaminated=contamination,
            ),
            models.SemanticClaim(
                id=f"claim-{run_id}",
                research_run_id=run_id,
                contract_type="ROOT_CORE",
            ),
        ]
    )
    db.commit()


def manifest(
    *,
    model_id: str = "synthetic-evaluation-adapter",
    revision: str = "fixture-r1",
    normalization: str = "l2",
    spaces: tuple[EmbeddingSpace, ...] = (
        EmbeddingSpace.CLAIM,
        EmbeddingSpace.VERSE_CONTEXT,
    ),
    governance_decision_ref: str | None = None,
) -> EmbeddingModelManifest:
    return EmbeddingModelManifest(
        model_id=model_id,
        revision=revision,
        dimensions=4,
        preprocessing_config={"normalization": normalization},
        allowed_spaces=spaces,
        governance_decision_ref=governance_decision_ref,
    )


def vector(
    embedding_id: str,
    values: tuple[float, float, float, float],
    *,
    eligible: bool = True,
) -> EvaluationVectorInput:
    return EvaluationVectorInput(
        embedding_id=embedding_id,
        entity_type="SYNTHETIC_FIXTURE",
        entity_id=embedding_id,
        source_revision="fixture-source-r1",
        source_hash=f"hash-{embedding_id}",
        vector=values,
        provenance_class=ExperimentalVectorProvenance.SYNTHETIC_EVALUATION,
        source_eligible=eligible,
    )


@pytest.fixture
def eligible_db(monkeypatch):
    engine, db = create_session()
    add_run(db, "run-a")
    add_run(db, "run-b")
    monkeypatch.setattr(vector_discovery, "has_valid_gate", lambda *_args: True)
    try:
        yield db
    finally:
        db.close()
        engine.dispose()


def test_rebuild_is_deterministic_and_removes_omitted_sources(eligible_db):
    inputs = [
        vector("a", (1.0, 0.0, 0.0, 0.0)),
        vector("b", (0.0, 1.0, 0.0, 0.0)),
    ]
    first = vector_discovery.VectorDiscoveryService.rebuild_evaluation(
        eligible_db,
        run_id="run-a",
        space=EmbeddingSpace.CLAIM,
        manifest=manifest(),
        vectors=inputs,
    )
    second = vector_discovery.VectorDiscoveryService.rebuild_evaluation(
        eligible_db,
        run_id="run-a",
        space=EmbeddingSpace.CLAIM,
        manifest=manifest(),
        vectors=list(reversed(inputs)),
    )
    assert first == second
    assert eligible_db.query(models.SemanticEmbedding).count() == 2

    reduced = vector_discovery.VectorDiscoveryService.rebuild_evaluation(
        eligible_db,
        run_id="run-a",
        space=EmbeddingSpace.CLAIM,
        manifest=manifest(),
        vectors=inputs[:1],
    )
    assert [
        item.entity_id for item in eligible_db.query(models.SemanticEmbedding).all()
    ] == ["a"]
    assert reduced != first


def test_query_is_deterministic_run_and_space_scoped(eligible_db):
    profile = manifest()
    vector_discovery.VectorDiscoveryService.rebuild_evaluation(
        eligible_db,
        run_id="run-a",
        space=EmbeddingSpace.CLAIM,
        manifest=profile,
        vectors=[
            vector("claim-close", (1.0, 0.0, 0.0, 0.0)),
            vector("claim-far", (0.0, 1.0, 0.0, 0.0)),
        ],
    )
    vector_discovery.VectorDiscoveryService.rebuild_evaluation(
        eligible_db,
        run_id="run-a",
        space=EmbeddingSpace.VERSE_CONTEXT,
        manifest=profile,
        vectors=[vector("wrong-space", (1.0, 0.0, 0.0, 0.0))],
    )
    vector_discovery.VectorDiscoveryService.rebuild_evaluation(
        eligible_db,
        run_id="run-b",
        space=EmbeddingSpace.CLAIM,
        manifest=profile,
        vectors=[vector("wrong-run", (1.0, 0.0, 0.0, 0.0))],
    )

    first = vector_discovery.VectorDiscoveryService.discover(
        eligible_db,
        run_id="run-a",
        space=EmbeddingSpace.CLAIM,
        manifest=profile,
        query_vector=(1.0, 0.0, 0.0, 0.0),
        candidate_type=CandidateType.SEMANTIC_NEIGHBOR,
        top_k=5,
    )
    second = vector_discovery.VectorDiscoveryService.discover(
        eligible_db,
        run_id="run-a",
        space=EmbeddingSpace.CLAIM,
        manifest=profile,
        query_vector=(1.0, 0.0, 0.0, 0.0),
        candidate_type=CandidateType.SEMANTIC_NEIGHBOR,
        top_k=5,
    )
    assert first == second
    assert [item.entity_ref for item in first] == [
        "SYNTHETIC_FIXTURE:claim-close",
        "SYNTHETIC_FIXTURE:claim-far",
    ]
    assert all(item.embedding_space is EmbeddingSpace.CLAIM for item in first)
    assert all(item.provenance["research_run_id"] == "run-a" for item in first)


def test_candidate_results_cannot_mutate_claim_graph_or_authority(eligible_db):
    profile = manifest()
    claim = eligible_db.get(models.SemanticClaim, "claim-run-a")
    before = (
        claim.epistemic_state,
        claim.review_state,
        claim.freshness_state,
        claim.publication_state,
        eligible_db.query(models.KnowledgeEdge).count(),
    )
    vector_discovery.VectorDiscoveryService.rebuild_evaluation(
        eligible_db,
        run_id="run-a",
        space=EmbeddingSpace.CLAIM,
        manifest=profile,
        vectors=[vector("candidate", (1.0, 0.0, 0.0, 0.0))],
    )
    candidates = vector_discovery.VectorDiscoveryService.discover(
        eligible_db,
        run_id="run-a",
        space=EmbeddingSpace.CLAIM,
        manifest=profile,
        query_vector=(1.0, 0.0, 0.0, 0.0),
        candidate_type=CandidateType.COUNTEREVIDENCE,
        top_k=1,
    )
    eligible_db.refresh(claim)
    after = (
        claim.epistemic_state,
        claim.review_state,
        claim.freshness_state,
        claim.publication_state,
        eligible_db.query(models.KnowledgeEdge).count(),
    )
    assert before == after
    assert candidates[0].status == "CANDIDATE"
    assert candidates[0].authority_notice == "DERIVED_DISCOVERY_NON_AUTHORITATIVE"
    assert candidates[0].similarity_score == 1.0


@pytest.mark.parametrize(
    ("changed_manifest", "expected_reason"),
    [
        (
            manifest(model_id="synthetic-evaluation-adapter-v2"),
            "MODEL_REVISION_CHANGED",
        ),
        (manifest(revision="fixture-r2"), "MODEL_REVISION_CHANGED"),
        (manifest(normalization="none"), "MODEL_CONFIG_CHANGED"),
    ],
)
def test_model_or_config_change_invalidates_and_excludes_stale_vectors(
    eligible_db, changed_manifest, expected_reason
):
    vector_discovery.VectorDiscoveryService.rebuild_evaluation(
        eligible_db,
        run_id="run-a",
        space=EmbeddingSpace.CLAIM,
        manifest=manifest(),
        vectors=[vector("candidate", (1.0, 0.0, 0.0, 0.0))],
    )
    with pytest.raises(vector_discovery.VectorStateStale):
        vector_discovery.VectorDiscoveryService.discover(
            eligible_db,
            run_id="run-a",
            space=EmbeddingSpace.CLAIM,
            manifest=changed_manifest,
            query_vector=(1.0, 0.0, 0.0, 0.0),
            candidate_type=CandidateType.SEMANTIC_NEIGHBOR,
            top_k=1,
        )

    assert (
        vector_discovery.VectorDiscoveryService.invalidate_mismatched(
            eligible_db,
            run_id="run-a",
            space=EmbeddingSpace.CLAIM,
            manifest=changed_manifest,
        )
        == 1
    )
    stored = eligible_db.query(models.SemanticEmbedding).one()
    assert stored.lifecycle_state == "STALE"
    assert stored.invalidated_reason == expected_reason
    assert (
        vector_discovery.VectorDiscoveryService.discover(
            eligible_db,
            run_id="run-a",
            space=EmbeddingSpace.CLAIM,
            manifest=changed_manifest,
            query_vector=(1.0, 0.0, 0.0, 0.0),
            candidate_type=CandidateType.SEMANTIC_NEIGHBOR,
            top_k=1,
        )
        == []
    )


def test_ineligible_input_fails_before_replacing_current_state(eligible_db):
    vector_discovery.VectorDiscoveryService.rebuild_evaluation(
        eligible_db,
        run_id="run-a",
        space=EmbeddingSpace.CLAIM,
        manifest=manifest(),
        vectors=[vector("eligible", (1.0, 0.0, 0.0, 0.0))],
    )
    with pytest.raises(vector_discovery.VectorAccessForbidden, match="Ineligible"):
        vector_discovery.VectorDiscoveryService.rebuild_evaluation(
            eligible_db,
            run_id="run-a",
            space=EmbeddingSpace.CLAIM,
            manifest=manifest(),
            vectors=[vector("ineligible", (1.0, 0.0, 0.0, 0.0), eligible=False)],
        )
    assert eligible_db.query(models.SemanticEmbedding).one().entity_id == "eligible"


def test_invalid_dimension_and_unauthorized_space_fail_before_rebuild(eligible_db):
    with pytest.raises(ValueError, match="Expected 4"):
        vector_discovery.VectorDiscoveryService.rebuild_evaluation(
            eligible_db,
            run_id="run-a",
            space=EmbeddingSpace.CLAIM,
            manifest=manifest(),
            vectors=[
                vector("bad-dimension", (1.0, 0.0, 0.0, 0.0)).model_copy(
                    update={"vector": (1.0, 0.0)}
                )
            ],
        )
    with pytest.raises(
        vector_discovery.VectorAccessForbidden, match="does not authorize"
    ):
        vector_discovery.VectorDiscoveryService.rebuild_evaluation(
            eligible_db,
            run_id="run-a",
            space=EmbeddingSpace.VERSE_CONTEXT,
            manifest=manifest(spaces=(EmbeddingSpace.CLAIM,)),
            vectors=[],
        )
    assert eligible_db.query(models.SemanticEmbedding).count() == 0


def test_prelock_access_is_blocked_without_marking_contamination():
    engine, db = create_session()
    add_run(db, "run-prelock")
    try:
        with (
            patch.object(vector_discovery, "has_valid_gate", return_value=False),
            pytest.raises(
                vector_discovery.VectorAccessForbidden, match="before Internal Lock"
            ),
        ):
            vector_discovery.VectorDiscoveryService.rebuild_evaluation(
                db,
                run_id="run-prelock",
                space=EmbeddingSpace.CLAIM,
                manifest=manifest(),
                vectors=[vector("blocked", (1.0, 0.0, 0.0, 0.0))],
            )
        state = db.query(models.IsolationState).one()
        assert state.is_contaminated == "CLEAN"
        assert state.contamination_reason is None
        assert db.query(models.SemanticEmbedding).count() == 0
        assert db.query(models.IsolationEvent).count() == 0
    finally:
        db.close()
        engine.dispose()


def test_missing_run_or_isolation_fails_closed(eligible_db):
    with pytest.raises(LookupError, match="missing-run"):
        vector_discovery.VectorDiscoveryService.rebuild_evaluation(
            eligible_db,
            run_id="missing-run",
            space=EmbeddingSpace.CLAIM,
            manifest=manifest(),
            vectors=[],
        )
    isolation = (
        eligible_db.query(models.IsolationState)
        .filter(models.IsolationState.research_run_id == "run-a")
        .one()
    )
    eligible_db.delete(isolation)
    eligible_db.commit()
    with pytest.raises(vector_discovery.VectorAccessForbidden, match="absent"):
        vector_discovery.VectorDiscoveryService.rebuild_evaluation(
            eligible_db,
            run_id="run-a",
            space=EmbeddingSpace.CLAIM,
            manifest=manifest(),
            vectors=[],
        )


def test_contaminated_run_and_production_manifest_are_rejected(eligible_db):
    isolation = (
        eligible_db.query(models.IsolationState)
        .filter(models.IsolationState.research_run_id == "run-a")
        .one()
    )
    isolation.is_contaminated = "PRIOR_CONTAMINATED"
    eligible_db.commit()
    with pytest.raises(vector_discovery.VectorAccessForbidden, match="contaminated"):
        vector_discovery.VectorDiscoveryService.rebuild_evaluation(
            eligible_db,
            run_id="run-a",
            space=EmbeddingSpace.CLAIM,
            manifest=manifest(),
            vectors=[],
        )
    with pytest.raises(vector_discovery.VectorProductionBoundaryError):
        vector_discovery.VectorDiscoveryService.rebuild_evaluation(
            eligible_db,
            run_id="run-b",
            space=EmbeddingSpace.CLAIM,
            manifest=manifest(governance_decision_ref="future:decision"),
            vectors=[],
        )


def test_deleting_vector_state_preserves_canonical_sources(eligible_db):
    run = eligible_db.get(models.ResearchRun, "run-a")
    claim = eligible_db.get(models.SemanticClaim, "claim-run-a")
    before = (run.status, claim.epistemic_state)
    vector_discovery.VectorDiscoveryService.rebuild_evaluation(
        eligible_db,
        run_id="run-a",
        space=EmbeddingSpace.CLAIM,
        manifest=manifest(),
        vectors=[vector("candidate", (1.0, 0.0, 0.0, 0.0))],
    )
    assert (
        vector_discovery.VectorDiscoveryService.delete_derived_state(
            eligible_db, run_id="run-a"
        )
        == 1
    )
    eligible_db.refresh(run)
    eligible_db.refresh(claim)
    assert (run.status, claim.epistemic_state) == before


def test_space_scoped_deletion_preserves_other_space(eligible_db):
    profile = manifest()
    for space in (EmbeddingSpace.CLAIM, EmbeddingSpace.VERSE_CONTEXT):
        vector_discovery.VectorDiscoveryService.rebuild_evaluation(
            eligible_db,
            run_id="run-a",
            space=space,
            manifest=profile,
            vectors=[vector(space.value, (1.0, 0.0, 0.0, 0.0))],
        )
    assert (
        vector_discovery.VectorDiscoveryService.delete_derived_state(
            eligible_db, run_id="run-a", space=EmbeddingSpace.CLAIM
        )
        == 1
    )
    remaining = eligible_db.query(models.SemanticEmbedding).one()
    assert remaining.embedding_space == EmbeddingSpace.VERSE_CONTEXT.value


@pytest.mark.parametrize("top_k", [0, 101])
def test_invalid_top_k_fails_closed(eligible_db, top_k):
    with pytest.raises(ValueError, match="top_k"):
        vector_discovery.VectorDiscoveryService.discover(
            eligible_db,
            run_id="run-a",
            space=EmbeddingSpace.CLAIM,
            manifest=manifest(),
            query_vector=(1.0, 0.0, 0.0, 0.0),
            candidate_type=CandidateType.SEMANTIC_NEIGHBOR,
            top_k=top_k,
        )


@settings(max_examples=6, deadline=None)
@given(space=st.sampled_from(list(EmbeddingSpace)))
def test_generated_space_scope_never_returns_another_space(space):
    engine, db = create_session()
    add_run(db, "run-property")
    profile = manifest(spaces=(space,))
    try:
        with patch.object(vector_discovery, "has_valid_gate", return_value=True):
            vector_discovery.VectorDiscoveryService.rebuild_evaluation(
                db,
                run_id="run-property",
                space=space,
                manifest=profile,
                vectors=[vector("scoped", (1.0, 0.0, 0.0, 0.0))],
            )
            result = vector_discovery.VectorDiscoveryService.discover(
                db,
                run_id="run-property",
                space=space,
                manifest=profile,
                query_vector=(1.0, 0.0, 0.0, 0.0),
                candidate_type=CandidateType.SEMANTIC_NEIGHBOR,
                top_k=1,
            )
        assert len(result) == 1
        assert result[0].embedding_space is space
    finally:
        db.close()
        engine.dispose()
