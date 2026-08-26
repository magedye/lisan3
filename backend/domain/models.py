import datetime
import enum

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    String,
    UniqueConstraint,
    event,
)
from sqlalchemy.orm import relationship

from ..infrastructure.database import Base


class ResearchStage(str, enum.Enum):
    PREFLIGHT = "PREFLIGHT"
    ISOLATION_PREFLIGHT = "ISOLATION_PREFLIGHT"
    CORPUS_COLLECTION = "CORPUS_COLLECTION"
    STRUCTURAL_OBSERVATION = "STRUCTURAL_OBSERVATION"
    HYPOTHESIS_GENERATION = "HYPOTHESIS_GENERATION"
    DIFFERENTIATION = "DIFFERENTIATION"
    LOCKING = "LOCKING"


class EpistemicState(str, enum.Enum):
    OBSERVATION = "OBSERVATION"
    HYPOTHESIS = "HYPOTHESIS"
    TESTED = "TESTED"
    SUPPORTED = "SUPPORTED"
    LOCK_BLOCKED = "LOCK_BLOCKED"
    LOCK_INTERNAL_RESULT = "LOCK_INTERNAL_RESULT"
    REJECTED = "REJECTED"
    UNRESOLVED = "UNRESOLVED"


class ReviewState(str, enum.Enum):
    NOT_REVIEWED = "NOT_REVIEWED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    OWNER_DECISION_REQUIRED = "OWNER_DECISION_REQUIRED"


class FreshnessState(str, enum.Enum):
    CURRENT = "CURRENT"
    STALE = "STALE"
    INVALIDATED = "INVALIDATED"
    REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"


class PublicationState(str, enum.Enum):
    PRIVATE_WORKING = "PRIVATE_WORKING"
    REVIEWABLE = "REVIEWABLE"
    PUBLISHABLE = "PUBLISHABLE"
    PUBLISHED = "PUBLISHED"
    WITHDRAWN = "WITHDRAWN"


class OfficialStatus(str, enum.Enum):
    """Legacy alias preserved for compatibility."""

    UNRESOLVED = "UNRESOLVED"
    LOCK_BLOCKED = "LOCK_BLOCKED"
    LOCK_INTERNAL_RESULT = "LOCK_INTERNAL_RESULT"
    REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"


class ResearchRun(Base):
    __tablename__ = "research_runs"

    id = Column(String, primary_key=True, index=True)
    target_contract = Column(String, nullable=False)  # e.g. ROOT_CORE, LOCAL_MEANING
    target_expression = Column(String, nullable=False)
    methodology_revision = Column(String, nullable=False)
    corpus_snapshot = Column(String, nullable=False)
    authority_context = Column(JSON, nullable=False)
    current_stage = Column(String, default=ResearchStage.PREFLIGHT.value)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    claims = relationship("SemanticClaim", back_populates="research_run")
    gate_reports = relationship("GateReport", back_populates="research_run")
    ai_execution_records = relationship(
        "AIExecutionRecord", back_populates="research_run"
    )


class SemanticClaim(Base):
    __tablename__ = "semantic_claims"
    __table_args__ = (
        CheckConstraint(
            "epistemic_state IN ('OBSERVATION', 'HYPOTHESIS', 'TESTED', "
            "'SUPPORTED', 'LOCK_BLOCKED', 'LOCK_INTERNAL_RESULT', 'REJECTED', "
            "'UNRESOLVED')",
            name="ck_semantic_claim_epistemic_state",
        ),
        CheckConstraint(
            "review_state IN ('NOT_REVIEWED', 'REVIEW_REQUIRED', 'IN_REVIEW', "
            "'APPROVED', 'REJECTED', 'OWNER_DECISION_REQUIRED')",
            name="ck_semantic_claim_review_state",
        ),
        CheckConstraint(
            "freshness_state IN ('CURRENT', 'STALE', 'INVALIDATED', "
            "'REVALIDATION_REQUIRED')",
            name="ck_semantic_claim_freshness_state",
        ),
        CheckConstraint(
            "publication_state IN ('PRIVATE_WORKING', 'REVIEWABLE', "
            "'PUBLISHABLE', 'PUBLISHED', 'WITHDRAWN')",
            name="ck_semantic_claim_publication_state",
        ),
    )

    id = Column(String, primary_key=True, index=True)
    research_run_id = Column(String, ForeignKey("research_runs.id"))
    contract_type = Column(String, nullable=False)
    # The 4 Canonical Independent Axes (UX Constitution v4.0 §5)
    epistemic_state = Column(
        String, nullable=False, default=EpistemicState.UNRESOLVED.value
    )
    review_state = Column(String, nullable=False, default=ReviewState.NOT_REVIEWED.value)
    freshness_state = Column(
        String, nullable=False, default=FreshnessState.CURRENT.value
    )
    publication_state = Column(
        String, nullable=False, default=PublicationState.PRIVATE_WORKING.value
    )

    revision_id = Column(Integer, default=1)

    # Coverage Profile
    index_coverage = Column(String)
    deep_analysis_coverage = Column(String)

    # Core Semantics
    abstract_root_core = Column(String)
    root_definition = Column(String)
    root_meaning = Column(String)
    root_concept = Column(String)

    # Falsification
    rejection_condition = Column(String)
    supporting_evidence = Column(JSON)
    counterevidence = Column(JSON)
    unresolved_cases = Column(JSON)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    research_run = relationship("ResearchRun", back_populates="claims")


class ReviewDecision(Base):
    __tablename__ = "review_decisions"

    id = Column(String, primary_key=True, index=True)
    claim_id = Column(String, ForeignKey("semantic_claims.id"))
    reviewer_identity = Column(String, nullable=False)
    decision = Column(String, nullable=False)  # APPROVED, REJECTED, REQUEST_REVISION
    rationale = Column(String)
    evaluated_claim_revision = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class GateReport(Base):
    __tablename__ = "gate_reports"

    id = Column(String, primary_key=True, index=True)
    research_run_id = Column(String, ForeignKey("research_runs.id"))
    gate_code = Column(String, nullable=False)
    display_name = Column(String, nullable=True)
    status = Column(String, nullable=False)  # PASSED, FAILED, BLOCKED
    evidence_refs = Column(JSON, nullable=True)
    failure_reason = Column(String)
    evaluated_revision = Column(String)
    required_action = Column(String)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    research_run = relationship("ResearchRun", back_populates="gate_reports")


class AIExecutionRecord(Base):
    __tablename__ = "ai_execution_records"
    id = Column(String, primary_key=True, index=True)
    research_run_id = Column(String, ForeignKey("research_runs.id"), nullable=False)
    analysis_stage = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    model = Column(String, nullable=False)
    skill_version = Column(String)
    prompt_revision = Column(String)
    tools_available = Column(JSON)
    input_artifact_refs = Column(JSON)
    output_artifact_refs = Column(JSON)
    execution_status = Column(String, nullable=False)  # SUCCESS, FAILED
    error_message = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    research_run = relationship("ResearchRun", back_populates="ai_execution_records")


class IsolationState(Base):
    __tablename__ = "isolation_states"

    id = Column(String, primary_key=True, index=True)
    research_run_id = Column(String, ForeignKey("research_runs.id"), unique=True)
    target_contract = Column(String)
    corpus_snapshot = Column(String)
    methodology_reference = Column(String)
    allowed_sources = Column(JSON)
    is_contaminated = Column(String, default="CLEAN")  # CLEAN, PRIOR_CONTAMINATED
    contamination_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ObservationArtifact(Base):
    __tablename__ = "observation_artifacts"

    id = Column(String, primary_key=True, index=True)
    research_run_id = Column(String, ForeignKey("research_runs.id"))
    occurrence_ref = Column(String, nullable=False)
    form = Column(String)
    syntax = Column(String)
    participant_roles = Column(String)
    local_context = Column(String)
    unresolved_ambiguity = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class CorpusSnapshot(Base):
    __tablename__ = "corpus_snapshots"

    id = Column(String, primary_key=True, index=True)
    canonical_text_source = Column(String, nullable=False)
    canonical_text_version = Column(String, nullable=False)
    canonical_text_hash = Column(String, nullable=False)
    structural_source = Column(String)
    structural_source_version = Column(String)
    import_revision = Column(String)
    validation_status = Column(String, default="PENDING")
    source_role_status = Column(String, nullable=False, default="SOURCE_ROLE_PENDING")
    artifact_presence_status = Column(
        String, nullable=False, default="ARTIFACT_MISSING"
    )
    expected_canonical_text_hash = Column(String, nullable=True)
    hash_verification_status = Column(String, nullable=False, default="HASH_UNVERIFIED")
    import_validation_status = Column(String, nullable=False, default="IMPORT_PENDING")
    activation_status = Column(
        String, nullable=False, default="CANONICAL_ACTIVATION_PENDING"
    )
    artifact_provenance = Column(String, nullable=True)
    fixture_only = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


@event.listens_for(CorpusSnapshot, "before_insert")
@event.listens_for(CorpusSnapshot, "before_update")
def enforce_corpus_snapshot_validation(_mapper, _connection, snapshot):
    if snapshot.validation_status != "VALIDATED":
        return

    from backend.domain.services.corpus.authority import production_validation_failures

    failures = production_validation_failures(snapshot)
    if failures:
        raise ValueError(
            "Cannot persist production VALIDATED CorpusSnapshot: " + "; ".join(failures)
        )


class CorpusOccurrence(Base):
    __tablename__ = "corpus_occurrences"

    id = Column(String, primary_key=True, index=True)
    snapshot_id = Column(String, index=True)
    expression = Column(String)
    verse_ref = Column(String)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class IsolationEvent(Base):
    __tablename__ = "isolation_events"
    id = Column(String, primary_key=True, index=True)
    research_run_id = Column(String, ForeignKey("research_runs.id"))
    attempted_action = Column(String)
    was_blocked = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Hypothesis(Base):
    __tablename__ = "hypotheses"
    id = Column(String, primary_key=True, index=True)
    research_run_id = Column(String, ForeignKey("research_runs.id"))
    hypothesis_type = Column(String)  # H1, H2, C0
    target_contract = Column(String)
    scope = Column(String)
    statement = Column(String)
    supporting_evidence_refs = Column(JSON)
    counterevidence_refs = Column(JSON)
    unresolved_cases = Column(JSON)
    rejection_condition = Column(JSON)  # Structured object
    provenance = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class EssentialNeighbor(Base):
    __tablename__ = "essential_neighbors"
    id = Column(String, primary_key=True, index=True)
    hypothesis_id = Column(String, ForeignKey("hypotheses.id"))
    shared_domain = Column(String)
    positive_distinguishing_candidate = Column(String)
    relevant_differentiation_axes = Column(JSON)
    substitution_probe = Column(String)
    boundary_negative_cases = Column(JSON)
    supporting_evidence = Column(JSON)
    counterevidence = Column(JSON)
    unresolved_distinction = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# --- Governance (Slice E) ---
class GovernanceRule(Base):
    __tablename__ = "governance_rules"
    id = Column(String, primary_key=True, index=True)
    rule_code = Column(String, unique=True, nullable=False)
    description = Column(String)
    active_revision = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class RuleRevision(Base):
    __tablename__ = "rule_revisions"
    id = Column(String, primary_key=True, index=True)
    rule_code = Column(String, ForeignKey("governance_rules.rule_code"))
    revision_number = Column(Integer, nullable=False)
    changes_described = Column(String)
    approved_by = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ChangeProposal(Base):
    __tablename__ = "change_proposals"
    id = Column(String, primary_key=True, index=True)
    rule_code = Column(String, ForeignKey("governance_rules.rule_code"))
    proposed_changes = Column(String)
    impact_analysis = Column(JSON)  # affected dependencies
    status = Column(String, default="PROPOSED")  # PROPOSED, APPROVED, REJECTED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class DependencyRecord(Base):
    __tablename__ = "dependency_records"
    id = Column(String, primary_key=True, index=True)
    dependent_claim_id = Column(String, ForeignKey("semantic_claims.id"))
    dependency_type = Column(
        String, nullable=False
    )  # e.g. "GOVERNANCE_RULE", "CORPUS_SNAPSHOT"
    dependency_ref = Column(String, nullable=False)  # e.g. rule_code
    dependency_revision = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# --- R1 Knowledge Graph projection ---
# These tables are derived from the governed records above.  They must never be
# used as a second source of semantic authority.
class GraphEdgeOrigin(str, enum.Enum):
    DOMAIN_PROJECTION = "DOMAIN_PROJECTION"
    GOVERNED_ASSERTION = "GOVERNED_ASSERTION"
    DISCOVERY_CANDIDATE = "DISCOVERY_CANDIDATE"


class GraphEdgeStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INVALIDATED = "INVALIDATED"
    GOVERNED = "GOVERNED"
    CANDIDATE = "CANDIDATE"


class GraphEdgeType(str, enum.Enum):
    OCCURS_IN = "OCCURS_IN"
    SUPPORTS = "SUPPORTS"
    CHALLENGES = "CHALLENGES"
    DEPENDS_ON = "DEPENDS_ON"
    DERIVED_FROM = "DERIVED_FROM"
    USES_CORPUS = "USES_CORPUS"
    USES_METHODOLOGY = "USES_METHODOLOGY"
    EVALUATED_BY = "EVALUATED_BY"
    INVALIDATED_BY = "INVALIDATED_BY"
    GENERATED_IN = "GENERATED_IN"
    NEIGHBOR_OF = "NEIGHBOR_OF"
    DISTINGUISHED_FROM = "DISTINGUISHED_FROM"


class KnowledgeNode(Base):
    __tablename__ = "knowledge_nodes"
    __table_args__ = (
        UniqueConstraint("entity_type", "entity_id", name="uq_knowledge_node_entity"),
    )

    node_id = Column(String, primary_key=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    entity_revision = Column(String, nullable=False)
    projection_revision = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


class KnowledgeEdge(Base):
    __tablename__ = "knowledge_edges"
    __table_args__ = (
        CheckConstraint(
            "edge_origin IN ('DOMAIN_PROJECTION', 'GOVERNED_ASSERTION', 'DISCOVERY_CANDIDATE')",
            name="ck_knowledge_edge_origin",
        ),
        CheckConstraint(
            "edge_status IN ('ACTIVE', 'INVALIDATED', 'GOVERNED', 'CANDIDATE')",
            name="ck_knowledge_edge_status",
        ),
        CheckConstraint(
            "edge_type IN ('OCCURS_IN', 'SUPPORTS', 'CHALLENGES', 'DEPENDS_ON', "
            "'DERIVED_FROM', 'USES_CORPUS', 'USES_METHODOLOGY', 'EVALUATED_BY', "
            "'INVALIDATED_BY', 'GENERATED_IN', 'NEIGHBOR_OF', 'DISTINGUISHED_FROM')",
            name="ck_knowledge_edge_type",
        ),
    )

    edge_id = Column(String, primary_key=True)
    source_node_id = Column(
        String, ForeignKey("knowledge_nodes.node_id"), nullable=False
    )
    edge_type = Column(String, nullable=False)
    target_node_id = Column(
        String, ForeignKey("knowledge_nodes.node_id"), nullable=False
    )
    edge_origin = Column(String, nullable=False)
    edge_status = Column(String, nullable=False)
    provenance_ref = Column(String, nullable=False)
    valid_from_revision = Column(String, nullable=False)
    invalidated_at = Column(DateTime, nullable=True)


@event.listens_for(KnowledgeEdge, "before_insert")
@event.listens_for(KnowledgeEdge, "before_update")
def enforce_knowledge_edge_authority(_mapper, _connection, edge):
    """Fail closed when a graph relation lacks governed vocabulary or origin."""
    valid_types = {item.value for item in GraphEdgeType}
    valid_origins = {item.value for item in GraphEdgeOrigin}
    valid_statuses = {item.value for item in GraphEdgeStatus}
    if edge.edge_type not in valid_types:
        raise ValueError("Unsupported governed graph edge type")
    if edge.edge_origin not in valid_origins:
        raise ValueError("Unsupported graph edge origin")
    if edge.edge_status not in valid_statuses:
        raise ValueError("Unsupported graph edge status")
    if not edge.provenance_ref:
        raise ValueError("Graph edges require provenance")
    if edge.edge_origin == GraphEdgeOrigin.DISCOVERY_CANDIDATE.value:
        if edge.edge_status != GraphEdgeStatus.CANDIDATE.value:
            raise ValueError("Discovery candidates must remain candidate edges")
    elif edge.edge_origin == GraphEdgeOrigin.GOVERNED_ASSERTION.value:
        if edge.edge_status != GraphEdgeStatus.GOVERNED.value:
            raise ValueError("Governed assertions require governed status")
    elif edge.edge_status not in {
        GraphEdgeStatus.ACTIVE.value,
        GraphEdgeStatus.INVALIDATED.value,
    }:
        raise ValueError("Domain projections require an active or invalidated status")
    if (
        edge.edge_type
        in {
            GraphEdgeType.NEIGHBOR_OF.value,
            GraphEdgeType.DISTINGUISHED_FROM.value,
        }
        and edge.edge_origin == GraphEdgeOrigin.DOMAIN_PROJECTION.value
    ):
        raise ValueError("Semantic neighbor relations cannot be domain projections")


# --- R2 derived vector evaluation infrastructure ---
# These records are disposable evaluation state. The current schema deliberately
# rejects production-eligible vectors until a governed model handoff exists.
class SemanticEmbedding(Base):
    __tablename__ = "semantic_embeddings"
    __table_args__ = (
        CheckConstraint(
            "embedding_space IN ('VERSE_CONTEXT', 'STRUCTURAL_PROFILE', "
            "'HYPOTHESIS', 'CLAIM', 'ROOT_CANDIDATE', 'EXTERNAL_RESEARCH')",
            name="ck_semantic_embedding_space",
        ),
        CheckConstraint(
            "provenance_class IN ('BENCHMARK_ONLY', 'SYNTHETIC_EVALUATION')",
            name="ck_semantic_embedding_provenance",
        ),
        CheckConstraint(
            "production_eligible = 0",
            name="ck_semantic_embedding_evaluation_only",
        ),
        CheckConstraint("dimensions > 0", name="ck_semantic_embedding_dimensions"),
        CheckConstraint(
            "lifecycle_state IN ('CURRENT', 'STALE')",
            name="ck_semantic_embedding_lifecycle",
        ),
        CheckConstraint(
            "(lifecycle_state = 'CURRENT' AND source_eligible = 1 "
            "AND invalidated_reason IS NULL) OR "
            "(lifecycle_state = 'STALE' AND invalidated_reason IS NOT NULL)",
            name="ck_semantic_embedding_current_eligibility",
        ),
        UniqueConstraint(
            "research_run_id",
            "entity_type",
            "entity_id",
            "embedding_space",
            "embedding_model",
            "embedding_model_revision",
            "model_config_hash",
            "source_revision",
            name="uq_semantic_embedding_identity",
        ),
        Index(
            "ix_semantic_embeddings_current_scope",
            "research_run_id",
            "embedding_space",
            "lifecycle_state",
            "model_config_hash",
        ),
    )

    id = Column(String, primary_key=True)
    research_run_id = Column(String, ForeignKey("research_runs.id"), nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    embedding_space = Column(String, nullable=False)
    embedding_model = Column(String, nullable=False)
    embedding_model_revision = Column(String, nullable=False)
    model_config_hash = Column(String, nullable=False)
    source_revision = Column(String, nullable=False)
    source_hash = Column(String, nullable=False)
    vector = Column(LargeBinary, nullable=False)
    dimensions = Column(Integer, nullable=False)
    provenance_class = Column(String, nullable=False)
    production_eligible = Column(Boolean, nullable=False, default=False)
    source_eligible = Column(Boolean, nullable=False, default=True)
    index_revision = Column(String, nullable=False)
    lifecycle_state = Column(String, nullable=False, default="CURRENT")
    invalidated_reason = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)


@event.listens_for(SemanticEmbedding, "before_insert")
@event.listens_for(SemanticEmbedding, "before_update")
def enforce_semantic_embedding_evaluation_boundary(_mapper, _connection, embedding):
    from backend.domain.vector_contracts import (
        EmbeddingSpace,
        ExperimentalVectorProvenance,
    )

    if embedding.embedding_space not in {item.value for item in EmbeddingSpace}:
        raise ValueError("Unsupported embedding space")
    if embedding.provenance_class not in {
        item.value for item in ExperimentalVectorProvenance
    }:
        raise ValueError("Unsupported experimental vector provenance")
    if embedding.production_eligible:
        raise ValueError("R2 evaluation infrastructure cannot store production vectors")
    if embedding.dimensions <= 0 or len(embedding.vector) != embedding.dimensions * 4:
        raise ValueError("Vector BLOB must contain exactly dimensions float32 values")
    if embedding.lifecycle_state == "CURRENT":
        if not embedding.source_eligible or embedding.invalidated_reason is not None:
            raise ValueError("Current vectors require an eligible source")
    elif embedding.lifecycle_state == "STALE":
        if not embedding.invalidated_reason:
            raise ValueError("Stale vectors require an invalidation reason")
    else:
        raise ValueError("Unsupported vector lifecycle state")


# --- Steward (Slice F) ---
class StewardCommand(Base):
    __tablename__ = "steward_commands"
    id = Column(String, primary_key=True, index=True)
    command_type = Column(String, nullable=False)
    intent = Column(String)
    parameters = Column(JSON)
    evaluated_rules = Column(JSON)
    execution_status = Column(String, default="PENDING")
    result_summary = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# --- Knowledge & Operations (Slice G) ---
class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True, index=True)
    entity_id = Column(String, index=True)
    entity_type = Column(String, nullable=False)
    action = Column(String, nullable=False)
    previous_state = Column(String)
    new_state = Column(String)
    actor = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class QualityProfile(Base):
    __tablename__ = "quality_profiles"
    id = Column(String, primary_key=True, index=True)
    claim_id = Column(String, ForeignKey("semantic_claims.id"))
    purity_score = Column(Integer)  # 0 to 100
    purity_rating = Column(
        String, default="PURE"
    )  # PURE, NEAR_PURE, SUSPICIOUS, CONTAMINATED
    purity_findings = Column(
        JSON, default=list
    )  # Structured list of PurityFinding objects
    synthetic_data_leak = Column(Boolean, default=False)
    external_data_leak = Column(Boolean, default=False)
    corpus_coverage = Column(Integer, default=0)
    deep_analysis_coverage = Column(Integer, default=0)
    reproducibility_score = Column(Integer, default=0)
    unresolved_conflict_burden = Column(Integer, default=0)
    methodological_purity_flags = Column(
        JSON, default=list
    )  # e.g. ["tafsir_contamination", "dictionary_first"]
    evaluation_summary = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
