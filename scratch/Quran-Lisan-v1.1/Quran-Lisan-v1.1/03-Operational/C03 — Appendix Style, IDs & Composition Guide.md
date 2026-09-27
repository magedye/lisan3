---
DOCUMENT_ID: C03
TITLE: "Appendix Style, IDs & Composition Guide"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: OPERATIONAL_COMPANION
STATUS: CANONICAL_BASELINE
PURPOSE: "توحيد تأليف ملفات الحزمة والمعرفات والإحالات والعقود."
SCOPE: "تحرير أو إضافة وثائق Quran Lisan."
ACTIVATION_CONDITION: "عند إنشاء/تعديل أي وثيقة."
DEPENDS_ON: [M01, A00]
EXPANDS_MASTER_SECTIONS: [M01-R28]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# C03 — Appendix Style, IDs & Composition Guide

## 1. File header

كل وثيقة غير Master تبدأ:
```yaml
DOCUMENT_ID:
TITLE:
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS:
STATUS:
PURPOSE:
SCOPE:
ACTIVATION_CONDITION:
DEPENDS_ON:
EXPANDS_MASTER_SECTIONS:
DOES_NOT_OVERRIDE:
SUPERSEDES:
```

## 2. IDs

#### C03-R01 — ID grammar
`<DOC>-<TYPE><NN>` حيث النوع:
`P D R Q T G F O EX RC XR N`.

مثال:
`A01-P01`, `A01-G01`, `A09-RC03`.

العناوين البشرية تبقى `4 / 4.1 / 4.2` عند الحاجة، والـID للإحالة الدقيقة.

#### C03-R02 — Definition rule
المعرف يُعرّف مرة واحدة فقط في heading أو registry مخصص. الإحالة تكتب `[A01-T03]`.

#### C03-R03 — No bare appendix refs
إذا أمكن precise ref فلا تقل «انظر ملحق الجذر» فقط.

## 3. Composition

#### C03-R04 — Master stays governing
M01 يحمل المبادئ والقواعد العليا فقط؛ التفاصيل والأمثلة والاختبارات في الملحقات.

#### C03-R05 — Appendix ending
كل normative appendix ينتهي:
```text
INTEGRATION_RULES =
OUTPUT_CONTRACT =
FAILURE_MODES =
REGRESSION_CASES =
REOPEN_IF =
END_OF_APPENDIX =
```

#### C03-R06 — Examples
الأمثلة توضح ولا تنشئ authority. استخدم `EX` IDs. مثال غير متحقق نصيًا لا يُعرض كشاهد.

#### C03-R07 — Failure/Regression
Failure mode يصف pattern ممنوعًا؛ regression case يصف سيناريو يجب أن يكشفه الاختبار.

## 4. Language

العربية الفصيحة الدقيقة هي الافتراضية. technical tokens تبقى كما هي عند الحاجة. لا تعرّب token بطريقة تغير معناه أو تنشئ مصطلحًا جديدًا.

## 5. Requirement priority

#### C03-D01 — P0
قاعدة سلامة/سلطة/دليل إذا فشلت قد يصبح claim أو package غير صالح: version consistency، citation integrity، no broken refs، governing principle، invalidating gates.

#### C03-D02 — P1
قاعدة منهجية مهمة تؤثر القوة/الاكتمال أو دقة النتيجة: hard cases، competitors، detailed output contract.

#### C03-D03 — P2
تحسين usability/presentation لا يغير validity الأساسية إذا غاب مؤقتًا.

لا تُستخدم P0/P1/P2 بدل epistemic status للبحث.

## 6. Change workflow

authority → identify owning doc → if governing gap use [A00-G01] → edit → update R01/R03 if terms/mapping change → add/adjust T01 → update CHANGELOG → validate package.

## 7. Cross-reference QA

Validator يجب أن يفحص:
- defined IDs unique؛
- refs point to defined IDs؛
- package version only 1.0 outside Migration؛
- no orphan document؛
- dependency graph acyclic؛
- normative footer present.

## 6. Derived artifacts & output style

#### C03-R10 — Derived artifact naming
استخدم `RESEARCH_RECORD`, `QUALIFIED_SEMANTIC_RESULT`, `ROOT_CARD`, `TERM_CARD`, `VERSE_CARD`, `COMPARISON_CARD`, `MEMORY_ENTRY` وفق تعريفات A15؛ لا تسم card «نتيجة canonical» إن كانت read model فقط.

#### C03-R11 — Output formatting
في `CONCISE/BALANCED` استخدم عناوين قصيرة وتجنب schema dump. في `DEEP/RESEARCH` يجوز الجداول وEvidence Trace. لا تستخدم حدود كلمات صلبة إذا أضرت بالدقة.

#### C03-R12 — Semantic Boundary notation
عند استخدام `REQUIRED/PERMITTED/EXCLUDED/UNKNOWN`: `EXCLUDED` يحتاج positive exclusion evidence؛ مجرد الغياب ينتقل إلى `UNKNOWN/NOT_FOUND_IN_VERIFIED_SCOPE` وفق A03/A09.
