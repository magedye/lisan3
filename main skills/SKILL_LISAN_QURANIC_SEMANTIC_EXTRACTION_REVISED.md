> [!WARNING]
> **SUPERSEDED/MIGRATED**
> This document has been migrated to `skills/lisan-semantic-extraction/SKILL.md` and serves as the canonical runtime skill baseline. See `docs/migration/SEMANTIC_SKILL_MIGRATION_DISPOSITION.md`.

# Skill: Lisan Quranic Semantic Extraction
## مهارة لسان للاستخراج الدلالي القرآني المنضبط

**Type:** Derived Runtime Skill / دليل تشغيل مشتق  
**Purpose:** تحليل الجذور والألفاظ والصيغ والتراكيب القرآنية، واستخراج الدلالات والتمييز بين الجيران، مع الفصل بين مستويات الدليل ومنع الاستدلال الدائري والتضخم الدلالي.

---

## 0. طبيعة هذه المهارة وحدود سلطتها

هذه المهارة **دليل تنفيذ مشتق** وليست مصدر سلطة مستقلًا.

MUST:
- تخضع لملفات السلطة والسياسات والمخططات والسجلات النشطة في مشروع Lisan.
- تستخدم الـ Corpus القرآني canonical المحدد في المشروع.
- تحافظ على الفصل بين ما هو `Observation` وما هو `Interpretation` وما هو `Hypothesis` وما هو `Claim`.
- تطابق قوة صياغة النتيجة مع حالة الدليل والحالة الرسمية.

MUST NOT:
- تمنح `OWNER_ACCEPTED` أو `RELEASE_ACCEPTED` أو `INDEPENDENTLY_REVIEWED` أو أي قبول لا تملكه.
- تعتبر نجاح Validator بنيوي دليلًا على صحة Claim دلالية.
- تغيّر حالة رسمية أو تضيف lifecycle جديدًا من تلقاء نفسها.
- تجعل محتوى هذه المهارة يتغلب على مصدر سلطة أعلى.
- تتحول إلى `CONSTITUTION` أو "مرجع أعلى" بمجرد إعادة تسميتها؛ رفع رتبتها يحتاج قرار سلطة صريحًا وتحديث ترتيب السلطة الرسمي.

إذا تعارضت هذه المهارة مع Authority أعلى، **Authority الأعلى يحكم**.

---

# 1. ترتيب السلطة ومرحلة `AUTHORITY_PREFLIGHT`

## 1.1 ترتيب السلطة

استخدم ترتيب السلطة الرسمي الموجود في المشروع إن وُجد.

وإن لم يوجد ترتيب أكثر تحديدًا، استخدم:

1. تعليمات المالك الصريحة للمهمة الحالية.
2. سياسة المستودع/الوكيل وملفات السلطة النشطة.
3. المتطلبات والمناهج والمواصفات canonical.
4. ADRs والعقود العامة المقبولة.
5. الخطط والمهام المعتمدة.
6. التنفيذ الحالي والاختبارات.
7. سجلات الحالة والتقارير.
8. الأمثلة والمحادثات والمواد التاريخية.
9. الاستنتاجات والافتراضات.

الـ Corpus القرآني canonical والـ Registries/Schemas الرسمية تُعامل بوصفها **مصادر بيانات/عقود حاكمة ضمن موضعها في هذا الترتيب**، ولا تستخدم لإلغاء سياسة أعلى منها.

## 1.2 `AUTHORITY_PREFLIGHT`

قبل أي Claim دلالي، MUST resolve:

```yaml
target:
  expression: "{...}"
  analysis_unit: "[ROOT_CORE | LEXEME | FORM | CONSTRUCTION | LOCAL_MEANING | CONCEPT]"
  claim_scope: "[what exactly is being claimed]"

authority:
  canonical_quran_source: "[resolved project source]"
  methodology_ref: "[active methodology authority]"
  official_statuses_ref: "[active status registry/policy]"
  source_role_policy_ref: "[external evidence policy]"
  morphology_policy_ref: "[active morphology/operator policy]"
  letter_semantics_policy_ref: "[active letter-semantics policy if relevant]"
  fallback_policy_ref: "[authority-approved fallback policy if one exists]"
  presentation_schema_ref: "[active output schema/template if one exists]"

runtime:
  tools_available: "[actual tools only]"
  prior_authoritative_result: "[none or resolved reference]"
  dependency_state: "[resolved / unresolved]"
  execution_evidence_mode: "[VERIFIED_TOOLING | AUTHORITY_APPROVED_FALLBACK | EXPLORATORY_ONLY]"
```

إذا تعذر حسم سلطة لازمة للمهمة:
- لا تخترع تسوية.
- سجّل `OPEN_AUTHORITY_QUESTION` بوصفه **عائق سلطة** لا حالة دلالية جديدة.
- أوقف فقط الجزء المتأثر، واستمر في الأجزاء المستقلة إن أمكن.

---

# 2. `TARGET_CONTRACT` — تحديد وحدة التحليل قبل البدء

لا تفترض أن كل سؤال هو سؤال Root Core.

MUST identify one primary analysis unit:

| الوحدة | السؤال |
|---|---|
| `ROOT_CORE` | ما النواة الدلالية الجذرية ضمن نطاق جذر مستقر؟ |
| `LEXEME` | ما دلالة اللفظة/المعجمية بوصفها وحدة استعمال؟ |
| `FORM` | ما الذي تضيفه الصيغة أو الوزن إلى المادة؟ |
| `CONSTRUCTION` | ما الذي ينشأ من التركيب النحوي أو البنية؟ |
| `LOCAL_MEANING` | ماذا تعني الصيغة في هذا الموضع المحدد؟ |
| `CONCEPT` | ما البنية المفهومية الأوسع وعلاقاتها عبر النص؟ |

MUST NOT:
- تعطي Root Core حين يكون المطلوب Local Meaning.
- تنسب معنى الصيغة إلى الجذر.
- تنسب حكم السياق إلى اللفظة بذاتها.
- تفترض وحدة جذرية واحدة إذا كانت هوية الجذر أو تعدد المعاني نفسها محل النزاع.

## 2.1 حل غموض طلب المستخدم

استخدم أضيق وحدة تحليل تفي بالطلب ولا تدعي أكثر منه:

| صياغة الطلب | العقد الافتراضي |
|---|---|
| "ما معنى هذه الكلمة/اللفظة؟" دون آية | `LEXEME` |
| "ما معنى هذه الكلمة في الآية/في قوله تعالى؟" | `LOCAL_MEANING` |
| "ما معنى هذا الجذر/ما نواته الجذرية؟" | `ROOT_CORE` |
| "ما دلالة وزن/صيغة/باب صرفي؟" | `FORM` |
| "ما دلالة هذا التركيب/حرف الجر/البناء؟" | `CONSTRUCTION` |
| "ما مفهوم المشيئة/العمل/الكسب في القرآن؟" | `CONCEPT`، مع تحديد المفردات والعلاقات الداخلة |

إذا احتمل الطلب أكثر من وحدة:
- اختر الوحدة الأضيق والأكثر تحفظًا.
- صرّح بالـ Scope الذي اخترته في المخرج.
- MAY تقدم طبقة ثانوية موجزة إذا كانت مفيدة، لكن لا تخلطها بالطبقة الأساسية.
- لا تستخدم `OPEN_AUTHORITY_QUESTION` لمجرد غموض صياغة المستخدم؛ فهذا الوسم مخصص لتعارض سلطة المشروع.
- لا تفترض `ROOT_CORE` تلقائيًا لمجرد أن السؤال عن "معنى" لفظة.

---

# 3. المبادئ الحاكمة

## P1. أولوية الـ Corpus القرآني في الاختبار الداخلي

التحليل الداخلي يبدأ من التوزيع القرآني الفعلي:
- المواضع.
- الصيغ.
- التراكيب.
- المشاركين.
- السياقات.
- العلاقات بين المواضع.

MUST NOT:
- تبدأ بتعريف معجمي جاهز ثم تعيد تفسير القرآن ليلائمه.
- تجعل مصدرًا خارجيًا بديلًا عن الاختبار داخل الـ Corpus.

المصادر الخارجية MAY:
- تولد فرضية.
- توفر مقارنة تاريخية.
- تقترح جارًا دلاليًا.
- تقدم شاهدًا مساعدًا.
- تساعد في اختبار بدائل.

لكن دورها الفعلي تحدده سياسة المشروع.

## P2. الفصل الطبقي

اعتبر المعنى الموضعي ناتجًا مركبًا:

```text
LOCAL MEANING
= ROOT/LEXICAL CONTRIBUTION
+ MORPHOLOGICAL OPERATOR
+ CONSTRUCTION/SYNTAX
+ PARTICIPANT ROLES
+ DISCOURSE/CONTEXT
```

هذه معادلة تحليلية، لا ادعاء بأن كل حد يملك مساهمة مستقلة في كل موضع.

MUST NOT تنسب إلى Root Core ما يمكن تفسيره بصورة أفضل من:
- الوزن/الصيغة.
- التعدية.
- حرف الجر.
- المفعول.
- الفاعل.
- المقام.
- النتيجة العملية.
- الحكم الفقهي.
- الأثر البلاغي.

## P3. التسلسل المعرفي

```text
Observation
→ Interpretation
→ Hypothesis
→ Claim
→ Locked Result
```

- `Observation`: ما يثبته النص/البيانات مباشرة.
- `Interpretation`: قراءة محتملة للملاحظة.
- `Hypothesis`: تفسير قابل للاختبار.
- `Claim`: نتيجة اجتازت شروطًا محددة ضمن نطاق معلن.
- `Locked Result`: Claim اجتازت بوابة القفل الرسمية فقط.

MUST NOT تقفز من `Observation` إلى `Claim`.

## P4. نقد صالح ≠ بديل صالح

```text
VALID_CRITIQUE ≠ VALID_REPLACEMENT
```

إسقاط تعريف سابق لا يثبت البديل الجديد.

كل بديل MUST يدخل دورة الاختبار من البداية.

## P5. البقية المميزة `DISTINCTIVE_RESIDUE`

التغطية وحدها لا تكفي.

الـ Root Core القوي يجب أن يجيب:

> لماذا اختير هذا الجذر هنا بدل أقرب جيرانه؟

`Distinctive Residue` هي أقل خاصية موجبة أو مجموعة خصائص:
- تبقى ضمن نطاق التحليل.
- تميز الهدف عن الجيران الضروريين.
- لا تأتي من السياق أو الصيغة وحدهما.
- يمكن اختبارها.

## P6. القابلية للدحض

كل Hypothesis مهمة MUST تتضمن:

```text
REJECTION_CONDITION
```

أي:
> ما الدليل المحدد الذي لو ثبت سيجعلنا نرفض الفرضية أو نعيد فتحها؟

يجب أيضًا حفظ:
- `supporting_evidence`
- `counterevidence`
- `unresolved_cases`
- `failed_predictions`

## P7. التوقف المنهجي مشروع

إذا كانت الحالة الرسمية للمشروع تتضمن `LOCK_BLOCKED`، فتعامل معها كـ **نتيجة منهجية صحيحة** وليست فشلًا يجب تجاوزه.

MUST NOT تختلق فرقًا أو معنى فقط لأن المستخدم طلب جوابًا نهائيًا.

---

# 4. المصطلحات الأساسية

| المصطلح | التعريف التشغيلي |
|---|---|
| `Root Core` — النواة الجذرية | أقل بنية دلالية موجبة يمكن الدفاع عن ثباتها وتمييزها ضمن نطاق الجذر المحدد بعد فصل أثر الصيغة والتركيب والسياق |
| `Root Definition` — التعريف الجذري | أقصر صياغة دقيقة للنواة التي ثبتت ضمن نطاقها |
| `Root Meaning` — المعنى الجذري | شرح زاوية الدلالة والتركيز الذي يقدمه الجذر |
| `Root Concept` — المفهوم الجذري | النموذج التصوري الأوسع: المشاركون، العلاقة، التحول/الحالة، والثابت والمتغير |
| `Local Meaning` — المعنى الموضعي | المعنى الناتج في موضع قرآني محدد بعد تفاعل الجذر/اللفظة والصيغة والتركيب والسياق |
| `Shared Domain` — المجال المشترك | المجال الذي يجعل لفظين أو جذورًا جيرانًا محتملين |
| `Distinctive Residue` — البقية المميزة | الخاصية الموجبة التي تفسر عدم الترادف الكامل |
| `Rejection Condition` — شرط رفض الفرضية | دليل محدد لو ثبت لأسقط الفرضية أو أوجب إعادة فتحها |
| `Validation Scope` — نطاق التحقق | المجال الفعلي الذي اختبرت فيه النتيجة، ولا يجوز الادعاء بما يتجاوزه |

---

# 5. سياسة الحالات `STATUS_POLICY`

MUST:
1. اقرأ الحالات من `official_statuses_ref`.
2. استخدم فقط الحالات الرسمية المعرّفة هناك.
3. لا تعتبر أي label في هذه المهارة رسميًا بذاته.
4. لا تضف حالة وسطية لتسهيل العرض.

Labels ظهرت في مسودات المنهج وقد توجد في المشروع، مثل:

```text
UNKNOWN
CANDIDATE_HYPOTHESIS
SPARSE_EVIDENCE_CEILING
LOCK_BLOCKED
LOCK_INTERNAL_RESULT
REVALIDATION_REQUIRED
```

لكن **لا تستخدم أيًا منها إلا إذا أكدتها Authority النشطة**.

إذا تعذر حسم سجل الحالات:
- لا تخترع حالة بديلة.
- لا تجعل `OPEN_AUTHORITY_QUESTION` حالة دلالية.
- اترك `official_status` غير مسند، أو استخدم تمثيل `null/unknown` الذي يعرّفه الـ Schema الرسمي إن وجد.
- MAY تستخدم أكثر الحالات الرسمية تحفظًا، مثل `UNKNOWN`، فقط إذا كانت مثبتة رسميًا وتنطبق شروطها فعلًا.
- سجّل عائق السلطة في حقل منفصل عن الحالة الدلالية.

إذا كان المشروع يعرّف `confidence` مستقلة عن `status`:
- استخدم القيم الرسمية فقط.
- لا تستخدم نسبًا مئوية إلا إذا كانت calibrated رسميًا.

إذا لم يوجد حقل `confidence` رسمي:
- لا تخترعه.

---

# 6. Coverage — اكتمال جمع الشواهد

لا تختزل Coverage في رقم واحد.

حيث تنطبق، افصل:

```yaml
coverage:
  index_coverage: "[what occurrences were indexed]"
  deep_analysis_coverage: "[what was actually analyzed deeply]"
  form_coverage: "[forms represented]"
  construction_coverage: "[syntactic patterns represented]"
  context_diversity: "[major contextual clusters]"
  neighbor_coverage: "[essential comparisons completed]"
  unresolved_items: "[remaining cases]"
```

MUST distinguish:
- `collected`
- `analyzed`
- `validated`

فجمع كل المواضع لا يعني تحليلها، وتحليلها لا يعني قفل النتيجة.

لا تفترض عتبة ثابتة مثل "مرة أو مرتين" لنقص الأدلة إلا إذا نصت عليها السياسة الرسمية.

## 6.1 الجذور كثيرة الورود والتحليل بالعينة

في الجذور كبيرة الحجم، ميّز بين غرضين:

### `EXPLORATORY_PROFILE`
يجوز استخدام عينة تحليل عميق إذا:
- اكتملت الفهرسة بالقدر الذي تسمح به الأدوات والمصدر canonical.
- كانت العينة طبقية ومبررة، لا عينة راحة.
- شملت الصيغ والسياقات والتراكيب النادرة أو الحرجة.
- صُرّح بأن النتيجة لا تتجاوز العينة وطبقاتها.
- لم تُستخدم العينة وحدها لمنح قفل لا تسمح به Authority.

### `LOCK_CANDIDATE_PROFILE`
يجب أن يحقق بوابة Coverage الرسمية. لا تُعد العينة كافية للقفل إلا إذا أجازت السياسة ذلك صراحة وحددت شروط التمثيل والتحقق.

عند استخدام عينة، سجّل:

```yaml
deep_analysis_sampling:
  method: "[stratified / purposive / full / other approved method]"
  strata: "[forms, constructions, contexts, rare cases]"
  selection_criteria: "[why these occurrences]"
  sample_size: "[n]"
  excluded_items: "[what was not deeply analyzed]"
  holdout_or_challenge_set: "[if used]"
  representativeness_limits: "[known limits]"
  generalization_boundary: "[what cannot be claimed]"
```

MUST NOT:
- تعتبر `INDEX_COVERAGE` بديلًا عن `DEEP_ANALYSIS_COVERAGE`.
- تعمم نتيجة عينة على جميع المواضع دون أساس مصرح.
- تستبعد الحالات الصعبة لأنها تعطل فرضية مريحة.

---

# 7. سير العمل التنفيذي

## Phase 0 — Preflight

1. Resolve `TARGET_CONTRACT`.
2. Resolve authorities and canonical corpus.
3. Resolve official statuses and source-role policy.
4. Resolve actual tooling.
5. Resolve prior authoritative claims and dependencies.
6. Classify any stale or contradictory context before reuse.

## Phase 1 — Corpus Collection

1. اجمع جميع المواضع المطلوبة حسب Scope.
2. تحقق من:
   - السورة/الآية.
   - النص canonical.
   - lemma/root/form إذا كانت الأدوات تسمح بذلك.
3. لا تستخدم قائمة من الذاكرة إذا كان المصدر canonical متاحًا.
4. سجّل أي ambiguity في التحليل الصرفي بدل حسمه بصمت.

## Phase 2 — Structural Observation

لكل موضع، سجّل ما يمكن إثباته بنيويًا قبل التفسير:

- الصيغة والوزن.
- الزمن/الوجه إن كان ذا صلة.
- التعدي.
- الفاعل.
- المفعول/المتعلق.
- حروف الجر.
- التركيب.
- participant roles.
- السياق القريب.
- النتيجة الظاهرة دون نسبتها تلقائيًا للجذر.

MUST label هذه الطبقة `OBSERVATION`.

## Phase 3 — Contextual Clustering

جمّع المواضع بحسب خصائص قابلة للوصف:
- مادي/اجتماعي/نفسي/تشريعي/إدراكي... عند الحاجة.
- نوع المشاركين.
- الصيغة.
- البناء النحوي.
- نوع الحدث.

MUST NOT تجعل اسم cluster نفسه تعريفًا للجذر.

## Phase 4 — Hypothesis Generation

أنشئ عند الحاجة:

```text
H1 = primary candidate
H2 = serious alternative
C0 = evidence does not yet establish a qualified invariant
```

`C0` لا تعني:
> "لا توجد نواة قطعًا"

بل:
> "الأدلة الحالية لا تثبت نواة مؤهلة ضمن الشروط".

لا تفرض H2 أو C0 شكليًا إذا لم تضف قيمة؛ الهدف هو البدائل الجدية لا ceremony.

سجّل فرضياتك بصياغة مختصرة قبل اختبارات التفريد حتى لا تعيد تعريفها بعد رؤية كل اختبار.

## Phase 5 — Semantic Family & Neighbors

حدد الجيران بناءً على:
- مجال استعمال مشترك.
- تقارب في participant structure.
- تقارب في نوع الحدث.
- إمكان الاستبدال الظاهري.
- مصادر مساعدة مصرح بها.

MUST NOT:
- تختار الجيران فقط لأنهم يجعلون فرضيتك تبدو مميزة.
- تفترض عددًا ثابتًا مثل 3–5.
- تقارن بجار بعيد بينما تتجاهل جارًا حاسمًا.

يكفي الجيران **الضروريون لاختبار الادعاء**.

## Phase 6 — Differentiation

طبّق المحاور ذات الصلة، لا كل محور آليًا:

### Core differentiation axes
1. `EVENT_TYPE` — نوع الحدث/الحالة.
2. `AGENCY` — طبيعة الفاعلية.
3. `INTENTIONALITY` — القصد/الإرادة.
4. `PARTICIPANT_STRUCTURE` — المشاركون والأدوار.
5. `DIRECTIONALITY` — الاتجاه/المسار.
6. `ASPECT_PHASE` — بداية/استمرار/اكتمال/نتيجة.
7. `RESULT_EFFECT` — ما الذي يتغير وعلى من يعود الأثر.
8. `AFFECTED_ENTITY` — طبيعة المتأثر.
9. `SYNTACTIC_BEHAVIOR` — التراكيب والتعدية والحروف.
10. `MORPHOLOGICAL_DISTRIBUTION` — الصيغ دون تحويلها مباشرة إلى معنى جذري.
11. `CONTEXTUAL_DISTRIBUTION` — أين يظهر/يمتنع.
12. `COLLOCATION` — المصاحبات ذات القيمة التفريقية.
13. `SCALARITY_INTENSITY` — الدرجة/الشدة إذا أثبتها التوزيع.
14. `TEMPORAL_PROFILE` — البنية الزمنية إذا كانت فارقة.

لا تُنشئ فرقًا في محور لا يملك evidence.

---

# 8. اختبارات التفريد والدحض

## 8.1 `SUBSTITUTION_TEST`

اسأل:
> ماذا نفقد لو وضعنا الجار مكان الهدف؟

**Probe, not evidence.**

لا يجوز استخدام عدم ورود الاستبدال في القرآن وحده كبرهان أن الاستبدال مستحيل لغويًا.

## 8.2 `BOUNDARY_TEST`

ابحث عن:
- حالة يقبل فيها الهدف.
- وحالة مماثلة يظهر فيها الجار أو يمتنع الهدف.
- والفارق البنيوي/الدلالي المتوقع بينهما.

## 8.3 `NEGATIVE_CASE`

أقوى من مجرد العثور على overlap.

ابحث عن حالة:
> يصح فيها A وفق الفرضية ولا يصح B، أو العكس.

## 8.4 `GENERICITY_TEST`

ارفض أو أضعف تعريفًا إذا كان:
- "حركة"
- "تغير"
- "علاقة"
- "فعل"
- أو أي وصف يمكن أن ينطبق دون تعديل على عدد كبير من الجذور.

إلا إذا كان نطاق Claim نفسه عامًا ومثبتًا ومميزًا بطريقة أخرى.

## 8.5 `PREDICTIVE_TEST`

قبل فتح بعض الشواهد أو المقارنات إن أمكن:
- اكتب توقعًا.
- حدد أين ينبغي أن يظهر الهدف.
- أين ينبغي أن يكون الجار أنسب.
- ثم اختبر.

Prediction يجب أن تكون قابلة للفشل، لا إعادة وصف للبيانات.

## 8.6 `COUNTEREXAMPLE_SEARCH`

ابحث عمدًا عن:
- أصعب موضع.
- أبعد سياق.
- صيغة غير مألوفة.
- شاهد يهدد invariant.

لا تبدأ فقط بالمواضع التي تجعل الفرضية سهلة.

## 8.7 `NEIGHBOR_CHALLENGE`

لكل جار حاسم:
- ما Shared Domain؟
- ما الخاصية المشتركة؟
- ما الفرق الموجب؟
- ما الشاهد الذي يختبر الفرق؟
- ما الذي لو ثبت يجعل الفرق مصطنعًا؟

---

# 9. استخراج `DISTINCTIVE_RESIDUE`

بعد الاختبارات، صغ البقية المميزة في صورة موجبة:

ضعيف:
> "ليس مجرد الارتفاع."

أفضل:
> "[خاصية موجبة محددة] تفسر لماذا يتوزع الجذر على هذه المواضع دون أن يساوي جاره."

شروطها:
- Positive.
- Minimal.
- Corpus-compatible.
- Layer-neutral.
- Neighbor-discriminating.
- Falsifiable.

إذا لم يبق Residue حقيقي بعد تجريد السياق والصيغة:
- لا تخترع واحدًا.
- اخفض Claim إلى الحالة الرسمية المناسبة أو امنع القفل.

---

# 10. Falsification وشرط الرفض

كل Root Core candidate يراد رفعه فوق فرضية أولية MUST يملك:

```yaml
falsification:
  rejection_condition:
    observable_trigger: "[what observable finding would challenge/reject the claim]"
    search_space: "[which canonical occurrences/forms/constructions are searched]"
    verification_method: "[tool/manual deterministic procedure]"
    confound_controls: "[how Form/Construction/Context alternatives are excluded]"
    decision_effect: "[reject / narrow scope / reopen / block lock]"
  strongest_counterevidence: "[evidence]"
  unresolved_cases: "[cases]"
  failed_predictions: "[if any]"
```

`Rejection Condition` يجب أن يكون:
- محددًا.
- قابلًا للبحث أو التحقق البشري/الآلي في مساحة معلنة.
- غير دائري.
- متعلقًا بالادعاء نفسه.
- مصاغًا بخصائص قابلة للرصد، لا بكلمات تفسيرية تفترض النتيجة.
- واضح الأثر على القرار: رفض، تضييق Scope، إعادة فتح، أو منع القفل.

ضعيف:
> "نرفض الفرضية إذا تبين أنها خاطئة."

ضعيف أيضًا:
> "نرفضها إذا استُعمل الجذر بمعنى آخر."

لأن "المعنى الآخر" قد يعيد إدخال الحكم المطلوب إثباته.

صالح:
> "نرفض الفرضية أو نضيّق نطاقها إذا وُجد موضع canonical يطابق البناء C ونوع المشاركين P، ولا يظهر فيه العنصر المزعوم Z بعد اختبار أن غيابه لا يفسَّر بالصيغة أو التركيب أو السياق، وفق الإجراء V."

---

# 11. الفصل بين الجذر والصرف والتركيب والسياق

عند كل Claim، اسأل بالتتابع:

1. هل الخاصية موجودة في جميع/النطاق المدعى من صور الجذر؟
2. هل تظهر فقط في وزن معين؟
3. هل تنتج من التعدية أو حرف الجر؟
4. هل تأتي من نوع المفعول أو الفاعل؟
5. هل هي نتيجة للفعل وليست معنى الفعل؟
6. هل هي تفسير فقهي/بلاغي/مقامي؟
7. هل تختفي في سياق آخر مع بقاء الجذر؟

إذا كان الجواب يشير إلى طبقة أخرى، انقل الخاصية إلى طبقتها ولا تضعها في Root Core.

---

# 12. تعدد المعاني وعدم فرض الوحدة

MUST NOT تفترض مسبقًا أن كل مادة إملائية يجب أن تنتهي إلى Root Core واحد بسيط.

إذا ظهرت احتمالات:
- homonymy.
- lexical split.
- historically distinct roots.
- unresolved semantic branching.

فقم بأحد الآتي حسب Authority:
- scope the claim إلى cluster محدد.
- حافظ على فرضيات متعددة.
- استخدم الحالة الرسمية المانعة للقفل.

الوحدة نتيجة يجب إثباتها، لا فرضًا يُحمى من الدحض.

## 12.1 عقد إخراج الفروع الدلالية

لا تستخدم مصطلح `ABSTRACT_ROOT_CORE` تلقائيًا؛ لأنه قد يفترض وجود جامع أعلى قبل إثباته.

إذا كان الانقسام **محتملًا**:
- أنشئ `branch_hypotheses` مستقلة.
- لا تقل إن Lexical Split "ثبت".
- اختبر إمكان الجامع وإمكان الانقسام بوصفهما فرضيتين متنافستين.

إذا كان الانقسام **مدعومًا ضمن Scope معلن**، استخدم بنية مثل:

```yaml
semantic_branching:
  relation_status: "[suspected / supported / authority-confirmed representation]"
  branches:
    - branch_id: "B1"
      scope: "[forms/constructions/contexts]"
      definition_or_hypothesis: "[branch-specific]"
      coverage: "[branch coverage]"
      supporting_evidence: "[branch-only evidence]"
      counterevidence: "[branch-only counterevidence]"
      nearest_neighbors: "[branch-specific]"
      rejection_condition: "[branch-specific]"
      official_status: "[resolved official status or unassigned]"
    - branch_id: "B2"
      scope: "[...]"
      definition_or_hypothesis: "[...]"
      coverage: "[...]"
      supporting_evidence: "[...]"
      counterevidence: "[...]"
      nearest_neighbors: "[...]"
      rejection_condition: "[...]"
      official_status: "[...]"
  shared_superordinate_candidate:
    value: "[only if independently supported; otherwise NOT ESTABLISHED]"
    evidence: "[independent evidence]"
    rejection_condition: "[independent condition]"
```

MUST:
- تفصل Coverage وEvidence وCounterevidence وStatus لكل فرع.
- تمنع خلط أدلة فرع بآخر لإنتاج ثبات وهمي.
- لا تنشئ جامعًا أعلى لمجرد الرغبة في المحافظة على وحدة الجذر.
- توضح هل الفروع Lexemes مستقلة، clusters تشغيلية، أم فرضيات مؤقتة؛ ولا تحسم التصنيف التاريخي بلا Evidence مناسب.

---

# 13. المجالات الخاصة

## 13.1 Morphological Operators — المؤثرات الصرفية

MUST:
- استخدم المرجع/الـ Registry الرسمي إذا كان متاحًا.
- اقرأ status وvalidation_scope لكل operator.
- افصل `structural observation` عن `semantic operator claim`.

MUST NOT:
- تعتبر كثرة الحالات البنيوية إثباتًا للدلالة.
- تنسب دلالة وزن provisional إلى Root Core.
- تستخدم وزنًا كدليل وحيد لقفل النواة.

إذا كانت مساهمة operator غير مقفلة:
- تعامل معها وفق الدور المسموح في Authority.
- سجّلها Hypothesis/Supporting فقط إن كان ذلك مسموحًا.

## 13.2 Letter Semantics — دلالات الحروف

اقرأ حالتها من `letter_semantics_policy_ref`.

إذا كانت الحالة الحالية `PROVISIONAL_RESEARCH_PROGRAM` أو ما يعادلها:
- MUST NOT تستخدمها sole evidence لتعريف Root Core.
- MUST NOT تنتج منها lock.
- MAY تستخدم فقط لتوليد سؤال أو Hypothesis حسب السياسة.
- MUST NOT ترفع النضج لأن الملفات أو Schema موجودة فقط.

## 13.3 External Sources

المعاجم، الشعر، التفسير، الفقه، البلاغة، اللسانيات، والمقارنات السامية:
- لا تُحظر تلقائيًا.
- لا تصبح حاكمة تلقائيًا.
- يُحدد دورها من `source_role_policy_ref`.

عند استخدامها، سجّل:
```text
SOURCE
ROLE
CLAIM_SUPPORTED
LIMIT
```

---

# 14. سلامة الاقتباس القرآني

عند إدراج آية أو جزء منها كدليل:
- تحقق من النص والمرجع من الـ Corpus canonical.
- لا تعتمد الذاكرة إذا كان المصدر متاحًا.
- لا تُصحح مرجعًا بصمت ثم تنسب التصحيح إلى مصدر آخر.
- إذا تعذر التحقق، لا تستخدم الاقتباس كدليل مقفِل.

---

# 15. الأدوات والتحقق — Tool Reality

## 15.1 أدوات فعلية

إذا كانت QAC/Parser/Validator/Registry/API متاحة فعليًا:
- استخدمها.
- سجّل الأمر/الاستدعاء والنتيجة.
- لا تدّع ما لا تثبته الأداة.

## 15.2 أداة غير متاحة

MUST NOT:
- تدّعي تشغيلها.
- تسمي المحاكاة الداخلية `VALIDATOR_PASSED`.
- تخلط reasoning مع runtime evidence.
- تعتبر المعجم أو ذاكرة النموذج fallback تلقائيًا عن الـ Corpus أو الأداة.
- تنشئ Claim بنيوية من معرفة داخلية غير قابلة للتتبع.

استخدم أحد أوضاع التدهور التالية فقط:

### A. `AUTHORITY_APPROVED_DETERMINISTIC_FALLBACK`
يجوز إذا صرحت به سياسة المشروع، مثل:
- فحص يدوي قابل للتكرار للمصدر canonical.
- Script محلي بديل معلوم المدخلات والمخرجات.
- Parser بديل مع حدود معلنة.
- مصدر خارجي في الدور المحدد له صراحة، لا بوصفه بديلًا غير معلن عن Corpus الداخلي.

هذا الوضع MAY ينتج Evidence ضمن حدود الإجراء الفعلي والسياسة.

### B. `EXPLORATORY_ONLY`
يجوز استخدام معرفة النموذج فقط لـ:
- توليد أسئلة.
- اقتراح فرضيات.
- اقتراح جيران أو اختبارات لاحقة.

لكن MUST NOT:
- تسجلها `OBSERVATION`.
- تستخدمها لإثبات Coverage.
- تستخدمها Evidence لبوابة القفل.
- تنسب إليها تحققًا خارجيًا.
- تمنح بها حالة أعلى مما تسمح به Authority للمواد غير المتحققة.

إذا لم توجد حالة رسمية مناسبة، اترك status غير مسند ووسم الناتج وصفيًا بأنه غير متحقق، خارج حقل الحالة الرسمية.

### C. `NO_VALID_FALLBACK`
إذا كانت الأداة/المصدر لازمًا للادعاء ولا يوجد fallback مصرح:
- سجّل `TOOL_UNAVAILABLE` و`NOT_VERIFIED` بوصفهما حقائق تشغيلية لا حالات دلالية.
- أوقف الجزء المتأثر.
- لا تمنح lock.

الـ fallback المسموح هو فقط ما تصرح به Authority أو ما يمكن إثبات مطابقته لسياساتها. محاكاة منطق الاختبار قد تساعد التفكير، لكنها **ليست Evidence تحقق**.

## 15.3 Validators

نجاح Validator يثبت فقط ما هو مصمم لاختباره.

مثال:
- Schema validator → سلامة البنية.
- Coverage validator → اكتمال نطاق محدد.
- Morphology validator → صحة/اتساق وسم صرفي.
- لا شيء منها يثبت وحده Root Core دلالية.

---

# 16. الاعتماديات وإعادة التحقق

إذا اعتمد Claim على نتيجة سابقة:
- استخدم ledger/project mechanism الفعلي إن وُجد.
- وإلا سجّل dependency بصورة صريحة في artifact العمل دون الادعاء بوجود سجل رسمي.

لكل dependency:
```yaml
dependency:
  id: "[resolvable reference]"
  claim_used: "[what was reused]"
  authority: "[source]"
  status_at_use: "[resolved official status]"
  validation_scope: "[scope]"
```

إذا تغيّرت dependency جوهرية:
- لا تعِد كل المشروع آليًا.
- حدد claims المتأثرة.
- طبّق الحالة/إجراء `REVALIDATION_REQUIRED` فقط إذا كان رسميًا ومطبقًا.

---

# 17. بوابة القفل `LOCK_GATE`

لا تمنح `LOCK_INTERNAL_RESULT` أو أي حالة lock مكافئة إلا إذا أكدت Authority أن الوكيل مخوّل بذلك وأن **جميع الشروط الرسمية** نجحت.

الحد الأدنى المقترح الذي يجب mapping إلى المعايير الرسمية:

| المعيار | المطلوب |
|---|---|
| `SCOPE_STABILITY` | وحدة التحليل وهوية الجذر/اللفظة مستقرة ضمن Claim |
| `COVERAGE` | Coverage كافية ومعلنة |
| `INVARIANCE` | العنصر المقترح ثابت ضمن Scope |
| `LAYER_NEUTRALITY` | لا يبتلع Form/Construction/Context |
| `POSITIVE_CONTENT` | يقرر ما هو المعنى، لا مجرد ما ليس هو |
| `DISTINCTIVENESS` | ينجح أمام الجيران الحاسمين |
| `FALSIFIABILITY` | Rejection Condition حقيقية |
| `PREDICTIVE_CONTENT` | له محتوى تنبؤي غير دائري حيث ينطبق |
| `COUNTEREVIDENCE_HANDLED` | لا توجد معارضة حاسمة مخفية |
| `TRACEABILITY` | الأدلة والمصادر والاعتماديات قابلة للتتبع |
| `NON_CIRCULARITY` | لا يعتمد إثباته على تفسير مفترض مسبقًا |

إذا فشل معيار حاسم:
- لا تعوّضه بالبلاغة أو الثقة.
- استخدم الحالة الرسمية المناسبة.

---

# 18. سياسة تحميل المراجع والقوائم المتطورة

هذه النسخة الشاملة تحتفظ بالحد الأدنى الضروري من محاور التفريد والأنماط المضادة لضمان عملها مستقلًا.

عند وجود Registries/References رسمية ومُصدّرة بإصدار:
- اقرأها في `AUTHORITY_PREFLIGHT`.
- اعتبرها المصدر الحاكم لتفاصيل القائمة.
- لا تنسخها إلى هذه المهارة إذا كان النسخ سيؤدي إلى drift.
- احتفظ داخل `SKILL.md` بالنواة التشغيلية ومسار التحميل وشروط الفشل فقط.

أمثلة لأسماء ممكنة، **لا تفترض وجودها**:
- `references/differentiation_axes.md`
- `references/anti_patterns.md`
- `references/lock_gate_criteria.md`
- `templates/root_result_template.md`
- `schemas/semantic_branching.schema.*`

إذا لم توجد هذه الملفات:
- لا تهلوس وجودها.
- استخدم القوائم المضمنة في هذه النسخة بوصفها candidate guardrails إلى أن تحسم Authority موضعها.
- لا تجعل غياب Reference اختيارية عائقًا إذا كان fallback المضمن كافيًا ومصرحًا.

---

# 19. الأنماط الممنوعة `ANTI-PATTERNS`

| ID | النمط |
|---|---|
| `FM-01` | `Dictionary-First`: تعريف جاهز ثم تكييف الشواهد |
| `FM-02` | `Contextual Leakage`: إدخال الفاعل/المفعول/الحكم/النتيجة في الجذر |
| `FM-03` | `Circular Confirmation`: افتراض المعنى ثم استخدام تفسير مبني عليه لإثباته |
| `FM-04` | `Untested Replacement`: قبول بديل لأن القديم فشل |
| `FM-05` | `Counterfactual-as-Proof`: "لو كان يعني X لقال Y" كدليل مستقل |
| `FM-06` | `Structural Overpromotion`: جعل حرف/عطف/تجاور بنيوي Root Core |
| `FM-07` | `Root-Form Conflation`: نسب أثر الوزن للجذر |
| `FM-08` | `Generic Overextraction`: نواة فضفاضة تصلح لعشرات الجذور |
| `FM-09` | `Frame Preselection`: فرض محور مثل أعلى/أسفل قبل الاستقراء |
| `FM-10` | `Avoiding Block`: اختراع جواب لتجنب حالة منع القفل |
| `FM-11` | `Overclaiming`: لغة يقين أعلى من Evidence/Status |
| `FM-12` | `Forced Unification`: دمج فرضيات متعارضة قسرًا |
| `FM-13` | `Neighbor Cherry-Picking`: اختيار جيران سهلين وتجاهل الجار الحاسم |
| `FM-14` | `Coverage Inflation`: اعتبار indexed = analyzed = validated |
| `FM-15` | `Tool Simulation as Evidence`: ادعاء تحقق لأداة لم تُشغّل |
| `FM-16` | `Status Invention`: إنشاء حالة جديدة لتناسب النتيجة |
| `FM-17` | `Silencing Counterevidence`: حذف أو إعادة تفسير الشاهد المعارض بلا اختبار |
| `FM-18` | `Presentation-as-Proof`: جمال التعريف أو اتساقه اللغوي ليس Evidence |

وجود Anti-pattern لا يعني دائمًا إيقاف المهمة كلها؛ صنّف أثره وفق السياسة، وأعد المرحلة المتأثرة أو امنع القفل.

---

# 20. Discovery vs Presentation

## 20.1 Discovery / Research Path

```text
Authority
→ Target Contract
→ Corpus
→ Observations
→ Structural Classification
→ Coverage
→ Context Clusters
→ Hypotheses
→ Semantic Family
→ Neighbor Tests
→ Counterevidence
→ Falsification
→ Layer Separation
→ Evaluation
→ Lock / Block / Remain Hypothesis
```

## 20.2 Presentation Path

```text
Definition
→ Meaning
→ Concept
→ Distinctive Residue
→ Neighbors
→ Boundaries
→ Contextual Realizations
→ Evidence
→ Counterevidence
→ Validation Scope
→ Official Status
```

MUST NOT تقدم discovery log أو private reasoning بوصفه النتيجة النهائية.

قدّم evidence and decision trace القابل للمراجعة فقط.

---

# 21. عقد صياغة النتيجة

## 21.1 `ROOT DEFINITION` — التعريف الجذري

السؤال:
> ما هو؟

المواصفات:
- جملة واحدة قدر الإمكان.
- موجبة.
- دقيقة.
- مميزة.
- خالية من تفاصيل السياق والصيغة.
- لا تدعي أكثر من Validation Scope.

صيغة:
> `{ROOT}: [نوع دلالي] يتمثل في [النواة المميزة] بحيث [العلاقة/الأثر الملازم إن ثبت أنه جذري].`

## 21.2 `ROOT MEANING` — المعنى الجذري

السؤال:
> ماذا يدل عليه، وأين يقع مركز ثقله؟

صيغة:
> يدل الجذر على [...]، حيث [...]، ويتركز البعد الدلالي على [...] لا على مجرد [...].

## 21.3 `ROOT CONCEPT` — المفهوم الجذري

السؤال:
> كيف تعمل البنية التصورية عبر السياقات؟

يصف:
- المشاركين.
- العلاقة.
- الحالة/التحول.
- invariant.
- contextual variables.
- boundaries.

لا يحول كل أثر سياقي إلى جزء من المفهوم الجذري.

---

# 22. قالب النتيجة النهائي

استخدم الحقول التي يدعمها المشروع. إذا لم يوجد Schema رسمي للعرض، استخدم هذا القالب:

```markdown
### TARGET: {ROOT / LEXEME / FORM}
**ANALYSIS UNIT:** [...]
**OFFICIAL STATUS:** [...]
**VALIDATION SCOPE:** [...]

**COVERAGE:**
- **Index Coverage:** [...]
- **Deep Analysis Coverage:** [...]
- **Form Coverage:** [...]
- **Construction Coverage:** [...]
- **Context Diversity:** [...]
- **Neighbor Coverage:** [...]
- **Unresolved Items:** [...]
- **Sampling/Generalization Boundary:** [...]

## 1. ROOT DEFINITION — التعريف الجذري
[إذا لم يثبت: NOT ESTABLISHED]

## 2. ROOT MEANING — المعنى الجذري
[إذا لم يثبت: NOT ESTABLISHED]

## 3. ROOT CONCEPT — المفهوم الجذري
[إذا لم يثبت: NOT ESTABLISHED]

## 4. DISTINCTIVE RESIDUE — البقية المميزة
[...]

## 5. SHARED DOMAIN & NEAREST NEIGHBORS
**Shared Domain:** [...]
- `{neighbor}`: [...]
- `{neighbor}`: [...]

## 6. LAYER SEPARATION — الفصل الطبقي
- **Root/Lexical Contribution:** [...]
- **Morphological Contribution:** [...]
- **Construction/Syntax Contribution:** [...]
- **Context/Pragmatic Contribution:** [...]

## 7. CONTEXTUAL REALIZATIONS — التحققات السياقية
- [...]
- [...]

## 8. BOUNDARIES — الحدود
**What the root/lexeme does not mean by itself:**
- [...]
**Scope limitations:**
- [...]

## 9. EVIDENCE
**Supporting Evidence:**
- [...]
**Counterevidence:**
- [...]
**Unresolved Cases:**
- [...]

## 10. FALSIFICATION
**Rejection Condition:** [...]
**Failed/Outstanding Predictions:** [...]

## 11. TRACEABILITY
**Canonical Corpus:** [...]
**Method/Policy Refs:** [...]
**Tool Evidence:** [...]
**Dependencies:** [...]
```

إذا كانت الحالة مانعة للقفل:
- لا تملأ `ROOT DEFINITION/MEANING/CONCEPT` بتخمين.
- اكتب `NOT ESTABLISHED` أو القيمة الرسمية المقابلة.
- اعرض ما ثبت بنيويًا وما الذي يمنع التقدم.

---

# 23. صيغة مختصرة للأسئلة السريعة

إذا كان المستخدم يسأل عن معنى لفظة واحدة ولا يطلب دراسة كاملة:

1. حدّد أن الجواب `LOCAL/PROVISIONAL` إن لم تُنفذ Coverage كاملة.
2. قدّم:
   - المعنى الموضعي الأقرب.
   - الجذر/الصيغة.
   - الفرق المحتمل عن أقرب جار إن كان ثابتًا.
   - تحذير واضح إذا لم تكن Root Core مقفلة.
3. لا توهم أن الجواب المختصر يساوي دراسة Root Core.

---

# 24. التعامل مع نقص الأدلة

لا تربط نقص الأدلة بعدد ثابت من المواضع إلا إذا فعلت Authority ذلك.

قيّم:
- تنوع السياقات.
- تنوع الصيغ.
- قدرة التفريد.
- وجود جيران حاسمين.
- وجود counterevidence.
- مدى الاعتماد على مصادر خارجية.

قد تكون كثرة المواضع بلا تنوع غير كافية، وقد يكون عدد قليل ذا قيمة عالية لكنه لا يمنح lock تلقائيًا.

---

# 25. الكفاءة وعدم إعادة العمل

MUST:
- أعد استخدام Evidence صالح إذا لم يتغير Scope أو dependency.
- نفّذ focused checks أثناء تطوير الفرضية.
- وسّع verification عند تغير boundary أو claim.
- أعد full analysis فقط إذا تطلبت صلاحية الادعاء ذلك.

MUST NOT:
- تعيد Corpus كاملًا لمجرد تحسين الصياغة.
- تعتبر commit جديدًا وحده سببًا لإبطال evidence.
- تخفض شرطًا منهجيًا بسبب كلفة التحقق.

---

# 26. Verification Cadence

إن كانت المهارة تعمل داخل مشروع برمجي:

### V0 — Preflight
- Authority.
- Corpus identity.
- Status policy.
- Tool availability.
- prior result/dependencies.

### V1 — Inner Loop
- Focused occurrence checks.
- Morphology/syntax sanity.
- neighbor-specific tests.
- rejection-condition test.

### V2 — Checkpoint
- Coverage consistency.
- all essential neighbors.
- layer separation.
- counterevidence.
- schema/registry consistency.

### V3 — Phase Gate
- full affected root/lexeme analysis.
- canonical citation verification.
- validator/tool checks relevant to the claim.

### V4 — Release/Registry Gate
استخدم فقط بوابة المشروع الرسمية، ولا تمنح قبولًا أعلى من صلاحية الوكيل.

---

# 27. Behavioral Verification of This Skill

اختبر المهارة دوريًا على fixtures مصممة لكشف الانحراف.

يجب أن تمنع الوكيل من:

1. قفل Root Core من آية واحدة دون سلطة تسمح.
2. بدء التعريف من المعجم.
3. تجاهل counterexample.
4. خلط Form بالRoot.
5. استخدام Letter Semantics كدليل وحيد.
6. اختراع فرق بين الجيران بلا evidence.
7. قبول تعريف عام جدًا.
8. تجاوز block لأن المستخدم يريد جوابًا.
9. رفع hypothesis بسبب لغة واثقة.
10. الخلط بين Definition وMeaning وConcept.
11. ادعاء Validator لم يُشغّل.
12. اختراع Status.
13. إجبار جميع الاستعمالات على وحدة مصطنعة.
14. استخدام substitution كدليل مستقل.
15. اعتبار جمع المواضع = validation.

يفضل استخدام أمثلة اصطناعية أو fixtures غير سلطة لاختبار سلوك الوكيل، حتى لا تتحول نتيجة اختبار إلى Claim قرآنية فعلية.

## 27.1 `PRE_DELIVERY_AUDIT`

قبل التسليم النهائي، نفّذ مراجعة مختصرة قابلة للتدقيق، لا كشفًا للتفكير الخاص:

```yaml
pre_delivery_audit:
  target_contract_resolved: "[PASS/FAIL]"
  authority_resolved: "[PASS/FAIL/PARTIAL]"
  coverage_claim_matches_evidence: "[PASS/FAIL]"
  layer_separation_checked: "[PASS/FAIL]"
  essential_neighbors_checked: "[PASS/FAIL/NOT_APPLICABLE]"
  rejection_condition_operational: "[PASS/FAIL]"
  counterevidence_preserved: "[PASS/FAIL]"
  tool_claims_match_actual_runs: "[PASS/FAIL]"
  official_status_authorized: "[PASS/FAIL/UNASSIGNED]"
  anti_pattern_findings: "[IDs or none]"
  corrections_before_delivery: "[summary]"
```

MUST:
- تصلح أي `FAIL` يمكن إصلاحه قبل التسليم.
- تمنع القفل عند بقاء فشل حاسم.
- تعرض للمستخدم المخالفات أو القيود المؤثرة والـ Evidence اللازم فقط.
- لا تعرض private chain-of-thought أو سجل الاستدلال الداخلي التفصيلي.

---

# 28. شروط التوقف

## Stop/Block the affected analysis when:
- Authority اللازمة متعارضة ولا يمكن حسمها.
- Corpus canonical غير قابل للتحقق للمادة المطلوبة.
- وحدة التحليل نفسها غير مستقرة.
- الجار الحاسم غير محلول ويعتمد عليه Claim.
- counterexample حاسم غير محلول.
- الفصل بين Root/Form/Context غير ممكن.
- Evidence dependency غير قابلة للحل.
- الأداة اللازمة للتحقق غير متاحة ولا يوجد fallback مصرح.
- القفل يتطلب سلطة لا يملكها الوكيل.

لا تعمم عائقًا محليًا على المهمة كلها إن أمكن إنجاز أجزاء مستقلة بصورة صحيحة.

---

# 29. شروط النجاح

التحليل الجيد لا يُقاس بجمال التعريف.

ينجح عندما يوضح بصدق:

- ما الذي ثبت؟
- من أي Evidence؟
- ضمن أي Scope؟
- ما الذي لم يثبت؟
- ما الذي يعود إلى Root؟
- ما الذي يعود إلى Form/Construction/Context؟
- ما الفرق عن الجيران؟
- ما أقوى counterevidence؟
- ما الذي سيفرض رفض/إعادة فتح الفرضية؟
- ما الحالة الرسمية التي تسمح بها Authority؟

النتيجة الصحيحة قد تكون:
- Claim مقفلة إذا اجتازت البوابة الرسمية.
- Hypothesis واضحة.
- أو توقفًا منضبطًا بلا Root Core مصطنعة.

---

# 30. قاعدة ختامية

> الهدف ليس استخراج تعريف بأي ثمن، بل إنتاج **أصغر Claim دلالية يمكن تتبعها واختبارها وتمييزها والدفاع عنها ضمن نطاق معلوم، مع القدرة الصريحة على رفضها إذا خالفت الأدلة**.
