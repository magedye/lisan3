---
DOCUMENT_ID: C04
TITLE: "Derived Cards, Cumulative Research Record & Publication Handoff Guide"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: OPERATIONAL_COMPANION
STATUS: CANONICAL_BASELINE
PURPOSE: "قوالب تشغيلية مشتقة لسجل البحث وبطاقات الجذر/المفردة وتسليم النشر دون إنشاء سلطة دلالية."
SCOPE: "إنشاء research artifacts وderived read models بعد/أثناء تطبيق البروتوكول."
ACTIVATION_CONDITION: "عند طلب سجل بحث كامل أو بطاقة مشتقة أو handoff للنشر/API/UI."
DEPENDS_ON: [M01, A01, A03, A04, A05, A11, A14, A15]
EXPANDS_MASTER_SECTIONS: [M01-P13, M01-R34]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Standalone root/term card candidate templates where they conflict with v1.1 governance"
---

# C04 — Derived Cards, Cumulative Research Record & Publication Handoff Guide

## 1. Cumulative Research Record

#### C04-O01 — CUMULATIVE_RESEARCH_RECORD
القالب الأدنى:
```yaml
metadata:
  run_id:
  target:
  analysis_unit:
  claim_scope:
  methodology_version: QURAN_LISAN_V1.1
  corpus_identity:
  execution_status:
  coverage_profile:
  quality_profile:
  created_at:
  updated_at:
  reopen_if:

concept_specification:
  root_identity:
  coverage:
  invariance:
  layer_neutrality:
  positive_content:
  lexical_distinctiveness:
  falsifiability:
  predictive_content:
  non_circularity:
  operationalization:
  compositional_traceability:
  traceability:

hypotheses:
claims:
evidence:
counterevidence:
dependencies:
semantic_boundary:
essential_neighbors:
local_realizations:
decisive_contexts:
internal_result_snapshot:
external_comparison:
methodology_observations:
```
`methodology_observations` لا تعدل Master تلقائيًا؛ تُرفع عبر A00 Rule Escalation.

## 2. Root Card

#### C04-O02 — ROOT_CARD
```yaml
artifact_type: ROOT_CARD
artifact_role: DERIVED_READ_MODEL
research_authority: NONE
identity:
  root_letters:
  corpus_identity:
semantic_result:
  root_axial_meaning: null
  root_definition: null
  root_meaning_explanation: null
  root_concept_model: null
semantic_boundary:
  required: []
  permitted: []
  excluded: []
  unknown: []
semantic_family:
  essential_neighbors: []
  supporting_neighbors: []
  distinctive_residue: null
layer_separation:
local_realizations: []
illustrative_verses: []
decisive_contexts: []
hardest_case:
strongest_counterevidence:
falsification:
coverage_profile:
quality_profile:
epistemic_axes:
limits:
traceability:
derivation:
```
`root_axial_meaning: null` إذا لم توجد نواة مؤهلة؛ status/blocking reason يشرح السبب.

## 3. Term Card

#### C04-O03 — TERM_CARD
يخدم `LEXEME` أو `LOCAL_MEANING` ولا يورث بطاقة الجذر كاملة:
```yaml
identity:
  surface_form:
  normalized_lookup_form:
  lemma:
  root_assignment:
scope:
root_relation:
morphology:
construction:
argument_structure:
context:
meaning:
  lexeme_level_meaning: null
  local_meanings: []
distribution:
semantic_boundary:
neighbors_and_alternatives:
evidence_and_falsification:
quality_profile:
limits:
traceability:
derivation:
```
يحفظ `surface_form` كما في corpus؛ normalized form للبحث فقط. Root assignment غير المستقر يسجل candidates/status ولا يفرض جذرًا.

## 4. Mapping & derivation rules

#### C04-R01 — Read-only derivation
البطاقة تقرأ upstream ولا تكتب فيه. كل statement دلالي يحتاج claim/evidence/dependency refs أو يبقى `null`/غير معروض.

#### C04-R02 — Same-level comparison
Root Card يقارن Root-level neighbor claims، وTerm Card يقارن Lexeme/Local على المستوى نفسه. يمنع level mismatch.

#### C04-R03 — Exclusion rule
كل item في `EXCLUDED` يحتاج `positive_exclusion_evidence`; الغياب وحده لا يكفي.

#### C04-R04 — Card status ceiling
قوة/حالة البطاقة لا تتجاوز أضعف upstream مادي، ولا تحول `INTERNAL_LOCK` إلى owner acceptance/review/publication.

#### C04-R05 — Deterministic derivation receipt
عند توفر tooling:
```yaml
derivation:
  generator_id:
  generator_version:
  generated_at:
  deterministic: true
  upstream_result_sha256:
  upstream_snapshot_sha256:
  created_claims: []
  created_evidence: []
  created_dependencies: []
  stale: false
```
إذا لم تتوفر hashes لا تختلقها؛ استخدم refs قابلة للحل وسجل limitation.

## 5. Display levels for derived cards

#### C04-D01 — CARD_DISPLAY_LEVEL
```text
STATUS_ONLY
CONTROLLED_CONCISE
EVIDENCE_TRACE
FULL_RESEARCH_REF
```
هذه مستقلة عن `OPT-01..04` للمحادثة؛ هي rendering levels لArtifact مشتق.

## 6. Publication/API/UI handoff

#### C04-O04 — PUBLICATION_HANDOFF
```yaml
handoff_id:
run_id:
requested_card_type:
requested_display_level:
source_result_refs: []
source_claim_ids: []
source_evidence_ids: []
source_dependency_ids: []
source_hashes: []
host_status_axes:
publication_gates:
  source_gate:
  claim_gate:
  evidence_gate:
  dependency_gate:
  status_ceiling_gate:
  distinction_gate:
  arabic_presentation_gate:
  lineage_gate:
  consistency_gate:
derivation_check:
blocking_reasons: []
warnings: []
```
هذه gates للتسليم/النشر ولا تمنح بذاتها صحة دلالية أو قبول مالك/مراجعة مستقلة.

## 7. Legacy qualification

#### C04-R06 — Legacy transformation
أي مادة قديمة تميز بين:
`FORMAT_MIGRATION_ONLY` و`METHODOLOGICAL_REQUALIFICATION` وفق [A15-D04]. يحفظ الأصل/lineage ولا تملأ الفجوات بالتخمين.

## 8. Acceptance checklist

#### C04-G01 — Derived artifact acceptance
قبل اعتماد Card/Handoff تحقق: authority/scope، cumulative record، root/term layer separation، essential neighbors/distinctive residue، strongest counterevidence، lineage/dependencies، deterministic derivation when claimed، status ceiling، null/unknown honesty، no new claims/evidence created by card.

`END_OF_COMPANION = C04`
