---
DOCUMENT_ID: A12
TITLE: "Source, Tool & External Comparison Governance"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "ضبط المصادر والأدوات والاكتشاف الحاسوبي والمقارنة الخارجية وحدود السلطة."
SCOPE: "الاسترجاع والصرف والشبكات والـembeddings والذكاء الاصطناعي والمصادر الخارجية."
ACTIVATION_CONDITION: "عند استخدام أي مصدر أو أداة أو post-lock comparison."
DEPENDS_ON: [M01, A03, A04, A05, A11]
EXPANDS_MASTER_SECTIONS: [M01-P10, M01-R22, M01-R23]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A12 — Source, Tool & External Comparison Governance


## 0. Canonical governance IDs

#### A12-R01 — Source roles
`QURAN_TEXT / STRUCTURE_ONLY / INTERNAL_OBSERVATION / DISCOVERY_ONLY / EXTERNAL_SEMANTICS / PRIOR_PROJECT_RESULT`. Field role يحدد ما يجوز للمعلومة أن تثبته.

#### A12-R02 — Parametric Prior Risk
`PARAMETRIC_PRIOR_RISK = PRESENT_AND_UNQUANTIFIED`. Blind Lab يعزل المصادر المدخلة، لا يدعي محو prior knowledge.

#### A12-R03 — Tool Receipt
كل أداة مستخدمة تسجل: tool, input/query, output/artifact, field role, verified status, corpus/model version عند الصلة.

#### A12-R04 — Discovery is not evidence
`COMPUTATIONAL_OUTPUT = CANDIDATE/DISCOVERY_AID` إلى أن يعود للشاهد القرآني ويُتحقق منه.

#### A12-R05 — Tool activation contract
لكل أداة:
```text
TRIGGER_PHENOMENON
MINIMUM_EVIDENCE_TO_ACTIVATE
WHAT_IT_CAN_REVEAL
WHAT_IT_CANNOT_PROVE
INTERACTION_WITH_OTHER_TOOLS
DEACTIVATION_CONDITION
```

#### A12-R06 — Post-Lock External Comparison
لا يبدأ external semantics قبل internal snapshot. كل معلومة تصنف: agrees/contradicts/adds/potential-counterevidence/not-relevant، وتسجل في influence log.

#### A12-G01 — Tool Authority Gate
لا أداة منفردة تمنح semantic verdict. المرشحات الحاسوبية أو الخارجية تحتاج source resolution + textual verification + claim/evidence admission.

## 0.1 Tool Activation Registry

| Tool family | Trigger | Minimum evidence | Can reveal | Cannot prove | Interaction | Deactivate when |
|---|---|---|---|---|---|---|
| Corpus retrieval | lexical/root/query target | verified corpus access | occurrences/forms | meaning | feeds A03/A02 | retrieval complete |
| Full distribution | general lexical/root claim | sufficient indexed set | patterns/invariants | causal/purpose by itself | A01/A02/A05 | scope analyzed |
| Morphology | form variation | verified form labels | contrasts by form | form meaning automatically | A02 | no material form contrast |
| Syntax/scope | construction present | verified parse/relations | structural constraints | semantic function automatically | A02 | structure stable |
| Participants/valency | event predicate | roles identifiable | role patterns | root component automatically | A02/A07 | non-applicable |
| Collocation | repeated co-occurrence | verified counts/contexts | candidate association | semantic component | A02/A05 | no useful pattern |
| Reverse | contrast/negation/reversal | A09 entry conditions | boundaries | full meaning | A09 | no relation established |
| Scene/event | event/passage | enough textual state evidence | transitions/roles | hidden states | A07/A10 | event model not useful |
| Rhetorical passes | phenomenon detected | actual structural shift/pattern | discourse function candidates | function from label | A02 | phenomenon absent |
| Graph/network | relation discovery | nodes/edges traceable | candidate relations | truth | A02/A12 | candidates resolved |
| Embeddings | neighbor/outlier discovery | benchmarked model + proper space | candidates/outliers | Quranic semantic proximity as fact | A05/A12 | candidates exhausted |
| Statistical clustering | large distribution | sufficient sample | clusters | independent senses | A02 | no stable cluster |
| LLM discovery | exploration | constrained prompt + source boundary | hypotheses/counterexamples | evidence/gate pass | A05 | candidate list adequate |
| External lexicon/tafsir | post-lock comparison | internal snapshot exists | historical alternatives | internal proof | A11/A12 | comparison complete |

## 0.2 Tool Reality & fallback governance

#### A12-R07 — Actual execution only
لا يُسجل `VALIDATOR_PASSED`, `TOOL_EXECUTED`, retrieval count، أو أي runtime fact إلا من تشغيل فعلي أو receipt قابل للتتبع. محاكاة المنطق أو معرفة النموذج ليست runtime evidence.

#### A12-D01 — Execution evidence mode
```text
EXECUTION_EVIDENCE_MODE =
  VERIFIED_TOOLING
  | AUTHORITY_APPROVED_FALLBACK
  | MANUAL_REPRODUCIBLE_CHECK
  | EXPLORATORY_ONLY
  | NO_VALID_FALLBACK
```

#### A12-G02 — Fallback Gate
إذا تعذر Tool لازم:
1. استخدم fallback مصرحًا وقابلًا لإعادة الإنتاج في دوره فقط؛ أو
2. صنف المخرج `EXPLORATORY_ONLY` ولا تسجله Observation/Evidence؛ أو
3. إذا لا fallback صالح، سجّل `TOOL_UNAVAILABLE / NOT_VERIFIED` وخفض/أوقف claim المتأثرة.

#### A12-R08 — Expanded Tool Receipt
لكل أداة مؤثرة سجل:
```yaml
TOOL_RECEIPT:
  tool:
  trigger:
  source_role:
  actual_execution:
  corpus_or_input:
  what_it_can_reveal:
  what_it_cannot_prove:
  output_used:
  evidence_effect:
```

#### A12-R09 — Internal result snapshot freeze
قبل فتح external semantics يجمّد `INTERNAL_RESULT_SNAPSHOT` بما يحفظ claims/evidence/counterevidence/dependencies/corpus identity. `snapshot_hash` مستحب عند توفر artifacts ثابتة، وليس شرطًا إن لم تدعم البيئة ذلك.

#### A12-R10 — External influence log
كل مصدر خارجي بعد القفل يسجل: `SOURCE`, `ROLE`, `CLAIM_COMPARED`, `AGREEMENT/DISAGREEMENT`, `IMPACT`. لا يتحول توافق المصدر لاحقًا إلى Internal Evidence بأثر رجعي.

## 1. Detailed Tooling Annex

# 1. الغرض من الملحق

يحدد هذا الملحق مجموعة الأدوات المعتمدة في `Quran Lisan v1.1` لكشف المعنى واختباره وتفسير كيفية تشكله داخل الاستعمال القرآني.

ولا يقصد بالأداة هنا «قاعدة تفسير جاهزة»، وإنما:

> **إجراء تحليلي منضبط يستخرج ملاحظة قابلة للفحص من النص، ثم يحدد مقدار ما تسمح تلك الملاحظة بإثباته وما لا تسمح بإثباته.**

وتنقسم وظيفة الأدوات إلى أربع طبقات:

```text
DISCOVERY
    ↓
EVIDENCE EXTRACTION
    ↓
SEMANTIC TESTING / FALSIFICATION
    ↓
EVIDENCE CONVERGENCE
```

ولا يجوز اختصار هذه السلسلة إلى:

```text
وجود ظاهرة لغوية
→ إذن المعنى الفلاني صحيح
```

---

# 2. القاعدة الحاكمة

أقوى أداة في Quran Lisan ليست الالتفات، ولا الفاصلة، ولا الاشتقاق، ولا الإحصاء، ولا التضمينات.

الأداة الحاكمة هي:

> `FULL INTERNAL DISTRIBUTIONAL ANALYSIS + FALSIFICATION + EVIDENCE CONVERGENCE`

أي:

1. استقراء الاستعمالات ذات الصلة.
2. تحليل بنيتها.
3. اقتراح نموذج دلالي.
4. البحث عن الشواهد المقاومة له.
5. مقارنته بأفضل نموذج منافس.
6. اختبار قدرته التفسيرية والتنبؤية.
7. تحديد ما يثبته النص وما يبقى فرضية.
8. عدم رفع الثقة إلا عند تقاطع أدلة مستقلة.

وعليه:

```text
ONE TOOL ≠ SEMANTIC VERDICT
```

و:

```text
MULTIPLE CORRELATED OBSERVATIONS
≠
MULTIPLE INDEPENDENT EVIDENCE SOURCES
```

---

# 3. طبقات الأدلة

يعتمد v1.1 التمييز بين ست طبقات.

## 3.1 `DIRECT_INTERNAL_EVIDENCE`

علاقة يصرح بها النص أو يبنيها بصورة مباشرة، مثل:

* تفسير بعد إجمال.
* بدل.
* عطف بيان.
* تصريح بسبب أو شرط أو نتيجة.
* تعريف أو وصف داخلي واضح.
* علاقة نحوية صريحة.

هذه أعلى الأدلة الداخلية من حيث المباشرة.

---

## 3.2 `DISTRIBUTIONAL_INTERNAL_EVIDENCE`

ينشأ من:

* تكرر الاستعمال.
* توزيع المفردة.
* المشاركين.
* الأبنية.
* الجيران.
* المجالات.
* أنماط الحضور والغياب.

وهو قوي بقدر اكتمال التغطية.

---

## 3.3 `STRUCTURAL_INTERNAL_EVIDENCE`

يشمل:

* التركيب.
* التعدية.
* التقديم.
* النفي.
* الاستثناء.
* الإحالة.
* التوازي.
* التكرار مع التغيير.
* بنية الخطاب.
* المشهد.

ولا يجوز تحويل اسم الظاهرة النحوية أو البلاغية مباشرة إلى وظيفة دلالية.

---

## 3.4 `CONVERGENT_INTERNAL_EVIDENCE`

ينشأ عندما تصل أدوات مستقلة نسبيًا إلى القيد الدلالي نفسه.

مثال منهجي:

```text
الاشتقاق
+
التوزيع
+
المشاركون
+
الجيران
+
الشواهد الصعبة
        ↓
قيد دلالي مشترك
```

وهذه أقوى من تكرار الشاهد نفسه بصور مختلفة.

---

## 3.5 `COMPUTATIONAL_DISCOVERY`

يشمل:

* البحث الآلي.
* الإحصاءات.
* الشبكات.
* Topic Modeling.
* Embeddings.
* LLM suggestions.
* clustering الآلي.

وحكمه:

```text
COMPUTATIONAL_OUTPUT
=
CANDIDATE / DISCOVERY AID

COMPUTATIONAL_OUTPUT
≠
QURANIC SEMANTIC EVIDENCE
```

حتى تتم إعادته إلى الشاهد القرآني وفحصه.

---

## 3.6 `EXTERNAL_POST_LOCK`

يشمل:

* المعاجم.
* غريب القرآن.
* التراث التفسيري.
* الدراسات اللسانية.
* أسباب النزول.
* الدراسات الحديثة.
* الأطر الفلسفية والمعرفية.

وهذه لا تدخل في تأسيس `INTERNAL_SEMANTIC_RESULT` قبل الموضع الذي تسمح به منهجية LISAN.

---

# 4. العائلات الكبرى لأدوات v1.1

تعتمد المنهجية ثماني عائلات مترابطة:

```text
A. CORPUS & DISTRIBUTION
B. ROOT & LEXICAL SEMANTICS
C. CONSTRUCTION & PARTICIPANT STRUCTURE
D. SEMANTIC RELATIONS & LOGIC
E. DISCOURSE, RHETORIC & STRUCTURE
F. SCENE, NARRATIVE & ARGUMENT
G. COMPUTATIONAL DISCOVERY
H. VALIDATION, FALSIFICATION & CONVERGENCE
```

وتوجد طبقة مستقلة بعد القفل:

```text
POST_LOCK_EXTERNAL_ENRICHMENT
```

---

# 5. العائلة A — Corpus & Distribution

## A1. `FULL_DISTRIBUTIONAL_ANALYSIS`

### الوظيفة

حصر الاستعمال القرآني ذي الصلة وفحص:

* أين يظهر اللفظ؟
* بأي صيغة؟
* مع من؟
* في أي بناء؟
* ما المشاركون؟
* ما المجال؟
* ما النتيجة؟
* ما الذي يبقى ثابتًا رغم تغير السياقات؟

### المبدأ

> المعنى المحوري الأقوى هو الذي يفسر أكبر قدر من الاستعمال بأقل قدر من الافتراضات الإضافية.

### الضابط

يحظر:

```text
CHERRY_PICKING
```

أي بناء النظرية من الشواهد السهلة مع تجاهل الشاهد المقاوم.

---

## A2. `QURANIC_SELF_EXPLANATION`

يفحص الحالات التي يفسر فيها السياق القرآني المفهوم مباشرة بواسطة:

* بيان.
* تفصيل.
* بدل.
* وصف.
* نتيجة صريحة.
* مقابل صريح.
* علاقة تفسيرية.

السؤال الحاكم:

> هل يقدم النص نفسه جوابًا مباشرًا أو شبه مباشر عن: ما هذا؟ ماذا يفعل؟ ما أثره؟ وما علاقته بما حوله؟

---

## A3. `NEGATIVE_DISTRIBUTION`

لا يدرس مواضع الظهور فقط، بل مواضع الغياب المتوقع.

السؤال:

> أين كان يمكن -وفق الفرضية- توقع اللفظ، لكن القرآن استعمل لفظًا آخر؟

قد تكشف هذه الأداة الحد الفاصل بين لفظين قريبين.

لكن:

```text
NEGATIVE_DISTRIBUTION
REQUIRES
CORPUS_COVERAGE
```

ولا يجوز الاستدلال بالغياب من بحث ناقص.

---

## A4. `USAGE_CLUSTERING`

يجمع الاستعمالات بحسب:

* الصيغة.
* البناء.
* المشاركين.
* المجال.
* الجيران.
* النتيجة.

لكن:

```text
USAGE_CLUSTER
≠
INDEPENDENT_ROOT_MEANING
```

فالهدف تفسير كيفية تحقق النواة الواحدة داخل أنماط استعمال مختلفة، لا اختراع «جذر دلالي» لكل مجموعة.

---

## A5. `PREDICTIVE_SEMANTIC_TEST`

بعد صياغة فرضية دلالية يطلب منها أن تتنبأ بما ينبغي أن يظهر في شواهد لم تستخدم في بنائها.

```text
MODEL
→ PREDICTION
→ UNSEEN / HELD-OUT EVIDENCE
→ TEST
```

وتعد هذه أقوى من مجرد إعادة تفسير البيانات التي ولدت منها الفرضية.

---

## A6. `HARD_CASES_AND_OUTLIERS`

يجب البحث عمدًا عن:

* أندر صيغة.
* أصعب سياق.
* الاستعمال الذي يبدو مخالفًا.
* السياق الذي يحتاج أكبر قدر من الافتراضات.

القاعدة:

> **الشاهد الصعب ليس هامشًا، بل اختبار صحة للنواة.**

ولا يجوز التخلص منه بإعلان «معنى مستقل» دون دليل.

---

# 6. العائلة B — Root & Lexical Semantics

## B1. `DERIVATIONAL_FAMILY`

يقارن:

* المجرد والمزيد.
* الفعل والاسم.
* المصدر.
* الصفة.
* اسم الفاعل.
* اسم المفعول.
* الصيغ المختلفة.

والسؤال:

> ما الذي يبقى ثابتًا؟ وما الذي يمكن تفسيره بوصفه أثر الصيغة؟

---

## B2. `ROOT_UNITY`

يفترض وحدةً مرشحة للجذر بوصفها **فرضية قابلة للنقض**، وليس مسلمة مطلقة.

ولا يقبل `ROOT_AXIAL_MEANING` حتى يستطيع تفسير فروع الاستعمال دون:

* تعميم فارغ.
* مجاز غير مبرهن.
* استثناءات اعتباطية.
* تقسيم سريع إلى معان غير مترابطة.

---

## B3. `CORE_NECESSITY_TEST`

السؤال:

> إذا حذفنا النواة المقترحة من تفسير الاستعمالات، هل نفقد شيئًا ضروريًا؟

إذا كان لا، فالنواة قد تكون:

* عامة أكثر من اللازم.
* وصفية فقط.
* زخرفية.
* غير مفسرة فعليًا للبيانات.

---

## B4. `DERIVATIONAL_EXPLAINABILITY`

يجب أن يسمح النموذج بمسار منضبط:

```text
ROOT_AXIAL_MEANING
→ MORPHOLOGICAL EFFECT
→ CONSTRUCTIONAL EFFECT
→ CONTEXTUAL EFFECT
→ LOCAL USAGE
```

إذا كان المعنى الموضعي لا يمكن اشتقاقه إلا بإضافة معنى مستقل غير مبرر، فالنموذج يحتاج مراجعة.

---

## B5. `CORE_DISTINCTIVENESS`

السؤال:

> هل النواة المقترحة تميز هذا الجذر عن أقرب جذوره الدلالية؟

إذا كان التعريف يصلح لعشرة جذور أخرى بالسهولة نفسها فهو أوسع مما ينبغي.

---

## B6. `NEAR_NEIGHBOR_DIFFERENTIATION`

تقارن المفردة بأقرب لفظ يؤدي وظيفة مشابهة.

محاور المقارنة المحتملة:

* الفاعل.
* المتأثر.
* الاتجاه.
* المدة.
* القوة.
* النتيجة.
* المرحلة.
* الإرادية.
* نوع العلاقة.
* البناء النحوي.

وهي كثيرًا ما تكون أدق من المقارنة بالضد.

---

## B7. `CONTRAST_AND_OPPOSITION`

يدرس:

* التضاد.
* التقابل.
* المقابلة النصية.

لكن:

```text
A CONTRASTED WITH B
≠
A = EXACT OPPOSITE OF B
```

فالتقابل قد يكون:

* أخلاقيًا.
* وظيفيًا.
* سرديًا.
* بنيويًا.
* نسبيًا.
* سياقيًا.

---

## B8. `COUNTERFACTUAL_SUBSTITUTION`

تختبر استبدال المفردة بأقرب بديل:

> ماذا نفقد؟ وما القيد الذي يتغير؟

إذا لم يتغير شيء قابل للإثبات فلا يجوز اختراع فارق.

---

## B9. `SEMANTIC_FIELD_ANALYSIS`

يبني شبكة الحقل الذي تتحرك فيه المفردة من داخل القرآن.

ولا يعني وجود لفظين في الحقل نفسه أنهما مترادفان.

الناتج المطلوب:

```text
CENTRAL_CONCEPT
NEIGHBORS
CONTRASTS
CAUSES
RESULTS
MEANS
PARTICIPANTS
BOUNDARIES
```

---

## B10. `COMPONENTIAL_ANALYSIS`

يفكك الفروق إلى سمات دلالية مرشحة، مثل:

```text
[±VOLITION]
[±INTENSITY]
[±DURATION]
[±DIRECTNESS]
[±SOCIAL]
[±INTERNAL]
```

لكن السمات لا تعتمد إلا إذا كان النص يدعمها.

---

# 7. العائلة C — Construction & Participant Structure

## C1. `CONSTRUCTIONAL_SEMANTICS`

تدرس معنى اللفظ داخل البناء، بما في ذلك:

* حروف الجر.
* التعدية.
* المفعولات.
* المبني للمعلوم والمجهول.
* المعرفة والنكرة.
* الإضافة.
* التقديم.
* الاستثناء.
* الشرط.

المبدأ:

> قد يحمل البناء قيدًا دلاليًا لا يوجد في المفردة المعزولة.

---

## C2. `VALENCY_AND_PARTICIPANT_ROLES`

يحلل بنية الحدث:

```text
AGENT
PATIENT
EXPERIENCER
SOURCE
GOAL
BENEFICIARY
INSTRUMENT
LOCATION
CAUSE
```

والهدف فصل:

```text
LEXICAL CORE
```

عن:

```text
PARTICIPANT EFFECT
```

---

## C3. `REFERENCE_RESOLUTION`

يفحص:

* الضمائر.
* أسماء الإشارة.
* الموصولات.
* المحذوفات الإحالية.
* تبدل المخاطب.

لأن خطأ مرجع واحد قد يغير بنية الحدث كاملة.

---

## C4. `SCOPE_ANALYSIS`

يحدد نطاق:

* النفي.
* العموم.
* الخصوص.
* الاستثناء.
* الشرط.
* الموصول.
* الكمية.

ويمنع نسبة معنى إلى المفردة وهو في الحقيقة ناتج عن نطاق التركيب.

---

## C5. `POLARITY_ANALYSIS`

يقارن:

```text
X
NOT-X
```

أو:

```text
AFFIRMATION
NEGATION
```

لدراسة أي عناصر تتغير وأيها يبقى ثابتًا.

---

## C6. `CONDITIONAL_AND_EXCEPTION_ANALYSIS`

السؤال:

> متى يعمل الحكم؟ ومتى يتوقف؟ وما الذي يكشفه الاستثناء عن حدوده؟

وقد تكون الحالة المستثناة أكثر كشفًا من الحالة العادية.

---

# 8. العائلة D — Semantic Relations & Logic

## D1. `COLLOCATION_ANALYSIS`

تحلل التشارك المتكرر بين الألفاظ.

لكن يجب الفصل بين:

```text
CO-OCCURRENCE
ASSOCIATION
RELATION
SEMANTIC_COMPONENT
```

فالمصاحب ليس بالضرورة جزءًا من معنى الكلمة.

المخرجات المحتملة:

```text
FREQUENCY
WINDOW
CONSTRUCTION
DIRECTION
DOMAIN
CANDIDATE_RELATION
```

---

## D2. `PARALLELISM`

عند وجود بنى متوازية:

```text
A → X
B → Y
```

نختبر العلاقة بين العناصر، لكن لا نفترض:

```text
PARALLELISM = SYNONYMY
```

ولا:

```text
PARALLELISM = ANTONYMY
```

دون تحليل مستقل.

---

## D3. `ENTAILMENT_AND_OUTCOME`

يفحص النتائج المتكررة المرتبطة بالمفهوم.

لكن القاعدة:

```text
OUTCOME OF X
≠
MEANING OF X
```

إلا إذا دعمت أدلة أخرى إدخال النتيجة في النواة.

---

## D4. `EVENT_STATE_TRANSITION`

يعيد بناء:

```text
PRE_STATE
→ TRIGGER / ACTION
→ TRANSITION
→ RESULT
→ POST_STATE
```

والسؤال المركزي:

> ما التغير الذي أحدثه الحدث؟

ولا يجوز إنشاء `PRE_STATE` أو `POST_STATE` لا يدعمهما النص.

---

## D5. `CAUSAL_RELATION_ANALYSIS`

يفرق بين:

```text
CAUSE
CONDITION
MEANS
PURPOSE
RESULT
CORRELATION
SEQUENCE
```

والقاعدة:

```text
SEQUENCE ≠ CAUSATION
CAUSATION ≠ PURPOSE
```

---

## D6. `CONCEPT_RELATIONSHIP_NETWORK`

تمثل المفاهيم كشبكة علاقات مثل:

```text
CAUSE
PURPOSE
MEANS
RESULT
PART_OF
CONTRAST
ASSOCIATION
CONDITION
SEQUENCE
```

لكن لا يسمح بأي edge بلا:

* شاهد.
* نوع علاقة.
* مصدر.
* درجة دعم.
* حالة معرفية.

---

## D7. `TEXTUAL_SILENCE`

يميز:

```text
NOT_SPECIFIED
≠
TEXTUAL_OPEN_SPACE
≠
NOT_ALLOWED
≠
NEGATED
```

والصمت لا يصبح دليلًا إلا مع تحديد نطاق البحث وما إذا كان النص متوقعًا منه أصلًا أن يصرح بالمعلومة.

---

# 9. العائلة E — Discourse, Rhetoric & Structure

تدخل هنا أهم إضافات v1.1.

والقاعدة الجديدة:

> **هذه الأدوات شرطية التفعيل وليست إلزامية لمجرد أن الهدف آية أو سورة.**

وجود الأداة في المنهج لا يعني وجود الظاهرة في كل موضع.

---

# 10. `ILTIFAT_PASS` — الالتفات

## التعريف التشغيلي

تحول قابل للإثبات في البنية الخطابية مثل:

* الغيبة → الخطاب.
* الخطاب → الغيبة.
* التكلم → الخطاب.
* الجمع → المفرد في موقع ذي صلة.
* تغير منظور الإحالة.

## الإجراء

```text
DETECT_BASELINE_PERSON
DETECT_ACTUAL_SHIFT
VERIFY_SAME_DISCOURSE_UNIT
RESOLVE_REFERENTS
COMPARE_PRE_SHIFT
COMPARE_POST_SHIFT
TEST_SEMANTIC_EFFECT
```

## ضابط أساسي

ليس كل انتقال بين اسم ظاهر وفعل أو ضمير «التفاتًا».

ولا يعتمد:

```text
SHIFT EXISTS
→ THEREFORE EFFECT = X
```

بل تصبح الوظيفة الدلالية فرضية منفصلة تحتاج دليلًا.

---

# 11. `TAQDIM_TAKHIR_PASS` — التقديم والتأخير

يفحص ترتيب العناصر عندما توجد مقارنة معتبرة تسمح بتحديد أن الترتيب ذو دلالة.

## الخطوات

```text
IDENTIFY_ACTUAL_ORDER
IDENTIFY_COMPARABLE_ALTERNATIVE
VERIFY_SYNTACTIC_LICENSE
COMPARE_PARALLELS
TEST_EFFECT
```

## الأغراض المرشحة

قد تشمل:

* التركيز.
* المقابلة.
* الحصر.
* الربط بالسياق.
* إدارة المعلومات.
* التشويق.

لكن:

```text
FRONTING ≠ AUTOMATIC_HASR
```

ولا يجوز افتراض «ترتيب طبيعي أصلي» دون برهان لغوي أو قرآني مناسب.

---

# 12. `MUTASHABIHAT_PASS` — المتشابهات اللفظية / التكرار مع التغيير

تعد من أهم أدوات v1.1.

تقارن مقطعين شديدي التقارب وتحدد الفرق الدقيق.

## أنواع الفرق

```text
LEXICAL
MORPHOLOGICAL
SYNTACTIC
ORDER
ADDITION
OMISSION
PARTICLE
REFERENCE
NUMBER
TENSE_ASPECT
```

## الإجراء

```text
ALIGN_PARALLEL_TEXT
IDENTIFY_MINIMAL_DIFFERENCE
COMPARE_LOCAL_CONTEXT
COMPARE_PARTICIPANTS
COMPARE_DISCOURSE_ROLE
GENERATE_DIFFERENCE_HYPOTHESIS
SEARCH_FOR_COUNTEREXAMPLES
```

وتعامل هذه الأداة بوصفها أقرب ما يكون إلى:

> `NATURAL CONTRASTIVE EXPERIMENT`

لكن لا تفترض أن كل فرق لفظي له تفسير مستقل قابل للإثبات.

---

# 13. `FASILA_PASS` — الفاصلة القرآنية

تدرس نهاية الآية وعلاقتها بما قبلها.

## ما تبحث عنه

* اسم أو صفة.
* نتيجة.
* حكم.
* سؤال.
* وعيد.
* وعد.
* تعقيب.
* نمط متكرر.

## الضابط

لا تعتمد قاعدة:

```text
FASILA = SUMMARY OF VERSE
```

بل تختبر:

```text
FASILA_RELATION_TO_VERSE
```

وقد تكون العلاقة:

* تلخيصًا.
* تعليلًا.
* نتيجة.
* تقابلًا.
* ربطًا بالسياق.
* انتقالًا.
* إيقاعًا ذا أثر دلالي.
* غير محسومة.

---

# 14. `QASAM_PASS` — القسم

يحلل:

```text
OATH_MARKER
OATH_OBJECT
OATH_SEQUENCE
JAWAB_AL_QASAM
RELATION
```

## الضابط

لا يكفي القول:

> «المقسم به عظيم، إذن المعنى المقصود هو...».

المطلوب هو تحليل العلاقة النصية بين:

```text
MUQSAM_BIH
↔
MUQSAM_ALAYH
```

مع السماح بالحالة:

```text
RELATION_UNRESOLVED
```

---

# 15. `ISTIFHAM_PASS` — الاستفهام

يبدأ من البنية الاستفهامية ولا يفترض مسبقًا أنها «بلاغية».

## المراحل

```text
DETECT_QUESTION
IDENTIFY_ADDRESSEE
IDENTIFY_EXPECTED_RESPONSE
COMPARE_CONTEXT
CLASSIFY_PRAGMATIC_FUNCTION
```

والوظائف المرشحة قد تشمل:

* سؤالًا حقيقيًا.
* تقريرًا.
* إنكارًا.
* توبيخًا.
* تعجبًا.
* تحديًا.
* توجيهًا للحجاج.

لكن التصنيف نتيجة تحليل، لا وسمًا آليًا.

---

# 16. `HADHF_IDMAR_PASS` — الحذف والإضمار

من أكثر الأدوات عرضة للإفراط.

ولا يثبت الحذف إلا إذا كانت هناك بنية تدل على عنصر غير مصرح به.

## المراحل

```text
IDENTIFY_INCOMPLETE_OR_DEPENDENT_STRUCTURE
GENERATE_MINIMAL_RECONSTRUCTION
GENERATE_COMPETING_RECONSTRUCTIONS
COMPARE_PARALLELS
TEST_WHICH_ELEMENTS_ARE_ACTUALLY_REQUIRED
```

## القاعدة

> لا يجوز اختراع محذوف ثم بناء معنى دلالي عليه.

يجب أن يكون:

```text
OMITTED_ELEMENT
=
TEXTUALLY_REQUIRED OR STRONGLY CONSTRAINED
```

---

# 17. `MUNASABA_PASS` — المناسبة والتماسك

تدرس علاقة الوحدة بما قبلها وما بعدها.

## مستوياتها

```text
LOCAL_VERSE
PASSAGE
SECTION
SURAH
CROSS_SURAH
```

## أنواع العلاقة

قد تشمل:

```text
COMPLETION
CONTRAST
SEQUENCE
EXPLANATION
CAUSE
RESULT
TRANSITION
FRAME
PARALLEL
```

ولا يلزم أن توجد «مناسبة واحدة خفية» لكل تجاور.

يجوز أن تكون النتيجة:

```text
MULTIPLE_PLAUSIBLE_RELATIONS
```

أو:

```text
RELATION_NOT_ESTABLISHED
```

---

# 18. `TAKRAR_PASS` — التكرار

يفرق بين:

* تكرار حرفي.
* تكرار جزئي.
* تكرار بنيوي.
* تكرار قصة.
* لازمة.
* صيغة متكررة.
* تكرار مع تغيير.

## الإجراء

```text
VERIFY_TEXT
COUNT_OCCURRENCES
CLASSIFY_REPETITION
MAP_LOCATIONS
COMPARE_CONTEXTS
TEST_EFFECT
```

والقاعدة:

```text
REPETITION
≠
AUTOMATIC_EMPHASIS
```

وقد يؤدي إلى:

* بناء هيكلي.
* تذكير.
* تقسيم.
* انتقال.
* تقابل.
* تصعيد.

أو تبقى الوظيفة غير محسومة.

---

# 19. `RING_COMPOSITION_PASS`

يدرس إمكان وجود بنية من نمط:

```text
A
 B
  C
   X
  C'
 B'
A'
```

ولكن لا يجوز فرض التناظر على النص عبر اختيار وحدات مصطنعة.

## شروط القبول

* حدود وحدات قابلة للتبرير.
* تقابلات محددة.
* تناظر غير انتقائي.
* قدرة النموذج على تفسير البناء أفضل من البدائل.

والعنصر الأوسط:

```text
CENTER
≠
AUTOMATIC_SEMANTIC_THESIS
```

إلا بقرائن مستقلة.

---

# 20. `COGNITIVE_PATTERN_PASS`

يختبر الأنماط التصورية التي تستخدم مجالًا محسوسًا لفهم مجال آخر، مثل:

* اتجاه.
* طريق.
* تجارة.
* نور.
* مرض.
* بناء.

لكن:

```text
CONCEPTUAL_MODEL
=
ANALYTICAL HYPOTHESIS
```

ولا يجوز إسقاط نظرية معرفية خارجية على النص ثم معاملتها كدليل قرآني.

---

# 21. العائلة F — Scene, Narrative & Argument

## F1. `SCENE_RECONSTRUCTION`

يعيد بناء المشهد:

```text
ACTORS
OBJECTS
LOCATION
CONSTRAINTS
ACTION
PROBLEM
CHANGE
RESULT
```

ثم يسأل:

> أين تعمل المفردة داخل المشهد؟

وتفيد هذه الأداة في منع عزل الكلمة عن الحدث الذي تعمل داخله.

---

## F2. `DIALOGUE_ANALYSIS`

يفحص:

* المتكلم.
* المخاطب.
* السؤال.
* الرد.
* عدم الرد.
* تغيير زاوية الخطاب.
* الاقتباس.

ويستخدم خصوصًا مع القصص والحجاج.

---

## F3. `REPEATED_NARRATIVE_ANALYSIS`

يقارن الروايات المتكررة للحدث نفسه.

والهدف ليس بناء «نسخة مركبة» فحسب، بل اكتشاف:

* ما الذي يثبت؟
* ما الذي يتغير؟
* ما الذي يبرز في كل سياق؟
* هل الاختلاف مرتبط بغرض السياق الحالي؟

---

## F4. `ARGUMENT_STRUCTURE_ANALYSIS`

يعيد بناء الحجاج:

```text
CLAIM
PREMISE
QUESTION
OBJECTION
RESPONSE
EXAMPLE
CONCLUSION
```

وتفيد هذه الأداة في منع نسبة الوظيفة الحجاجية إلى معنى المفردة ذاتها.

---

## F5. `CROSS_SURAH_COMPARISON`

يستخدم عندما تتكرر:

* المفاهيم.
* القصص.
* العبارات.
* العلاقات.

ولا يفترض أن السور يجب أن تقدم المعنى نفسه بالطريقة نفسها.

---

# 22. العائلة G — Computational Discovery

## G1. `CORPUS_RETRIEVAL`

وظيفته:

* الحصر.
* البحث.
* التصريف.
* الفرز.
* استخراج السياقات.

لكن:

```text
SEARCH_RESULT
≠
ANALYZED_EVIDENCE
```

---

## G2. `STATISTICAL_COLLOCATION`

يستخدم المقاييس الإحصائية لتحديد الأزواج أو الأنماط المرشحة للفحص.

الإحصاء يحدد:

> ما الذي يستحق النظر؟

ولا يحدد:

> ماذا يعني؟

---

## G3. `NETWORK_ANALYSIS`

تمثل:

```text
WORDS
ROOTS
CONCEPTS
CONSTRUCTIONS
```

كعقد وعلاقات مشتقة.

لكن:

```text
GRAPH_EDGE
≠
SEMANTIC_TRUTH
```

---

## G4. `TOPIC_OR_CLUSTER_DISCOVERY`

يستخدم للكشف عن تجمعات غير واضحة مسبقًا.

ويجب إرجاع كل cluster إلى الشواهد النصية قبل أي استعمال استدلالي.

---

## G5. `EMBEDDING_DISCOVERY`

التشابه المتجهي يستخدم لاكتشاف:

* الجيران المحتملين.
* الاستعمالات البعيدة.
* counterevidence candidates.
* الأنماط غير المتوقعة.

ولا يجوز استخدام:

```text
COSINE_SIMILARITY
```

بوصفها درجة قرابة دلالية قرآنية محكومة.

---

## G6. `LLM_DISCOVERY`

يجوز للنموذج اللغوي اقتراح:

* فرضيات.
* فروق.
* شواهد تستحق البحث.
* counterexamples.
* محاور مقارنة.

لكن:

```text
LLM_OUTPUT
≠
EVIDENCE
≠
GATE_PASS
≠
SEMANTIC_LOCK
```

---

# 23. العائلة H — Validation, Falsification & Convergence

هذه العائلة ليست اختيارية.

---

## H1. `FALSIFICATION_PASS`

لكل نموذج دلالي يجب السؤال:

> ما الشاهد الذي يستطيع إسقاط هذا النموذج؟

ثم البحث عنه بالفعل.

لا يكفي:

```text
FIND_SUPPORTING_EVIDENCE
```

بل يجب:

```text
SEARCH_FOR_DISCONFIRMING_EVIDENCE
```

---

## H2. `COMPETING_MODELS_PASS`

يجب، متى كان ذلك معقولًا، صياغة نموذج منافس واحد على الأقل.

ثم المقارنة حسب:

* التغطية.
* عدد الافتراضات.
* التعامل مع الشواهد الصعبة.
* القدرة التنبؤية.
* التمييز.
* قابلية الاشتقاق.

---

## H3. `EVIDENCE_CONVERGENCE`

هذا هو المجمّع النهائي.

لا يحسب عدد الأدوات فقط، بل استقلالها.

مثال:

```text
COLLOCATION
+
NETWORK GRAPH
+
EMBEDDING NEIGHBOR
```

قد تكون كلها انعكاسًا لنمط توزيع واحد، وبالتالي لا تعد ثلاث أدلة مستقلة.

بينما:

```text
MORPHOLOGY
+
CONSTRUCTION
+
NEGATIVE DISTRIBUTION
+
CONTRASTIVE PARALLEL
```

قد توفر استقلالًا أكبر.

---

## H4. `LAYER_ATTRIBUTION`

كل عنصر مستخلص يجب إسناده إلى طبقته الصحيحة:

```text
ROOT
FORM
CONSTRUCTION
PARTICIPANT
CONTEXT
DISCOURSE
RHETORIC
INFERENCE
```

الهدف منع وضع أثر السياق داخل معنى الجذر.

---

## H5. `COVERAGE_AUDIT`

قبل الادعاءات العامة:

```text
ALL / NEVER / ALWAYS / ONLY
```

يجب التحقق من اكتمال corpus والنطاق.

---

## H6. `PROVENANCE_AND_REPRODUCIBILITY`

كل نتيجة مهمة يجب أن تسمح بإعادة بنائها من:

* corpus/version.
* query.
* occurrences.
* classification.
* analyst decisions.
* excluded cases.
* counterevidence.
* tool outputs.

---

# 24. الأدوات الثانوية

يجوز استخدام الأدوات التالية بوصفها `SUPPORTING_TOOLS`:

* الإيقاع.
* التشابه الصوتي.
* النمط الأسلوبي.
* التناسب الصوتي.
* طول الآيات.
* انتظام الفواصل.

لكن:

```text
PHONETIC_SIMILARITY
≠
SEMANTIC_RELATION
```

و:

```text
RHYTHMIC_PATTERN
≠
SEMANTIC PROOF
```

إلا إذا دعمتها قرائن مستقلة.

---

# 25. أدوات ما بعد القفل `POST_LOCK`

بعد اكتمال النتيجة الداخلية بحسب قواعد LISAN يمكن استخدام الأدوات الخارجية للمقارنة والإثراء.

## 25.1 المعاجم وغريب القرآن

تستخدم من أجل:

* المقارنة التاريخية.
* كشف استعمالات عربية خارج القرآن.
* اكتشاف فروق تحتاج اختبارًا.

ولا تمنح الحكم النهائي على النواة القرآنية.

---

## 25.2 التراث التفسيري

وظيفته بعد القفل:

```text
COMPARE
CHALLENGE
ENRICH
IDENTIFY_ALTERNATIVE
```

لا:

```text
PRELOAD_INTERNAL_RESULT
```

---

## 25.3 أسباب النزول

قد تساعد في فهم سياق تاريخي محتمل.

لكن يجب الفصل بين:

```text
HISTORICAL_OCCASION
```

و:

```text
TEXTUAL_SCOPE
```

ولا يخصص اللفظ العام بمجرد رواية السبب ما لم توجد قرينة معتبرة في نطاق المنهج.

---

## 25.4 الدراسات اللسانية الحديثة

يمكن استخدام:

* Semantic Field Analysis.
* Cognitive Linguistics.
* Discourse Analysis.
* Ring Composition.
* Componential Analysis.

بوصفها نماذج تحليل أو منافسين تفسيريين، لا مصادر سلطة أعلى من النص.

---

# 26. `TOOL_RESULT_CONTRACT`

يجب أن تعيد كل أداة نتيجة موحدة.

```yaml
TOOL_RESULT:
  tool_id:
  target:
  trigger:
  applicability:
    status: APPLICABLE | NOT_APPLICABLE | UNCERTAIN

  corpus_scope:
  evidence_units: []

  observations: []

  proposed_inference:
  inference_layer:

  alternative_explanations: []
  counterevidence: []
  unresolved_cases: []

  does_support: []
  does_not_prove: []

  status:
    - SUPPORTED
    - HYPOTHESIZED
    - UNRESOLVED
    - NOT_EVALUATED
    - NOT_APPLICABLE

  confidence:
    class:
    rationale:

  provenance:
    corpus_version:
    query:
    analyst:
    tool_outputs:
```

---

# 27. قاعدة `DOES_NOT_PROVE`

يجب أن يصرح كل Pass بما لا يستطيع إثباته.

أمثلة:

```text
COLLOCATION
DOES_NOT_PROVE
SEMANTIC_COMPONENT

TAQDIM
DOES_NOT_PROVE
HASR AUTOMATICALLY

REPETITION
DOES_NOT_PROVE
EMPHASIS AUTOMATICALLY

FASILA
DOES_NOT_PROVE
VERSE SUMMARY AUTOMATICALLY

OATH
DOES_NOT_PROVE
EXACT RELATION BETWEEN OATH OBJECT AND CONTENT

EMBEDDING
DOES_NOT_PROVE
SEMANTIC NEIGHBORHOOD

NETWORK EDGE
DOES_NOT_PROVE
CANONICAL CONCEPT RELATION
```

---

# 28. MEGA_ROUTER v1.1

لم يعد التوجيه يعتمد على تشغيل جميع الأدوات البلاغية على كل هدف.

يعتمد على:

```text
TARGET TYPE
+
OBSERVED PHENOMENA
+
RESEARCH QUESTION
+
RISK LEVEL
```

---

## 28.1 بحث الجذر

الحد الأدنى:

```text
FULL_DISTRIBUTIONAL_ANALYSIS
DERIVATIONAL_FAMILY
ROOT_UNITY
CONSTRUCTIONAL_SEMANTICS
PARTICIPANT_ROLES
NEAR_NEIGHBOR_DIFFERENTIATION
CORE_NECESSITY
DERIVATIONAL_EXPLAINABILITY
CORE_DISTINCTIVENESS
HARD_CASES
FALSIFICATION
EVIDENCE_CONVERGENCE
```

ويضاف عند الحاجة:

```text
COLLOCATION
MUTASHABIHAT
NEGATIVE_DISTRIBUTION
SEMANTIC_FIELD
```

---

## 28.2 بحث المفردة

الحد الأدنى:

```text
FULL_DISTRIBUTIONAL_ANALYSIS
QURANIC_SELF_EXPLANATION
CONSTRUCTIONAL_SEMANTICS
PARTICIPANT_ROLES
NEAR_NEIGHBORS
COLLOCATION
HARD_CASES
FALSIFICATION
CONVERGENCE
```

---

## 28.3 تحليل آية

الحد الأدنى:

```text
REFERENCE_RESOLUTION
CONSTRUCTIONAL_SEMANTICS
PARTICIPANT_ROLES
SCOPE
POLARITY
CONDITIONS / EXCEPTIONS
LOCAL_CONTEXT
```

ثم تشغل فقط عند وجود الظاهرة:

```text
ILTIFAT
TAQDIM_TAKHIR
HADHF_IDMAR
ISTIFHAM
QASAM
FASILA
PARALLELISM
```

---

## 28.4 تحليل سورة

تضاف:

```text
MUNASABA
TAKRAR
ARGUMENT_STRUCTURE
CROSS_SECTION_PARALLELISM
RING_COMPOSITION
REPEATED_NARRATIVE
FASILA_PATTERNS
```

مع بقاء كل منها مشروطًا بالشاهد.

---

## 28.5 تحليل قصة

الأولوية لـ:

```text
SCENE_RECONSTRUCTION
PARTICIPANT_ROLES
EVENT_STATE_TRANSITION
DIALOGUE
REPEATED_NARRATIVE
MUTASHABIHAT
CAUSE / RESULT
HARD_CASES
```

---

## 28.6 تحليل مفهوم

الأولوية لـ:

```text
SEMANTIC_FIELD
FULL_DISTRIBUTIONAL_ANALYSIS
COLLOCATION
CONCEPT_RELATIONSHIP_NETWORK
NEAR_NEIGHBORS
CONTRASTS
CAUSES
RESULTS
MUTASHABIHAT
FALSIFICATION
```

---

# 29. أدوات الموضوعات عالية الحساسية

في النتائج ذات الأثر العقدي أو التشريعي أو المنهجي الكبير يجب توسيع التحليل.

يطبق:

```text
FULL_CORPUS_COVERAGE
REFERENCE_RESOLUTION
SCOPE_ANALYSIS
CONDITIONAL_EXCEPTION
HARD_CASES
NEGATIVE_DISTRIBUTION
COMPETING_MODELS
FALSIFICATION
EVIDENCE_CONVERGENCE
PROVENANCE_AUDIT
```

ولا يسمح بأقفال عالية الثقة من شاهد واحد أو أداة واحدة.

---

# 30. بروتوكول التشغيل الكامل

## المرحلة 0 — `SCOPE_LOCK`

حدد:

* السؤال.
* الهدف.
* الوحدة.
* corpus.
* ما يدخل وما لا يدخل.

---

## المرحلة 1 — `BLIND_DISCOVERY`

تستخدم أدوات الاسترجاع لاكتشاف:

* المواضع.
* الصيغ.
* الجيران.
* المرشحات.

دون إدخال تفسير خارجي سابق.

---

## المرحلة 2 — `CORPUS_SWEEP`

يجرى الاستقراء الكامل ذي الصلة.

ويحفظ:

```text
MATCHED
EXCLUDED
AMBIGUOUS
HARD_CASE
```

---

## المرحلة 3 — `STRUCTURAL_ANALYSIS`

تحلل:

* الصيغة.
* البناء.
* المشاركون.
* الإحالة.
* النطاق.

---

## المرحلة 4 — `RELATIONAL_ANALYSIS`

تحلل:

* الجيران.
* التقابل.
* الاقتران.
* النتائج.
* الشبكة.

---

## المرحلة 5 — `DISCOURSE_ANALYSIS`

تشغل الوحدات البلاغية والخطابية التي ثبت وجود ظواهرها.

---

## المرحلة 6 — `MODEL_FORMATION`

تولد فرضية:

```text
PROPOSED_CORE
LOCAL_REALIZATIONS
BOUNDARIES
DISTINCTIVE_FEATURES
```

---

## المرحلة 7 — `FALSIFICATION`

يبحث عن:

* الشاهد المخالف.
* البديل الأقوى.
* التفسير الأبسط.
* الحالات التي تحتاج ترقيعًا.

---

## المرحلة 8 — `PREDICTIVE_TEST`

تختبر الفرضية على بيانات لم تستخدم في بنائها متى أمكن.

---

## المرحلة 9 — `EVIDENCE_CONVERGENCE`

تحسب قوة النتيجة بحسب:

* التغطية.
* استقلال الأدلة.
* الشواهد الصعبة.
* النماذج المنافسة.
* الافتراضات المطلوبة.

---

## المرحلة 10 — `INTERNAL_SEMANTIC_RESULT`

تنتج النتيجة الداخلية.

---

## المرحلة 11 — `POST_LOCK`

يمكن بعدها فتح المقارنة الخارجية حسب السياسة المعتمدة.

---

# 31. بنية `INTERNAL_SEMANTIC_RESULT`

```yaml
INTERNAL_SEMANTIC_RESULT:

  research_target:

  proposed_axial_meaning:

  invariant_constraints: []

  local_realizations: []

  derivational_mapping: []

  constructional_effects: []

  participant_effects: []

  semantic_neighbors:
    confirmed: []
    candidate: []

  contrasts: []

  supporting_evidence: []

  hard_cases: []

  counterevidence: []

  competing_models: []

  falsification_result:

  predictive_test:

  evidence_convergence:

  unresolved_questions: []

  not_established: []

  confidence:
    class:
    basis:
```

---

# 32. درجات الحالة

لا يكفي إعطاء درجة رقمية.

تعتمد الحالات:

```text
OBSERVED
HYPOTHESIZED
SUPPORTED
STRONGLY_SUPPORTED
UNRESOLVED
COUNTEREVIDENCE_PRESENT
REJECTED
NOT_EVALUATED
NOT_APPLICABLE
```

أما الثقة فتعتمد على تفسير مكتوب، لا على نجوم.

---

# 33. ما الذي يمنع القفل؟

يحظر `SEMANTIC_LOCK` عندما يوجد أحد الآتي:

```text
MATERIAL_CORPUS_GAP

UNEXPLAINED_HARD_CASE

UNTESTED_CRITICAL_ALTERNATIVE

ROOT_CORE_REQUIRES_AD_HOC_EXCEPTION

CONTEXT_EFFECT_MISATTRIBUTED_TO_ROOT

COMPUTATIONAL_CANDIDATE_USED_AS_EVIDENCE

EXTERNAL_PRIOR_CONTAMINATION

NEGATIVE_DISTRIBUTION_CLAIM_WITHOUT_COVERAGE

RHETORICAL_FUNCTION_ASSERTED_FROM_LABEL_ONLY
```

---

# 34. الأخطاء المنهجية المحظورة

## 34.1 `DICTIONARY_FIRST`

البدء بتعريف معجمي ثم إعادة قراءة القرآن عليه.

---

## 34.2 `CONTEXTUAL_LEAKAGE`

إدخال أثر السياق داخل المعنى الأصلي للكلمة.

---

## 34.3 `FORCED_UNIFICATION`

اختراع نواة فضفاضة لإنقاذ فرض وحدة الجذر.

---

## 34.4 `FORCED_POLYSEMY`

تقسيم الجذر سريعًا إلى معان مستقلة للهروب من الشواهد الصعبة.

---

## 34.5 `RHETORICAL_LABEL_FALLACY`

مثل:

```text
هذا تقديم
→ إذن حصر
```

أو:

```text
هذا استفهام
→ إذن توبيخ
```

---

## 34.6 `COLLOCATION_FALLACY`

```text
X يتكرر مع Y
→ Y جزء من معنى X
```

---

## 34.7 `COMPUTATIONAL_AUTHORITY`

```text
Embedding / AI / Graph suggests X
→ X is Quranically established
```

---

## 34.8 `TEXTUAL_SILENCE_OVERREACH`

```text
لم يذكر النص X
→ النص ينفي X
```

---

## 34.9 `REPETITION_INTENT_OVERCLAIM`

```text
هناك تكرار
→ لا بد أن تكون له الوظيفة Y
```

---



# 36. ترتيب الأولوية العملي

لا يوجد «ترتيب مطلق للقوة»، لكن عند البحث الدلالي العام تكون الأولوية التشغيلية غالبًا:

```text
1. FULL DISTRIBUTIONAL ANALYSIS

2. QURANIC SELF-EXPLANATION

3. DERIVATIONAL / CONSTRUCTIONAL ANALYSIS

4. PARTICIPANT ROLES

5. NEIGHBORS / CONTRASTS / COLLOCATION

6. DISCOURSE & STRUCTURAL TOOLS

7. HARD CASES

8. COMPETING MODELS

9. FALSIFICATION

10. EVIDENCE CONVERGENCE
```

وهذا ترتيب سير عمل، لا ترتيب «قيمة» بين الأدوات.

---

# 37. الأدوات السبع التي لا ينبغي أن يخلو منها بحث دلالي جاد

إذا احتيج إلى أصغر نواة تشغيلية، فهي:

```text
FULL_DISTRIBUTIONAL_ANALYSIS

DERIVATIONAL / FORM ANALYSIS

CONSTRUCTION + VALENCY

NEAR_NEIGHBOR / CONTRAST ANALYSIS

HARD_CASE ANALYSIS

FALSIFICATION / COMPETING_MODELS

EVIDENCE_CONVERGENCE
```

ويضاف إليها في بحوث الجذر:

```text
CORE_NECESSITY
DERIVATIONAL_EXPLAINABILITY
CORE_DISTINCTIVENESS
```

---

# 38. المبدأ الخاص بالجذر

لا يقبل `ROOT_AXIAL_MEANING` لمجرد أنه يستطيع «تأويل» كل الاستعمالات.

بل يجب أن يحقق معًا:

```text
COVERAGE
+
NECESSITY
+
DERIVATIONAL_EXPLAINABILITY
+
DISTINCTIVENESS
+
HARD_CASE_RESILIENCE
+
FALSIFICATION_SURVIVAL
```

والفرق جوهري بين:

```text
A MEANING CAN BE MADE TO FIT
```

و:

```text
THE MODEL EXPLAINS THE DATA BETTER THAN ITS COMPETITORS
```

---

# 39. فلسفة Quran Lisan Tools v1.1

يمكن اختصار المنظومة كاملة في الصياغة التالية:

> **النص المباشر يضع الحدود.
> الاستقراء يحدد مجال العمل.
> الاشتقاق يبحث عن الثابت.
> التركيب يكشف كيفية تحقق المعنى.
> المشاركون يكشفون بنية الحدث.
> الجيران يحددون الفروق.
> التقابل يختبر الحدود.
> التكرار مع التغيير يصنع المقارنة.
> الخطاب يكشف وظيفة الموضع.
> المشهد يعيد الكلمة إلى الحدث.
> النتائج تكشف الآثار دون خلطها بالمعنى.
> الغياب يختبر الحدود حين تكتمل التغطية.
> الحالات الصعبة تضغط على النموذج.
> التنبؤ يختبر قدرته خارج بيانات بنائه.
> النقض يمنع الانحياز التأكيدي.
> وتقاطع الأدلة هو الذي يرفع الثقة.**

---

# 40. القاعدة النهائية

لا ينبغي أن يكون السؤال في Quran Lisan:

> «ما معنى هذه الكلمة؟»

فقط.

بل:

> ما أصغر نموذج دلالي قادر على تفسير توزيع هذه الكلمة، وصيغها، وأبنيتها، ومشاركيها، وجيرانها، وفروقها، واستعمالاتها الصعبة، دون إضافة ما لا يحتاجه النص؟

ثم:

> ما أقوى نموذج منافس؟

ثم:

> ما الذي يمكن أن يسقط نموذجنا؟

ثم:

> هل وصلنا إلى النتيجة نفسها من أدلة مستقلة؟

وعندها فقط يمكن الانتقال من:

```text
POSSIBLE_MEANING
```

إلى:

```text
SUPPORTED_INTERNAL_SEMANTIC_MODEL
```

دون الخلط بين قوة النموذج وبين عصمته.

---

# 41. الخلاصة المعيارية

`Quran Lisan Tools v1.1` ليست قائمة من التقنيات البلاغية المتجاورة.

إنها منظومة ذات طبقات:

```text
CORPUS
↓
OBSERVATION
↓
STRUCTURE
↓
RELATION
↓
MODEL
↓
COUNTEREVIDENCE
↓
FALSIFICATION
↓
PREDICTION
↓
CONVERGENCE
↓
INTERNAL_RESULT
↓
POST_LOCK COMPARISON
```

ويظل المبدأ الحاكم:

> **لا أداة منفردة تقرر المعنى.**

و:

> **لا إحصاء ولا رسم شبكي ولا Embedding ولا LLM يتحول إلى دليل قرآني بمجرد إنتاجه.**

و:

> **لا قاعدة بلاغية عامة تطبق تلقائيًا على كل موضع.**

و:

> **لا معنى محوري قوي ما لم يصمد أمام أصعب الاستعمالات وأفضل النماذج المنافسة.**

والغاية النهائية ليست إنتاج أكبر عدد من التفسيرات، بل:

> **الوصول إلى أقل نموذج دلالي افتراضًا، وأوسعها تفسيرًا، وأكثرها تمييزًا، وأقواها صمودًا أمام النقض، مع بيان واضح لما ثبت وما بقي مفتوحًا.**

**END — Quran Lisan Tools v1.1**

---

## نهاية الملحق

```text
INTEGRATION_RULES = M01 source/tool boundaries + A03/A04/A05/A11
OUTPUT_CONTRACT = TOOL_RESULT + TOOL_RECEIPTS + EXTERNAL_INFLUENCE_LOG
FAILURE_MODES = computational authority, dictionary-first, rhetorical-label, false tool execution
REGRESSION_CASES = tooling regression families + T01
REOPEN_IF = tool/model/corpus change, new source influence, benchmark failure
END_OF_APPENDIX = A12
```
