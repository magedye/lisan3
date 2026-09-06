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
    inspect,
)
from sqlalchemy.orm import relationship

from ..infrastructure.database import Base


class ResearchStage(str, enum.Enum):
    RESEARCH = "RESEARCH"
    CHALLENGE = "CHALLENGE"
    JUDGMENT = "JUDGMENT"
    CANONICALIZATION = "CANONICALIZATION"


class ResearchState(str, enum.Enum):
    PREFERRED = "PREFERRED"
    UNRESOLVED = "UNRESOLVED"
    REJECTED = "REJECTED"


class CanonicalState(str, enum.Enum):
    NOT_CANONICAL = "NOT_CANONICAL"
    ACCEPTED = "ACCEPTED"
    REOPEN_REQUIRED = "REOPEN_REQUIRED"


class ResultStrength(str, enum.Enum):
    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"
    UNRESOLVED = "UNRESOLVED"


class VerificationState(str, enum.Enum):
    NOT_REQUIRED = "NOT_REQUIRED"
    NOT_VERIFIED = "NOT_VERIFIED"
    VERIFIED = "VERIFIED"


class FalsificationStatus(str, enum.Enum):
    NOT_REQUIRED = "NOT_REQUIRED"
    NOT_RUN = "NOT_RUN"
    PASSED = "PASSED"
    FAILED = "FAILED"


class ClaimScope(str, enum.Enum):
    UNIVERSAL = "UNIVERSAL"
    REPRESENTATIVE = "REPRESENTATIVE"
    LOCAL = "LOCAL"


class HypothesisOrigin(str, enum.Enum):
    """Marks where a hypothesis entered, so an external candidate can never be
    presented as blind internal discovery (INT-EXT-001..007; policy doc §9).

    This is the lightest mechanism enforcing that separation; a full permanent
    dual-lane lifecycle is an OPEN, non-owner proposal (SUP-008) and is not built.
    """

    INDEPENDENT_INTERNAL_DERIVATION = "INDEPENDENT_INTERNAL_DERIVATION"
    EXTERNAL_CANDIDATE = "EXTERNAL_CANDIDATE"


class MethodologyRevision(Base):
    __tablename__ = "methodology_revisions"
    __table_args__ = (
        CheckConstraint(
            "lifecycle_state IN ('CURRENT', 'RETIRED')",
            name="ck_methodology_revision_lifecycle",
        ),
        CheckConstraint(
            "length(source_sha256) = 64",
            name="ck_methodology_revision_source_sha256",
        ),
        UniqueConstraint(
            "methodology_id",
            "revision",
            name="uq_methodology_revision_identity",
        ),
    )

    id = Column(String, primary_key=True)
    methodology_id = Column(String, nullable=False, index=True)
    revision = Column(String, nullable=False)
    lifecycle_state = Column(String, nullable=False)
    authority_reference = Column(String, nullable=False)
    source_reference = Column(String, nullable=False)
    source_sha256 = Column(String, nullable=False)
    allowed_use = Column(String, nullable=False)
    research_run_eligible = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)


@event.listens_for(MethodologyRevision, "before_update")
def enforce_methodology_revision_immutability(_mapper, _connection, revision):
    immutable_fields = (
        "methodology_id",
        "revision",
        "authority_reference",
        "source_reference",
        "source_sha256",
        "allowed_use",
        "created_at",
    )
    changed = [
        field
        for field in immutable_fields
        if inspect(revision).attrs[field].history.has_changes()
    ]
    if changed:
        raise ValueError(
            "Methodology revision provenance is immutable; create a new revision "
            "instead of changing: " + ", ".join(changed)
        )


class ResearchRun(Base):
    __tablename__ = "research_runs"

    id = Column(String, primary_key=True, index=True)
    target_contract = Column(String, nullable=False)  # e.g. ROOT_CORE, LOCAL_MEANING
    target_expression = Column(String, nullable=False)
    methodology_revision = Column(String, nullable=False)
    corpus_snapshot = Column(String, nullable=False)
    authority_context = Column(JSON, nullable=False)
    current_stage = Column(String, default=ResearchStage.RESEARCH.value)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    claims = relationship("SemanticClaim", back_populates="research_run")
    ai_execution_records = relationship(
        "AIExecutionRecord", back_populates="research_run"
    )


class SemanticClaim(Base):
    __tablename__ = "semantic_claims"
    __table_args__ = (
        CheckConstraint(
            "research_state IN ('PREFERRED', 'UNRESOLVED', 'REJECTED')",
            name="ck_semantic_claim_research_state",
        ),
        CheckConstraint(
            "canonical_state IN ('NOT_CANONICAL', 'ACCEPTED', 'REOPEN_REQUIRED')",
            name="ck_semantic_claim_canonical_state",
        ),
        CheckConstraint(
            "result_strength IN ('WEAK', 'MODERATE', 'STRONG', 'UNRESOLVED')",
            name="ck_semantic_claim_result_strength",
        ),
        CheckConstraint(
            "verification_state IN ('NOT_REQUIRED', 'NOT_VERIFIED', 'VERIFIED')",
            name="ck_semantic_claim_verification_state",
        ),
        CheckConstraint(
            "falsification_status IN ('NOT_REQUIRED', 'NOT_RUN', 'PASSED', 'FAILED')",
            name="ck_semantic_claim_falsification_status",
        ),
        CheckConstraint(
            "claim_scope IN ('UNIVERSAL', 'REPRESENTATIVE', 'LOCAL')",
            name="ck_semantic_claim_scope",
        ),
    )

    id = Column(String, primary_key=True, index=True)
    research_run_id = Column(String, ForeignKey("research_runs.id"))
    contract_type = Column(String, nullable=False)
    research_state = Column(
        String, nullable=False, default=ResearchState.UNRESOLVED.value
    )
    canonical_state = Column(
        String, nullable=False, default=CanonicalState.NOT_CANONICAL.value
    )
    result_strength = Column(
        String, nullable=False, default=ResultStrength.UNRESOLVED.value
    )
    verification_state = Column(
        String, nullable=False, default=VerificationState.NOT_REQUIRED.value
    )
    falsification_status = Column(
        String, nullable=False, default=FalsificationStatus.NOT_REQUIRED.value
    )
    claim_scope = Column(String, nullable=False, default=ClaimScope.LOCAL.value)
    sampling_basis = Column(String)

    revision_id = Column(Integer, default=1)

    # Host-derived coverage; the AI/client cannot self-certify it.
    research_completeness = Column(JSON, nullable=False, default=dict)

    # Semantic result and layer attribution.
    preferred_conclusion = Column(String)
    root_concept = Column(String)
    plain_explanation = Column(String)
    semantic_boundary = Column(String)
    layer_attribution = Column(JSON, nullable=False, default=dict)

    # Falsification
    rejection_condition = Column(JSON)
    supporting_evidence = Column(JSON, nullable=False, default=list)
    counterevidence = Column(JSON, nullable=False, default=list)
    unresolved_cases = Column(JSON, nullable=False, default=list)
    hard_cases = Column(JSON, nullable=False, default=list)
    strongest_counterexample = Column(String)
    strongest_competitor = Column(String)
    reopen_conditions = Column(JSON, nullable=False, default=list)
    accepted_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    research_run = relationship("ResearchRun", back_populates="claims")


class VerificationRecord(Base):
    __tablename__ = "verification_records"

    id = Column(String, primary_key=True, index=True)
    claim_id = Column(String, ForeignKey("semantic_claims.id"))
    verifier_identity = Column(String, nullable=False)
    verification_type = Column(String, nullable=False)
    decision = Column(String, nullable=False)  # VERIFIED, REJECTED
    rationale = Column(String)
    evidence_refs = Column(JSON, nullable=False, default=list)
    evaluated_claim_revision = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


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
    __table_args__ = (
        UniqueConstraint(
            "canonical_text_source",
            "canonical_text_version",
            "canonical_text_hash",
            name="uq_corpus_snapshot_artifact_identity",
        ),
        CheckConstraint(
            "artifact_size_bytes IS NULL OR artifact_size_bytes > 0",
            name="ck_corpus_snapshot_artifact_size_positive",
        ),
        CheckConstraint(
            "verse_count IS NULL OR verse_count > 0",
            name="ck_corpus_snapshot_verse_count_positive",
        ),
    )

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
    artifact_reference = Column(String, nullable=True)
    artifact_size_bytes = Column(Integer, nullable=True)
    artifact_format = Column(String, nullable=True)
    artifact_verified_at = Column(DateTime, nullable=True)
    artifact_verification_revision = Column(String, nullable=True)
    identity_index_reference = Column(String, nullable=True)
    identity_index_sha256 = Column(String, nullable=True)
    verse_count = Column(Integer, nullable=True)
    canon_001_reconciliation = Column(String, nullable=True)
    fixture_only = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


@event.listens_for(CorpusSnapshot, "before_insert")
@event.listens_for(CorpusSnapshot, "before_update")
def enforce_corpus_snapshot_validation(_mapper, _connection, snapshot):
    from backend.domain.services.corpus.authority import (
        IMPORT_VALIDATED,
        PRODUCTION_ACTIVE,
        import_validation_failures,
        production_validation_failures,
    )

    failures: list[str] = []
    if snapshot.import_validation_status == IMPORT_VALIDATED:
        failures.extend(import_validation_failures(snapshot))
    if (
        snapshot.activation_status == PRODUCTION_ACTIVE
        and snapshot.validation_status != "VALIDATED"
    ):
        failures.append("production-active snapshot must be VALIDATED")
    if (
        snapshot.validation_status == "VALIDATED"
        or snapshot.activation_status == PRODUCTION_ACTIVE
    ):
        failures.extend(production_validation_failures(snapshot))
    if failures:
        raise ValueError(
            "Cannot persist CorpusSnapshot lifecycle transition: "
            + "; ".join(dict.fromkeys(failures))
        )


@event.listens_for(CorpusSnapshot, "before_update")
def preserve_imported_corpus_provenance(_mapper, _connection, snapshot):
    state = inspect(snapshot)
    import_history = state.attrs.import_validation_status.history
    was_import_validated = (
        snapshot.import_validation_status == "IMPORT_VALIDATED"
        or "IMPORT_VALIDATED" in import_history.deleted
    )
    if not was_import_validated:
        return

    immutable_fields = (
        "canonical_text_source",
        "canonical_text_version",
        "canonical_text_hash",
        "source_role_status",
        "artifact_presence_status",
        "expected_canonical_text_hash",
        "hash_verification_status",
        "import_validation_status",
        "artifact_provenance",
        "artifact_reference",
        "artifact_size_bytes",
        "artifact_format",
        "artifact_verified_at",
        "artifact_verification_revision",
        "identity_index_reference",
        "identity_index_sha256",
        "verse_count",
        "canon_001_reconciliation",
        "fixture_only",
    )
    changed = [field for field in immutable_fields if state.attrs[field].history.has_changes()]
    if changed:
        raise ValueError(
            "Cannot mutate imported CorpusSnapshot provenance: " + ", ".join(changed)
        )


class CorpusOccurrence(Base):
    __tablename__ = "corpus_occurrences"
    __table_args__ = (
        UniqueConstraint(
            "snapshot_id", "verse_ref", name="uq_corpus_occurrence_snapshot_verse"
        ),
    )

    id = Column(String, primary_key=True, index=True)
    snapshot_id = Column(
        String, ForeignKey("corpus_snapshots.id"), nullable=False, index=True
    )
    expression = Column(String)
    verse_ref = Column(String, nullable=False)
    text = Column(String, nullable=False)
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
    __table_args__ = (
        CheckConstraint(
            "origin IN ('INDEPENDENT_INTERNAL_DERIVATION', 'EXTERNAL_CANDIDATE')",
            name="ck_hypothesis_origin",
        ),
    )
    id = Column(String, primary_key=True, index=True)
    research_run_id = Column(String, ForeignKey("research_runs.id"))
    hypothesis_type = Column(String)  # H1, H2, C0
    # Blind internal derivation vs a known-source external candidate (e.g. a
    # scholar's central meaning). Defaults to internal so nothing is silently
    # relabelled; an external candidate must declare itself.
    origin = Column(
        String,
        nullable=False,
        default=HypothesisOrigin.INDEPENDENT_INTERNAL_DERIVATION.value,
        server_default=HypothesisOrigin.INDEPENDENT_INTERNAL_DERIVATION.value,
    )
    target_contract = Column(String)
    scope = Column(String)
    statement = Column(String)
    supporting_evidence_refs = Column(JSON)
    counterevidence_refs = Column(JSON)
    unresolved_cases = Column(JSON)
    rejection_condition = Column(JSON)  # Structured object
    provenance = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


@event.listens_for(Hypothesis, "before_update")
def enforce_hypothesis_origin_write_once(_mapper, _connection, hypothesis):
    """Origin is write-once: a recorded external candidate can never be silently
    relabelled as blind internal discovery, and vice-versa."""
    if inspect(hypothesis).attrs.origin.history.has_changes():
        raise ValueError(
            "Hypothesis origin is write-once; it cannot be relabelled after creation"
        )


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


# --- Descriptive Knowledge Base (INT-PRE-OWN-001) ---
# Persisted, reusable, deterministic structural facts. Each row is one
# structural-source attribution of a word occurrence to a root. Counts/profiles
# are DERIVED read-models over these rows (never re-guessed by an LLM). Root/form
# attribution is a reviewable structural annotation, tracked by attribution_status.
class StructuralAttributionStatus(str, enum.Enum):
    CONFIRMED = "CONFIRMED"
    DISPUTED = "DISPUTED"
    UNRESOLVED = "UNRESOLVED"


class StructuralToken(Base):
    __tablename__ = "structural_tokens"
    __table_args__ = (
        CheckConstraint(
            "attribution_status IN ('CONFIRMED', 'DISPUTED', 'UNRESOLVED')",
            name="ck_structural_token_attribution_status",
        ),
        UniqueConstraint(
            "snapshot_id",
            "word_ref",
            "extraction_version",
            name="uq_structural_token_identity",
        ),
        Index("ix_structural_tokens_root", "snapshot_id", "root"),
    )

    id = Column(String, primary_key=True)
    snapshot_id = Column(
        String, ForeignKey("corpus_snapshots.id"), nullable=False, index=True
    )
    word_ref = Column(String, nullable=False)  # e.g. "2:233:53"  (DIRECT location)
    verse_ref = Column(String, nullable=False)  # e.g. "2:233"    (DIRECT location)
    root = Column(String, nullable=False)  # structural annotation (reviewable)
    form = Column(String)  # derived form / morphological group (reviewable)
    pos_tag = Column(String)
    source_id = Column(String, nullable=False)
    source_version = Column(String)
    extraction_version = Column(String, nullable=False)
    attribution_status = Column(
        String, nullable=False, default=StructuralAttributionStatus.CONFIRMED.value
    )
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# --- Unified External Hypothesis Register (INT-EXT-001..007) ---
# One mechanism for every external claim. External sources generate hypotheses
# and tests only; they never gain authority and carry NO confidence field.
class ExternalClaimType(str, enum.Enum):
    ROOT_MEANING_CANDIDATE = "ROOT_MEANING_CANDIDATE"
    FORM_EFFECT_CANDIDATE = "FORM_EFFECT_CANDIDATE"
    DERIVATIONAL_EFFECT_CANDIDATE = "DERIVATIONAL_EFFECT_CANDIDATE"
    LETTER_EFFECT_CANDIDATE = "LETTER_EFFECT_CANDIDATE"
    CONSTRUCTION_EFFECT_CANDIDATE = "CONSTRUCTION_EFFECT_CANDIDATE"
    METHOD_RULE_CANDIDATE = "METHOD_RULE_CANDIDATE"


class ExternalClaimRole(str, enum.Enum):
    RULE_CLAIM = "RULE_CLAIM"
    AUTHOR_APPLICATION = "AUTHOR_APPLICATION"


class ExternalHypothesisStatus(str, enum.Enum):
    EXTERNAL_CANDIDATE = "EXTERNAL_CANDIDATE"
    TESTED = "TESTED"
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    NOT_SUPPORTED = "NOT_SUPPORTED"
    FALSIFIED = "FALSIFIED"
    UNRESOLVED = "UNRESOLVED"


class ExternalHypothesisRecord(Base):
    __tablename__ = "external_hypothesis_records"
    __table_args__ = (
        CheckConstraint(
            "claim_type IN ('ROOT_MEANING_CANDIDATE', 'FORM_EFFECT_CANDIDATE', "
            "'DERIVATIONAL_EFFECT_CANDIDATE', 'LETTER_EFFECT_CANDIDATE', "
            "'CONSTRUCTION_EFFECT_CANDIDATE', 'METHOD_RULE_CANDIDATE')",
            name="ck_external_hypothesis_claim_type",
        ),
        CheckConstraint(
            "claim_role IN ('RULE_CLAIM', 'AUTHOR_APPLICATION')",
            name="ck_external_hypothesis_claim_role",
        ),
        CheckConstraint(
            "status IN ('EXTERNAL_CANDIDATE', 'TESTED', 'SUPPORTED', "
            "'PARTIALLY_SUPPORTED', 'NOT_SUPPORTED', 'FALSIFIED', 'UNRESOLVED')",
            name="ck_external_hypothesis_status",
        ),
        Index("ix_external_hypothesis_target", "claim_type", "target_scope"),
    )

    id = Column(String, primary_key=True, index=True)
    claim_type = Column(String, nullable=False)
    source = Column(String, nullable=False)  # e.g. "المعجم الاشتقاقي المؤصل"
    author = Column(String, nullable=False)  # e.g. "محمد حسن حسن جبل"
    source_locator = Column(String)  # URL / page / entry
    claim = Column(String, nullable=False)
    normalized_claim = Column(String)
    target_scope = Column(String, nullable=False)  # root / form / letter / rule id
    claim_role = Column(
        String, nullable=False, default=ExternalClaimRole.RULE_CLAIM.value
    )
    status = Column(
        String, nullable=False, default=ExternalHypothesisStatus.EXTERNAL_CANDIDATE.value
    )
    test_plan = Column(String)
    test_evidence_refs = Column(JSON, nullable=False, default=list)
    counterevidence_refs = Column(JSON, nullable=False, default=list)
    result = Column(String)
    provenance = Column(String, nullable=False)
    research_run_id = Column(String, ForeignKey("research_runs.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


@event.listens_for(ExternalHypothesisRecord, "before_insert")
@event.listens_for(ExternalHypothesisRecord, "before_update")
def enforce_external_hypothesis_vocabulary(_mapper, _connection, record):
    """External claims carry no confidence/authority; only governed vocabulary."""
    if record.claim_type not in {item.value for item in ExternalClaimType}:
        raise ValueError("Unsupported external hypothesis claim_type")
    if record.claim_role not in {item.value for item in ExternalClaimRole}:
        raise ValueError("Unsupported external hypothesis claim_role")
    if record.status not in {item.value for item in ExternalHypothesisStatus}:
        raise ValueError("Unsupported external hypothesis status")
    if not record.provenance:
        raise ValueError("External hypothesis requires provenance")


# --- Campaign checkpoint / resume state ---
# A durable, queryable campaign cursor so a session/runtime interruption cannot
# lose progress. The campaign runner (Request 02) reads/writes this.
class CampaignState(Base):
    __tablename__ = "campaign_states"
    id = Column(String, primary_key=True, index=True)
    campaign_id = Column(String, nullable=False, unique=True)
    methodology_revision = Column(String)
    corpus_snapshot = Column(String)
    queue = Column(JSON, nullable=False, default=list)  # roots pending
    completed_roots = Column(JSON, nullable=False, default=list)
    current_batch = Column(JSON, nullable=False, default=dict)
    findings = Column(JSON, nullable=False, default=list)
    status = Column(String, nullable=False, default="INITIALIZED")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
