---
DOCUMENT_ID: A11
TITLE: "Epistemic Governance Protocol"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "فصل قوة النتيجة واكتمال البحث والتحقق المستقل وإدارة الثقة والفشل والنقاء والقفل وإعادة الفتح."
SCOPE: "كل نتيجة بحثية قبل internal lock أو publication."
ACTIVATION_CONDITION: "دائم في التقييم النهائي؛ يتشدد للنتائج العالية المخاطر."
DEPENDS_ON: [M01, A03, A04, A05]
EXPANDS_MASTER_SECTIONS: [M01-P09, M01-R20, M01-R21, M01-G02, M01-G03]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A11 — Epistemic Governance Protocol

## 1. Three axes

#### A11-P01 — Three-Axis Model
```text
RESULT_STRENGTH
≠
RESEARCH_COMPLETENESS
≠
INDEPENDENT_VERIFICATION
```
لا تجمع المحاور في score واحد.

#### A11-D01 — Result strength
`WEAK / MODERATE / STRONG / UNRESOLVED` أو statuses أكثر تفصيلًا حسب الملحق.

#### A11-D02 — Research completeness
تقاس بملاءمة coverage، hard cases، counterevidence، competitors، activated modules، unresolved material.

#### A11-D03 — Verification class
`SELF_REVIEW / SAME_MODEL_CONTEXT_BLIND / DIFFERENT_MODEL / HUMAN_REVIEW / INDEPENDENT_REPLICATION`.
الفئة تصف عملية التحقق ولا تضمن صحة النتيجة.

#### A11-R01 — Confidence rationale
الثقة وصف تفسيري مبني على coverage/evidence independence/hard cases/falsification، لا stars أو رقم سحري.

## 2. Independence

#### A11-R02 — Same evidence is not independent
عدة أدوات مشتقة من نفس distribution لا تعد مصادر أدلة مستقلة بمجرد اختلاف الواجهة.

#### A11-R03 — Same-model independence error
مراجعتان بالنموذج نفسه لا تسجلان `INDEPENDENT_REPLICATION`. قد تكونان adversarial self-review أو context-blind حسب التنفيذ.

## 3. Failure severity

#### A11-D04 — INVALIDATING_FAILURE
فشل يمس سلامة النص/الدليل/النطاق/الدور المنطقي/مصدر جوهري؛ يمنع claim أو lock حتى يعالج أو يضيق scope.

#### A11-D05 — NON_INVALIDATING_GAP
نقص يخفض strength/completeness لكنه لا يبطل بالضرورة.

#### A11-G01 — Failure classification
قبل تعديل scope أو requirements صنف الفشل، وسجل أثره على claims. لا تخفّض القاعدة لتلائم failure.

## 4. Purity

#### A11-R04 — Purity dimensions
افحص على الأقل: Dictionary-First، Contextual Leakage، Heritage/Tafsir contamination، Modern Ideological Projection، Forced Unification، Generic Overextraction، Circular Confirmation، Grammar/Morphology semantic leakage، Purpose inflation، Slot filling.

#### A11-D06 — Purity status
`EVALUATED_CLEAN / ISSUE_FOUND / NOT_EVALUATED / NOT_APPLICABLE`.
`NOT_EVALUATED ≠ CLEAN`.

#### A11-R05 — Purity score guard
أي aggregate score إن استخدم أداة إدارة مخاطر فقط، ولا يساوي epistemic truth.

## 5. Completeness & lock

#### A11-G02 — Research Completeness Gate
قبل lock:
question محدد؛ coverage مناسب؛ hard cases/counterevidence/competitors معالجون؛ purity المطلوبة؛ freeze/holdout عند الانطباق؛ specialized gates مكتملة؛ no invalidating failure؛ scope aligned.

#### A11-G03 — Internal Lock
`INTERNAL_SEMANTIC_RESULT` لا ينشأ إلا بعد [A11-G02]. وهو snapshot لأفضل نتيجة داخلية ضمن scope، وليس حقيقة مقدسة/إجماعًا/نهاية بحث.

يحتوي: result، scope، evidence، counterevidence، coverage، status، three axes، purity، open questions، `REOPEN_IF`.

#### A11-R06 — Internal snapshot
قبل Post-Lock External Comparison، ثبّت snapshot لا يعاد تحريره لإخفاء أثر الخارج. أي تغيير لاحق revision.

## 5.5 Quality profile and status separation

#### A11-D07 — MULTI_DIMENSIONAL_QUALITY_PROFILE
عند الحاجة يمكن وصف جودة النتيجة دون Overall Score عبر:
```text
POSITIVE_CORE_ROBUSTNESS
NEGATIVE_DETERMINATION_ROBUSTNESS
LEXICAL_DISTINCTIVENESS
COMPOSITIONAL_TRACEABILITY
FALSIFICATION_STRENGTH
PREDICTIVE_PERFORMANCE
UNRESOLVED_CASE_BURDEN
```
لا تجمع في رقم واحد إلا إذا عرفت سياسة calibrated مستقلة ذلك.

#### A11-R08 — Status-axis separation
لا تخلط `ROOT_CORE_STATUS` مع `RESULT_STRENGTH` أو `CLAIM_SCOPE` أو Lifecycle للمضيف. يمكن للناتج أن يكون `STRONG + LOCAL` أو `PROVISIONAL + UNIVERSAL_CANDIDATE`; Local ليست ثقة منخفضة، والنشر ليس قوة دلالية.

#### A11-G05 — PRE_DELIVERY_AUDIT
في `DEEP/RESEARCH` والدراسات المهمة يفحص قبل التسليم:
`TARGET_CONTRACT`, authority/source reality, coverage alignment, Root Unity, Layer Attribution, Essential Neighbors، Distinctive Residue، Rejection Condition، Counterevidence، Tool Reality، Status Integrity، Memory/Dependency Integrity، Unresolved Material، وAnti-patterns.
يصلح ما يمكن إصلاحه؛ أما failure حاسم فيمنع Internal Lock/Claim قوية.

## 6. Pre-output gate

#### A11-G04 — PRE_OUTPUT_VERIFICATION_GATE
```text
SOURCE_ISOLATION_OK
CITATIONS_VERIFIED
SCOPE_COVERAGE_ALIGNED
ACTIVATED_MODULES_COMPLETE
COUNTEREVIDENCE_ADDRESSED
NO_SLOT_FILLING
NO_GRAMMAR_TO_SEMANTICS_LEAP
TEXTUAL_SILENCE_WORDING_SAFE
PURPOSE_RELATIONS_CLASSIFIED
TEXT_OPEN_HUMAN_DISTINCTION_OK
THREE_AXIS_REPORTED
NO_INVALIDATING_FAILURE
```
فشل الحاسم → `REVISE / NARROW / UNRESOLVED / BLOCKED`.

## 7. Reopen

#### A11-R07 — Reopen rules
new witness، corpus change، hard case، competing model، provenance correction، purity issue، external source يكشف شاهدًا داخليًا لم يدرس، أو dependency revision.

#### A11-F01 — CONFIDENCE_COLLAPSE
خلط strength/completeness/verification في «ثقة عالية».

#### A11-F02 — NOT_EVALUATED_AS_CLEAN
خطر لم يُفحص يسجل clean.

#### A11-RC01 — Strong but incomplete
يجوز `RESULT_STRENGTH=STRONG` و`RESEARCH_COMPLETENESS=PARTIAL` إذا كان scope/wording واضحًا.

#### A11-RC02 — Complete but unresolved
تغطية كاملة قد تنتهي `UNRESOLVED` إذا evidence غير حاسمة.

---

## نهاية الملحق

```text
INTEGRATION_RULES = M01 epistemic governance + A03/A04/A05
OUTPUT_CONTRACT = three axes + gate/lock/reopen record
FAILURE_MODES = confidence collapse, false independence, not-evaluated-as-clean
REGRESSION_CASES = A11-RC01..02; T01 independence/purity cases
REOPEN_IF = new evidence/failure/purity issue/dependency change
END_OF_APPENDIX = A11
```
