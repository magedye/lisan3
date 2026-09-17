from __future__ import annotations
from datetime import datetime
from typing import Annotated, Any
from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator
from .enums import *

IdStr=Annotated[str, Field(min_length=3,max_length=128,pattern=r'^[A-Za-z][A-Za-z0-9_.:\-]{2,127}$')]
SemVer=Annotated[str, Field(pattern=r'^\d+\.\d+\.\d+$')]

class StrictRecord(BaseModel):
    model_config=ConfigDict(extra='forbid', validate_assignment=True)
    schema_version: SemVer='2.1.0'
    record_revision: int=Field(default=1,ge=1)
    supersedes_id: IdStr|None=None
    @field_validator('*', mode='before')
    @classmethod
    def no_nan_strings(cls,v): return v

class SourceIdentity(StrictRecord):
    source_id: IdStr; name:str; source_class:SourceClass; source_role:SourceRole
    version:str; sha256:Annotated[str,Field(pattern=r'^[0-9a-f]{64}$')]|None=None
    uri:str|None=None; allowed_phases:list[ResearchPhase]=Field(default_factory=list)
    allowed_fields:list[str]=Field(default_factory=list); forbidden_fields:list[str]=Field(default_factory=list)
class CorpusSnapshot(StrictRecord):
    snapshot_id:IdStr; source_id:IdStr; text_profile_id:IdStr; sha256:Annotated[str,Field(pattern=r'^[0-9a-f]{64}$')]; size_bytes:int=Field(gt=0); verse_count:int=Field(gt=0); encoding:str='UTF-8'; newline:str='LF'; normalization:str='NONE'
class Occurrence(StrictRecord):
    occurrence_id:IdStr; snapshot_id:IdStr; surah:int=Field(ge=1,le=114); ayah:int=Field(ge=1); word_index:int|None=Field(default=None,ge=1); surface_text:str|None=None; target_id:IdStr; source_locator:str|None=None
class StructuralAnnotation(StrictRecord):
    annotation_id:IdStr; occurrence_id:IdStr; source_id:IdStr; root:str|None=None; lemma:str|None=None; form_label:str|None=None; pos:str|None=None; segmentation:list[str]=Field(default_factory=list); syntactic_relations:list[dict[str,Any]]=Field(default_factory=list); ambiguity_notes:list[str]=Field(default_factory=list); review_status:str='UNREVIEWED'; fixture_only:bool=False
class Observation(StrictRecord):
    observation_id:IdStr; run_id:IdStr; statement:str; occurrence_ids:list[IdStr]=Field(min_length=1); layer:InterpretationLayer|None=None; source_ids:list[IdStr]=Field(default_factory=list)
class RejectionCondition(StrictRecord):
    rejection_condition_id:IdStr; hypothesis_id:IdStr; operational_test:str; failure_effect:str
class Hypothesis(StrictRecord):
    hypothesis_id:IdStr; run_id:IdStr; kind:HypothesisKind; statement:str; scope:str; observation_ids:list[IdStr]=Field(default_factory=list); rejection_condition_ids:list[IdStr]=Field(default_factory=list); is_serious_competitor:bool=True; status:str='OPEN'; origin:HypothesisOrigin=HypothesisOrigin.INDEPENDENT_INTERNAL_DERIVATION; origin_source_ids:list[IdStr]=Field(default_factory=list)
class LexicalUnitHypothesis(Hypothesis):
    kind:HypothesisKind=HypothesisKind.LEXICAL_UNIT; branch_label:str; included_occurrence_ids:list[IdStr]=Field(min_length=1); excluded_occurrence_ids:list[IdStr]=Field(default_factory=list)
class LayerAttribution(StrictRecord):
    attribution_id:IdStr; run_id:IdStr; claim_fragment:str; layer:InterpretationLayer; evidence_relation_ids:list[IdStr]=Field(default_factory=list); rationale_brief:str
class EvidenceRelation(StrictRecord):
    evidence_relation_id:IdStr; run_id:IdStr; target_hypothesis_id:IdStr|None=None; target_decision_id:IdStr|None=None; direction:EvidenceDirection; role:EvidenceRole; occurrence_ids:list[IdStr]=Field(default_factory=list); observation_ids:list[IdStr]=Field(default_factory=list); source_ids:list[IdStr]=Field(default_factory=list); note:str
    @model_validator(mode='after')
    def has_target_and_evidence(self):
        if not (self.target_hypothesis_id or self.target_decision_id): raise ValueError('evidence relation requires a target')
        if not (self.occurrence_ids or self.observation_ids or self.source_ids): raise ValueError('evidence relation requires evidence refs')
        return self
class SemanticNeighborResult(StrictRecord):
    neighbor_result_id:IdStr; run_id:IdStr; target_id:IdStr; neighbor_id:IdStr; shared_domain:str|None=None; target_residue:list[str]=Field(default_factory=list); neighbor_residue:list[str]=Field(default_factory=list); tested_dimensions:list[str]=Field(default_factory=list); established_differences:list[str]=Field(default_factory=list); unresolved_differences:list[str]=Field(default_factory=list); same_context_collisions:list[str]=Field(default_factory=list); substitution_cases:list[str]=Field(default_factory=list); counterfactual_losses:list[str]=Field(default_factory=list); disposition:DecisionDisposition
class FalsificationRun(StrictRecord):
    falsification_run_id:IdStr; run_id:IdStr; hypothesis_id:IdStr; rejection_condition_ids:list[IdStr]=Field(min_length=1); tested_occurrence_ids:list[IdStr]=Field(default_factory=list); hard_case_ids:list[str]=Field(default_factory=list); counterevidence_relation_ids:list[IdStr]=Field(default_factory=list); predictions:list[str]=Field(default_factory=list); weakening_conditions:list[str]=Field(default_factory=list); rejection_conditions_text:list[str]=Field(default_factory=list); reopen_conditions:list[str]=Field(default_factory=list); strongest_counterexample:str|None=None; strongest_competitor_id:IdStr|None=None; verdict:str; execution_receipt_ids:list[IdStr]=Field(min_length=1)
class CompletenessDimensionStatus(StrictRecord):
    dimension:CompletenessDimension; expected_count:int|None=Field(default=None,ge=0); examined_count:int|None=Field(default=None,ge=0); status:str; gap_notes:list[str]=Field(default_factory=list)
    @model_validator(mode='after')
    def counts(self):
        if self.expected_count is not None and self.examined_count is not None and self.examined_count>self.expected_count: raise ValueError('examined_count exceeds expected_count')
        return self
class CompletenessProfile(StrictRecord): completeness_profile_id:IdStr; run_id:IdStr; dimensions:list[CompletenessDimensionStatus]=Field(min_length=1); unresolved_gaps:list[str]=Field(default_factory=list)
class ConfidenceComponent(StrictRecord):
    component_id:IdStr; name:str; band:ConfidenceBand; evaluated:bool; reason:str; numeric_value:float|None=None; calibration_version:str|None=None
    @model_validator(mode='after')
    def calibrated_numeric_only(self):
        if self.numeric_value is not None and not self.calibration_version: raise ValueError('numeric confidence requires calibration_version')
        return self
class SemanticBoundaryItem(StrictRecord):
    boundary_item_id:IdStr; category:BoundaryCategory; statement:str; evidence_relation_ids:list[IdStr]=Field(default_factory=list); scope:str; establishment:ClaimEstablishment=ClaimEstablishment.UNKNOWN
class SemanticBoundary(StrictRecord): boundary_id:IdStr; run_id:IdStr; target_id:IdStr; items:list[SemanticBoundaryItem]=Field(min_length=1)
class DecisiveContextAssessment(StrictRecord):
    assessment_id:IdStr; run_id:IdStr; occurrence_id:IdStr; tested_hypothesis_ids:list[IdStr]=Field(min_length=1); effect:DecisiveContextEffect; evidence_relation_ids:list[IdStr]=Field(default_factory=list); structural_sensitivity:str; outcome_brief:str
class SemanticOperatorContribution(StrictRecord):
    contribution_id:IdStr; run_id:IdStr; operator_type:SemanticOperatorType; operator_label:str; general_function:str|None=None; local_realization:str|None=None; evidence_scope:str; evidence_relation_ids:list[IdStr]=Field(default_factory=list); establishment:ClaimEstablishment=ClaimEstablishment.UNKNOWN
class SemanticDerivationStep(StrictRecord):
    step_id:IdStr; run_id:IdStr; stage:SemanticDerivationStage; statement:str; establishment:ClaimEstablishment; evidence_relation_ids:list[IdStr]=Field(default_factory=list); attribution_ids:list[IdStr]=Field(default_factory=list); evidence_scope:str; unresolved_notes:list[str]=Field(default_factory=list)
class SemanticDerivationChain(StrictRecord):
    chain_id:IdStr; run_id:IdStr; target_id:IdStr; analysis_unit:str; steps:list[SemanticDerivationStep]=Field(min_length=1); final_statement:str|None=None
    @model_validator(mode='after')
    def ordered(self):
        order={s:i for i,s in enumerate(SemanticDerivationStage)}
        idx=[order[x.stage] for x in self.steps]
        if idx!=sorted(idx): raise ValueError('semantic derivation steps out of order')
        if len(set(x.stage for x in self.steps))!=len(self.steps): raise ValueError('duplicate semantic derivation stage')
        return self
class ReopenCondition(StrictRecord): reopen_condition_id:IdStr; run_id:IdStr; trigger:str; required_new_evidence:str; affected_result_id:IdStr
class ResearchBlocker(StrictRecord): blocker_id:IdStr; run_id:IdStr; code:str; severity:BlockerSeverity; description:str; affected_result_ids:list[IdStr]=Field(default_factory=list); reopen_condition_ids:list[IdStr]=Field(default_factory=list)
class SemanticDecision(StrictRecord):
    decision_id:IdStr; run_id:IdStr; authority_level:DecisionAuthorityLevel=DecisionAuthorityLevel.RESEARCH_JUDGMENT; disposition:DecisionDisposition; analysis_unit:str; preferred_hypothesis_id:IdStr|None=None; competing_hypothesis_ids:list[IdStr]=Field(default_factory=list); evidence_relation_ids:list[IdStr]=Field(default_factory=list); layer_attribution_ids:list[IdStr]=Field(default_factory=list); falsification_run_ids:list[IdStr]=Field(default_factory=list); neighbor_result_ids:list[IdStr]=Field(default_factory=list); semantic_boundary_id:IdStr|None=None; derivation_chain_ids:list[IdStr]=Field(default_factory=list); decisive_context_ids:list[IdStr]=Field(default_factory=list); blocker_ids:list[IdStr]=Field(default_factory=list); completeness_profile_id:IdStr; confidence_components:list[ConfidenceComponent]=Field(default_factory=list); concise_reason:str; unresolved_items:list[str]=Field(default_factory=list)
    @model_validator(mode='after')
    def preferred_requires_hypothesis(self):
        if self.disposition==DecisionDisposition.PREFERRED and not self.preferred_hypothesis_id: raise ValueError('PREFERRED requires preferred_hypothesis_id')
        return self
class CanonicalAuthorization(StrictRecord):
    authorization_id:IdStr; run_id:IdStr; research_decision_id:IdStr; reviewer_actor_id:str; decision:AuthorizationDecision; decided_at:datetime; rationale_brief:str; evidence_reviewed_ids:list[IdStr]=Field(default_factory=list); verification_ids:list[IdStr]=Field(default_factory=list); supersedes_authorization_id:IdStr|None=None

class ExecutionReceipt(StrictRecord):
    receipt_id:IdStr; run_id:IdStr; actor:ExecutionActor; actor_id:str; actor_version:str; status:ExecutionStatus; started_at:datetime; ended_at:datetime; input_digest:str; output_digest:str|None=None; source_ids:list[IdStr]=Field(default_factory=list); tool_call_id:str|None=None; error_code:str|None=None; retry_of_receipt_id:IdStr|None=None
    @model_validator(mode='after')
    def chronological(self):
        if self.ended_at < self.started_at: raise ValueError('ended_at before started_at')
        return self
class SourceAccessEvent(StrictRecord): event_id:IdStr; run_id:IdStr; phase:ResearchPhase; source_id:IdStr; outcome:SourceAccessOutcome; reason:str; receipt_id:IdStr|None=None
class ResearchRun(StrictRecord): run_id:IdStr; methodology_version:str; terminology_version:str; text_snapshot_id:IdStr; stage:ResearchStage=ResearchStage.CREATED; phase:ResearchPhase=ResearchPhase.INTERNAL_ANALYSIS; created_at:datetime; updated_at:datetime; primary_analysis_unit:str|None=None; execution_receipt_ids:list[IdStr]=Field(default_factory=list)
class InternalSnapshot(StrictRecord): internal_snapshot_id:IdStr; run_id:IdStr; decision_id:IdStr; closed_at:datetime; immutable_digest:str
class ExternalComparisonRevision(StrictRecord): external_revision_id:IdStr; parent_internal_snapshot_id:IdStr; run_id:IdStr; source_ids:list[IdStr]=Field(min_length=1); agreements:list[str]=Field(default_factory=list); disagreements:list[str]=Field(default_factory=list); reopen_internal_research:bool=False
class IndependentVerification(StrictRecord): verification_id:IdStr; run_id:IdStr; kind:VerificationKind; independence_class:IndependenceClass; prior_result_visible:bool; finding:str; evidence_relation_ids:list[IdStr]=Field(default_factory=list); receipt_ids:list[IdStr]=Field(default_factory=list)
class RootResearchArtifact(StrictRecord):
    artifact_id:IdStr; artifact_type:ArtifactType=ArtifactType.ROOT_RESEARCH; run_id:IdStr; root_id:IdStr; decision_id:IdStr; research_scope:str; concept_specification:str; root_concept_summary:str|None=None; semantic_boundary_id:IdStr; illustrative_occurrence_ids:list[IdStr]=Field(default_factory=list); decisive_context_ids:list[IdStr]=Field(default_factory=list); operator_contribution_ids:list[IdStr]=Field(default_factory=list); neighbor_result_ids:list[IdStr]=Field(default_factory=list); derivation_chain_ids:list[IdStr]=Field(default_factory=list); hypothesis_ids:list[IdStr]=Field(default_factory=list); evidence_relation_ids:list[IdStr]=Field(default_factory=list); falsification_run_ids:list[IdStr]=Field(default_factory=list); completeness_profile_id:IdStr; independent_verification_ids:list[IdStr]=Field(default_factory=list); internal_snapshot_id:IdStr|None=None; external_revision_id:IdStr|None=None; standard_conclusion:str; methodology_outcome:str; unresolved_items:list[str]=Field(default_factory=list)
class TermResearchArtifact(StrictRecord):
    artifact_id:IdStr; artifact_type:ArtifactType=ArtifactType.TERM_RESEARCH; run_id:IdStr; term_id:IdStr; lemma:str|None=None; root_id:IdStr|None=None; quran_reference:str|None=None; scope:str; derivation_chain_id:IdStr; local_meaning:str|None=None; alternatives:list[str]=Field(default_factory=list); rejection_reasons:list[str]=Field(default_factory=list); evidence_relation_ids:list[IdStr]=Field(default_factory=list); counterevidence_relation_ids:list[IdStr]=Field(default_factory=list); unknowns:list[str]=Field(default_factory=list); dependency_ids:list[IdStr]=Field(default_factory=list); reopen_condition_ids:list[IdStr]=Field(default_factory=list)
class VerseSemanticAnalysisArtifact(StrictRecord):
    artifact_id:IdStr; artifact_type:ArtifactType=ArtifactType.VERSE_ANALYSIS; run_id:IdStr; verse_id:IdStr; target_term_ids:list[IdStr]=Field(default_factory=list); term_artifact_ids:list[IdStr]=Field(default_factory=list); aggregate_meaning:str; scope:str; evidence_relation_ids:list[IdStr]=Field(default_factory=list); unresolved_items:list[str]=Field(default_factory=list)
class RootCard(StrictRecord):
    artifact_id:IdStr; artifact_type:ArtifactType=ArtifactType.ROOT_CARD; source_root_artifact_id:IdStr; root_id:IdStr; concise_root_concept:str|None=None; boundary_summary:list[str]=Field(default_factory=list); decisive_evidence_ids:list[IdStr]=Field(default_factory=list); neighbor_result_ids:list[IdStr]=Field(default_factory=list); falsification_summary:str; traceability_refs:list[IdStr]=Field(default_factory=list)
class TermCard(StrictRecord):
    artifact_id:IdStr; artifact_type:ArtifactType=ArtifactType.TERM_CARD; source_term_artifact_id:IdStr; term_id:IdStr; root_contribution:str|None=None; inflection_derivation:str|None=None; form_contribution:str|None=None; construction_contribution:str|None=None; context_contribution:str|None=None; local_meaning:str|None=None; traceability_refs:list[IdStr]=Field(default_factory=list)
class MOARoleFinding(StrictRecord): role:MOARole; finding:str; evidence_relation_ids:list[IdStr]=Field(default_factory=list); unresolved_items:list[str]=Field(default_factory=list); receipt_ids:list[IdStr]=Field(default_factory=list)
class MOADeepReviewReport(StrictRecord):
    review_id:IdStr; run_id:IdStr; findings:list[MOARoleFinding]=Field(min_length=2); aggregator_result:str; unresolved_disagreements:list[str]=Field(default_factory=list); consensus_is_evidence:bool=False; independence_class:IndependenceClass=IndependenceClass.NONE
    @model_validator(mode='after')
    def consensus_guard(self):
        if self.consensus_is_evidence: raise ValueError('MOA consensus cannot be evidence by itself')
        return self
class PriorClaimAssessment(StrictRecord): assessment_id:IdStr; run_id:IdStr; original_claim:str; origin_source_id:IdStr; disposition:PriorClaimDisposition; rationale:str; evidence_relation_ids:list[IdStr]=Field(default_factory=list); retained_for_audit:bool=True
class CrossRootConsistencyReview(StrictRecord): review_id:IdStr; run_ids:list[IdStr]=Field(min_length=2); checked_dimensions:list[str]=Field(min_length=1); inconsistencies:list[str]=Field(default_factory=list); resolutions:list[str]=Field(default_factory=list); unresolved_items:list[str]=Field(default_factory=list)
