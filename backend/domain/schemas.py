from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, field_validator

from .models import EpistemicState, FreshnessState, PublicationState, ReviewState


class BaseSchema(BaseModel):
    @field_validator("*", mode="after")
    @classmethod
    def force_utc(cls, v):
        from datetime import datetime

        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class ResearchStage(str, Enum):
    PREFLIGHT = "PREFLIGHT"
    ISOLATION_PREFLIGHT = "ISOLATION_PREFLIGHT"
    CORPUS_COLLECTION = "CORPUS_COLLECTION"
    STRUCTURAL_OBSERVATION = "STRUCTURAL_OBSERVATION"
    HYPOTHESIS_GENERATION = "HYPOTHESIS_GENERATION"
    DIFFERENTIATION = "DIFFERENTIATION"
    LOCKING = "LOCKING"


class OfficialStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    CANDIDATE_HYPOTHESIS = "CANDIDATE_HYPOTHESIS"
    SPARSE_EVIDENCE_CEILING = "SPARSE_EVIDENCE_CEILING"
    LOCK_BLOCKED = "LOCK_BLOCKED"
    LOCK_INTERNAL_RESULT = "LOCK_INTERNAL_RESULT"
    REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"


# --- Research Run Schemas ---
class ResearchRunBase(BaseSchema):
    target_contract: str
    target_expression: str
    methodology_revision: str
    corpus_snapshot: str
    authority_context: dict[str, Any]


class ResearchRunCreate(ResearchRunBase):
    pass


class ResearchRunResponse(ResearchRunBase):
    id: str
    current_stage: ResearchStage
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Semantic Claim Schemas ---
class SemanticClaimBase(BaseSchema):
    contract_type: str
    # The 4 Canonical Independent Axes (UX Constitution v4.0 §5)
    epistemic_state: EpistemicState = EpistemicState.UNRESOLVED
    review_state: ReviewState = ReviewState.NOT_REVIEWED
    freshness_state: FreshnessState = FreshnessState.CURRENT
    publication_state: PublicationState = PublicationState.PRIVATE_WORKING
    revision_id: int = 1
    index_coverage: str | None = None
    deep_analysis_coverage: str | None = None
    abstract_root_core: str | None = None
    root_definition: str | None = None
    root_meaning: str | None = None
    root_concept: str | None = None
    rejection_condition: str | None = None
    supporting_evidence: dict[str, Any] | None = None
    counterevidence: dict[str, Any] | None = None
    unresolved_cases: dict[str, Any] | None = None


class SemanticClaimCreate(SemanticClaimBase):
    research_run_id: str


class SemanticClaimResponse(SemanticClaimBase):
    id: str
    # Historical/governance claims may predate ResearchRun linkage. The create
    # contract still requires a run, while read models must preserve that
    # persisted distinction instead of failing serialization.
    research_run_id: str | None = None


class ReviewDecisionBase(BaseSchema):
    reviewer_identity: str
    decision: Literal["APPROVED", "REJECTED"]
    rationale: str | None = None


class ReviewDecisionCreate(ReviewDecisionBase):
    pass


class ReviewDecisionResponse(ReviewDecisionBase):
    id: str
    claim_id: str
    evaluated_claim_revision: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PublicationRequest(BaseSchema):
    publisher_identity: str
    target_registry: str

    model_config = ConfigDict(from_attributes=True)


# --- Ask Lisan Schemas ---
class AskLisanRequest(BaseSchema):
    expression: str
    contract_type: str


class AskLisanResponse(BaseSchema):
    status: str  # e.g. INSUFFICIENT_EVIDENCE, FOUND
    claim: SemanticClaimResponse | None = None


# --- Blind Lab Schemas ---
class IsolationStateBase(BaseSchema):
    target_contract: str
    corpus_snapshot: str
    methodology_reference: str
    allowed_sources: list[str]
    is_contaminated: str = "CLEAN"
    contamination_reason: str | None = None


class IsolationStateCreate(IsolationStateBase):
    pass


class IsolationStateResponse(IsolationStateBase):
    id: str
    research_run_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ObservationArtifactBase(BaseSchema):
    occurrence_ref: str
    form: str | None = None
    syntax: str | None = None
    participant_roles: str | None = None
    local_context: str | None = None
    unresolved_ambiguity: str | None = None


class ObservationArtifactCreate(ObservationArtifactBase):
    model_config = ConfigDict(extra="forbid")


class ObservationArtifactResponse(ObservationArtifactBase):
    id: str
    research_run_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CorpusOccurrenceBase(BaseSchema):
    snapshot_id: str
    expression: str
    verse_ref: str
    text: str


class CorpusOccurrenceResponse(CorpusOccurrenceBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Slice C Schemas ---
class RejectionCondition(BaseSchema):
    challenging_finding: str
    search_location: str
    verification_method: str
    confounder_control: str
    failure_consequence: str

    def model_post_init(self, __context: Any) -> None:
        circular_phrases = [
            "if wrong",
            "if incorrect",
            "if it fails",
            "reject if false",
        ]
        combined = f"{self.challenging_finding} {self.verification_method}".lower()
        for phrase in circular_phrases:
            if phrase in combined:
                raise ValueError("Rejection condition cannot be circular.")


class HypothesisBase(BaseSchema):
    hypothesis_type: str  # H1, H2, C0
    target_contract: str
    scope: str
    statement: str
    supporting_evidence_refs: list[str]
    counterevidence_refs: list[str]
    unresolved_cases: list[str]
    rejection_condition: RejectionCondition
    provenance: str


class HypothesisCreate(HypothesisBase):
    pass


class HypothesisResponse(HypothesisBase):
    id: str
    research_run_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EssentialNeighborBase(BaseSchema):
    shared_domain: str
    positive_distinguishing_candidate: str
    relevant_differentiation_axes: list[str]
    substitution_probe: str
    boundary_negative_cases: list[str]
    supporting_evidence: list[str]
    counterevidence: list[str]
    unresolved_distinction: str


class EssentialNeighborCreate(EssentialNeighborBase):
    pass


class EssentialNeighborResponse(EssentialNeighborBase):
    id: str
    hypothesis_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GateReportBase(BaseSchema):
    gate_code: str
    status: str
    evidence_refs: list[str]
    failure_reason: str | None = None
    evaluated_revision: str
    required_action: str | None = None


class GateReportCreate(GateReportBase):
    pass


class GateReportResponse(GateReportBase):
    id: str
    research_run_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- AI Runtime Schemas ---
class AIExecutionRecordBase(BaseSchema):
    analysis_stage: str
    provider: str
    model: str
    skill_version: str | None = None
    prompt_revision: str | None = None
    tools_available: list[str] | None = None
    input_artifact_refs: list[str] | None = None
    output_artifact_refs: list[str] | None = None
    execution_status: str
    error_message: str | None = None


class AIExecutionRecordCreate(AIExecutionRecordBase):
    pass


class AIExecutionRecordResponse(AIExecutionRecordBase):
    id: str
    research_run_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HypothesisProposal(BaseSchema):
    hypothesis_type: str
    target_contract: str
    scope: str
    statement: str
    rationale: str
    supporting_evidence_refs: list[str]
    unresolved_cases: list[str]
    rejection_condition: RejectionCondition


class EssentialNeighborProposal(BaseSchema):
    shared_domain: str
    positive_distinguishing_candidate: str
    relevant_differentiation_axes: list[str]
    substitution_probe: str
    boundary_negative_cases: list[str]
    unresolved_distinction: str


# --- Governance (Slice E) ---
class GovernanceRuleBase(BaseSchema):
    rule_code: str
    description: str


class GovernanceRuleCreate(GovernanceRuleBase):
    pass


class GovernanceRuleResponse(GovernanceRuleBase):
    id: str
    active_revision: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RuleRevisionResponse(BaseSchema):
    id: str
    rule_code: str
    revision_number: int
    changes_described: str | None = None
    approved_by: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChangeProposalCreate(BaseSchema):
    rule_code: str
    proposed_changes: str


class ChangeProposalResponse(BaseSchema):
    id: str
    rule_code: str
    proposed_changes: str
    impact_analysis: dict
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RuleHistoryResponse(BaseSchema):
    rule_code: str
    description: str | None = None
    active_revision: int
    revisions: list[RuleRevisionResponse] = []
    proposals: list[ChangeProposalResponse] = []

    model_config = ConfigDict(from_attributes=True)


class DependencyRecordResponse(BaseSchema):
    id: str
    dependent_claim_id: str
    dependency_type: str
    dependency_ref: str
    dependency_revision: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LegacyKnowledgeExplorerClaim(BaseSchema):
    claim_id: str
    contract_type: str
    target_expression: str
    epistemic_state: str
    review_state: str
    freshness_state: str
    publication_state: str
    dependencies: list[DependencyRecordResponse]
    affected_by: list[str]  # List of rules/snapshots that can invalidate this node

    model_config = ConfigDict(from_attributes=True)


# --- R1 Knowledge Graph read models ---
class GraphKnowledgeNodeResponse(BaseSchema):
    node_id: str
    entity_type: str
    entity_id: str
    entity_revision: str
    projection_revision: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GraphKnowledgeEdgeResponse(BaseSchema):
    edge_id: str
    source_node_id: str
    edge_type: str
    target_node_id: str
    edge_origin: str
    edge_status: str
    provenance_ref: str
    valid_from_revision: str
    invalidated_at: datetime | None = None
    presentation_label: str

    model_config = ConfigDict(from_attributes=True)


class GraphAnalysisResponse(BaseSchema):
    node_count: int
    edge_count: int
    cycle_node_ids: list[str]
    reachable_node_ids: list[str]


class KnowledgeGraphResponse(BaseSchema):
    run_id: str
    projection_revision: str
    nodes: list[GraphKnowledgeNodeResponse]
    edges: list[GraphKnowledgeEdgeResponse]
    analysis: GraphAnalysisResponse
    authority_notice: str


class KnowledgeGraphRebuildResponse(KnowledgeGraphResponse):
    rebuilt: bool


# --- Steward (Slice F) ---
class StewardCommandBase(BaseSchema):
    command_type: str
    intent: str
    parameters: dict


class StewardCommandCreate(StewardCommandBase):
    pass


class StewardCommandResponse(StewardCommandBase):
    id: str
    evaluated_rules: dict | None = None
    execution_status: str
    result_summary: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Knowledge & Operations (Slice G) ---
class AuditLogResponse(BaseSchema):
    id: str
    entity_id: str
    entity_type: str
    action: str
    previous_state: str | None = None
    new_state: str | None = None
    actor: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseSchema):
    status: str
    message: str
    details: dict | None = None

    model_config = ConfigDict(from_attributes=True)


class ClaimRevisionItem(BaseSchema):
    revision_id: int
    epistemic_state: str
    review_state: str
    freshness_state: str
    publication_state: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClaimHistoryResponse(BaseSchema):
    claim_id: str
    current_revision: int
    revisions: list[ClaimRevisionItem] = []
    review_decisions: list[ReviewDecisionResponse] = []
    audit_events: list[AuditLogResponse] = []

    model_config = ConfigDict(from_attributes=True)


class PurityFinding(BaseSchema):
    dimension: str
    status: str  # EVALUATED_CLEAN, FLAGGED, NOT_EVALUATED_IN_PROFILE
    severity: str  # NONE, LOW, MEDIUM, HIGH, CRITICAL
    details: str

    model_config = ConfigDict(from_attributes=True)


class QualityProfileResponse(BaseSchema):
    available: bool
    source: Literal[
        "PERSISTED_QUALITY_PROFILE", "DERIVED_METHODOLOGICAL_PURITY_ONLY"
    ]
    id: str | None = None
    claim_id: str
    purity_score: int | None = None
    purity_rating: str = "PURE"  # PURE, NEAR_PURE, SUSPICIOUS, CONTAMINATED
    purity_findings: list[PurityFinding] = []
    synthetic_data_leak: bool | None = None
    external_data_leak: bool | None = None
    corpus_coverage: int | None = None
    deep_analysis_coverage: int | None = None
    reproducibility_score: int | None = None
    unresolved_conflict_burden: int | None = None
    methodological_purity_flags: list[str] = []
    evaluation_summary: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ReproductionManifestResponse(BaseSchema):
    claim_id: str
    target_expression: str | None = None
    methodology_revision: str | None = None
    corpus_snapshot_id: str | None = None
    ai_execution_traces: list[str] = []
    dependencies: list[dict] = []
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Production UI read models ---
class CorpusSnapshotResponse(BaseSchema):
    id: str
    canonical_text_source: str
    canonical_text_version: str
    validation_status: str
    source_role_status: str
    artifact_presence_status: str
    hash_verification_status: str
    import_validation_status: str
    activation_status: str
    artifact_provenance: str | None = None
    fixture_only: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RunAdmissionStateResponse(BaseSchema):
    available: bool
    corpus_snapshot_ids: list[str] = []
    methodology_revisions: list[str] = []
    blockers: list[str] = []


class AttentionCenterResponse(BaseSchema):
    recent_runs: list[ResearchRunResponse] = []
    review_required_claims: list[SemanticClaimResponse] = []
    freshness_attention_claims: list[SemanticClaimResponse] = []
    pending_proposals: list[ChangeProposalResponse] = []
    recent_changes: list[AuditLogResponse] = []
    corpus_snapshots: list[CorpusSnapshotResponse] = []
    run_admission: RunAdmissionStateResponse


class RunWorkspaceResponse(BaseSchema):
    run: ResearchRunResponse
    isolation_state: IsolationStateResponse | None = None
    observations: list[ObservationArtifactResponse] = []
    hypotheses: list[HypothesisResponse] = []
    neighbors: list[EssentialNeighborResponse] = []
    gates: list[GateReportResponse] = []
    claims: list[SemanticClaimResponse] = []
    claims_visible: bool
    audit_events: list[AuditLogResponse] = []


class GovernanceOverviewResponse(BaseSchema):
    rules: list[GovernanceRuleResponse] = []
    proposals: list[ChangeProposalResponse] = []
    review_queue: list[SemanticClaimResponse] = []
    freshness_queue: list[SemanticClaimResponse] = []
    corpus_snapshots: list[CorpusSnapshotResponse] = []
