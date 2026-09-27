---
DOCUMENT_ID: A07
TITLE: "Event, Transformation, Attentional Orientation & Practical Reconstruction"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "إعادة بناء الحدث والتحول والانتباه والحد الأدنى العملي دون اختراع خانات."
SCOPE: "الأفعال والأوامر والنواهي والحالات الممتدة والأسئلة العملية."
ACTIVATION_CONDITION: "EVENT/PRACTICE/ATTENTION target أو سؤال كيف/ماذا أفعل."
DEPENDS_ON: [M01]
EXPANDS_MASTER_SECTIONS: [M01-R16, M01-R17, M01-R18]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A07 — Event, Transformation, Attentional Orientation & Practical Reconstruction

## 1. Event State Model

#### A07-D01 — Event states
`ENTRY / ACTIVE / COMPLETION / POST_STATE` فئات ممكنة وليست واجبة.

#### A07-R01 — Minimal model
```text
PRE_STATE? → TRIGGER/ENTRY → ACTIVE_STATE → CORE_ACTIONS/RESTRAINTS → COMPLETION? → POST_STATE?
```
علامة `?` تعني أن الحقل لا ينشأ بلا evidence.

#### A07-R02 — Pre-state/Causal Guard
لا تستنتج `PRE_STATE` من نقيض النتيجة، `FAILURE_PATH` من ضد لغوي، `RECOVERY_PATH` لإكمال الرسم، causality من sequence، أو teleological hierarchy من causality.

#### A07-T01 — Transition test
لادعاء transition يلزم بقدر الادعاء: pre/active evidence، transition marker، post-effect، وضبط المشاركين/المجال. إذا نقص جزء: `PARTIALLY_ESTABLISHED`.

## 2. Transformation

#### A07-R03 — Transformation Model
افحص - دون افتراض -: conduct، self-restraint، attention/remembrance، relational/social/protective/economic/communal/ethical effects.

#### A07-T02 — Persistent effect
لا تثبت `PERSISTENT_EFFECT` لمجرد أن النتيجة مرغوبة. يلزم witness أو network support.

## 3. Attentional Orientation

#### A07-D02 — Orientation classes
`TEXTUALLY_REQUIRED_ORIENTATION / SUPPORTED_ATTENTIONAL_FRAME / REFLECTIVE_IMPLICATION / PERSONAL_MEDITATION`.

#### A07-R04 — Orientation evidence
النص المباشر في الذكر/العلم/التفكر/الخشية/التعظيم/الشكر قد يثبت orientation؛ network repeated support قد يثبت frame؛ الاستنباط النافع يبقى reflective.

#### A07-R05 — Mental State Projection Guard
لا تستنتج نية/خشوع/شعورًا نفسيًا من حركة خارجية فقط، ولا تحول منفعة نفسية متوقعة إلى مقصد.

## 4. Practical Reconstruction

#### A07-O01 — Practical fields
```text
ENTRY_CONDITION =
ACTIONS =
RESTRAINTS =
ACTIVE_STATE =
BOUNDARIES =
COMPLETION_CONDITION =
POST_STATE =
TEXTUAL_OPEN_SPACE =
```

#### A07-G01 — No Slot Filling
أي حقل بلا evidence = `NOT_ESTABLISHED` أو `NOT_APPLICABLE`.

#### A07-G02 — Practical Reconstruction Gate
لكل action/restraint صنف:
`TEXTUALLY_REQUIRED / TEXTUALLY_SUPPORTED / STRONGLY_ENTAILED / OPTIONAL_HUMAN_IMPLEMENTATION / NOT_ESTABLISHED`.

لا تستخرج number/order/time/place/formula/posture/clothing/tool من wisdom/root/common practice وحدها.

#### A07-R06 — Purpose does not replace action
معرفة الحكمة لا تلغي الفعل النصي، وتنفيذ الفعل لا يغني عن تحليل purpose/result عندما يكون السؤال عنها.

## 5. Boundaries

#### A07-R07 — Intrinsic vs priority
فرّق `INTRINSIC_PROHIBITION` عن `TEMPORAL_PRIORITY_CONFLICT`; تراجع نشاط مشروع خلال نافذة أولوية لا يجعله محرمًا بذاته.

#### A07-O02 — Event/practice output
يشمل states المثبتة فقط، actions/restraints بدرجاتها، orientation بدرجتها، transformation بدرجته، unsupported details، و`REOPEN_IF`.

#### A07-F01 — PRESTATE_INVENTION
اختراع حالة سابقة من نتيجة لاحقة.

#### A07-F02 — PRACTICAL_SLOT_FILLING
اختراع عدد/هيئة/ترتيب من الفراغ.

#### A07-F03 — MENTAL_PROJECTION
نسبة شعور أو قصد بلا witness.

#### A07-RC01 — Result without prestate
نتيجة صريحة ولا prestate صريح → لا تخترع prestate.

#### A07-RC02 — Rich template, sparse text
النتيجة الصحيحة عدة `NOT_ESTABLISHED`.

---

## نهاية الملحق

```text
INTEGRATION_RULES = M01 event/practical rules; text-open decision delegated to A08
OUTPUT_CONTRACT = EVENT/PRACTICAL result
FAILURE_MODES = prestate invention, slot filling, mental projection
REGRESSION_CASES = A07-RC01..02; T01 pre-state/slot cases
REOPEN_IF = new event witness/practical detail/orientation evidence
END_OF_APPENDIX = A07
```
