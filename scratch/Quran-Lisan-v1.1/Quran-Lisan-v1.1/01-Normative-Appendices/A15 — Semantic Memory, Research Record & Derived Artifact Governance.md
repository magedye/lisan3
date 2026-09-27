---
DOCUMENT_ID: A15
TITLE: "Semantic Memory, Research Record & Derived Artifact Governance"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "حوكمة الذاكرة الدلالية، سجل البحث، البطاقات المشتقة، التبعيات، التعارضات وإعادة التحقق."
SCOPE: "كل حفظ أو إعادة استخدام لنتيجة Quran Lisan وكل Artifact مشتق منها."
ACTIVATION_CONDITION: "عند حفظ/استرجاع نتيجة، بناء Research Record/Card، أو اعتماد نتيجة سابقة كDependency."
DEPENDS_ON: [M01, A04, A05, A11, A14]
EXPANDS_MASTER_SECTIONS: [M01-P13, M01-P14, M01-R34]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Memory/runtime rules previously embedded only in prompts or working skills"
---

# A15 — Semantic Memory, Research Record & Derived Artifact Governance

## 1. الطبقات

#### A15-P01 — Four-layer artifact model
```text
QURANIC_EVIDENCE
↓
RESEARCH_RECORD
↓
QUALIFIED_SEMANTIC_RESULT
↓
DERIVED_PRESENTATION_CARD
↓
USER_ANSWER
```
`RESEARCH_RECORD` قد يحتوي فرضيات مرفوضة ومواد unresolved؛ `QUALIFIED_RESULT` claims اجتازت البوابات؛ `CARD` و`USER_ANSWER` لا تنشئ دليلًا أو قوة جديدة.

#### A15-P02 — Memory axes are independent
لا تجمع في Tier واحد:
```text
MEMORY_RELIABILITY
CLAIM_SCOPE
CONFLICT_STATE
LIFECYCLE_STATUS
```
`LOCAL` Scope وليس ثقة. `DISPUTED` حالة تعارض وليست تلقائيًا ضعف الأدلة الأصلية.

## 2. Memory capability

#### A15-D01 — MEMORY_MODE
```text
PERSISTENT | SESSION_LEDGER | NONE
```
لا يجوز ادعاء الحفظ إذا كانت البيئة لا توفره. عند `NONE`: `EXTERNAL_PERSISTENCE_REQUIRED`.

## 3. Reliability and scope

#### A15-D02 — MEMORY_RELIABILITY
```text
TRUSTED | PROVISIONAL | DISPUTED | RETIRED
```
- `TRUSTED`: نتيجة قوية قابلة لإعادة الاستخدام ضمن Scope المحفوظ.
- `PROVISIONAL`: مفيدة كبداية مع تحذير صريح.
- `DISPUTED`: تعارض مادي غير محسوم يمنع استخدامها منفردة كأساس قوي.
- `RETIRED`: تاريخية/مرفوضة أو superseded ولا تستخدم كأساس نشط.

#### A15-D03 — Memory target/scope
`MEMORY_TARGET_TYPE = ROOT | LEXEME | FORM | CONSTRUCTION | LOCAL_MEANING | VERSE | CONCEPT | COMPARISON | PRACTICE`.
`CLAIM_SCOPE = UNIVERSAL | REPRESENTATIVE | LOCAL` وفق تعريف A03/A04.

## 4. Admission

#### A15-G01 — TRUSTED_MEMORY_ADMISSION_GATE
لا تحفظ كـ`TRUSTED` إلا إذا:
```text
NO_INVALIDATING_FAILURE = YES
CLAIM_SCOPE_DECLARED = YES
COVERAGE_PROFILE_RECORDED = YES
EVIDENCE_TRACEABLE = YES
COUNTEREVIDENCE_ADDRESSED = YES
DEPENDENCIES_RECORDED = YES_OR_NOT_APPLICABLE
REOPEN_IF_RECORDED = YES
RESULT_STRENGTH = STRONG
```
وللجذر: `ROOT_CORE_STATUS = STRONGLY_SUPPORTED`.

نتيجة `STRONG + LOCAL` يجوز حفظها Trusted **داخل Local Scope**؛ لا تحتاج Tier ثقة منفصلًا.

#### A15-R01 — Preserve uncertainty
ممنوع أثناء الحفظ:
`PROVISIONAL→STRONG`, `INFERENCE→TEXTUALLY_FIXED`, `REPRESENTATIVE→UNIVERSAL`, `NOT_FOUND→ABSENT`, `NOT_SPECIFIED→OPEN_SPACE`.

#### A15-R02 — Memory minimality
احفظ الخلاصة الدلالية + scope + evidence refs + material counterevidence + status/axes + dependencies + reopen conditions. لا تحفظ private Chain-of-Thought أو كل Tool Output.

## 5. Schema

#### A15-O01 — LISAN_SEMANTIC_MEMORY_ENTRY
```yaml
memory_id:
revision:
target:
target_type:
claim_scope:
reliability:
lifecycle_status:
conflict_state:
primary_result:
root_letters:
root_axial_meaning:
root_core_status:
formal_definition:
plain_explanation:
semantic_boundary:
  required: []
  permitted: []
  excluded: []
  unknown: []
distinctive_residue:
important_distinctions: []
layer_attribution_summary:
local_realizations: []
textually_fixed: []
not_established: []
strongest_evidence_refs: []
material_counterevidence: []
decisive_context_refs: []
coverage_profile_summary:
result_strength:
research_completeness:
independent_verification:
quality_profile:
related_memory_ids: []
dependency_ids: []
provenance:
  protocol: QURAN_LISAN_V1.1
  corpus:
  source_study:
  snapshot_ref:
  created_at:
reopen_if: []
```

## 6. Retrieval and reuse

#### A15-R03 — Saved result role
```text
SAVED_RESULT ≠ QURANIC_WITNESS
SAVED_RESULT ≠ INDEPENDENT_EVIDENCE
```
عند إعادة الاستخدام يسجل `SOURCE_ROLE = PRIOR_RESEARCH_RESULT`. إذا تغير Scope أو corpus أو ظهر Hard Case مادي، يجب إعادة الفتح/التحقق.

#### A15-G02 — Retrieval scope gate
لا تستخدم memory entry لتغطية Scope أوسع من المحفوظ. النتيجة Local لا تترقى Universal بمجرد كثرة إعادة استخدامها.

## 7. Conflict and revision

#### A15-R04 — Conflict detection
عند new save/retrieval افحص تعارضًا ماديًا مع active memory. إذا وجد:
`MARK_CONFLICT → PRESERVE_BOTH_VERSIONS → DO_NOT_AUTO_RESOLVE → REOPEN_IF_MATERIAL`.
الأحدث لا ينتصر تلقائيًا؛ الدليل والبوابات يحكمان.

#### A15-R05 — Revision lineage
```text
REOPEN
→ NEW_REVISION
→ LINK_PARENT
→ RECORD_NEW_EVIDENCE
→ RECORD_COUNTEREVIDENCE
→ RECORD_REVISION_REASON
```
Lifecycle: `ACTIVE | REOPENED | SUPERSEDED | REJECTED`.

## 8. Dependencies & cards

#### A15-O02 — Dependency record
```yaml
upstream_result:
claim_used:
scope_used:
status_at_use:
validation_scope:
```

#### A15-R06 — Dependency impact
تغير dependency لا يبطل كل المشروع آليًا؛ حدد claims/cards المتأثرة. إذا كان التغير ماديًا بالنسبة لها، امنع إعادة الاستخدام المرجعي حتى revalidation.

#### A15-R07 — Derived card rule
`ROOT_CARD / TERM_CARD / VERSE_CARD / COMPARISON_CARD` هي `DERIVED_READ_MODEL`. لا تغير claim، لا تخفي material counterevidence، ولا توسع scope.

#### A15-R08 — Derived strength ceiling
```text
DERIVED_ARTIFACT_STRENGTH
≤
WEAKEST_MATERIAL_UPSTREAM_RESULT
```
إذا أعيد فتح upstream مادي، يعاد تحقق dependent artifact قبل اعتماده من جديد.

## 9. User operations

#### A15-R09 — Memory commands
يفهم النظام أوامر: «احفظ النتيجة»، «لا تحفظ»، «اعرض ما حفظناه عن X»، «أعد فتح X»، «حدّث X»، «ما الذي تغير؟». التنفيذ الفعلي يخضع لقدرات المضيف ولا يجوز الادعاء بعملية لم تحدث.

## 9.5 Host governance, qualification and deterministic derivation

#### A15-R10 — Optional host governance axes
إذا كان المضيف يعرّف lifecycle منفصلًا، يجوز نسخ محاوره دون دمجها بالقوة الدلالية:
```text
HOST_EPISTEMIC_STATUS
HOST_REVIEW_STATUS
HOST_FRESHNESS_STATUS
HOST_PUBLICATION_STATUS
```
لا تنشئ قيمًا غير موجودة في Registry المضيف، ولا تجعل `PUBLISHED` أو `APPROVED` مرادفًا لـ`STRONG`، ولا تجعل Internal Lock قبولًا بشريًا/نشرًا.

#### A15-D04 — FORMAT_MIGRATION_ONLY vs METHODOLOGICAL_REQUALIFICATION
- `FORMAT_MIGRATION_ONLY`: نقل مادة قديمة إلى Schema/Card جديد دون إثبات أنها اجتازت المنهج الحالي.
- `METHODOLOGICAL_REQUALIFICATION`: فحص/إعادة تشغيل يكفي لإثبات صلاحية النتيجة تحت corpus والبوابات الحالية.
نجاح parsing/schema لا يرقّي الأولى إلى الثانية.

#### A15-R11 — Null semantics in machine contracts
في العقود الآلية structured outputs: حقل المعنى نفسه يكون `null` إذا لم يوجد معنى مؤهل، وتوضع أسباب المنع/عدم الحسم في status/blocking fields. في العرض البشري يجوز إظهار `NOT_ESTABLISHED` بدل الفراغ. لا تضع token حالة داخل حقل meaning بوصفه معنى.

#### A15-R12 — Deterministic derivation & hashes
عند توليد Card/Publication Artifact آليًا، يفضل حفظ: generator/version، generated_at، source refs، upstream result/snapshot hashes أو بصمات مكافئة، وقائمة `created_claims/evidence/dependencies` التي يجب أن تكون فارغة للـread model الخالص. إذا كانت البيئة لا تدعم hashing فتوثق limitation ولا يُختلق hash.

#### A15-G03 — Derived Artifact Qualification Gate
قبل اعتبار Card مرشحًا للاعتماد تحقق: sources resolvable، claims qualified، evidence/dependencies traceable، status ceiling respected، semantic distinction preserved، Arabic presentation faithful، lineage reconstructible، consistency passed. فشل gate يبقي Artifact `CANDIDATE/BLOCKED` في طبقة النشر ولا يغير semantic result.


#### A15-R13 — Memory write disclosure
لا تعرض إشعار حفظ إذا لم يحدث write فعلي. بعد Trusted write يكفي تنبيه 1–2 سطر يوضح أن الخلاصة حفظت ضمن Scope وشروط إعادة الفتح؛ إذا لا persistence، صرح `EXTERNAL_PERSISTENCE_REQUIRED` بدل الادعاء بالحفظ.


## 10. Failures & regression

#### A15-F01 — MEMORY_SCOPE_LOSS
حفظ نتيجة دون Scope أو استخدامها خارجه.

#### A15-F02 — PROVISIONAL_TO_FACT_UPGRADE
ترقية نتيجة أثناء الحفظ/الاسترجاع بلا Gate.

#### A15-F03 — SILENT_MEMORY_REWRITE
استبدال نسخة سابقة بلا lineage/reason.

#### A15-F04 — CARD_AS_AUTHORITY
استخدام بطاقة مشتقة كEvidence مستقلة أو رفع قوتها فوق upstream.

#### A15-F05 — MEMORY_TIER_COLLAPSE
خلط reliability/scope/conflict/lifecycle في محور واحد ينتج استدلالًا خاطئًا.

#### A15-RC01 — Strong local result
نتيجة قوية محلية تحفظ `TRUSTED + LOCAL`، ولا تعامل Universal.

#### A15-RC02 — Conflicting trusted memory
نتيجتان سابقتان تتعارضان بعد Evidence جديدة؛ المتوقع `DISPUTED + REOPEN` لا latest-wins.

#### A15-RC03 — Reopened dependency
Card يعتمد على upstream claim أعيد فتحها؛ المتوقع منع إعادة الاعتماد حتى revalidation.

## نهاية الملحق

```text
INTEGRATION_RULES = A04 research record + A11 epistemic axes + A14 presentation cards
OUTPUT_CONTRACT = scope-safe memory entry / derived card / dependency trace
FAILURE_MODES = scope loss, silent upgrade, silent rewrite, card authority, axis collapse
REGRESSION_CASES = T01 memory/derived-artifact cases
REOPEN_IF = upstream dependency change, material conflict, new hard case, corpus/policy change
END_OF_APPENDIX = A15
```
