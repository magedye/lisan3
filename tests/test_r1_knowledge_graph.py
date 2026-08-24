import uuid
from datetime import datetime
from unittest.mock import patch

import networkx as nx
import pytest
from fastapi.testclient import TestClient
from hypothesis import given, settings
from hypothesis import strategies as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.domain.services import knowledge_graph
from backend.infrastructure.database import Base, get_db
from backend.main import app

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
client = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def isolated_graph_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def graph_sources():
    db = TestingSessionLocal()
    try:
        snapshot = models.CorpusSnapshot(
            id="snap_r1",
            canonical_text_source="fixture",
            canonical_text_version="v1",
            canonical_text_hash="fixture-hash",
            import_revision="import-r1",
        )
        run = models.ResearchRun(
            id="run_r1",
            target_contract="ROOT_CORE",
            target_expression="علم",
            methodology_revision="method-r1",
            corpus_snapshot=snapshot.id,
            authority_context={"source": "test"},
        )
        clean_isolation = models.IsolationState(
            id="iso_r1",
            research_run_id=run.id,
            target_contract=run.target_contract,
            corpus_snapshot=snapshot.id,
            methodology_reference=run.methodology_revision,
            allowed_sources=["QURAN_CORPUS"],
            is_contaminated="CLEAN",
        )
        claim = models.SemanticClaim(
            id="claim_r1",
            research_run_id=run.id,
            contract_type="ROOT_CORE",
            revision_id=2,
        )
        rule = models.GovernanceRule(
            id="rule_r1", rule_code="RULE_R1", active_revision=3
        )
        dependency = models.DependencyRecord(
            id="dep_r1",
            dependent_claim_id=claim.id,
            dependency_type="GOVERNANCE_RULE",
            dependency_ref=rule.rule_code,
            dependency_revision=rule.active_revision,
        )
        gate = models.GateReport(
            id="gate_r1",
            research_run_id=run.id,
            gate_code="INTERNAL_LOCK",
            status="PASSED",
            evaluated_revision=run.methodology_revision,
        )
        db.add_all([snapshot, run, clean_isolation, claim, rule, dependency, gate])
        db.commit()
        return {"run_id": run.id, "claim_id": claim.id, "snapshot_id": snapshot.id}
    finally:
        db.close()


def allow_graph_access(monkeypatch):
    monkeypatch.setattr(knowledge_graph, "has_valid_gate", lambda *_args: True)


def rebuild_via_api(run_id: str):
    response = client.post(f"/runs/{run_id}/knowledge-graph/rebuild")
    assert response.status_code == 200, response.json()
    return response.json()


def test_graph_read_is_blocked_before_internal_lock(graph_sources):
    response = client.get(f"/runs/{graph_sources['run_id']}/knowledge-graph")
    assert response.status_code == 403
    assert "before Internal Lock" in response.json()["detail"]
    db = TestingSessionLocal()
    try:
        isolation = (
            db.query(models.IsolationState)
            .filter(models.IsolationState.research_run_id == graph_sources["run_id"])
            .one()
        )
        assert isolation.is_contaminated == "CLEAN"
        assert db.query(models.KnowledgeNode).count() == 0
        assert db.query(models.KnowledgeEdge).count() == 0
    finally:
        db.close()


def test_prelock_run_cannot_enter_graph_persistence(graph_sources):
    db = TestingSessionLocal()
    try:
        knowledge_graph.KnowledgeGraphService.rebuild(db)
        assert db.query(models.KnowledgeNode).count() == 0
        assert db.query(models.KnowledgeEdge).count() == 0
        assert db.get(models.SemanticClaim, graph_sources["claim_id"]) is not None
    finally:
        db.close()


def test_projection_rebuild_is_deterministic_and_provenance_bound(
    graph_sources, monkeypatch
):
    allow_graph_access(monkeypatch)
    first = rebuild_via_api(graph_sources["run_id"])
    second = rebuild_via_api(graph_sources["run_id"])

    assert first["nodes"] == second["nodes"]
    assert first["edges"] == second["edges"]
    assert all(edge["edge_origin"] == "DOMAIN_PROJECTION" for edge in first["edges"])
    assert all(edge["provenance_ref"] for edge in first["edges"])
    assert {edge["edge_type"] for edge in first["edges"]} >= {
        "GENERATED_IN",
        "DEPENDS_ON",
        "USES_CORPUS",
        "USES_METHODOLOGY",
        "EVALUATED_BY",
    }


def test_projection_deletion_never_deletes_canonical_source(graph_sources, monkeypatch):
    allow_graph_access(monkeypatch)
    rebuild_via_api(graph_sources["run_id"])
    db = TestingSessionLocal()
    try:
        db.query(models.KnowledgeEdge).delete()
        db.query(models.KnowledgeNode).delete()
        db.commit()
        assert db.get(models.SemanticClaim, graph_sources["claim_id"]) is not None
        assert db.get(models.CorpusSnapshot, graph_sources["snapshot_id"]) is not None
    finally:
        db.close()
    rebuilt = rebuild_via_api(graph_sources["run_id"])
    assert rebuilt["analysis"]["node_count"] > 0


def test_dependency_projection_matches_its_governed_source(graph_sources, monkeypatch):
    allow_graph_access(monkeypatch)
    projection = rebuild_via_api(graph_sources["run_id"])
    dependency_edges = [
        edge for edge in projection["edges"] if edge["provenance_ref"].startswith("dependency_record:dep_r1")
    ]
    assert len(dependency_edges) == 2
    assert all(edge["edge_type"] == "DEPENDS_ON" for edge in dependency_edges)


def test_corpus_dependency_projects_only_to_the_matching_snapshot(
    graph_sources, monkeypatch
):
    allow_graph_access(monkeypatch)
    db = TestingSessionLocal()
    try:
        dependency_snapshot = models.CorpusSnapshot(
            id="snap_dependency_r1",
            canonical_text_source="fixture-dependency",
            canonical_text_version="v2",
            canonical_text_hash="fixture-dependency-hash",
            import_revision="import-dependency-r1",
        )
        db.add_all(
            [
                dependency_snapshot,
                models.DependencyRecord(
                    id="dep_corpus_r1",
                    dependent_claim_id=graph_sources["claim_id"],
                    dependency_type="CORPUS_SNAPSHOT",
                    dependency_ref=dependency_snapshot.id,
                    dependency_revision=4,
                ),
            ]
        )
        db.commit()
    finally:
        db.close()
    projection = rebuild_via_api(graph_sources["run_id"])
    snapshot_node = "node::CORPUS_SNAPSHOT::snap_dependency_r1"
    corpus_edges = [
        edge
        for edge in projection["edges"]
        if edge["provenance_ref"] == "dependency_record:dep_corpus_r1:target"
    ]
    assert len(corpus_edges) == 1
    assert corpus_edges[0]["target_node_id"] == snapshot_node


def test_contaminated_blind_lab_run_cannot_read_graph(graph_sources, monkeypatch):
    allow_graph_access(monkeypatch)
    db = TestingSessionLocal()
    try:
        isolation = (
            db.query(models.IsolationState)
            .filter(models.IsolationState.research_run_id == graph_sources["run_id"])
            .one()
        )
        isolation.is_contaminated = "PRIOR_CONTAMINATED"
        db.commit()
    finally:
        db.close()
    response = client.get(f"/runs/{graph_sources['run_id']}/knowledge-graph")
    assert response.status_code == 403
    assert "contaminated" in response.json()["detail"]

    db = TestingSessionLocal()
    try:
        knowledge_graph.KnowledgeGraphService.rebuild(db)
        assert db.query(models.KnowledgeNode).count() == 0
        assert db.query(models.KnowledgeEdge).count() == 0
    finally:
        db.close()


def test_rebuild_removes_projection_when_run_becomes_ineligible(
    graph_sources, monkeypatch
):
    allow_graph_access(monkeypatch)
    rebuild_via_api(graph_sources["run_id"])
    db = TestingSessionLocal()
    try:
        assert db.query(models.KnowledgeNode).count() > 0
        isolation = (
            db.query(models.IsolationState)
            .filter(models.IsolationState.research_run_id == graph_sources["run_id"])
            .one()
        )
        isolation.is_contaminated = "PRIOR_CONTAMINATED"
        db.commit()

        knowledge_graph.KnowledgeGraphService.rebuild(db)

        assert db.query(models.KnowledgeNode).count() == 0
        assert db.query(models.KnowledgeEdge).count() == 0
        assert db.get(models.SemanticClaim, graph_sources["claim_id"]) is not None
    finally:
        db.close()


def test_networkx_analysis_reconstructs_from_persisted_projection(graph_sources, monkeypatch):
    allow_graph_access(monkeypatch)
    rebuild_via_api(graph_sources["run_id"])
    db = TestingSessionLocal()
    try:
        nodes, edges, analysis = knowledge_graph.KnowledgeGraphService.read(
            db, graph_sources["run_id"]
        )
        graph = knowledge_graph.KnowledgeGraphService.to_networkx(nodes, edges)
        assert graph.number_of_nodes() == analysis["node_count"]
        assert graph.number_of_edges() == analysis["edge_count"]
        assert graph.graph == {}
    finally:
        db.close()


def test_reachability_is_exact_and_excludes_unreachable_cross_scope_and_blind_lab_material(
    graph_sources,
):
    db = TestingSessionLocal()
    try:
        other_run = models.ResearchRun(
            id="run_other_reachable",
            target_contract="LOCAL_MEANING",
            target_expression="عدل",
            methodology_revision="method-other",
            corpus_snapshot="missing-other",
            authority_context={"source": "test"},
        )
        blocked_run = models.ResearchRun(
            id="run_blind_lab_blocked",
            target_contract="LOCAL_MEANING",
            target_expression="قول",
            methodology_revision="method-blocked",
            corpus_snapshot="missing-blocked",
            authority_context={"source": "test"},
        )
        db.add_all(
            [
                other_run,
                models.IsolationState(
                    id="iso_other_reachable",
                    research_run_id=other_run.id,
                    target_contract=other_run.target_contract,
                    corpus_snapshot=other_run.corpus_snapshot,
                    methodology_reference=other_run.methodology_revision,
                    allowed_sources=["QURAN_CORPUS"],
                    is_contaminated="CLEAN",
                ),
                models.SemanticClaim(
                    id="claim_other_reachable",
                    research_run_id=other_run.id,
                    contract_type="LOCAL_MEANING",
                ),
                blocked_run,
                models.IsolationState(
                    id="iso_blind_lab_blocked",
                    research_run_id=blocked_run.id,
                    target_contract=blocked_run.target_contract,
                    corpus_snapshot=blocked_run.corpus_snapshot,
                    methodology_reference=blocked_run.methodology_revision,
                    allowed_sources=["QURAN_CORPUS"],
                    is_contaminated="PRIOR_CONTAMINATED",
                ),
                models.SemanticClaim(
                    id="claim_blind_lab_blocked",
                    research_run_id=blocked_run.id,
                    contract_type="LOCAL_MEANING",
                ),
            ]
        )
        db.commit()

        eligible_run_ids = {graph_sources["run_id"], other_run.id, blocked_run.id}
        with patch.object(
            knowledge_graph,
            "has_valid_gate",
            side_effect=lambda _db, run_id, _gate: run_id in eligible_run_ids,
        ):
            knowledge_graph.KnowledgeGraphService.rebuild(db)
            persisted_node_ids = {
                node.node_id for node in db.query(models.KnowledgeNode).all()
            }
            nodes, edges, analysis = knowledge_graph.KnowledgeGraphService.read(
                db, graph_sources["run_id"]
            )

        scoped_node_ids = {node.node_id for node in nodes}
        graph = knowledge_graph.KnowledgeGraphService.to_networkx(nodes, edges)
        run_node_id = "node::RESEARCH_RUN::run_r1"
        expected_reachable_node_ids = {
            "node::CORPUS_SNAPSHOT::snap_r1",
            "node::GATE_REPORT::gate_r1",
            "node::METHODOLOGY_REFERENCE::method-r1",
        }
        unreachable_node_ids = {
            "node::DEPENDENCY_RECORD::dep_r1",
            "node::GOVERNANCE_RULE::rule_r1",
            "node::SEMANTIC_CLAIM::claim_r1",
        }

        assert "node::RESEARCH_RUN::run_other_reachable" in persisted_node_ids
        assert "node::SEMANTIC_CLAIM::claim_other_reachable" in persisted_node_ids
        assert "node::RESEARCH_RUN::run_blind_lab_blocked" not in persisted_node_ids
        assert "node::SEMANTIC_CLAIM::claim_blind_lab_blocked" not in persisted_node_ids
        assert "node::RESEARCH_RUN::run_other_reachable" not in scoped_node_ids
        assert "node::SEMANTIC_CLAIM::claim_other_reachable" not in scoped_node_ids
        assert unreachable_node_ids <= scoped_node_ids
        assert set(analysis["reachable_node_ids"]) == expected_reachable_node_ids
        assert analysis["reachable_node_ids"]
        assert not unreachable_node_ids.intersection(analysis["reachable_node_ids"])
        assert set(nx.descendants(graph, run_node_id)) == expected_reachable_node_ids
    finally:
        db.close()


def test_read_and_networkx_traversal_cannot_mutate_canonical_source(
    graph_sources, monkeypatch
):
    allow_graph_access(monkeypatch)
    rebuild_via_api(graph_sources["run_id"])
    db = TestingSessionLocal()
    try:
        claim = db.get(models.SemanticClaim, graph_sources["claim_id"])
        before = (claim.revision_id, claim.epistemic_state, claim.review_state)
        knowledge_graph.KnowledgeGraphService.read(db, graph_sources["run_id"])
        db.refresh(claim)
        assert (claim.revision_id, claim.epistemic_state, claim.review_state) == before
    finally:
        db.close()


def test_stale_projection_is_replaced_after_source_deletion(graph_sources, monkeypatch):
    allow_graph_access(monkeypatch)
    rebuild_via_api(graph_sources["run_id"])
    db = TestingSessionLocal()
    try:
        db.delete(db.get(models.DependencyRecord, "dep_r1"))
        db.commit()
    finally:
        db.close()
    rebuilt = rebuild_via_api(graph_sources["run_id"])
    assert not any(edge["provenance_ref"].startswith("dependency_record:dep_r1") for edge in rebuilt["edges"])


def test_graph_scope_does_not_expose_another_run(graph_sources, monkeypatch):
    allow_graph_access(monkeypatch)
    db = TestingSessionLocal()
    try:
        other_run = models.ResearchRun(
            id="run_other",
            target_contract="LOCAL_MEANING",
            target_expression="عدل",
            methodology_revision="method-other",
            corpus_snapshot=graph_sources["snapshot_id"],
            authority_context={"source": "test"},
        )
        other_claim = models.SemanticClaim(
            id="claim_other", research_run_id=other_run.id, contract_type="LOCAL_MEANING"
        )
        db.add_all([other_run, other_claim])
        db.commit()
    finally:
        db.close()
    projection = rebuild_via_api(graph_sources["run_id"])
    node_ids = {node["node_id"] for node in projection["nodes"]}
    assert "node::SEMANTIC_CLAIM::claim_other" not in node_ids
    db = TestingSessionLocal()
    try:
        assert (
            db.get(models.KnowledgeNode, "node::SEMANTIC_CLAIM::claim_other") is None
        )
    finally:
        db.close()


@settings(max_examples=12, deadline=None)
@given(
    eligibility=st.lists(
        st.tuples(st.booleans(), st.booleans()), min_size=1, max_size=6
    )
)
def test_mixed_run_eligibility_materially_controls_persisted_projection(
    eligibility,
):
    locked_run_ids: set[str] = set()
    expected_claim_node_ids: set[str] = set()
    property_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=property_engine)
    property_session = sessionmaker(bind=property_engine)
    db = property_session()
    try:
        for index, (has_lock, is_clean) in enumerate(eligibility):
            run_id = f"mixed_run_{index}"
            claim_id = f"mixed_claim_{index}"
            if has_lock:
                locked_run_ids.add(run_id)
            if has_lock and is_clean:
                expected_claim_node_ids.add(f"node::SEMANTIC_CLAIM::{claim_id}")
            db.add_all(
                [
                    models.ResearchRun(
                        id=run_id,
                        target_contract="ROOT_CORE",
                        target_expression=str(index),
                        methodology_revision="method-r1",
                        corpus_snapshot="missing",
                        authority_context={"source": "property"},
                    ),
                    models.IsolationState(
                        id=f"mixed_iso_{index}",
                        research_run_id=run_id,
                        target_contract="ROOT_CORE",
                        corpus_snapshot="missing",
                        methodology_reference="method-r1",
                        allowed_sources=["QURAN_CORPUS"],
                        is_contaminated="CLEAN" if is_clean else "PRIOR_CONTAMINATED",
                    ),
                    models.SemanticClaim(
                        id=claim_id,
                        research_run_id=run_id,
                        contract_type="ROOT_CORE",
                    ),
                ]
            )
        db.commit()
        with patch.object(
            knowledge_graph,
            "has_valid_gate",
            side_effect=lambda _db, run_id, _gate: run_id in locked_run_ids,
        ):
            knowledge_graph.KnowledgeGraphService.rebuild(db)

        projected_claim_node_ids = {
            node.node_id
            for node in db.query(models.KnowledgeNode)
            .filter(models.KnowledgeNode.entity_type == "SEMANTIC_CLAIM")
            .all()
        }
        assert projected_claim_node_ids == expected_claim_node_ids
    finally:
        db.close()
        property_engine.dispose()


def test_candidate_edge_cannot_be_promoted_or_presented_as_established(
    graph_sources, monkeypatch
):
    allow_graph_access(monkeypatch)
    rebuild_via_api(graph_sources["run_id"])
    db = TestingSessionLocal()
    try:
        source = db.get(models.KnowledgeNode, "node::SEMANTIC_CLAIM::claim_r1")
        target = db.get(models.KnowledgeNode, "node::RESEARCH_RUN::run_r1")
        candidate = models.KnowledgeEdge(
            edge_id="candidate_r1",
            source_node_id=source.node_id,
            edge_type="NEIGHBOR_OF",
            target_node_id=target.node_id,
            edge_origin="DISCOVERY_CANDIDATE",
            edge_status="CANDIDATE",
            provenance_ref="test:candidate",
            valid_from_revision="2",
        )
        db.add(candidate)
        db.commit()
    finally:
        db.close()
    response = client.get(f"/runs/{graph_sources['run_id']}/knowledge-graph")
    assert response.status_code == 200
    candidate_response = next(edge for edge in response.json()["edges"] if edge["edge_id"] == "candidate_r1")
    assert candidate_response["presentation_label"] == "DISCOVERY_CANDIDATE_NOT_ESTABLISHED"


@pytest.mark.parametrize(
    ("origin", "expected_label"),
    [
        ("DISCOVERY_CANDIDATE", "DISCOVERY_CANDIDATE_NOT_ESTABLISHED"),
        ("GOVERNED_ASSERTION", "GOVERNED_ASSERTION"),
        ("DOMAIN_PROJECTION", "DERIVED_PROJECTION"),
    ],
)
def test_edge_origin_presentation_labels_preserve_authority(origin, expected_label):
    edge = models.KnowledgeEdge(edge_origin=origin)
    assert knowledge_graph.KnowledgeGraphService.presentation_label(edge) == expected_label


@settings(max_examples=12, deadline=None)
@given(edge_type=st.text(min_size=1, max_size=24).filter(lambda value: value not in {item.value for item in models.GraphEdgeType}))
def test_unsupported_graph_vocabulary_fails_closed(edge_type):
    db = TestingSessionLocal()
    try:
        suffix = uuid.uuid4().hex
        source_id = f"node::TEST::{suffix}:source"
        target_id = f"node::TEST::{suffix}:target"
        db.add_all(
            [
                models.KnowledgeNode(
                    node_id=source_id,
                    entity_type="TEST",
                    entity_id=f"{suffix}:source",
                    entity_revision="1",
                    projection_revision="test",
                    created_at=datetime.utcnow(),
                ),
                models.KnowledgeNode(
                    node_id=target_id,
                    entity_type="TEST",
                    entity_id=f"{suffix}:target",
                    entity_revision="1",
                    projection_revision="test",
                    created_at=datetime.utcnow(),
                ),
            ]
        )
        db.commit()
        db.add(
            models.KnowledgeEdge(
                edge_id=f"edge::{uuid.uuid4().hex}",
                source_node_id=source_id,
                edge_type=edge_type,
                target_node_id=target_id,
                edge_origin="DOMAIN_PROJECTION",
                edge_status="ACTIVE",
                provenance_ref="test:invalid",
                valid_from_revision="1",
            )
        )
        with pytest.raises(ValueError, match="Unsupported governed graph edge type"):
            db.flush()
        db.rollback()
    finally:
        db.close()
