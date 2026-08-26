"""R1 derived Knowledge Graph projection and read-only analysis boundary."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from datetime import datetime, timezone

import networkx as nx
from sqlalchemy.orm import Session

from .. import models
from .claim_visibility import ClaimReleasePolicy

PROJECTION_REVISION = "R1_GRAPH_PROJECTION_V1"


class GraphAccessForbidden(Exception):
    """Raised when a Blind Lab run has not reached internal lock."""


class GraphSourceNotFound(Exception):
    """Raised for an unknown research run."""


def _node_id(entity_type: str, entity_id: str) -> str:
    return f"node::{entity_type}::{entity_id}"


def _edge_id(*parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:24]
    return f"edge::{digest}"


def _timestamp(value: datetime | None) -> datetime:
    if value is None:
        return datetime(1970, 1, 1, tzinfo=timezone.utc).replace(tzinfo=None)
    return value.replace(tzinfo=None) if value.tzinfo else value


def _revision(value: object | None) -> str:
    return str(value) if value is not None else "1"


class KnowledgeGraphService:
    """Builds SQLite-derived projections; it never writes canonical source records."""

    @staticmethod
    def _is_projection_eligible(db: Session, run: models.ResearchRun) -> bool:
        """Return whether current canonical state permits graph projection."""
        return ClaimReleasePolicy.evaluate_run(db, run.id).released

    @staticmethod
    def require_read_access(db: Session, run_id: str) -> models.ResearchRun:
        run = db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()
        if run is None:
            raise GraphSourceNotFound(run_id)
        decision = ClaimReleasePolicy.evaluate_run(db, run_id)
        if not decision.released:
            raise GraphAccessForbidden(f"Graph access blocked: {decision.reason}")
        return run

    @staticmethod
    def rebuild(db: Session) -> None:
        """Replace the disposable projection from current governed source state."""
        db.query(models.KnowledgeEdge).delete(synchronize_session=False)
        db.query(models.KnowledgeNode).delete(synchronize_session=False)

        nodes: dict[str, models.KnowledgeNode] = {}

        def add_node(
            entity_type: str,
            entity_id: str,
            entity_revision: object | None,
            created_at: datetime | None,
        ) -> models.KnowledgeNode:
            node_id = _node_id(entity_type, entity_id)
            node = nodes.get(node_id)
            if node is None:
                node = models.KnowledgeNode(
                    node_id=node_id,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    entity_revision=_revision(entity_revision),
                    projection_revision=PROJECTION_REVISION,
                    created_at=_timestamp(created_at),
                )
                nodes[node_id] = node
                db.add(node)
            return node

        def add_edge(
            source: models.KnowledgeNode,
            edge_type: models.GraphEdgeType,
            target: models.KnowledgeNode,
            provenance_ref: str,
            valid_from_revision: object | None,
        ) -> None:
            db.add(
                models.KnowledgeEdge(
                    edge_id=_edge_id(
                        source.node_id,
                        edge_type.value,
                        target.node_id,
                        provenance_ref,
                        _revision(valid_from_revision),
                    ),
                    source_node_id=source.node_id,
                    edge_type=edge_type.value,
                    target_node_id=target.node_id,
                    edge_origin=models.GraphEdgeOrigin.DOMAIN_PROJECTION.value,
                    edge_status=models.GraphEdgeStatus.ACTIVE.value,
                    provenance_ref=provenance_ref,
                    valid_from_revision=_revision(valid_from_revision),
                )
            )

        snapshots = {
            snapshot.id: snapshot
            for snapshot in db.query(models.CorpusSnapshot).order_by(models.CorpusSnapshot.id)
        }
        rules = {
            rule.rule_code: rule
            for rule in db.query(models.GovernanceRule).order_by(models.GovernanceRule.rule_code)
        }
        runs = [
            run
            for run in db.query(models.ResearchRun).order_by(models.ResearchRun.id)
            if KnowledgeGraphService._is_projection_eligible(db, run)
        ]
        claims = db.query(models.SemanticClaim).order_by(models.SemanticClaim.id).all()
        claims_by_run: dict[str, list[models.SemanticClaim]] = {}
        for claim in claims:
            if claim.research_run_id:
                claims_by_run.setdefault(claim.research_run_id, []).append(claim)
        gates_by_run: dict[str, list[models.GateReport]] = {}
        for gate in db.query(models.GateReport).order_by(models.GateReport.id):
            if gate.research_run_id:
                gates_by_run.setdefault(gate.research_run_id, []).append(gate)
        dependencies_by_claim: dict[str, list[models.DependencyRecord]] = {}
        for dependency in db.query(models.DependencyRecord).order_by(models.DependencyRecord.id):
            dependencies_by_claim.setdefault(dependency.dependent_claim_id, []).append(
                dependency
            )

        for run in runs:
            run_node = add_node("RESEARCH_RUN", run.id, run.updated_at, run.created_at)
            methodology_node = add_node(
                "METHODOLOGY_REFERENCE",
                run.methodology_revision,
                run.methodology_revision,
                run.created_at,
            )
            add_edge(
                run_node,
                models.GraphEdgeType.USES_METHODOLOGY,
                methodology_node,
                f"research_run:{run.id}:methodology_revision",
                run.updated_at,
            )
            snapshot = snapshots.get(str(run.corpus_snapshot))
            if snapshot is not None:
                snapshot_node = add_node(
                    "CORPUS_SNAPSHOT",
                    snapshot.id,
                    snapshot.import_revision or snapshot.canonical_text_version,
                    snapshot.created_at,
                )
                add_edge(
                    run_node,
                    models.GraphEdgeType.USES_CORPUS,
                    snapshot_node,
                    f"research_run:{run.id}:corpus_snapshot",
                    run.updated_at,
                )
            for gate in gates_by_run.get(str(run.id), []):
                gate_node = add_node(
                    "GATE_REPORT", gate.id, gate.evaluated_revision, gate.created_at
                )
                add_edge(
                    run_node,
                    models.GraphEdgeType.EVALUATED_BY,
                    gate_node,
                    f"gate_report:{gate.id}",
                    gate.evaluated_revision,
                )
            for claim in claims_by_run.get(str(run.id), []):
                claim_node = add_node(
                    "SEMANTIC_CLAIM", claim.id, claim.revision_id, claim.created_at
                )
                add_edge(
                    claim_node,
                    models.GraphEdgeType.GENERATED_IN,
                    run_node,
                    f"semantic_claim:{claim.id}:research_run",
                    claim.revision_id,
                )
                for dependency in dependencies_by_claim.get(str(claim.id), []):
                    dependency_node = add_node(
                        "DEPENDENCY_RECORD",
                        dependency.id,
                        dependency.dependency_revision,
                        dependency.created_at,
                    )
                    add_edge(
                        claim_node,
                        models.GraphEdgeType.DEPENDS_ON,
                        dependency_node,
                        f"dependency_record:{dependency.id}",
                        dependency.dependency_revision,
                    )
                    if dependency.dependency_type == "CORPUS_SNAPSHOT":
                        target_snapshot = snapshots.get(dependency.dependency_ref)
                        if target_snapshot is not None:
                            target_node = add_node(
                                "CORPUS_SNAPSHOT",
                                target_snapshot.id,
                                target_snapshot.import_revision
                                or target_snapshot.canonical_text_version,
                                target_snapshot.created_at,
                            )
                            add_edge(
                                dependency_node,
                                models.GraphEdgeType.DEPENDS_ON,
                                target_node,
                                f"dependency_record:{dependency.id}:target",
                                dependency.dependency_revision,
                            )
                    elif dependency.dependency_type == "GOVERNANCE_RULE":
                        rule = rules.get(str(dependency.dependency_ref))
                        if rule is not None:
                            rule_node = add_node(
                                "GOVERNANCE_RULE",
                                rule.id,
                                rule.active_revision,
                                rule.created_at,
                            )
                            add_edge(
                                dependency_node,
                                models.GraphEdgeType.DEPENDS_ON,
                                rule_node,
                                f"dependency_record:{dependency.id}:target",
                                dependency.dependency_revision,
                            )
        db.commit()

    @staticmethod
    def _scoped_node_ids(db: Session, run: models.ResearchRun) -> set[str]:
        scoped = {_node_id("RESEARCH_RUN", run.id), _node_id("METHODOLOGY_REFERENCE", run.methodology_revision)}
        if db.query(models.CorpusSnapshot).filter(models.CorpusSnapshot.id == run.corpus_snapshot).first():
            scoped.add(_node_id("CORPUS_SNAPSHOT", run.corpus_snapshot))
        for claim in (
            db.query(models.SemanticClaim)
            .filter(models.SemanticClaim.research_run_id == run.id)
            .all()
        ):
            scoped.add(_node_id("SEMANTIC_CLAIM", claim.id))
            for dependency in (
                db.query(models.DependencyRecord)
                .filter(models.DependencyRecord.dependent_claim_id == claim.id)
                .all()
            ):
                scoped.add(_node_id("DEPENDENCY_RECORD", dependency.id))
                if dependency.dependency_type == "CORPUS_SNAPSHOT":
                    scoped.add(_node_id("CORPUS_SNAPSHOT", dependency.dependency_ref))
                elif dependency.dependency_type == "GOVERNANCE_RULE":
                    rule = (
                        db.query(models.GovernanceRule)
                        .filter(models.GovernanceRule.rule_code == dependency.dependency_ref)
                        .first()
                    )
                    if rule is not None:
                        scoped.add(_node_id("GOVERNANCE_RULE", rule.id))
        for gate in (
            db.query(models.GateReport)
            .filter(models.GateReport.research_run_id == run.id)
            .all()
        ):
            scoped.add(_node_id("GATE_REPORT", gate.id))
        return scoped

    @staticmethod
    def to_networkx(
        nodes: Iterable[models.KnowledgeNode], edges: Iterable[models.KnowledgeEdge]
    ) -> nx.MultiDiGraph:
        graph = nx.MultiDiGraph()
        for node in nodes:
            graph.add_node(
                node.node_id,
                entity_type=node.entity_type,
                entity_id=node.entity_id,
                entity_revision=node.entity_revision,
            )
        for edge in edges:
            graph.add_edge(
                edge.source_node_id,
                edge.target_node_id,
                key=edge.edge_id,
                edge_type=edge.edge_type,
                edge_origin=edge.edge_origin,
                edge_status=edge.edge_status,
                provenance_ref=edge.provenance_ref,
            )
        return graph

    @classmethod
    def read(cls, db: Session, run_id: str) -> tuple[list[models.KnowledgeNode], list[models.KnowledgeEdge], dict[str, object]]:
        run = cls.require_read_access(db, run_id)
        scoped_ids = cls._scoped_node_ids(db, run)
        nodes = (
            db.query(models.KnowledgeNode)
            .filter(models.KnowledgeNode.node_id.in_(scoped_ids))
            .order_by(models.KnowledgeNode.node_id)
            .all()
            if scoped_ids
            else []
        )
        present_ids = {node.node_id for node in nodes}
        edges = (
            db.query(models.KnowledgeEdge)
            .filter(
                models.KnowledgeEdge.source_node_id.in_(present_ids),
                models.KnowledgeEdge.target_node_id.in_(present_ids),
            )
            .order_by(models.KnowledgeEdge.edge_id)
            .all()
            if present_ids
            else []
        )
        graph = cls.to_networkx(nodes, edges)
        cycle_nodes = sorted({node for cycle in nx.simple_cycles(graph) for node in cycle})
        run_node_id = _node_id("RESEARCH_RUN", run_id)
        reachable = (
            sorted(nx.descendants(graph, run_node_id)) if run_node_id in graph else []
        )
        return nodes, edges, {
            "node_count": graph.number_of_nodes(),
            "edge_count": graph.number_of_edges(),
            "cycle_node_ids": cycle_nodes,
            "reachable_node_ids": reachable,
        }

    @staticmethod
    def presentation_label(edge: models.KnowledgeEdge) -> str:
        if edge.edge_origin == models.GraphEdgeOrigin.DISCOVERY_CANDIDATE.value:
            return "DISCOVERY_CANDIDATE_NOT_ESTABLISHED"
        if edge.edge_origin == models.GraphEdgeOrigin.GOVERNED_ASSERTION.value:
            return "GOVERNED_ASSERTION"
        return "DERIVED_PROJECTION"
