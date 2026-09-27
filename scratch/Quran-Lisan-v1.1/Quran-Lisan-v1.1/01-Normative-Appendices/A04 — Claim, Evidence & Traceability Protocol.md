---
DOCUMENT_ID: A04
TITLE: "Claim, Evidence & Traceability Protocol"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "فصل الشاهد والملاحظة والدليل والادعاء والتفسير وبناء graph دعم قابل للتتبع."
SCOPE: "كل Claim بحثي أو Evidence Ledger."
ACTIVATION_CONDITION: "كل بحث ينتج claim غير بديهي."
DEPENDS_ON: [M01]
EXPANDS_MASTER_SECTIONS: [M01-R09, M01-R10]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A04 — Claim, Evidence & Traceability Protocol

## 1. Ontology

#### A04-D01 — Witness
نص/موضع/بنية متحققة يمكن الرجوع إليها.

#### A04-D02 — Observation
وصف لما يظهر في witness دون تفسير زائد.

#### A04-D03 — Evidence
Observation أو مجموعة observations بعد تحديد علاقتها بclaim.

#### A04-D04 — Claim
دعوى قابلة للفحص ذات scope وحالة.

#### A04-D05 — Interpretation
قراءة تفسيرية تتجاوز الوصف المباشر ويجب وسم درجتها.

#### A04-D06 — Entailment
ما يلزم من مقدمات مثبتة دون إضافة فرضية مستقلة؛ درجته لا تتجاوز أضعف premise مادية.

`Witness ≠ Observation ≠ Evidence ≠ Interpretation ≠ Claim`.

## 2. Atomicity & relations

#### A04-R01 — Claim Atomicity
كل claim يكون atomic قدر الإمكان. إذا احتوى سببًا ونتيجة وغرضًا، يفكك إلى claims وروابط.

#### A04-D07 — Evidence Relation
`SUPPORT / CHALLENGE / LIMIT / NON_DISCRIMINATING`.
كل edge يحدد relation لا مجرد قائمة مراجع.

#### A04-D08 — Support class
`DIRECT / ENTAILED / DERIVED`.
الدعم المشتق لا يتجاوز قوة السلسلة التي يعتمد عليها.

#### A04-R02 — Derived Support Ceiling
إذا اعتمد Claim B على Claim A المشتق، فلا يمكن أن يصبح B أقوى معرفيًا من A دون witness مستقل.

## 3. Ledger

#### A04-O01 — CLAIM_EVIDENCE_LEDGER
```yaml
CLAIM:
  claim_id:
  text:
  scope:
  status:
  support_class:
  evidence_relations:
    - evidence_id:
      relation:
      basis:
  counterevidence: []
  assumptions: []
  limits: []
  derived_from: []
  reopen_if: []
```

#### A04-R03 — Evidence provenance
كل evidence node يربط بوitness أو source receipt يمكن إعادة بنائه.

#### A04-R04 — Acyclic support
لا يسمح بدورة support تعتمد فيها claims على بعضها لتثبت نفسها. Cycles في concept graph لا تعني cycles في evidence graph.

#### A04-G01 — Claim Admission Gate
قبل claim قوي:
- scope معلن؛
- witness متحقق؛
- evidence relation مصنفة؛
- counterevidence مذكور أو لا يوجد بعد بحث مناسب؛
- derived chain تنتهي إلى observations؛
- لا circularity؛
- لا external candidate masquerading as evidence.

#### A04-G02 — Traceability Closure Gate
قبل قفل claim يجب أن يكون لكل دعم جوهري مسار قابل للتتبع إلى witness/observation أصلية، وأن تكون العلاقات والحدود وcounterevidence قابلة لإعادة البناء. إذا تعذر traceability لجزء مادي، لا يُستخدم ذلك الجزء لرفع قوة claim.

## 3.5 Research Record & dependencies

#### A04-D09 — RESEARCH_RECORD
`RESEARCH_RECORD` سجل قابل للتدقيق يحفظ الملاحظات، القيود، hypotheses/revisions، evidence، counterevidence، competing models، predictions/failed predictions، coverage، dependencies، unresolved items والقرارات. قد يحتوي فرضيات مرفوضة، لذلك لا يساوي Final Result.

#### A04-R07 — Research record separation
```text
RESEARCH_RECORD
≠
QUALIFIED_SEMANTIC_RESULT
≠
PRESENTATION_CARD
```
النتيجة المؤهلة subset من claims اجتازت البوابات؛ البطاقة المشتقة تعرضها فقط. يوسع [A15-P01].

#### A04-O02 — DEPENDENCY_LEDGER
لكل اعتماد مادي:
```yaml
dependency_id:
upstream_result:
claim_used:
scope_used:
status_at_use:
validation_scope:
```
إذا لم توجد آلية رسمية للمضيف، يحتفظ بهذا كسجل بحثي صريح دون ادعاء وجود Registry رسمي.

#### A04-R08 — Dependency traceability
لا يجوز لClaim مشتقة أن تخفي upstream assumptions. تغير dependency جوهرية يحدد claims المتأثرة فقط، ولا يلزم إعادة كل المشروع بلا تحليل impact.

#### A04-G03 — Dependency Validity Gate
قبل إعادة استخدام نتيجة سابقة تحقق أنها: قابلة للحل، ضمن Scope صالح، غير Reopened ماديًا، وأن status/coverage المستخدمين لم يتغيرا بما يبطل claim التابعة.

## 4. Reopen and revision

#### A04-R05 — Revision lineage
إذا تغير claim، أنشئ revision واضحًا بسبب التغيير ولا تعيد كتابة التاريخ. سجل parent/revision reason.

#### A04-R06 — Reopen
كل claim مادي يحمل `REOPEN_IF`: witness correction، new counterevidence، scope expansion، dependency change، أو failure discovery.

## 5. Failure modes

#### A04-F01 — EVIDENCE_DUMP
إيراد آيات كثيرة دون بيان علاقتها بالclaim.

#### A04-F02 — CIRCULAR_CONFIRMATION
افتراض المعنى ثم عد readings المتولدة منه دليلًا مستقلاً.

#### A04-F03 — CLAIM_BUNDLING
جمع عدة دعاوى في claim واحد يمنع falsification الدقيق.

#### A04-F04 — AUTHORITY_LEAK
ترقية مصدر/أداة خارجية إلى evidence داخليًا.

#### A04-RC01 — One witness supports and limits
يجب السماح لنفس witness أن `SUPPORT` claim وتـ`LIMIT` claim آخر.

#### A04-RC02 — Derived chain
Claim ثالث مبني على claim مشتق ضعيف → لا يرقى إلى قوي بلا شاهد مستقل.

---

## نهاية الملحق

```text
INTEGRATION_RULES = M01 evidence discipline; feeds all analytic appendices
OUTPUT_CONTRACT = CLAIM_EVIDENCE_LEDGER
FAILURE_MODES = circularity, bundling, evidence dump, authority leak
REGRESSION_CASES = A04-RC01..02; T01 evidence graph
REOPEN_IF = claim revision/new witness/counterevidence/scope expansion
END_OF_APPENDIX = A04
```
