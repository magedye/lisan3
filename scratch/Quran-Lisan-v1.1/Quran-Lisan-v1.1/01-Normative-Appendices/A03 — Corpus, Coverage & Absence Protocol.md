---
DOCUMENT_ID: A03
TITLE: "Corpus, Coverage & Absence Protocol"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "ضبط corpus ومستويات التغطية والعينات والغياب والصمت."
SCOPE: "كل ادعاء كلي أو غياب أو negative distribution."
ACTIVATION_CONDITION: "دائم؛ يتشدد عند UNIVERSAL/ALL/NEVER/ABSENCE."
DEPENDS_ON: [M01]
EXPANDS_MASTER_SECTIONS: [M01-P06, M01-R04, M01-R12, M01-R13]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A03 — Corpus, Coverage & Absence Protocol

## 1. Coverage semantics

#### A03-D01 — Coverage Profile
```text
INDEXED =
ANALYZED =
VALIDATED =
FORM_COVERAGE =
CONSTRUCTION_COVERAGE =
CONTEXT_COVERAGE =
HARD_CASE_COVERAGE =
NEIGHBOR_COVERAGE =
EXCLUDED =
UNRESOLVED =
SAMPLING_BASIS =
GENERALIZATION_BOUNDARY =
```

#### A03-P01 — Indexed is not analyzed
`INDEXED ≠ ANALYZED ≠ VALIDATED`. ولا يكفي عدد النتائج أو retrieval count لإثبات completeness.

#### A03-D02 — Coverage classes
- `FULL`: الحيز الملائم المحدد حُصر وحُلّل وتحقق منه بما يكفي للclaim.
- `REPRESENTATIVE`: عينة متنوعة مصممة لتغطية الأنماط دون ادعاء الحصر.
- `LOCAL`: موضع/مجموعة محدودة.
لا يجوز استخدام `FULL` لمجرد اكتمال query إذا بقي تحليل أو validation.

#### A03-G01 — Scope/Coverage Alignment Gate
| Claim scope | Minimum acceptable basis |
|---|---|
| LOCAL | Local verified evidence |
| REPRESENTATIVE | Diverse representative analyzed set |
| UNIVERSAL | Full relevant coverage أو مبرر مستقل موثق |
إذا فشل: ضيّق claim ولا تُحسن wording فقط.

## 2. Sampling & exclusions

#### A03-R01 — Sampling disclosure
كل sampling يوضح basis، stratification إن وجد، سبب الاستبعاد، وما لا يسمح بتعميمه.

#### A03-R02 — Exclusions
أي occurrence مستبعد يسجل مع السبب: false match، identity uncertainty، scope exclusion، data defect، أو unresolved. الاستبعاد الصامت ممنوع.

#### A03-R03 — Hard-case coverage
الحالات النادرة/المقاومة لا تستبعد لكونها صعبة. غيابها المادي يمنع strong universal lock.

## 2.5 التغطية متعددة الأبعاد والعينات الكبيرة

#### A03-D04 — MULTI_DIMENSIONAL_COVERAGE
`COVERAGE_PROFILE` لا يختزل في count واحد. يجب — بحسب الادعاء — الفصل بين:
```text
INDEX_COVERAGE
DEEP_ANALYSIS_COVERAGE
FORM_COVERAGE
CONSTRUCTION_COVERAGE
CONTEXT_DIVERSITY
HARD_CASE_COVERAGE
NEIGHBOR_COVERAGE
NEGATIVE_DISTRIBUTION_COVERAGE
UNRESOLVED_ITEMS
EXCLUDED_ITEMS
SAMPLING_BASIS
GENERALIZATION_BOUNDARY
```

#### A03-R07 — Stratified sampling for discovery
عندما يكون corpus كبيرًا يجوز استخدام عينة طبقية في مرحلة discovery بشرط توثيق method/strata/selection criteria/excluded items/challenge set/limits. لا تعتمد عتبة عددية ثابتة لتحديد «الكبير»؛ المعيار هو كلفة التحليل مع الحفاظ على تنوع الصيغ والتراكيب والسياقات والحالات الصعبة.

```text
EXPLORATORY_SAMPLE ≠ UNIVERSAL_PROOF
```

#### A03-G03 — Universal generalization gate
أي ادعاء `UNIVERSAL_PRESENCE` أو غياب كلي يحتاج تغطية تعالج material diversity لا مجرد فهرسة كاملة. إذا بقي جزء غير محلل يمكنه قلب claim، تضيق الصياغة إلى النطاق المتحقق.

#### A03-RC03 — Sample inflation
فهرسة corpus كامل مع تحليل عينة متنوعة ثم إعلان «ثبت في جميع الاستعمالات». المتوقع: رفض التعميم حتى تحقق [A03-G03].

## 3. Absence

#### A03-G02 — ABSENCE_CLAIM_GATE
ادعاءات «لا يرد/لا يوجد/لم يستخدم/لا يأتي مع» تحتاج:
```text
SEARCH_SPACE_DEFINED = YES
FULL_RELEVANT_COVERAGE = YES
INDEXING_COMPLETE_FOR_SCOPE = YES
RELEVANT_VARIANTS_ACCOUNTED_FOR = YES
UNRESOLVED_MATCHES = 0_OR_NON_MATERIAL
```
وإلا الصياغة:
> لم يظهر في المواضع التي تم التحقق منها في هذا البحث.

#### A03-R04 — Absence is not negation
`ABSENCE_OF_X ≠ PROOF_OF_NOT_X`. قد توجد صياغة بديلة، حذف، اختلاف سياقي، أو توقع خاطئ.

#### A03-R05 — Negative Distribution
قبل البحث سجّل `EXPECTED_CONTEXT_DEFINED_IN_ADVANCE`. إذا ولّدت التوقع بعد رؤية الغياب، تعامل معه exploratory لا confirmatory.

## 4. Textual Silence

#### A03-D03 — Silence status
```text
TEXTUAL_SILENCE_STATUS =
  ESTABLISHED_FOR_SCOPE
  | NOT_FOUND_IN_VERIFIED_SCOPE
  | UNRESOLVED
```

#### A03-R06 — Silence wording
`ESTABLISHED_FOR_SCOPE` يسمح بصياغة «ضمن النطاق المتحقق بالكامل لم يحدد النص...». غير ذلك يلزم wording مقيد. الانتقال إلى `TEXTUAL_OPEN_SPACE` يخضع [A08-G01].

## 5. Integrity

#### A03-T01 — Citation Integrity
لا تختلق نص آية/رقم/موضع/عدد/lemma/root/form/analysis. غير المتحقق يسجل `CITATION_NOT_VERIFIED` أو `STRUCTURALLY_UNVERIFIED`.

#### A03-T02 — Corpus provenance
سجل corpus/version/query أو وسيلة الحصر، وقت الاستخراج عند الحاجة، والتحويلات المؤثرة في النتائج.

#### A03-F01 — PARTIAL_CORPUS_SILENCE
تغطية جزئية + claim «القرآن لا...» = invalidating for that claim.

#### A03-F02 — INDEXED_AS_VALIDATED
استخدام retrieval hits كأنها analyzed/validated.

#### A03-RC01 — Missing rare form
عينة كبيرة تفوت صيغة نادرة مقاومة → لا `FULL`.

#### A03-RC02 — No-hit query
query صفر نتائج لكن variants لم تفحص → لا absence claim.

---

## نهاية الملحق

```text
INTEGRATION_RULES = M01 scope alignment; feeds A01/A09/A11/A12/A13
OUTPUT_CONTRACT = COVERAGE_PROFILE + TEXTUAL_SILENCE_STATUS
FAILURE_MODES = partial-corpus absence, silent exclusion, indexed-as-validated
REGRESSION_CASES = A03-RC01..02; T01 silence/absence
REOPEN_IF = corpus/version/query change, new occurrence, exclusion correction
END_OF_APPENDIX = A03
```
