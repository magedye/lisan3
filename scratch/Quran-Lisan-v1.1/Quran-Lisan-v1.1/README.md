# Quran Lisan v1.1

**Package:** `QURAN_LISAN_V1.1`  
**Status:** `CANONICAL_BASELINE — v1.1 HARDENED`  
**Purpose:** أول baseline موحد، معياري، قابل للتدقيق والتطوير لمنهجية Quran Lisan.

## ما Quran Lisan؟

منهج بحث دلالي قرآني يقدّم **البحث قبل الجواب، والدليل قبل القبول، والاستعمال القرآني قبل التعريف المسبق**. ينظم دراسة الجذر والمفردة والتركيب والآية والمفهوم عبر corpus متحقق، ملاحظات قابلة للتتبع، فرضيات قابلة للنقض، Counterevidence، ونموذج حوكمة معرفي يفصل قوة النتيجة عن اكتمال البحث وعن التحقق المستقل.

المبدأ الجذري الحاكم: للجذر القرآني `ROOT_AXIAL_MEANING` واحد، بينما تُفسّر الفروق الموضعية عبر الاشتقاق والصيغة والتركيب والمشاركين والسياق والخطاب. إذا لم يتحدد الأصل الجامع فالنتيجة `UNRESOLVED`، لا «أصول متنافرة».

## ما الجديد في v1.1؟

- `TARGET_CONTRACT` صريح يمنع خلط Root/Lexeme/Form/Local Meaning.
- `DISTINCTIVE_RESIDUE` و`ESSENTIAL_NEIGHBORS` لتقوية التفريد دون إنشاء نواة ثانية.
- `OPERATIONAL_REJECTION_CONDITION` يجعل النقض قابلًا للتنفيذ وإعادة الإنتاج.
- Coverage متعددة الأبعاد وعينات طبقية منضبطة دون عتبات عددية اعتباطية.
- Tool Reality/Fallback Governance تمنع ادعاء Validators/Tools غير المشغلة.
- فصل `RESEARCH_RECORD` عن `QUALIFIED_RESULT` وعن بطاقات العرض المشتقة.
- A15 لذاكرة النتائج، Scope، التعارضات، revisions، dependencies وإعادة التحقق.
- Root/Term/Verse/Comparison Cards محسنة، مع `REQUIRED/PERMITTED/EXCLUDED/UNKNOWN` وIllustrative/Decisive Contexts.
- QA موسع لاختبار الانحرافات الجديدة.

## كيف تبدأ؟

1. اقرأ `00-Master/M01 — Quran Lisan v1.1 — Master Protocol.md`.
2. استخدم `03-Operational/C01 — Runtime Kernel & Module Router.md` للتشغيل.
3. فعّل فقط الملحقات التي يحددها نوع السؤال.
4. استخدم `02-References/R02 — Master Research Question Matrix.md` كقائمة أسئلة مرجعية، لا كقالب تعبئة إلزامي.
5. قبل القفل/الإخراج مرّ عبر A11 وA14.
6. عند تطوير الحزمة شغّل قواعد A00 وT01.

## Authority Order

```text
QURAN
↓
M01 MASTER
↓
A00–A15 NORMATIVE APPENDICES
↓
R01–R03 REFERENCES
↓
C01–C04 OPERATIONAL COMPANIONS
↓
T01 TEST/QA
↓
E01 EXEMPLARS
```

`EXEMPLAR ≠ AUTHORITY`.

## Quick Start by task

| المهمة | اقرأ/فعّل |
|---|---|
| جذر | M01 + A01 + A02 + A03 + A04 + A05 |
| مفردة | M01 + A02 + A03 + A04 + A05 |
| مقارنة/ضد/نفي | + A09 |
| آية | + A10 |
| غاية/نتيجة/حكمة | + A06 |
| فعل/كيفية/تحول | + A07 + A08 |
| موضوع حساس | + A13 |
| أدوات/مصادر خارجية | + A12 |
| إخراج نهائي | A11 + A14 |
| ذاكرة دلالية/سجل بحث/بطاقات مشتقة | + A15 |
| قالب Cumulative Result / Root & Term Cards / Publication Handoff | C04 |

## Package Tree

```text
Quran-Lisan-v1.1/
├── README.md
├── MANIFEST.md
├── CHANGELOG.md
├── QA_REPORT.md
├── Quran Lisan v1.1 — Migration & Reconciliation Report.md
├── 00-Master/
│   └── M01 — Quran Lisan v1.1 — Master Protocol.md
├── 01-Normative-Appendices/
│   ├── A00 — Appendix Governance, Registry & Dependency Map.md
│   ├── A01 — Root Unity & Axial Meaning Protocol.md
│   ├── A02 — Structural & Distributional Analysis Protocol.md
│   ├── A03 — Corpus, Coverage & Absence Protocol.md
│   ├── A04 — Claim, Evidence & Traceability Protocol.md
│   ├── A05 — Hypothesis, Prediction & Falsification Protocol.md
│   ├── A06 — Purpose, Function, Outcome, Benefit & Wisdom Protocol.md
│   ├── A07 — Event, Transformation, Attentional Orientation & Practical Reconstruction.md
│   ├── A08 — Text, Silence, Open Space & Human Implementation Protocol.md
│   ├── A09 — Quran Lisan Reverse Protocol.md
│   ├── A10 — Bottom-Up Verse Analysis & Scene Reconstruction Protocol.md
│   ├── A11 — Epistemic Governance Protocol.md
│   ├── A12 — Source, Tool & External Comparison Governance.md
│   ├── A13 — Sensitive & Contested Topics Protocol.md
│   ├── A14 — Result Presentation, Output & User Options Protocol.md
│   └── A15 — Semantic Memory, Research Record & Derived Artifact Governance.md
├── 02-References/
│   ├── R01 — Terminology, Aliases & Controlled Vocabulary.md
│   ├── R02 — Master Research Question Matrix.md
│   └── R03 — Master Coverage & Cross-Reference Matrix.md
├── 03-Operational/
│   ├── C01 — Runtime Kernel & Module Router.md
│   ├── C02 — Quick Reference Cards.md
│   ├── C03 — Appendix Style, IDs & Composition Guide.md
│   └── C04 — Derived Cards, Cumulative Research Record & Publication Handoff Guide.md
├── 04-Tests/
│   └── T01 — Regression & Adversarial Test Suite.md
└── 05-Exemplars/
    └── E01 — Gold Standard Worked Studies.md
```

## Core invariants

- `INDEXED ≠ ANALYZED ≠ VALIDATED`
- `STRUCTURAL_LABEL ≠ SEMANTIC_FUNCTION`
- `NOT_SPECIFIED ≠ TEXTUAL_OPEN_SPACE`
- `RETRIEVAL_CANDIDATE ≠ EVIDENCE`
- `RESULT_STRENGTH ≠ RESEARCH_COMPLETENESS ≠ INDEPENDENT_VERIFICATION`
- `EXEMPLAR ≠ AUTHORITY`

## Versioning

جميع الوثائق التشغيلية في هذه الحزمة تعتمد:
`VERSION = 1.1` و`BASE_PROTOCOL = QURAN_LISAN_V1.1`.

تفاصيل الانتقال من المواد التأسيسية التاريخية محفوظة حصريًا في `Quran Lisan v1.1 — Migration & Reconciliation Report.md`.

## Package integrity

راجع `MANIFEST.md` للملفات والحجوم وSHA256، و`QA_REPORT.md` لنتيجة التحقق البنيوي للحزمة.
