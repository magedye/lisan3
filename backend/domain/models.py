import datetime
import enum

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
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

    id = Column(String, primary_key=True, index=True)
    research_run_id = Column(String, ForeignKey("research_runs.id"))
    contract_type = Column(String, nullable=False)
    # The 4 Canonical Independent Axes (UX Constitution v4.0 §5)
    epistemic_state = Column(String, default=EpistemicState.UNRESOLVED.value)
    review_state = Column(String, default=ReviewState.NOT_REVIEWED.value)
    freshness_state = Column(String, default=FreshnessState.CURRENT.value)
    publication_state = Column(String, default=PublicationState.PRIVATE_WORKING.value)

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
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


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
    purity_rating = Column(String, default="PURE")  # PURE, NEAR_PURE, SUSPICIOUS, CONTAMINATED
    purity_findings = Column(JSON, default=list)  # Structured list of PurityFinding objects
    synthetic_data_leak = Column(Boolean, default=False)
    external_data_leak = Column(Boolean, default=False)
    corpus_coverage = Column(Integer, default=0)
    deep_analysis_coverage = Column(Integer, default=0)
    reproducibility_score = Column(Integer, default=0)
    unresolved_conflict_burden = Column(Integer, default=0)
    methodological_purity_flags = Column(JSON, default=list)  # e.g. ["tafsir_contamination", "dictionary_first"]
    evaluation_summary = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

