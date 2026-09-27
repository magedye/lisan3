---
DOCUMENT_ID: A05
TITLE: "Hypothesis, Prediction & Falsification Protocol"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "إدارة الفرضيات من التوليد إلى التجميد والتنبؤ والنقض والمراجعة."
SCOPE: "كل نموذج دلالي أو causal/relational model قابل للتنافس."
ACTIVATION_CONDITION: "عند الانتقال من observations إلى تفسير أو model."
DEPENDS_ON: [M01]
EXPANDS_MASTER_SECTIONS: [M01-P05, M01-R10, M01-R11]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A05 — Hypothesis, Prediction & Falsification Protocol

## 1. Canonical loop

#### A05-R01 — Evidence Loop
```text
OBSERVATION
→ PATTERN
→ HYPOTHESIS
→ FREEZE
→ PREDICTION
→ HOLDOUT
→ COUNTEREVIDENCE
→ FALSIFICATION
→ REVISION / SUPPORT / REJECT
```

#### A05-D01 — Semantic Hypothesis
فرضية محددة، قابلة للنقض، غير دائرية، ذات scope وتوقعات وشروط رفض.

#### A05-G01 — Hypothesis Freeze
قبل مجموعة التحدي:
```text
HYPOTHESIS_Vn =
SCOPE =
PREDICTS =
REJECT_IF =
FROZEN_BEFORE_CHALLENGE = YES
```
أي تعديل بعد الفشل يصبح revision جديدًا لا تعديلًا صامتًا.

## 2. Predictions & holdout

#### A05-R02 — Positive/Negative Predictions
اكتب ما ينبغي أن يظهر وما ينبغي ألا يظهر إذا صحت الفرضية. التنبؤ الذي يمكن صياغته بعد رؤية كل البيانات أقل قوة.

#### A05-G02 — Predictive Test
استخدم `HELD_OUT_CHALLENGE_SET` متى أمكن ومفيدًا. إذا لم يمكن:
`HOLDOUT_NOT_POSSIBLE/NOT_APPLICABLE` مع السبب.

#### A05-R03 — Hard Cases
الحالات الأصعب تُختار عمدًا؛ rarity ليست سببًا للاستبعاد.

## 3. Counterevidence

#### A05-R04 — Search for disconfirmation
يجب البحث عن حالات تناقض أو تحد أو تجعل الدليل non-discriminating، لا انتظار ظهورها عرضًا.

#### A05-R05 — No patching
إذا احتاج النموذج سلسلة exceptions ad hoc، فهذه evidence against model parsimony.

#### A05-D02 — Internal tension
إذا تعارضت مجموعتان داخليتان ولا تحسم الأدلة، سجل `INTERNAL_TENSION_ACKNOWLEDGED` وضيّق النتيجة.

## 4. Competing models

#### A05-R06 — Competitor policy
لا عدد ثابتًا للنماذج. أنشئ أفضل بديل جاد إذا كان موجودًا، وسجل `NO_SERIOUS_COMPETITOR_IDENTIFIED` إن لم يوجد بعد بحث مناسب.

#### A05-T01 — Model comparison
قارن:
coverage، assumptions، hard cases، predictive power، distinctiveness، derivational path، falsification burden.

## 5. Decision

#### A05-D03 — Hypothesis status
`HYPOTHESIZED / TESTED / SUPPORTED / STRONGLY_SUPPORTED / UNRESOLVED / COUNTEREVIDENCE_PRESENT / REJECTED`.

#### A05-G03 — Support decision
لا يتحول كثرة التأويلات المؤيدة إلى قوة إذا كانت كلها مشتقة من نفس observation أو غير مستقلة. التكامل evidence convergence يخضع A12.

## 5.5 Operational falsification contract

#### A05-D04 — C0 qualified-null model
`C0` يعني: **الأدلة الحالية لا تثبت بعد نواة/فرقًا مؤهلًا**. لا يعني «لا توجد نواة» ولا «اللفظ بلا معنى». يستخدم منافسًا منهجيًا يمنع فرض جواب لمجرد الحاجة إلى ملء الخانة.

#### A05-G04 — OPERATIONAL_REJECTION_CONDITION_GATE
كل Hypothesis مركزية يراد ترقيتها إلى Claim قوية تسجل:
```yaml
REJECTION_CONDITION:
  observable_trigger:
  search_space:
  verification_method:
  confound_controls:
  decision_effect: REJECT | NARROW_SCOPE | REOPEN | BLOCK_STRONG_SUPPORT
```
يفشل الشرط إذا كان دائريًا، غير قابل للرصد، أو يفترض مسبقًا النتيجة التي يفترض اختبارها.

#### A05-T02 — Rejection-condition quality test
السؤال: هل يستطيع باحث آخر تحديد ما يبحث عنه وأين وكيف، وماذا سيحدث للClaim إذا وجده؟ إذا لا، فالشرط غير تشغيلي ولا يعد Falsification كافية.

## 6. Failures

#### A05-F01 — MOVING_TARGET
تعديل الفرضية مع كل counterexample بلا revision lineage.

#### A05-F02 — CONFIRMATION_ONLY
البحث عن support فقط.

#### A05-F03 — HOLDOUT_CONTAMINATION
استخدام holdout في توليد النموذج ثم تسميته اختبارًا.

#### A05-F04 — FAKE_COMPETITOR
بديل ضعيف مصطنع لرفع النموذج المفضل.

#### A05-RC01 — Failed prediction
توقع frozen يفشل؛ المطلوب revision/reject لا reinterpretation صامت.

#### A05-RC02 — No competitor
عدم وجود بديل جاد ليس إذنًا لاختراع واحد.

---

## نهاية الملحق

```text
INTEGRATION_RULES = M01 evidence loop; integrates A04 and specialized tests
OUTPUT_CONTRACT = hypothesis ledger + prediction/falsification decision
FAILURE_MODES = moving target, confirmation only, contaminated holdout
REGRESSION_CASES = A05-RC01..02; T01 falsification cases
REOPEN_IF = failed prediction/new counterevidence/competitor/new holdout
END_OF_APPENDIX = A05
```
