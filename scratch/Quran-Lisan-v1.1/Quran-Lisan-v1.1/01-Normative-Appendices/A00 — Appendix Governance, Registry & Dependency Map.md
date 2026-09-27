---
DOCUMENT_ID: A00
TITLE: "Appendix Governance, Registry & Dependency Map"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "حوكمة الحزمة، التسجيل، التبعيات، التعارضات، والتتبع."
SCOPE: "جميع وثائق Quran Lisan v1.1."
ACTIVATION_CONDITION: "دائم عند تطوير أو تفسير أو تعديل الحزمة."
DEPENDS_ON: [M01]
EXPANDS_MASTER_SECTIONS: [M01-R28, M01-P02]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A00 — Appendix Governance, Registry & Dependency Map

## 1. Registry

#### A00-D01 — Document Classes
`M` Master، `A` Normative Appendix، `R` Reference، `C` Operational Companion، `T` Test/QA، `E` Exemplar.

#### A00-R01 — Canonical Registry
| ID | الوثيقة | الطبقة | الحالة |
|---|---|---|---|
| M01 | Master Protocol | MASTER | CANONICAL_BASELINE |
| A00 | Governance, Registry & Dependency Map | NORMATIVE | CANONICAL_BASELINE |
| A01 | Root Unity & Axial Meaning | NORMATIVE | CANONICAL_BASELINE |
| A02 | Structural & Distributional Analysis | NORMATIVE | CANONICAL_BASELINE |
| A03 | Corpus, Coverage & Absence | NORMATIVE | CANONICAL_BASELINE |
| A04 | Claim, Evidence & Traceability | NORMATIVE | CANONICAL_BASELINE |
| A05 | Hypothesis, Prediction & Falsification | NORMATIVE | CANONICAL_BASELINE |
| A06 | Purpose, Function, Outcome, Benefit & Wisdom | NORMATIVE | CANONICAL_BASELINE |
| A07 | Event, Transformation, Attentional Orientation & Practical Reconstruction | NORMATIVE | CANONICAL_BASELINE |
| A08 | Text, Silence, Open Space & Human Implementation | NORMATIVE | CANONICAL_BASELINE |
| A09 | Quran Lisan Reverse Protocol | NORMATIVE | CANONICAL_BASELINE |
| A10 | Bottom-Up Verse Analysis & Scene Reconstruction | NORMATIVE | CANONICAL_BASELINE |
| A11 | Epistemic Governance | NORMATIVE | CANONICAL_BASELINE |
| A12 | Source, Tool & External Comparison Governance | NORMATIVE | CANONICAL_BASELINE |
| A13 | Sensitive & Contested Topics | NORMATIVE | CANONICAL_BASELINE |
| A14 | Result Presentation, Output & User Options | NORMATIVE | CANONICAL_BASELINE |
| A15 | Semantic Memory, Research Record & Derived Artifact Governance | NORMATIVE | CANONICAL_BASELINE |
| R01 | Terminology, Aliases & Controlled Vocabulary | REFERENCE | CANONICAL_BASELINE |
| R02 | Master Research Question Matrix | REFERENCE | CANONICAL_BASELINE |
| R03 | Master Coverage & Cross-Reference Matrix | REFERENCE | CANONICAL_BASELINE |
| C01 | Runtime Kernel & Module Router | OPERATIONAL | CANONICAL_BASELINE |
| C02 | Quick Reference Cards | OPERATIONAL | CANONICAL_BASELINE |
| C03 | Appendix Style, IDs & Composition Guide | OPERATIONAL | CANONICAL_BASELINE |
| C04 | Derived Cards, Cumulative Research Record & Publication Handoff Guide | OPERATIONAL | CANONICAL_BASELINE |
| T01 | Regression & Adversarial Test Suite | TEST_QA | BASELINE |
| E01 | Gold Standard Worked Studies | EXEMPLAR | NON_AUTHORITATIVE_BASELINE |

## 2. Dependency Graph

#### A00-R02 — Acyclic normative dependencies
```text
M01
├─ A00
├─ A02
├─ A03
├─ A04
├─ A05
├─ A06
├─ A07
├─ A08
├─ A11
├─ A14
├─ A15 ← A04,A05,A11,A14
├─ A01 ← A02,A03,A04,A05
├─ A09 ← A02,A03,A04,A05
├─ A10 ← A01,A02,A04,A07
├─ A12 ← A03,A04,A05,A11
└─ A13 ← A03,A04,A05,A11,A12

References ← M01 + applicable appendices
Operational ← M01 + applicable appendices
Tests ← M01 + A00..A15
Exemplars ← M01 + A00..A15
```
التبعية تعني «يحتاج تعريفات أو بوابات»، لا تعني أن الوثيقة التابعة أعلى سلطة.

## 3. Version Compatibility

#### A00-R03 — Version Compatibility Matrix
| Package | Master | Appendices | Compatibility |
|---|---|---|---|
| `QURAN_LISAN_V1.1` | 1.1 | 1.1 | REQUIRED |
| أي mix بإصدار أساس مختلف | — | — | NOT_SUPPORTED |

كل وثيقة غير Master تحمل `BASE_PROTOCOL = QURAN_LISAN_V1.1`. لا يعتمد التشغيل على وثيقة تاريخية خارج Migration Report.

## 4. Conflict Resolution & Rule Escalation

#### A00-R04 — Conflict Resolution
عند التعارض: القرآن المتحقق → M01 → الملحق المعياري المختص → المرجع → companion → test/exemplar. إذا تعارض ملحقان في نطاق مشترك، يُرجع أولًا إلى M01 ثم إلى الملحق الأخص موضوعًا؛ إذا بقي التعارض يسجل `OPEN_DECISION` ولا يخفى.

#### A00-G01 — Rule Escalation Protocol
```text
MASTER_GAP_FOUND
→ record gap
→ MASTER_CHANGE_REQUEST
→ determine if governing or local
→ if governing: amend M01 first
→ amend dependent appendix
→ update R03 + CHANGELOG
→ run T01
```

#### A00-F01 — Silent escalation
إضافة قاعدة حاكمة في ملحق دون تعديل M01 فشل معياري.

## 5. Activation Triggers

#### A00-R05 — Trigger Map
| Phenomenon / Task | Required appendix |
|---|---|
| Root/core | A01 |
| Morphology/syntax/distribution | A02 |
| Coverage/absence | A03 |
| Claims/evidence | A04 |
| Hypothesis/falsification | A05 |
| Purpose/result/wisdom | A06 |
| Event/practice/attention | A07 |
| Silence/open/human | A08 |
| Negation/opposition/reversal | A09 |
| Verse/scene | A10 |
| confidence/lock/verification | A11 |
| tools/external source | A12 |
| sensitive/contested | A13 |
| user-facing output | A14 |
| semantic memory/research record/derived cards | A15 |
| cumulative record/cards/publication handoff | C04 (operational, under A15/A14) |

## 6. Master Coverage Map

#### A00-XR01 — Master to appendix map
| Master area | Expansion |
|---|---|
| Root Unity | [A01-G01] |
| Structural firewall | [A02-R01] |
| Coverage | [A03-R01] |
| Evidence | [A04-R01] |
| Falsification | [A05-R01] |
| Purpose | [A06-G01] |
| Practical/Event | [A07-G02] |
| Text/Open/Human | [A08-G01] |
| Reverse | [A09-G01] |
| Verse | [A10-R01] |
| Epistemic model | [A11-P01] |
| Tools | [A12-R04] |
| Sensitive | [A13-G01] |
| Output | [A14-O01] |
| Memory/Research Record/Derived Artifacts | [A15-P01] |

## 7. Cross-Reference Syntax

#### A00-R06 — Precise references
استخدم `[A01-T03]`, `[A04-G02]`, `[M01-R12]`. الإحالة العامة باسم الملحق وحده لا تكفي إذا كان الهدف قابلًا للإحالة الدقيقة.

## 8. Traceability

#### A00-R07 — Traceability Matrix
يجب أن تسمح الحزمة بالمسار:
```text
MASTER_RULE
→ APPENDIX_RULE/GATE
→ REFERENCE/OPERATIONAL EXPRESSION
→ TEST CASE
→ STATUS
```
المصفوفة التنفيذية في R03.

## 9. Known Gaps / Pending Appendices

#### A00-N01 — Known Gaps
لا توجد ملحقات معيارية ناقصة ضمن baseline المحدد. الدراسات الموسعة للجذور المذكورة في E01 ما زالت `PENDING_RESEARCH` ولا تعد فجوة في البروتوكول.

#### A00-N02 — Pending Appendices
`NONE_FOR_V1.1_BASELINE`. أي ملحق جديد يحتاج Rule Escalation إذا حمل قاعدة حاكمة.

## 10. Change Log Policy

#### A00-R08 — Change discipline
كل تغيير معياري يسجل في `CHANGELOG.md` مع الوثيقة/IDs المتأثرة، سبب التغيير، أثر التوافق، واختبارات regression المطلوبة.

---

## نهاية الملحق

```text
INTEGRATION_RULES = Registry + precedence + escalation + dependency DAG
OUTPUT_CONTRACT = Governance decision + traceability update
FAILURE_MODES = silent override, version mix, orphan document
REGRESSION_CASES = T01 governance cases
REOPEN_IF = new governing rule, conflict, dependency change
END_OF_APPENDIX = A00
```
