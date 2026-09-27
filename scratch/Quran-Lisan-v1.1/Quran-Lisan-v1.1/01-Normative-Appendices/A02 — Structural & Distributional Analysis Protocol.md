---
DOCUMENT_ID: A02
TITLE: "Structural & Distributional Analysis Protocol"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "فصل البنية والتوزيع والمشاركين عن الدلالة الجذرية وضبط التحليل البنيوي."
SCOPE: "الصرف والنحو والتعدية والتوزيع والجيران والشبكات المفهومية."
ACTIVATION_CONDITION: "كل بحث دلالي؛ تتوسع الوحدات بحسب الظاهرة."
DEPENDS_ON: [M01]
EXPANDS_MASTER_SECTIONS: [M01-P04, M01-R07, M01-R08]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A02 — Structural & Distributional Analysis Protocol

## 1. Firewall

#### A02-P01 — Structure before semantics
الوصف البنيوي يسبق تفسيره. يُسمح بإثبات root/POS/form/marker/relation البنيوية إذا تحققت، لكن لا تُحوّل تسمية محفوظة إلى وظيفة دلالية بلا اختبار.

#### A02-R01 — Grammatical Function Quarantine
```text
STRUCTURAL_FACT ≠ SEMANTIC_FUNCTION
MORPHOLOGICAL_FORM ≠ MORPHOLOGICAL_MEANING
GRAMMAR_RULE_FROM_MEMORY ≠ QURAN_INTERNAL_EVIDENCE
```
مثال فشل: `Form X → طلب` أو `لام → تعليل` بوصفهما حسمًا داخليًا قبل شبكة الاستعمال.

#### A02-G01 — Layer Attribution Gate
لكل فرق دلالي مقترح اسأل بالترتيب:
`ROOT → DERIVATION → LEXICAL_UNIT → FORM → CONSTRUCTION → PARTICIPANTS → CONTEXT → DISCOURSE/RHETORIC`.
لا يرقى الفرق إلى طبقة أعلى إذا كفت طبقة أدنى لتفسيره.

## 2. Morphology

#### A02-R02 — Morphology pass
سجل surface/lemma/root/POS/form. قارن المجرد والمزيد، الفعل/الاسم/المصدر/الصفة/اسم الفاعل/اسم المفعول والجمع، لكن استنتج أثر الصيغة من distribution لا من label وحده.

#### A02-T01 — Form effect test
ثبّت core/participant/domain بقدر الإمكان وقارن occurrences ذات form مختلف. إذا اختلط العامل، `FORM_EFFECT = UNRESOLVED`.

## 3. Syntax, Scope, Reference

#### A02-R03 — Constructional semantics
افحص التعدية، المتعلقات، حروف الجر، الفاعل والمفعول، المعرفة/النكرة، المفرد/الجمع، البناء للمعلوم/المجهول، الزمن، الشرط، الاستثناء، النفي، الترتيب والإحالة.

#### A02-T02 — Reference resolution
أي ضمير/إشارة/موصول/حذف يؤثر في event structure يجب أن يكون مرجعه متحققًا أو `UNRESOLVED`.

#### A02-T03 — Scope analysis
حدد نطاق النفي/العموم/الخصوص/الشرط/الاستثناء والكمية قبل أي inference. خطأ scope قد يبطل claim.

## 4. Participants & Valency

#### A02-R04 — Participant roles
استخدم عند الانطباق:
`AGENT, PATIENT, EXPERIENCER, SOURCE, GOAL, BENEFICIARY, INSTRUMENT, LOCATION, CAUSE`.
صفة المشارك لا تصبح مكوّنًا معجميًا تلقائيًا.

#### A02-T04 — Participant confound
عند مقارنة موضعين، إذا تغير participant class تغيرًا يمكن أن يفسر الفرق، لا تنسب الفرق للفظ قبل control.

#### A02-R05 — Valency
سجل أنماط التعدية والمتعلقات، واترك `VALENCY_EFFECT = UNRESOLVED` إذا لم تتكرر شبكة تكفي للاستنتاج.

## 5. Distribution

#### A02-R06 — Full Distributional Analysis
افحص مواضع الظهور، الصيغة، البناء، المشاركين، المجال، الجيران، النتائج، وما يبقى ثابتًا. يحظر `CHERRY_PICKING`.

#### A02-R07 — Usage clustering
يجوز تجميع الاستعمالات حسب form/construction/participants/domain، لكن:
`USAGE_CLUSTER ≠ INDEPENDENT_ROOT_MEANING`.

#### A02-R08 — Collocation
```text
CO_OCCURRENCE ≠ ASSOCIATION ≠ RELATION ≠ SEMANTIC_COMPONENT
```
التكرار يرشح علاقة للفحص ولا يثبت أن المصاحب جزء من معنى اللفظ.

#### A02-R09 — Negative distribution
تفعّل فقط مع شروط [A03-G02]. الغياب المتوقع أداة falsification لا برهانًا منفردًا.

## 6. Neighbors, contrasts, networks

#### A02-R10 — Near Neighbor Differentiation
قارن الجيران عبر الفاعل، المتأثر، الاتجاه، المدة، القوة، المرحلة، الإرادية، النتيجة، البناء والمجال. النتيجة الصحيحة قد تكون `NO_DIFFERENCE_ESTABLISHED`.

#### A02-R11 — Concept Network
يجوز إنشاء edges من أنواع: `CAUSE, PURPOSE, MEANS, RESULT, PART_OF, CONTRAST, ASSOCIATION, CONDITION, SEQUENCE` بشرط witness + relation type + support status. `GRAPH_EDGE ≠ SEMANTIC_TRUTH`.

#### A02-R12 — Parallelism
التوازي لا يثبت synonymy أو antonymy تلقائيًا. استخرج المتغيرات والثوابت ثم اختبر العلاقة.

## 7. Discourse/Rhetorical phenomena

#### A02-R13 — Conditional activation
الالتفات، التقديم/التأخير، المتشابهات اللفظية، الفاصلة، القسم، الاستفهام، الحذف/الإضمار، المناسبة، التكرار، ring composition والأنماط التصورية تُفعّل عند ثبوت phenomenon فقط، لا لمجرد أن target آية/سورة.

#### A02-T05 — Rhetorical function test
`PHENOMENON_DETECTED → FUNCTION_HYPOTHESIS → PARALLEL/DISTRIBUTION TEST → LOCAL_FUNCTION`.
يجوز `FUNCTION_UNRESOLVED`.

#### A02-F01 — RHETORICAL_LABEL_FALLACY
`هذا تقديم → إذن حصر`، أو `استفهام → توبيخ` بلا اختبار.

#### A02-F02 — HADHF_OVERREACH
اختراع محذوف ثم بناء معنى عليه. المقبول: عنصر `TEXTUALLY_REQUIRED_OR_STRONGLY_CONSTRAINED`.

## 8. Tool-neutral result

#### A02-O01 — Structural result
```yaml
STRUCTURAL_DISTRIBUTIONAL_RESULT:
  verified_structure: []
  morphology:
  construction:
  scope:
  reference_resolution:
  participants: []
  valency:
  distribution_patterns: []
  negative_distribution:
  neighbors: []
  concept_relations: []
  layer_attribution:
  unresolved: []
  does_not_prove: []
```

#### A02-RC01 — Grammar leakage
وسم نحوي صحيح لكن inference غير مختبر → FAIL.

#### A02-RC02 — Participant confound
فرق ظاهري يختفي عند ضبط الفاعل/المفعول → لا يرقى للlexeme/root.

#### A02-RC03 — Construction confound
حرف جر/تركيب يفسر الفرق → لا ينسب للجذر.

---

## 7. Target Contract & comparison level

#### A02-R14 — TARGET_CONTRACT
قبل Structural/Distributional pass حدد `ANALYSIS_UNIT = ROOT | LEXEME | FORM | CONSTRUCTION | LOCAL_MEANING | VERSE | CONCEPT | COMPARISON | PRACTICE`. أي مقارنة دلالية تستخدم المستوى نفسه على الطرفين؛ لا يقارن Root بLocal Meaning لجار ثم يستنتج Distinctiveness جذرية.

#### A02-R15 — General participant roles first
لا تفترض `AGENT/PATIENT` في كل بناء. استخدم أدوارًا أعم مثل `ROLE_1/ROLE_2/EXPERIENCER/SOURCE/GOAL/BENEFICIARY/AFFECTED_ENTITY` ثم خصصها فقط عندما تثبت البنية ذلك.

#### A02-F03 — LEVEL_MISMATCH
استخراج فرق دلالي من مقارنة طرفين على مستويين مختلفين (`ROOT vs LOCAL_MEANING`, `LEXEME vs CONSTRUCTION`) دون ضبط.


## 8. Experimental structural hypotheses

#### A02-R16 — Morphological Operator Guard
إذا استُخدم مفهوم `MORPHOLOGICAL_OPERATOR` لتفسير أثر وزن/صيغة، فيجب فصل `STRUCTURAL_OBSERVATION` عن `OPERATOR_SEMANTIC_CLAIM`. لا يكفي وجود الوزن لإثبات دلالته، ولا تستخدم مساهمة operator غير متحققة كدليل وحيد على `ROOT_AXIAL_MEANING`.

#### A02-R17 — LETTER_SEMANTICS_GUARD
أي برنامج بحث في دلالات الحروف أو phonological/letter patterns يبقى `HYPOTHESIS_GENERATION` ما لم يعتمد له corpus evidence وبوابة مستقلة. لا يستخدم sole evidence لتعريف الجذر أو قفله، ولا تُرفع نضجه لمجرد وجود schema/tool.

#### A02-RC04 — Letter-only core
فرضية Root Core مبنية أساسًا على دلالة الحروف مع ضعف distributional evidence. المتوقع: لا Strong Core؛ الحروف discovery hypothesis فقط.


## نهاية الملحق

```text
INTEGRATION_RULES = M01 structural firewall; feeds A01/A09/A10
OUTPUT_CONTRACT = STRUCTURAL_DISTRIBUTIONAL_RESULT
FAILURE_MODES = grammar leakage, participant/construction confound, rhetorical label fallacy
REGRESSION_CASES = A02-RC01..03; T01 structural cases
REOPEN_IF = new verified construction/distribution or resolved confound
END_OF_APPENDIX = A02
```
