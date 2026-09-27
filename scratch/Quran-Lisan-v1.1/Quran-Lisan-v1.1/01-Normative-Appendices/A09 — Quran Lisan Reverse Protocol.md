---
DOCUMENT_ID: A09
TITLE: "Quran Lisan Reverse Protocol"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "تقنين الاستدلال العكسي: التقابل والنفي والعكس والاستثناء والنتائج والتوزيع السلبي والغياب."
SCOPE: "حدود المعنى عبر الجهة المقابلة أو النافية أو المعكوسة."
ACTIVATION_CONDITION: "سؤال ضد/فرق/نفي/استثناء/عكس/غياب أو اختبار core بالReverse."
DEPENDS_ON: [M01, A02, A03, A04, A05]
EXPANDS_MASTER_SECTIONS: [M01-P08]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A09 — Quran Lisan Reverse Protocol

## 1. Definition & control IDs

#### A09-P01 — Reverse bounds; it does not define alone
`REVERSE_INFORMATION ≠ FULL_LEXICAL_MEANING`. الغرض discovery + bounding + testing + falsification، ويجب إعادة كل نتيجة إلى شبكة الاستعمال المباشر.

#### A09-D01 — Reverse families
`OPPOSITION | NEGATION | PRIVATION | REVERSAL | RELATIONAL_CONVERSE | EXCEPTION_BOUNDARY | OUTCOME_INVERSION | COUNTERFACTUAL_SUBSTITUTION | NEGATIVE_DISTRIBUTION | ABSENCE_CLAIM | THIRD_TERM_TEST | NEAR_FAR_TRIANGULATION`.

#### A09-T01 — Shared Domain
لا تقابل بلا `SHARED_OR_RELEVANT_DOMAIN_ESTABLISHED`.

#### A09-T02 — Negation Scope
حدد المنفي وما لا يتأثر بالنفي قبل أي binary inference.

#### A09-T03 — Third Term
ابحث عن C قبل إعلان A/B ثنائية كاملة.

#### A09-T04 — Participant Control
اختلاف participant قد يفسر فرقًا يبدو lexical.

#### A09-T05 — Construction Control
اختلاف construction قد يفسر الفرق؛ لا يرفع للlexeme/root.

#### A09-T06 — Outcome Inversion
النتائج المختلفة/المعكوسة لا تثبت lexical antonymy وحدها.

#### A09-T07 — Negative Distribution
لا تستخدم الغياب إلا بعد [A03-G02] ومساحة توقع محددة مسبقًا.

#### A09-T08 — Near/Far Triangulation
المقابل البعيد يختبر domain boundary، والجار القريب يختبر distinctive feature. اتفاقهما مع distribution/construction يقوي الحد ولا يعرّف الجذر وحده.

#### A09-G01 — Reverse Acceptance Gate
يلزم بحسب النوع: targets verified، domain established، relation classified، participant/construction confounds controlled، scope declared، serious alternatives/third term considered، counterevidence addressed، boundary of inference declared، direct network crosschecked. وإلا `REVERSE_INFERENCE = UNRESOLVED`.

#### A09-O01 — Required reverse output
كل نتيجة تعلن: relation type، witness، domain، contrast/boundary، what it reveals، what it does not prove، alternatives/third term، counterevidence، status.

## 2. Canonical detailed protocol

# 2. المبادئ الحاكمة

## 2.1. المبدأ الأول

> **الاستدلال العكسي يكشف الحدود ولا يعرّف المفردة وحده.**

```text
REVERSE_INFORMATION ≠ FULL_LEXICAL_MEANING
```

---

## 2.2. المبدأ الثاني

> **المتقابلان الحقيقيان يشتركان أولًا في مجال قابل للمقارنة، ثم يفترقان على محور محدد.**

```text
SHARED_DOMAIN
+
CONTRAST_AXIS
=
CONTRASTIVE_INFORMATION
```

بدون `SHARED_DOMAIN` لا يُقبل ادعاء تقابل دلالي.

---

## 2.3. المبدأ الثالث

> **نفي المقابل لا يساوي تلقائيًا إثبات الطرف الآخر.**

```text
NOT(B) ≠ A
NOT(A) ≠ B
```

إلا إذا ثبت أن العلاقة `COMPLEMENTARY_EXHAUSTIVE` داخل نطاق مضبوط.

---

## 2.4. المبدأ الرابع

> **انقلاب النتيجة لا يثبت وحده تضاد المعنى.**

قد يكون A وB:
- سببين لنتيجتين مختلفتين.
- حالتين متعاقبتين.
- فعلين غير متضادين.
- طرفين في علاقة أوسع.

لذلك:

```text
OPPOSITE_OUTCOMES ≠ LEXICAL_ANTONYMY
```

---

## 2.5. المبدأ الخامس

> **التقابل السياقي لا يُرقّى إلى تضاد معجمي عام دون ثبات عابر للسياقات.**

---

## 2.6. المبدأ السادس

> **الغياب ليس نفيًا، والنفي ليس ضدًا، والصمت ليس مساحة تنفيذ مفتوحة.**

```text
ABSENCE ≠ NEGATION
NEGATION ≠ OPPOSITION
NOT_SPECIFIED ≠ TEXTUAL_OPEN_SPACE
```

---

## 2.7. المبدأ السابع

> **ابحث عن الطرف الثالث قبل إعلان الثنائية.**

وجود C قد يكشف أن:
- A/B قطبان على مقياس.
- A أوسع من B.
- B حالة فرعية.
- الثنائية سياقية فقط.

---

## 2.8. المبدأ الثامن

> **الضد يختبر الحد البعيد، والجار الدلالي يختبر الحد القريب.**

```text
TARGET ↔ OPPOSITE
TARGET ≈ NEAR_NEIGHBOR
```

التحليل الأقوى يجمع الاثنين.

---

## 2.9. المبدأ التاسع

> **لا تُشتق الدلالة من تسمية نحوية أو صرفية جاهزة.**

`نفي، استثناء، شرط، عطف، لام، صيغة...` أوصاف بنيوية أولًا؛ وظيفتها الدلالية نفسها تحتاج اختبارًا وفق v1.1.

---

## 2.10. المبدأ العاشر

> **كل استدلال عكسي يجب أن يعود في النهاية إلى شبكة الاستعمال الأصلية.**

```text
REVERSE_RESULT
→ FEED_BACK_TO_DIRECT_MODEL
→ CROSS_CHECK
→ FALSIFY
```

---

# 3. متى يُفعّل الملحق؟

فعّل:

```text
REVERSE_PASS = ON
```

إذا تضمن السؤال واحدًا أو أكثر من الآتي:

- «ما ضد X؟»
- «ما الفرق بين X وY؟»
- ادعاء أن لفظين متقابلان.
- تحليل نفي أو نهي أو استثناء.
- انتقال من حالة إلى حالة معكوسة.
- اختلاف نتائج حالتين.
- سؤال: لماذا X وليس Y؟
- استعمال الغياب أو الصمت كدليل.
- `NEGATIVE_DISTRIBUTION`.
- البحث عن حدود `ROOT_AXIAL_MEANING`.
- التحقق من فرضية دلالية عبر حالات معاكسة.
- مقارنة طرف موجب بطرف سالب.
- بناء `EVENT_STATE_MODEL` فيه دخول/خروج أو تقييد/حل أو فتح/إغلاق.

---

# 4. عائلات الاستدلال العكسي

لا تختزل `Reverse` في التضاد وحده.

```text
REVERSE_INFERENCE_FAMILY =
  OPPOSITION
  | NEGATION
  | PRIVATION
  | REVERSAL
  | RELATIONAL_CONVERSE
  | EXCEPTION_BOUNDARY
  | OUTCOME_INVERSION
  | COUNTERFACTUAL_SUBSTITUTION
  | NEGATIVE_DISTRIBUTION
  | ABSENCE_CLAIM
  | THIRD_TERM_TEST
  | NEAR_FAR_TRIANGULATION
```

---

# 5. الأسرة الأولى — `OPPOSITION`

## 5.1. الأنواع

```text
OPPOSITION_TYPE =
  DIRECT_POLAR_CONTRAST
  | COMPLEMENTARY_STATE
  | SCALAR_POLARITY
  | REVERSIVE_TRANSITION
  | RELATIONAL_CONVERSE
  | PRIVATIVE_RELATION
  | CONTEXTUAL_FUNCTIONAL_CONTRAST
  | NEGATED_SAME_PREDICATE
  | UNRESOLVED
```

---

## 5.2. `DIRECT_POLAR_CONTRAST`

طرفان يضعهما النص على قطبين داخل مجال واحد.

مثال آمن منهجيًا:
> **خير / شر** في بنية متوازية مثل الزلزلة 7–8.

لا يعني ذلك أن كل استعمال لـ«خير» يمكن تعريفه بنفي «شر».

---

## 5.3. `COMPLEMENTARY_STATE`

حالان يستبعد أحدهما الآخر **في نطاق محدد فقط**.

شرطه:

```text
SCOPE_DEFINED = YES
MUTUAL_EXCLUSION = TESTED
THIRD_STATE_SEARCHED = YES
```

لا تستخدم هذا التصنيف إذا أمكن وجود حالة ثالثة معتبرة.

---

## 5.4. `SCALAR_POLARITY`

طرفان على مقياس يسمح بدرجات وسطى.

مثل:
- كثير / قليل
- قريب / بعيد

القاعدة:

```text
NOT(HIGH) ≠ LOW
```

إلا إذا حدد السياق ثنائية مغلقة.

---

## 5.5. `REVERSIVE_TRANSITION`

حال أو فعل يعكس انتقالًا سابقًا أو يرفع حالة قائمة.

هذا مهم في:
- دخول / خروج.
- تقييد / حل.
- إحياء / إماتة عند ثبوت العلاقة في السياق.
- فتح / إغلاق عند ثبوتها.

المحور هنا ديناميكي:

```text
STATE_A
→ TRANSITION
→ STATE_B
```

---

## 5.6. `RELATIONAL_CONVERSE`

طرفان يصفان علاقة واحدة من جهتين.

أمثلة تصورية:
- أعطى / أخذ.
- علّم / تعلّم.

هذا **ليس تضادًا بسيطًا**.

اختبر:
- ثبات الحدث.
- تبدل أدوار المشاركين.
- اتجاه العلاقة.

---

## 5.7. `PRIVATIVE_RELATION`

وجود خاصية مقابل فقدها أو غيابها.

الضابط:

> غياب الخاصية لا يعني وجود خاصية مضادة.

---

## 5.8. `CONTEXTUAL_FUNCTIONAL_CONTRAST`

القرآن يضع فعلين أو حالتين في مقابلة وظيفية داخل سياق، مع عدم ثبوت تضاد معجمي عام.

مثال:
> **﴿لَتُبَيِّنُنَّهُ لِلنَّاسِ وَلَا تَكْتُمُونَهُ﴾** — آل عمران 187.

الذي يثبت مباشرة:
- فعل مطلوب يتعلق بالإظهار للناس.
- وفعل منهي عنه يتعلق بالكتمان.
- وجود محور سياقي قوي بين الإظهار والكتمان في هذا الموضع.

ولا نستنتج من ذلك وحده تعريفًا كاملًا لجذر **ب ي ن** أو **ك ت م**.

---

## 5.9. `NEGATED_SAME_PREDICATE`

مثل:
```text
يعلم / لا يعلم
```

هذه ليست مفردتين متضادتين، بل:

```text
PREDICATE
vs
NEGATED(PREDICATE)
```

ويجب تحليل **نطاق النفي** قبل أي استنتاج.

---

# 6. الأسرة الثانية — `NEGATION`

## 6.1. لماذا النفي أداة قوية؟

لأنه يكشف:
- ما الذي يبقى من الجملة بعد إزالة الحكم.
- نطاق الخاصية.
- ما الذي ينقلب وما الذي لا ينقلب.

---

## 6.2. `NEGATION_SCOPE_TEST`

قبل الاستدلال حدد:

```text
NEGATED_ELEMENT =
NEGATION_SCOPE =
PRESUPPOSED_MATERIAL =
UNAFFECTED_MATERIAL =
```

ولا تعامل كل ما في الجملة بوصفه منفيًا.

---

## 6.3. `DOUBLE_DIRECTION_NEGATION_TEST`

```text
NOT(B) ⇒ A ?
NOT(A) ⇒ B ?
```

النتائج:

- كلاهما صحيح داخل نطاق مغلق → مرشح لـ`COMPLEMENTARY_STATE`.
- أحدهما فقط → علاقة غير متماثلة.
- كلاهما غير لازم → النفي لا يثبت الثنائية.

---

# 7. الأسرة الثالثة — `REVERSAL_AND_RELEASE`

## 7.1. السؤال المركزي

> ما الحالة التي كانت قائمة؟ وما الذي رفعها أو قلبها؟ وما الذي أصبح ممكنًا بعد التحول؟

---

## 7.2. الضابط

لا تستنتج الحالة السابقة من النتيجة وحدها.

يلزم شاهد على:

```text
PRE_STATE
TRANSITION_MARKER
POST_STATE
```

وإلا:

`REVERSAL_STATUS = PARTIALLY_ESTABLISHED`

---

## 7.3. مثال مضبوط: `حُرُم / حللتم`

في المائدة 2 يظهر:

> **﴿وَإِذَا حَلَلْتُمْ فَاصْطَادُوا﴾**

ومع شبكة:
> **﴿غَيْرَ مُحِلِّي الصَّيْدِ وَأَنْتُمْ حُرُمٌ﴾** ونحوها.

المستفاد العكسي المنضبط:

```text
SHARED_DOMAIN =
حالة الشخص بالنسبة إلى صيد البر/الصيد في السياق المتحقق

STATE_A =
حُرُم → قيد خاص متعلق بالصيد

TRANSITION =
حللتم

STATE_B =
زوال القيد الخاص بما يسمح بعودة الصيد في هذا السياق

CONTRAST_AXIS =
STATE-SPECIFIC RESTRICTION ↔ RELEASE
```

ثم تُعاد النتيجة إلى شبكة **ح ر م** كلها؛ فلا يصبح هذا المثال وحده تعريفًا للجذر.

---

# 8. الأسرة الرابعة — `EXCEPTION_BOUNDARY`

## 8.1. لماذا الاستثناء مهم؟

الاستثناء قد يكشف:
- الحد الذي تنتهي عنده القاعدة.
- الفئة الخارجة.
- هل الأصل عام أم مقيد.

---

## 8.2. لا تجعل كل «إلا» تضادًا

```text
EXCEPTION ≠ OPPOSITION
```

وقد يكون الاستثناء:
- متصلًا.
- منفصلًا.
- موضحًا للنطاق.
- حجاجيًا.

وظيفته يجب أن تُفحص داخل التركيب لا من الاسم النحوي وحده.

---

## 8.3. الحقول

```text
BASE_SET =
EXCLUDED_OR_EXCEPTED_SET =
RELATION_TO_BASE =
BOUNDARY_DISCOVERED =
EXCEPTION_FUNCTION_STATUS =
```

---

# 9. الأسرة الخامسة — `OUTCOME_INVERSION`

## 9.1. المبدأ

إذا ارتبط A بنتيجة X وB بنتيجة Y مختلفة أو معاكسة، فقد يكشف ذلك فرقًا وظيفيًا.

لكن:

```text
OUTCOME_DIFFERENCE
≠
MEANING_DIFFERENCE_PROVED
```

---

## 9.2. اختبارات إلزامية

1. هل العلاقة A→X ثابتة؟
2. هل العلاقة B→Y ثابتة؟
3. هل X وY متعاكستان فعلًا أم مختلفتان فقط؟
4. هل الاختلاف سببه A/B أم عامل ثالث؟
5. هل المشاركون والسياق متقاربون؟
6. هل توجد حالات A بنتيجة مختلفة أو B بنتيجة مختلفة؟

---

## 9.3. الحالة

```text
OUTCOME_RELATION =
  DIRECT
  | STRONGLY_ENTAILED
  | ASSOCIATED
  | CONFOUNDED
  | UNRESOLVED
```

---

# 10. الأسرة السادسة — `COUNTERFACTUAL_SUBSTITUTION`

## 10.1. السؤال

> لماذا استعمل النص X لا Y؟

---

## 10.2. وظيفة الاختبار

الاستبدال الافتراضي:

`ANALYTICAL_PROBE`

وليس دليلًا قرآنيًا مستقلًا.

---

## 10.3. شروط المقارنة

يجب أن يكون Y:
- قابلًا للمقارنة وظيفيًا.
- عربيًا ممكنًا في البناء.
- ويفضل أن يكون حاضرًا في القرآن في مواضع قابلة للمقارنة.
- غير مختار فقط لأنه يؤكد الفرضية.

---

## 10.4. الناتج

```text
WHAT_X_PRESERVES =
WHAT_Y_WOULD_CHANGE =
DISTINCTION_CANDIDATE =
TEXTUAL_SUPPORT_FOR_DISTINCTION =
STATUS =
```

إذا لم يظهر فرق ثابت:

`NO_DIFFERENCE_ESTABLISHED`

ولا تخترع فرقًا.

---

# 11. الأسرة السابعة — `NEGATIVE_DISTRIBUTION`

## 11.1. السؤال

> أين كان يمكن توقع X ضمن فرضيتنا، لكنه لم يظهر؟

هذه أداة قوية لاختبار حدود المعنى.

---

## 11.2. شرط التغطية

لا تستخدم الغياب كدليل إلا إذا كان:

```text
SEARCH_SPACE_DEFINED = YES
INDEXING_COMPLETE_FOR_SCOPE = YES
EXPECTED_CONTEXT_DEFINED_IN_ADVANCE = YES
```

وإلا:

`NEGATIVE_DISTRIBUTION = NOT_ESTABLISHED`

---

## 11.3. لا تستنتج من الغياب وحده

```text
ABSENCE_OF_X
≠
PROOF_OF_NOT-X
```

قد تكون هناك:
- صياغة بديلة.
- حذف.
- اختلاف سياقي.
- عدم كفاية corpus.
- فرضية توقع خاطئة.

---

# 12. الأسرة الثامنة — `ABSENCE_CLAIM`

لأي دعوى من نوع:

- «لا يرد».
- «لم يستخدم القرآن».
- «لا يوجد».
- «لا يقابل».
- «لا يأتي مع».

طبّق:

`ABSENCE_CLAIM_GATE` من v1.1.

### الصياغة الآمنة

إذا كانت التغطية كاملة:
> ضمن النطاق المتحقق بالكامل، لم يظهر...

إذا كانت جزئية:
> لم يظهر في المواضع التي تم التحقق منها في هذا البحث...

---

# 13. الأسرة التاسعة — `THIRD_TERM_TEST`

## 13.1. المبدأ

قبل إعلان A/B ثنائية، ابحث عن C.

---

## 13.2. ما الذي قد يفعله C؟

قد يثبت أن:
- A وB طرفان على مقياس.
- B ليس نقيض A بل فرعًا.
- A أوسع من B.
- هناك منطقة وسطى.
- التقابل سياقي فقط.

---

## 13.3. الحالة

```text
THIRD_TERM_STATUS =
  NONE_FOUND_IN_FULL_SCOPE
  | FOUND_AND_COMPATIBLE
  | FOUND_AND_BREAKS_BINARY
  | SEARCH_INCOMPLETE
```

---

# 14. الأسرة العاشرة — `NEAR_FAR_TRIANGULATION`

## 14.1. المبدأ

لا تكتفِ بالضد.

ابحث عن:
- **المقابل البعيد** الذي يكشف المجال.
- **الجار القريب** الذي يكشف الخصوصية.

```text
OPPOSITE_AXIS → DOMAIN_BOUNDARY
NEAR_NEIGHBOR_AXIS → DISTINCTIVE_FEATURE
```

---

## 14.2. النتيجة

إذا اتفق:
- الجار،
- المقابل،
- التوزيع،
- التركيب،

على خاصية واحدة، ارتفعت قوة تلك الخاصية بوصفها حدًا دلاليًا.

---

# 15. شروط قيام علاقة Reverse معتبرة

لا يكفي «شرط واحد».

## 15.1. الشروط الضرورية العامة

لكل ادعاء تقابلي أو عكسي رئيسي يلزم بحسب نوعه:

```text
TARGETS_VERIFIED = YES
SHARED_OR_RELEVANT_DOMAIN_ESTABLISHED = YES
RELATION_TYPE_CLASSIFIED = YES
CONSTRUCTION_CONFOUND_CONTROLLED = YES
PARTICIPANT_CONFOUND_CONTROLLED = YES
SCOPE_DECLARED = YES
SERIOUS_ALTERNATIVES_TESTED = YES
```

---

## 15.2. شروط داعمة وليست بدائل عن الضرورية

قد تزيد القوة:

```text
DIRECT_COUPLING
STRUCTURAL_PARALLELISM
REPETITION
NEGATION_PATTERN
OUTCOME_REVERSAL
CROSS_CONTEXT_STABILITY
COUNTERFACTUAL_DISCRIMINATION
NEGATIVE_DISTRIBUTION
THIRD_TERM_SEARCH
NEAR_NEIGHBOR_CONFIRMATION
```

وجود واحد منها **لا يعوض** غياب المجال المشترك أو ضبط العوامل المربكة.

---

# 16. ضبط Blind Lab

## 16.1. محظور داخل الاكتشاف الداخلي

لا تستخدم:
- «المعجم يقول إن ضد X هو Y».
- قوائم antonyms الجاهزة.
- تفسيرًا تراثيًا لتحديد الطرف المقابل.
- ترجمة أجنبية لتوليد التضاد.
- تصنيفًا فلسفيًا حديثًا قبل الشبكة.

---

## 16.2. ماذا عن `LEXICAL_ANTONYMY`؟

داخل Blind Lab لا تحتاج إثباتًا معجميًا خارجيًا.

استخدم:

```text
QURAN_INTERNAL_POLAR_RELATION
```

إذا ثبتت العلاقة قرآنيًا.

بعد `INTERNAL_LOCK` يمكن مقارنة النتيجة بالمعاجم في `POST_LOCK_EXTERNAL_COMPARISON`.

---

# 17. ضبط التركيب والصرف

لا تقل:

- «هذه أداة نفي إذن الطرفان متضادان».
- «هذا استثناء إذن ما بعده نقيض ما قبله».
- «هذه صيغة انعكاسية إذن المعنى عكسي».

بل:

```text
STRUCTURAL_OBSERVATION
→ FUNCTION_HYPOTHESIS
→ QURANIC_DISTRIBUTION_TEST
→ LOCAL_FUNCTION
```

---

# 18. `REVERSE_CORE_KERNEL`

عند تفعيل الملحق، نفّذ هذه الخطوات دائمًا:

1. `VERIFY_TARGETS`
2. `DEFINE_REVERSE_QUESTION`
3. `IDENTIFY_RELATION_CANDIDATE`
4. `ESTABLISH_SHARED/RELEVANT_DOMAIN`
5. `CLASSIFY_RELATION_TYPE`
6. `CONTROL_CONSTRUCTION_AND_PARTICIPANTS`
7. `EXTRACT_AXIS_OR_BOUNDARY`
8. `TEST_THIRD_TERM_AND_ALTERNATIVES`
9. `CROSS_CHECK_WITH_DIRECT_NETWORK`
10. `FALSIFY_AND_BOUND_SCOPE`

---

# 19. `REVERSE_MODULE_ROUTER`

لا تنفذ كل الوحدات دائمًا.

| حالة السؤال | الوحدات |
| :--- | :--- |
| ضد/مقابل | Opposition + Third Term + Near/Far |
| نفي | Negation Scope + Complementarity Test |
| دخول/خروج/حل/تقييد | Reversal + Event State |
| استثناء | Exception Boundary |
| نتائج مختلفة | Outcome Inversion |
| لماذا X لا Y | Counterfactual Substitution |
| «لا يرد» | Absence Claim + Coverage Gate |
| أين لا يظهر X | Negative Distribution |
| مقارنة جذور/ألفاظ | Opposition + Neighbor + Root/Layer Attribution |
| اختبار Root Core | Reverse + Direct Network + Core Tests |

```text
REVERSE_EXECUTION_PROFILE =
  REVERSE_CORE_KERNEL
  + APPLICABLE_REVERSE_MODULES
```

---

# 20. البروتوكول التنفيذي الكامل

## المرحلة 1 — تعريف السؤال

```text
REVERSE_TARGET =
REVERSE_QUESTION =
CLAIM_SCOPE =
DIRECT_MODEL_AVAILABLE =
```

---

## المرحلة 2 — توليد المرشح

```text
CANDIDATE_A =
CANDIDATE_B =
WHY_CANDIDATE =
SOURCE_OF_CANDIDACY =
```

إذا جاء B من مصدر خارجي قبل القفل:
`SOURCE_POLICY_BLOCKED`

---

## المرحلة 3 — المجال

```text
SHARED_DOMAIN =
SAME_QUESTION_TEST =
```

إذا فشل:
`RELATION = NO_OPPOSITION_ESTABLISHED`

---

## المرحلة 4 — ضبط المشاركين

```text
AGENT_A/B =
PATIENT_A/B =
BENEFICIARY_A/B =
TIME_A/B =
DOMAIN_A/B =
```

---

## المرحلة 5 — ضبط البناء

```text
CONSTRUCTION_A =
CONSTRUCTION_B =
PARALLELISM =
GRAMMATICAL_FUNCTION_STATUS =
```

---

## المرحلة 6 — التصنيف

اختر من `REVERSE_INFERENCE_FAMILY` ثم subtype.

---

## المرحلة 7 — استخراج المحور

```text
INVARIANT_FEATURES =
CHANGING_FEATURE =
DIRECTION =
BOUNDARY =
```

---

## المرحلة 8 — التماثل

```text
SYMMETRY =
  SYMMETRIC
  | ASYMMETRIC
  | PARTIAL
  | UNRESOLVED
```

---

## المرحلة 9 — الثنائية

```text
BINARY_STATUS =
  EXHAUSTIVE_WITHIN_SCOPE
  | POLAR_WITH_MIDDLE
  | CONTEXTUAL_PAIRING
  | FALSE_BINARY
  | UNRESOLVED
```

---

## المرحلة 10 — النفي

طبّق `NEGATION_SCOPE_TEST` عند الحاجة.

---

## المرحلة 11 — النتيجة

اختبر `OUTCOME_INVERSION` دون الخلط بين اختلاف النتيجة واختلاف المعنى.

---

## المرحلة 12 — الاستنساخ عبر السياقات

```text
CROSS_CONTEXT_REPLICATION =
  STRONG
  | PARTIAL
  | SINGLE_CONTEXT
  | FAILED
```

---

## المرحلة 13 — الطرف الثالث

نفذ `THIRD_TERM_TEST`.

---

## المرحلة 14 — الجار القريب

نفذ `NEAR_FAR_TRIANGULATION`.

---

## المرحلة 15 — الاستبدال

نفذ `COUNTERFACTUAL_SUBSTITUTION` إذا كان مفيدًا.

---

## المرحلة 16 — التوزيع السلبي

لا يُفعّل إلا مع search space معرف مسبقًا وتغطية كافية.

---

## المرحلة 17 — بناء الادعاء

```text
REVERSE_CLAIM =
REVERSE_INFORMATION =
BOUNDARY_OF_INFERENCE =
WHAT_IT_DOES_NOT_PROVE =
```

---

## المرحلة 18 — التغذية العكسية

```text
DIRECT_MODEL_BEFORE =
REVERSE_CONSTRAINT =
DIRECT_MODEL_AFTER =
```

لا تغير النموذج بصمت؛ سجّل السبب.

---

## المرحلة 19 — النقض

ابحث عن:
- سياق لا يعمل فيه المحور.
- طرف ثالث.
- اختلاف مشاركين يفسر الفرق.
- بناء مختلف.
- نتيجة غير معكوسة.
- موضع يضع A وB في علاقة غير متقابلة.

---

## المرحلة 20 — الحالة النهائية

```text
REVERSE_RELATION_STATUS =
  CANDIDATE
  | OBSERVED
  | TESTED
  | SUPPORTED
  | UNRESOLVED
  | REJECTED
  | NO_RELATION_ESTABLISHED
```

---

# 21. مصفوفة الأدلة — لا تختزلها في Status واحد

```text
REVERSE_EVIDENCE_PROFILE:

TEXTUAL_COUPLING =
STRUCTURAL_PARALLELISM =
SHARED_DOMAIN =
PARTICIPANT_CONTROL =
CONSTRUCTION_CONTROL =
NEGATION_SUPPORT =
OUTCOME_SUPPORT =
CROSS_CONTEXT_STABILITY =
THIRD_TERM_SEARCH =
NEIGHBOR_CONFIRMATION =
COUNTERFACTUAL_DISCRIMINATION =
NEGATIVE_DISTRIBUTION_SUPPORT =
COUNTEREVIDENCE_BURDEN =
```

القيم:

`STRONG / MODERATE / WEAK / NOT_EVALUATED / NOT_APPLICABLE`

---

# 22. سجل الاستدلال العكسي

## `REVERSE_EVIDENCE_LEDGER`

| الحقل | المحتوى |
| :--- | :--- |
| `REVERSE_ID` | معرف |
| `TERM_A` | الطرف الأول |
| `TERM_B` | الطرف الثاني إن وجد |
| `FAMILY` | عائلة Reverse |
| `SUBTYPE` | النوع الفرعي |
| `PRIMARY_WITNESS` | الشاهد |
| `CLAIM_SCOPE` | النطاق |
| `SHARED_DOMAIN` | المجال |
| `INVARIANT_FEATURES` | الثوابت |
| `CHANGING_FEATURE` | المتغير |
| `CONTRAST_AXIS` | محور الفرق |
| `PARTICIPANT_CONTROL` | النتيجة |
| `CONSTRUCTION_CONTROL` | النتيجة |
| `THIRD_TERM_RESULT` | النتيجة |
| `NEAR_NEIGHBOR_RESULT` | النتيجة |
| `CROSS_CONTEXT_RESULT` | النتيجة |
| `SUPPORTING_EVIDENCE_REFS` | الأدلة |
| `COUNTEREVIDENCE_REFS` | المضاد |
| `BOUNDARY_OF_INFERENCE` | ما يسمح به |
| `DOES_NOT_PROVE` | ما لا يسمح به |
| `STATUS` | الحالة |
| `REOPEN_IF` | شرط إعادة الفتح |

---

# 23. درجات القوة المعرفية

افصل:

```text
REVERSE_RESULT_STRENGTH
≠
REVERSE_RESEARCH_COMPLETENESS
≠
REVERSE_INDEPENDENT_VERIFICATION
```

## 23.1. القوة

`WEAK / MODERATE / STRONG / UNRESOLVED`

## 23.2. الاكتمال

يعتمد على:
- عدد السياقات ذات الصلة.
- تغطية الطرف الثالث.
- تغطية الجيران.
- الحالات الصعبة.
- التوزيع السلبي عند الادعاء به.

## 23.3. التحقق

وفق درجات v1.1:
- self-review
- same-model context-blind
- different-model
- human review
- independent replication

---

# 24. الأخطاء المنهجية المحظورة

1. `FALSE_ANTONYM` — اختراع ضد.
2. `CIRCULAR_OPPOSITION` — إثبات المعنى بالضد ثم الضد بالمعنى.
3. `ANTONYM_AS_DEFINITION` — تعريف A بأنه ليس B.
4. `SINGLE_CONTEXT_OVERGENERALIZATION`.
5. `FALSE_BINARY`.
6. `FORCED_SYMMETRY`.
7. `SCALAR_MIDDLE_ERASURE`.
8. `NEGATION_AS_ANTONYMY`.
9. `CONJUNCTION_AS_CONTRAST`.
10. `OUTCOME_AS_MEANING`.
11. `CONSEQUENCE_TO_CAUSE_REVERSAL`.
12. `DENYING_THE_CONSEQUENT` — استنتاج غياب السبب من غياب نتيجة غير حصرية.
13. `CONTRAPOSITION_OVERREACH` — استخدام عكس النقيض حيث لا تسمح العلاقة.
14. `ABSENCE_AS_NEGATION`.
15. `ABSENCE_FROM_PARTIAL_CORPUS`.
16. `EXCEPTION_AS_OPPOSITION`.
17. `GRAMMAR_LABEL_AS_SEMANTICS`.
18. `PARTICIPANT_CONFOUND`.
19. `CONSTRUCTION_CONFOUND`.
20. `DICTIONARY_ANTONYM_FIRST`.
21. `THIRD_TERM_OMISSION`.
22. `NEGATION_SCOPE_ERROR`.
23. `PRIVATION_AS_POSITIVE_OPPOSITE`.
24. `CONTEXTUAL_TO_LEXICAL_UPGRADE`.
25. `REVERSE_ONLY_ROOT_DEFINITION` — تعريف الجذر من المقابل دون شبكة مشتقات.
26. `NO_DIFFERENCE_AVOIDANCE` — اختراع فرق بدل قبول عدم ثبوته.
27. `TEXTUAL_SILENCE_TO_OPEN_SPACE`.
28. `REVERSE_SLOT_FILLING`.

---

# 25. بوابة القبول العامة

لا يُستخدم Reverse لتعديل معنى قائم إلا إذا:

```text
TARGET_VERIFIED = YES
RELATION_TYPE_CLASSIFIED = YES
RELEVANT_DOMAIN_ESTABLISHED = YES
PARTICIPANT_CONFOUND_CONTROLLED = YES
CONSTRUCTION_CONFOUND_CONTROLLED = YES
SERIOUS_ALTERNATIVES_TESTED = YES
THIRD_TERM_CONSIDERED = YES
COUNTEREVIDENCE_ADDRESSED = YES
BOUNDARY_OF_INFERENCE_DECLARED = YES
DIRECT_NETWORK_CROSSCHECKED = YES
```

وإلا:

`REVERSE_INFERENCE = UNRESOLVED`

---

# 26. بوابات خاصة حسب نوع الادعاء

## 26.1. ادعاء ثنائية كاملة

يلزم:

```text
THIRD_TERM_SEARCH_SUFFICIENT = YES
MUTUAL_EXCLUSION_ESTABLISHED = YES
SCOPE_FULLY_DEFINED = YES
```

---

## 26.2. ادعاء غياب

يلزم:

```text
FULL_RELEVANT_COVERAGE = YES
```

---

## 26.3. ادعاء تقابل معجمي عام

داخل Blind Lab لا تستخدم المعجم.

يلزم قرآنيًا:
- ثبات المجال.
- تكرار عابر للسياقات.
- محور مستقر.
- عدم اعتماد العلاقة على تركيب محلي واحد.

ثم يمكن بعد القفل إجراء مقارنة معجمية خارجية.

---

## 26.4. ادعاء عكس حالة

يلزم:
- حالة قبل.
- علامة انتقال.
- حالة بعد.
- ضبط المجال.

---

# 27. التكامل مع `ROOT_UNITY_PRINCIPLE`

## 27.1. الوظيفة

Reverse لا يقرر أن للجذر أكثر من أصل.

بل يستخدم لتقييد مرشح:

`ROOT_AXIAL_MEANING`

---

## 27.2. الأسئلة

إذا اقترحنا نواة X:

1. ما المقابل أو المعكوس الذي تتنبأ به X؟
2. هل يظهر هذا المحور في عدة مشتقات؟
3. هل الطرف المقابل يميز الجذر عن جذر قريب؟
4. هل الاستعمالات الصعبة تبقى قابلة للاشتقاق؟
5. هل النواة ضرورية أم مجرد وصف عام؟

ثم تطبق:

- `DERIVATIONAL_EXPLAINABILITY_TEST`
- `CORE_NECESSITY_TEST`
- `CORE_DISTINCTIVENESS_TEST`

---

## 27.3. القاعدة

> **Reverse يضيّق النواة ويختبرها، لكنه لا يحل محل شبكة الجذر.**

---

# 28. التكامل مع `LAYER_ATTRIBUTION_PASS`

كل فرق مكتشف يجب إسناده إلى الطبقة الصحيحة:

```text
ROOT?
DERIVATION?
FORM?
CONSTRUCTION?
PARTICIPANTS?
CONTEXT?
DISCOURSE?
```

إذا كان الفرق بين A وB ناتجًا عن:
- حرف جر.
- فاعل.
- مفعول.
- سياق.

فلا يُرفع تلقائيًا إلى Root أو Lexeme.

---

# 29. التكامل مع `PURPOSE_FUNCTION_OUTCOME_PASS`

لا تستخدم النتائج المعكوسة لصناعة مقصد.

```text
OPPOSITE_OUTCOME
≠
EXPLICIT_PURPOSE
```

وقد يكشف Reverse:
- وظيفة.
- حدًا.
- نتيجة.

لكن الغاية تحتاج دليلها المستقل.

---

# 30. التكامل مع `TEXTUAL_SILENCE_GATE`

إذا كشف Reverse أن تفصيلًا لا يظهر:

لا تقل:
> النص فوّضه للبشر.

إلا بعد:
1. إثبات `NOT_SPECIFIED`.
2. فحص النطاق.
3. تطبيق `SILENCE_OPEN_SPACE_GATE`.

---

# 31. المثال الأول — «لَتُبَيِّنُنَّهُ / وَلَا تَكْتُمُونَهُ»

## 31.1. الشاهد

آل عمران 187:

> **﴿لَتُبَيِّنُنَّهُ لِلنَّاسِ وَلَا تَكْتُمُونَهُ﴾**

---

## 31.2. ما نلاحظه مباشرة

- فعلان يتعلقان بشيء واحد في السياق.
- الأول مرتبط بـ«للناس».
- الثاني منفي/منهي عنه في العهد المذكور.
- البنية تجمع الفعلين في موضع واحد.

---

## 31.3. التصنيف

`CONTEXTUAL_FUNCTIONAL_CONTRAST`

وليس مطلوبًا داخل Blind Lab تسميته `LEXICAL_ANTONYMY`.

---

## 31.4. المجال والمحور

```text
SHARED_DOMAIN =
التعامل مع ما أُخذ الميثاق بشأن إظهاره للناس في السياق

CONTRAST_AXIS =
إظهار/بيان ↔ كتمان

BOUNDARY =
التقابل يثبت محورًا سياقيًا في كيفية التعامل مع الشيء محل البيان
```

---

## 31.5. ما لا يثبته

لا يثبت وحده:
- كامل معنى **ب ي ن**.
- كامل معنى **ك ت م**.
- أن كل عدم بيان هو كتمان.
- أن كل كتمان هو النقيض المعجمي الوحيد للبيان.

---

# 32. المثال الثاني — «حُرُم / حللتم»

## 32.1. التصنيف

`REVERSIVE_TRANSITION`

---

## 32.2. المجال

في شبكة المائدة ذات الصلة بالصيد:

```text
PRE/ACTIVE_STATE =
وأنتم حُرُم

TRANSITION =
إذا حللتم

POST_TRANSITION_EFFECT =
فاصطادوا
```

---

## 32.3. الاستنتاج العكسي

```text
CONTRAST_AXIS =
قيد مرتبط بالحالة ↔ زوال ذلك القيد

REVERSE_INFORMATION =
«حللتم» يكشف أن حالة «حُرُم» ليست وصفًا ساكنًا فقط، بل حالة يمكن الخروج منها ويتغير معها حكم الصيد في السياق.
```

---

## 32.4. ما لا يثبته

لا يثبت وحده:
- أن كل معنى ح ر م = تقييد الصيد.
- أن «الحل» هو الضد المعجمي لكل مشتقات ح ر م.
- كامل تعريف «الحرمة».

بل يعاد إلى:
- البيت الحرام.
- الشهر الحرام.
- حرمات الله.
- حرّم.
- محروم.
- بقية الاستعمالات.

---

# 33. المثال الثالث — `خير / شر`

في بنية الزلزلة 7–8:

```text
مِثْقَالَ ذَرَّةٍ خَيْرًا
مِثْقَالَ ذَرَّةٍ شَرًّا
```

## 33.1. ما تكشفه البنية

- تركيب متوازٍ جدًا.
- نفس الفعل.
- نفس المقدار.
- المتغير هو `خير / شر`.

هذا يجعل الزوج مفيدًا لاستخراج **محور قطبي** في ذلك الموضع.

## 33.2. ما لا نستنتجه

لا نعرّف كل «خير» في القرآن بأنه:
> «ما ليس شرًا».

بل نستخدم المحور في اختبار شبكة «خير» و«شر» الأوسع.

---

# 34. صيغة المخرج المختصر

عند استخدام Reverse في جواب للمستخدم، لا تعرض كل البروتوكول.

استخدم:

```text
REVERSE_FINDING

1. العلاقة المرشحة:
2. نوعها:
3. الشاهد:
4. المجال المشترك/المرتبط:
5. محور الاختلاف أو العكس:
6. ما تكشفه عن معنى الهدف:
7. ما لا تثبته:
8. أقوى بديل/طرف ثالث:
9. Counterevidence:
10. الحالة:
```

---

# 35. صيغة البحث العميق

```text
[REVERSE_ANALYSIS_BLOCK]

TARGET =
QUESTION =
FAMILY =
SUBTYPE =
CLAIM_SCOPE =

PRIMARY_WITNESS =
CROSS_CONTEXT_WITNESSES =

SHARED_DOMAIN =
INVARIANT_FEATURES =
CHANGING_FEATURE =
CONTRAST_AXIS =

PARTICIPANT_CONTROL =
CONSTRUCTION_CONTROL =
NEGATION_SCOPE =
BINARY_STATUS =
SYMMETRY =

THIRD_TERM_RESULT =
NEAR_NEIGHBOR_RESULT =
COUNTERFACTUAL_RESULT =
NEGATIVE_DISTRIBUTION_RESULT =
OUTCOME_RESULT =

SUPPORTING_EVIDENCE =
COUNTEREVIDENCE =
ALTERNATIVES =

REVERSE_INFORMATION =
BOUNDARY_OF_INFERENCE =
DOES_NOT_PROVE =

DIRECT_MODEL_CROSSCHECK =
ROOT_MODEL_IMPACT =

RESULT_STRENGTH =
RESEARCH_COMPLETENESS =
INDEPENDENT_VERIFICATION =

STATUS =
REOPEN_IF =
```

---

# 36. `REVERSE_PRE_OUTPUT_GATE`

قبل إخراج نتيجة Reverse:

```text
TARGETS_VERIFIED =
DOMAIN_ESTABLISHED =
RELATION_CLASSIFIED =
NEGATION_SCOPE_SAFE =
PARTICIPANTS_CONTROLLED =
CONSTRUCTION_CONTROLLED =
NO_FALSE_BINARY =
THIRD_TERM_CHECKED =
NO_OUTCOME_TO_MEANING_LEAP =
NO_ABSENCE_TO_NEGATION_LEAP =
NO_GRAMMAR_TO_SEMANTICS_LEAP =
DIRECT_NETWORK_CROSSCHECKED =
COUNTEREVIDENCE_ADDRESSED =
BOUNDARY_DECLARED =
THREE_AXIS_REPORTED =
```

إذا فشل عنصر حاسم:
`NARROW / UNRESOLVED / REJECT`

---

# 37. `REVERSE_REGRESSION_SUITE`

يجب اختبار الملحق دوريًا على حالات مصممة لإسقاطه:

1. كلمتان في آية واحدة لكن بلا تقابل.
2. تضاد متدرج مع حالة وسط.
3. نفي لا ينتج مقابله.
4. نتيجة معكوسة سببها عامل ثالث.
5. استثناء ليس تضادًا.
6. corpus جزئي مع ادعاء «لا يرد».
7. طرف ثالث يهدم الثنائية.
8. فرق ناشئ من المشاركين لا اللفظ.
9. فرق ناشئ من حرف الجر لا الجذر.
10. مقابل جلبه معجم خارجي قبل Blind Lock.
11. استبدال افتراضي غير عربي/غير محتمل.
12. Root Core يبدو صالحًا بسبب الضد لكنه يفشل في مشتق صعب.
13. نفس الزوج يتقابل في سياق ويجتمع بلا تقابل في سياق آخر.
14. `NOT(A)` و`B` غير متكافئين.
15. نموذج يرفض قول `NO_DIFFERENCE_ESTABLISHED`.
16. غياب تفصيل يُحوّل خطأ إلى `TEXTUAL_OPEN_SPACE`.

---



# 39. القواعد الذهبية الاثنتا عشرة

> **1. Reverse يكشف الحد ولا يعرّف وحده.**

> **2. لا تقابل بلا مجال مشترك أو علاقة قابلة للمقارنة.**

> **3. النفي ليس ضدًا تلقائيًا.**

> **4. الغياب ليس نفيًا.**

> **5. اختلاف النتائج لا يثبت اختلاف المعاني.**

> **6. الاستثناء يحدد نطاقًا قبل أن يثبت تقابلًا.**

> **7. ابحث عن الطرف الثالث قبل إعلان الثنائية.**

> **8. الضد يختبر الحد البعيد، والجار يختبر الحد القريب.**

> **9. لا ترفع فرق السياق أو المشاركين إلى الجذر.**

> **10. لا تستعمل معجمًا خارجيًا لتوليد الضد داخل Blind Lab.**

> **11. كل نتيجة Reverse يجب أن تعود إلى شبكة الاستعمال المباشر.**

> **12. إذا لم تصمد العلاقة، فـ`NO_RELATION_ESTABLISHED` أو `UNRESOLVED` نتيجة صحيحة.**

---

# 40. القاعدة الجامعة

> **لا تسأل فقط: «ماذا يعني اللفظ حين يحضر؟» بل اسأل أيضًا: ما الذي يتغير عندما يُنفى، أو يُقابل، أو تُرفع حالته، أو يُستثنى منه، أو يُستبدل، أو تنعكس نتائجه، أو يغيب حيث كان متوقعًا؟ ثم لا تجعل أي جواب من هذه الأجوبة تعريفًا مستقلًا؛ بل استخدمه قيدًا يعود إلى شبكة الاستعمال ليختبر المعنى المباشر ويحدد حدوده.**

---

# 41. صيغة التفعيل داخل Quran Lisan

أضف إلى `MODULE_ROUTER` في Quran Lisan v1.1:

```text
REVERSE_PASS = AUTO

ACTIVATE_IF:
  comparison
  opposition
  negation
  exception
  state_reversal
  outcome_inversion
  counterfactual_substitution
  negative_distribution
  absence_claim
  root_distinctiveness_test
```

وأضف إلى `PRE_OUTPUT_VERIFICATION_GATE`:

```text
IF REVERSE_PASS = ON:
  REVERSE_PRE_OUTPUT_GATE = REQUIRED
```

---

# 42. صيغة الحفظ

```text
[LISAN_REVERSE_SAVE_BLOCK]

VERSION = QURAN_LISAN_V1.1_A09
BASE_PROTOCOL = QURAN_LISAN_V1.1

TARGET =
QUESTION =
REVERSE_FAMILY =
SUBTYPE =
CLAIM_SCOPE =

PRIMARY_WITNESS =
SHARED_DOMAIN =
CONTRAST_OR_BOUNDARY_AXIS =

PARTICIPANT_CONTROL =
CONSTRUCTION_CONTROL =
THIRD_TERM_RESULT =
NEAR_NEIGHBOR_RESULT =
COUNTERFACTUAL_RESULT =
NEGATIVE_DISTRIBUTION_RESULT =

SUPPORTING_EVIDENCE =
COUNTEREVIDENCE =
ALTERNATIVES =

REVERSE_INFORMATION =
BOUNDARY_OF_INFERENCE =
DOES_NOT_PROVE =

DIRECT_MODEL_CROSSCHECK =
ROOT_MODEL_IMPACT =

RESULT_STRENGTH =
RESEARCH_COMPLETENESS =
INDEPENDENT_VERIFICATION =

STATUS =
REOPEN_IF =
SOURCE_CHECKPOINT =
```

---

# 43. الحكم النهائي للملحق

`QURAN_LISAN_V1.1_A09` لا ينافس التحليل المباشر، بل يكمله.

المسار الكامل:

```text
DIRECT QURANIC USAGE
→ OBSERVATION
→ SEMANTIC MODEL CANDIDATE
→ REVERSE PASS
   ├─ opposition
   ├─ negation
   ├─ reversal
   ├─ exception
   ├─ outcome inversion
   ├─ substitution
   ├─ negative distribution
   └─ third-term / neighbor tests
→ BOUNDARIES DISCOVERED
→ DIRECT NETWORK CROSSCHECK
→ COUNTEREVIDENCE
→ FALSIFICATION
→ REFINED SEMANTIC MODEL
→ THREE-AXIS EPISTEMIC REPORT
```

والقاعدة الأخيرة:

> **المعنى الأقوى ليس الذي يجد له مرادفًا، بل الذي يستطيع أن يفسر حضور اللفظ وحدوده، وما يقابله، وما لا يقابله، وما يتغير عند نفيه أو رفع حالته، وما يبقى ثابتًا عبر تلك التحولات، دون أن يتجاوز ما يسمح به النص.**

---

**`END_OF_QURAN_LISAN_V1.1_A09`**

---

## نهاية الملحق

```text
INTEGRATION_RULES = M01 Reverse principle + A02/A03/A04/A05
OUTPUT_CONTRACT = REVERSE_FINDING / REVERSE_ANALYSIS_BLOCK
FAILURE_MODES = false antonym/binary, negation-scope, outcome-as-meaning, partial-corpus absence
REGRESSION_CASES = legacy-derived regression suite + T01 reverse cases
REOPEN_IF = new counterexample/third term/domain or construction change
END_OF_APPENDIX = A09
```
