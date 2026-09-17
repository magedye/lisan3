from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field
from .records import *
from .enums import *
class ToolModel(BaseModel): model_config=ConfigDict(extra='forbid')
class GetOccurrencesRequest(ToolModel): target_id:str; text_profile_id:str
class GetOccurrencesResponse(ToolModel): occurrences:list[Occurrence]; receipt:ExecutionReceipt
class GetVerseRequest(ToolModel): surah:int=Field(ge=1,le=114); ayah:int=Field(ge=1); text_profile_id:str
class GetVerseResponse(ToolModel): verse_id:str; exact_text:str; receipt:ExecutionReceipt
class GetContextRequest(ToolModel): occurrence_id:str; window_policy:str='VERSE_ONLY'
class GetContextResponse(ToolModel): occurrence_id:str; context_verse_ids:list[str]; exact_texts:list[str]; receipt:ExecutionReceipt
class GetMorphologyRequest(ToolModel): occurrence_id:str
class GetMorphologyResponse(ToolModel): annotations:list[StructuralAnnotation]; receipt:ExecutionReceipt
class GetDerivationalFamilyRequest(ToolModel): root_id:str; text_profile_id:str
class GetDerivationalFamilyResponse(ToolModel): root_id:str; occurrence_ids:list[str]; annotations:list[StructuralAnnotation]; receipt:ExecutionReceipt
class GetSyntacticRelationsRequest(ToolModel): occurrence_id:str
class GetSyntacticRelationsResponse(ToolModel): occurrence_id:str; relations:list[dict[str,Any]]; receipt:ExecutionReceipt
class GetCollocationsRequest(ToolModel): target_id:str; scope:str; text_profile_id:str
class GetCollocationsResponse(ToolModel): target_id:str; counts:dict[str,int]; receipt:ExecutionReceipt
class CalculateCompletenessRequest(ToolModel): run_id:str
class CalculateCompletenessResponse(ToolModel): profile:CompletenessProfile; receipt:ExecutionReceipt
class ValidateEvidenceRefsRequest(ToolModel): run_id:str; evidence_relation_ids:list[str]
class ValidateEvidenceRefsResponse(ToolModel): valid:bool; missing_refs:list[str]; receipt:ExecutionReceipt
class ApplySourcePolicyRequest(ToolModel): source_id:str; phase:ResearchPhase; requested_fields:list[str]=Field(default_factory=list)
class ApplySourcePolicyResponse(ToolModel): outcome:SourceAccessOutcome; allowed_fields:list[str]; denied_fields:list[str]; reason:str; receipt:ExecutionReceipt
class CalculateConfidenceComponentsRequest(ToolModel): run_id:str; calibration_version:str|None=None
class CalculateConfidenceComponentsResponse(ToolModel): components:list[ConfidenceComponent]; overall_numeric:float|None=None; receipt:ExecutionReceipt
class RetrieveExternalSourcesRequest(ToolModel): run_id:str; query:str; source_classes:list[SourceClass]=Field(default_factory=list)
class RetrieveExternalSourcesResponse(ToolModel): source_records:list[dict[str,Any]]; receipt:ExecutionReceipt
class RecordToolExecutionRequest(ToolModel): receipt:ExecutionReceipt
class RecordToolExecutionResponse(ToolModel): stored:bool; receipt_id:str
