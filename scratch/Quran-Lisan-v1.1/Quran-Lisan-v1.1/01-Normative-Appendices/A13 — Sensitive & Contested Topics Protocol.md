---
DOCUMENT_ID: A13
TITLE: "Sensitive & Contested Topics Protocol"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "رفع صرامة البحث في المسائل ذات الإرث التفسيري أو الأثر الفقهي/المذهبي/السياسي/الهووي/الأسري/الأخلاقي."
SCOPE: "الموضوعات الحساسة والمتنازع عليها."
ACTIVATION_CONDITION: "ارتفاع خطر الإسقاط أو selective evidence أو أثر النتيجة."
DEPENDS_ON: [M01, A03, A04, A05, A11, A12]
EXPANDS_MASTER_SECTIONS: [M01-R24]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A13 — Sensitive & Contested Topics Protocol

## 1. Activation

#### A13-D01 — Sensitive topic
موضوع ترتفع فيه مخاطر الانتقاء أو التلوث المسبق أو أثر النتيجة بسبب الفقه/المذهب/السياسة/الهوية/الأسرة/الأخلاق أو إرث تفسيري كثيف.

#### A13-R01 — Open list
تشمل -دون حصر- مسائل التشريع والعقائد الجدلية، السلطة والطاعة والحكم والقتال، الهوية الدينية، الأسرة والجنس واللباس، العقوبات، الاقتصاد المحرم، الحرية الدينية، وسائر القضايا التي تحمل models جاهزة قوية.

## 2. Escalated path

#### A13-G01 — Sensitive Topic Gate
يلزم قبل strong/internal lock:
```text
BLIND_QURANIC_ANALYSIS
→ STRUCTURE / LEXICAL / ROOT as applicable
→ FULL_OR_JUSTIFIED_CORPUS_COVERAGE
→ SCOPE CONTROL
→ PARTICIPANT/LAYER ATTRIBUTION
→ COMPETING MODELS
→ HYPOTHESIS FREEZE
→ PREDICTION/HOLDOUT when possible
→ COUNTEREVIDENCE
→ FALSIFICATION
→ CLAIM_EVIDENCE_LEDGER
→ PURITY CHECK
→ FAILURE SEVERITY
→ COMPLETENESS GATE
→ INTERNAL LOCK
```

#### A13-R02 — Heritage Projection Guard
لا يبدأ البحث بتصنيف فقهي/مذهبي/تفسيري موروث بوصفه meaning. يمكن مقارنته بعد lock وفق [A12-R06].

#### A13-R03 — Modern Ideological Projection Guard
لا يرفض الإطار الحديث بذاته، لكن لا يُسمح له بتوليد semantic result قبل Blind Lock. يشمل political/psychological/scientific/economic/gender/legal frames.

#### A13-R04 — Neutral question
إذا صيغ السؤال لإثبات موقف، افصل `USER_HYPOTHESIS` وصغ سؤالًا محايدًا.

#### A13-R05 — Scope discipline
لا تُحوّل local verse claim إلى نظام سياسي/فقهي/اجتماعي كلي بلا corpus/concept test مستقل.

## 3. Counterevidence and alternatives

#### A13-T01 — Selective Evidence Test
ابحث عمدًا عن passages التي يستخدمها النموذج المنافس أو التي تبدو عكس الاتجاه الحالي.

#### A13-T02 — Competing Model Test
يجب تقديم أقوى نموذج جاد لا caricature. إذا كان غير قابل للتمييز evidence-wise، النتيجة `UNRESOLVED`.

#### A13-T03 — Purity Test
يسجل لكل dimension `EVALUATED_CLEAN/ISSUE_FOUND/NOT_EVALUATED/NOT_APPLICABLE`; لا تساوي عدم الفحص بالنقاء.

## 4. Output

#### A13-O01 — Sensitive result
المخرج يعلن scope، evidence/counterevidence، competing models، purity، three axes، ما هو Quran-internal وما هو external comparison، وما لم يحسم.

#### A13-F01 — HERITAGE_LEAKAGE
استخدام الحكم الموروث لتعيين المعنى الداخلي قبل البحث.

#### A13-F02 — MODERN_IDEOLOGICAL_PROJECTION
إسقاط model حديث ثم البحث عما يؤيده.

#### A13-F03 — ADVOCACY_COLLAPSE
تحويل التحليل إلى دفاع عن موقف بدل اختبار claims.

#### A13-RC01 — Attractive modern frame
إطار معاصر يفسر بعض الشواهد لكنه يفشل hard case → لا يُرقى.

#### A13-RC02 — Dominant heritage reading
شيوع القراءة لا يغني عن internal evidence؛ agreement after lock يسجل comparison لا proof.

---

## نهاية الملحق

```text
INTEGRATION_RULES = M01 sensitive escalation + A03/A04/A05/A11/A12
OUTPUT_CONTRACT = sensitive result with purity/three axes/models
FAILURE_MODES = heritage leakage, modern projection, selective evidence
REGRESSION_CASES = A13-RC01..02; T01 projection cases
REOPEN_IF = new counterevidence/model/purity issue/scope expansion
END_OF_APPENDIX = A13
```
