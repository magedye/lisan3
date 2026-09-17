# دليل عقود البيانات

## طبقات P0
**P0_PERSISTENCE:** SourceIdentity/CorpusSnapshot/Occurrence/StructuralAnnotation/ResearchRun/Observation/EvidenceRelation/Hypothesis/SemanticDecision/ExecutionReceipt/CompletenessProfile/InternalSnapshot.  
**P0_CONTRACT:** LayerAttribution/FalsificationRun/LexicalUnitHypothesis/SemanticNeighborResult/SourceAccessEvent/ExternalComparisonRevision.  
**P0_CAPABILITY:** branching للوحدات المعجمية، مقارنة جار واحد، held-out، falsification، UNRESOLVED.

## الهوية والإصدارات
- كل record يحمل `schema_version`, `record_revision`, و`supersedes_id` الاختياري.
- IDs مستقرة ولا يعاد استخدامها لكيان مختلف.
- التعديل التاريخي لا يكتب فوق السجل بصمت؛ revision جديدة أو record جديد.
- `ExecutionReceipt` append-only.

## العلاقات الأساسية
- CorpusSnapshot → many Occurrence.
- Occurrence → zero/many StructuralAnnotation (الغموض محفوظ).
- ResearchRun → many Observation/Hypothesis/EvidenceRelation/ExecutionReceipt.
- Hypothesis → one/many RejectionCondition عند الحاجة للدحض.
- SemanticDecision → hypotheses/evidence/layer attribution/falsification + one CompletenessProfile.
- InternalSnapshot → one closed SemanticDecision؛ ExternalComparisonRevision → parent InternalSnapshot.

JSON Schemas المولدة في `contracts/schemas/` هي نسخ مشتقة من Pydantic source، وليست مصدرًا أعلى منه.
