from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, field_validator

from .models import (
    CanonicalState,
    ClaimScope,
    FalsificationStatus,
    ResearchState,
    ResultStrength,
    VerificationState,
)


class BaseSchema(BaseModel):
    @field_validator("*", mode="after")
    @classmethod
    def force_utc(cls, v):
        from datetime import datetime

        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class ResearchStage(str, Enum):
    RESEARCH = "RESEARCH"
    CHALLENGE = "CHALLENGE"
    JUDGMENT = "JUDGMENT"
    CANONICALIZATION = "CANONICALIZATION"


# --- Research Run Schemas ---
class ResearchRunCreate(BaseSchema):
    target_contract: str
    target_expression: str
    model_config = ConfigDict(extra="forbid")


class ResearchRunResponse(BaseSchema):
    id: str
    target_contract: str
    target_expression: str
    methodology_revision: str
    corpus_snapshot: str
    authority_context: dict[str, Any]
    current_stage: ResearchStage
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MethodologyRevisionResponse(BaseSchema):
    id: str
    methodology_id: str
    revision: str
    lifecycle_state: Literal["CURRENT", "RETIRED"]
    authority_reference: str
    source_reference: str
    source_sha256: str
    allowed_use: str
    research_run_eligible: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


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


# --- Research Judgment Schemas ---
class ResearchJudgmentCreate(BaseSchema):
    contract_type: Literal[
        "ROOT_CONCEPT",
        "LEXEME",
        "LOCAL_MEANING",
        "VERSE_MEANING",
        "SEMANTIC_DIFFERENCE",
    ]
    research_state: ResearchState
    claim_scope: ClaimScope
    sampling_basis: str | None = None
    result_strength: ResultStrength
    preferred_conclusion: str | None = None
    root_concept: str | None = None
    plain_explanation: str | None = None
    semantic_boundary: str | None = None
    layer_attribution: dict[str, str] = {}
    supporting_evidence_refs: list[str] = []
    counterevidence_refs: list[str] = []
    unresolved_cases: list[str] = []
    hard_cases: list[str] = []
    strongest_counterexample: str | None = None
    strongest_competitor: str | None = None
    rejection_condition: RejectionCondition | None = None
    falsification_status: FalsificationStatus = FalsificationStatus.NOT_REQUIRED
    reopen_conditions: list[str] = []

    model_config = ConfigDict(extra="forbid")


class SemanticClaimResponse(BaseSchema):
    id: str
    research_run_id: str | None = None
    contract_type: str
    research_state: ResearchState
    canonical_state: CanonicalState
    result_strength: ResultStrength
    verification_state: VerificationState
    falsification_status: FalsificationStatus
    claim_scope: ClaimScope
    sampling_basis: str | None = None
    revision_id: int
    research_completeness: dict[str, Any]
    preferred_conclusion: str | None = None
    root_concept: str | None = None
    plain_explanation: str | None = None
    semantic_boundary: str | None = None
    layer_attribution: dict[str, str]
    rejection_condition: RejectionCondition | None = None
    supporting_evidence: list[str]
    counterevidence: list[str]
    unresolved_cases: list[str]
    hard_cases: list[str]
    strongest_counterexample: str | None = None
    strongest_competitor: str | None = None
    reopen_conditions: list[str]
    accepted_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VerificationRecordCreate(BaseSchema):
    decision: Literal["VERIFIED", "REJECTED"]
    verification_type: str
    rationale: str | None = None
    evidence_refs: list[str] = []
    model_config = ConfigDict(extra="forbid")


class VerificationRecordResponse(VerificationRecordCreate):
    id: str
    claim_id: str
    verifier_identity: str
    evaluated_claim_revision: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CanonicalizationRequest(BaseSchema):
    rationale: str
    model_config = ConfigDict(extra="forbid")


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


class IsolationStateCreate(BaseSchema):
    model_config = ConfigDict(extra="forbid")


class IsolationStateResponse(IsolationStateBase):
    id: str
    research_run_id: str
    created_at: datetime
    establishment_status: str = "NOT_ESTABLISHED"
    prohibited_sources: list[str] | None = None
    input_manifest: dict | None = None
    attesting_actor: str | None = None
    attested_at: datetime | None = None
    audit_ref: str | None = None

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
class HypothesisBase(BaseSchema):
    hypothesis_type: str  # H1, H2, C0
    # Defaults to internal derivation; an external candidate (e.g. Jabal's central
    # meaning) must declare itself so it cannot masquerade as blind internal
    # discovery. External origin grants no confidence bonus and is never canonical.
    origin: Literal[
        "INDEPENDENT_INTERNAL_DERIVATION", "EXTERNAL_CANDIDATE"
    ] = "INDEPENDENT_INTERNAL_DERIVATION"
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


class AIResearchJudgmentResponse(BaseSchema):
    status: Literal["CREATED", "VALIDATION_FAILED", "EXECUTION_FAILED"]
    trace: AIExecutionRecordResponse
    judgment: SemanticClaimResponse | None = None
    failure_reason: str | None = None


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


class KnowledgeExplorerJudgment(BaseSchema):
    claim_id: str
    contract_type: str
    target_expression: str
    research_state: ResearchState
    canonical_state: CanonicalState
    result_strength: ResultStrength
    verification_state: VerificationState
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
    research_state: ResearchState
    canonical_state: CanonicalState
    result_strength: ResultStrength
    verification_state: VerificationState
    falsification_status: FalsificationStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClaimHistoryResponse(BaseSchema):
    claim_id: str
    current_revision: int
    revisions: list[ClaimRevisionItem] = []
    verification_records: list[VerificationRecordResponse] = []
    audit_events: list[AuditLogResponse] = []

    model_config = ConfigDict(from_attributes=True)


class MethodologyFinding(BaseSchema):
    dimension: str
    status: str  # EVALUATED_CLEAN, FLAGGED, NOT_EVALUATED
    severity: str  # NONE, LOW, MEDIUM, HIGH, CRITICAL
    details: str
    evidence_refs: list[str] = []
    hard_blocker: bool = False

    model_config = ConfigDict(from_attributes=True)


class MethodologyDiagnosticsResponse(BaseSchema):
    claim_id: str
    findings: list[MethodologyFinding] = []
    hard_blockers: list[str] = []
    warnings: list[str] = []
    evaluated_at: datetime

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
    canonicalization_candidates: list[SemanticClaimResponse] = []
    reopen_required_claims: list[SemanticClaimResponse] = []
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
    research_judgments: list[SemanticClaimResponse] = []
    judgments_visible: bool
    audit_events: list[AuditLogResponse] = []


class GovernanceOverviewResponse(BaseSchema):
    rules: list[GovernanceRuleResponse] = []
    proposals: list[ChangeProposalResponse] = []
    canonicalization_candidates: list[SemanticClaimResponse] = []
    reopen_required: list[SemanticClaimResponse] = []
    corpus_snapshots: list[CorpusSnapshotResponse] = []
