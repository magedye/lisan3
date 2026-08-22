> [!WARNING]
> **SUPERSEDED/MIGRATED**
> This document has been migrated to `skills/lisan-semantic-extraction/SKILL.md`. See `docs/migration/SEMANTIC_SKILL_MIGRATION_DISPOSITION.md`.

# Skill: Lisan Quranic Semantic Extraction — Executive Protocol

**Version:** 9.1.0 (Final - Refined)
**Architecture:** Dynamic Authority-Driven & Epistemically Constrained
**Type:** Runtime Kernel for AI Agent

---

## 0. Meta-Rules & System Handshake

### 0.1 AUTHORITY_PREFLIGHT (التحقق المبدئي من السلطة)

قبل الشروع في أي تحليل، **MUST** يحدد الوكيل:

1. **TARGET_CONTRACT:** ما هو العقد المطلوب؟
   - `ROOT_CORE` | `LEXEME` | `FORM` | `CONSTRUCTION` | `LOCAL_MEANING` | `CONCEPT_MODEL`
   - **يُمنع** استخراج `ROOT_CORE` إذا كان العقد يطلب معنى موضعياً، والعكس صحيح.

2. **CANONICAL_PROFILE:** تحديد المرجع القرآني القانوني (مثل: `HAFS_ASIM_MADINAH_TANZIL_UTHMANI_1.1`).

3. **Status Registry:** استدعاء الحالات الرسمية من المصدر المعتمد. يُحظر اختراع حالات وسيطة (`PROVISIONAL_STABLE` ممنوع ما لم يثبت رسمياً).

4. **Source Role Policy:** تحديد دور المصادر الخارجية (المعاجم، الشعر، التفسير) وفق سياسة المشروع. المصادر الخارجية **ليست نقطة انطلاق**، بل أدوات اختبار مساعدة تخدم Corpus الحاكم.

### 0.2 Epistemic Hierarchy (التسلسل المعرفي الإلزامي)

يُلزم الوكيل بوسم مراحل تفكيره الداخلي، ولا يُسمح بالقفز بين الطبقات دون دليل:

```
OBSERVATION (ملاحظة بنيوية/توزيعية)
    ↓
CONSTRAINT (قيد نصي - ما لا يمكن أن يكون)
    ↓
HYPOTHESIS (فرضية قابلة للاختبار)
    ↓
INFERENCE (استدلال مبدئي)
    ↓
RESULT (نتيجة اجتازت بوابات الاختبار)
```

---

## 1. Core Constitutional Directives (القواعد الدستورية الحاكمة)

1. **Corpus Supremacy (سيادة النص):** القرآن الكريم هو الـ Corpus الحاكم والأساسي. المعاجم والمصادر الخارجية هي `AUXILIARY` وتُستخدم للاختبار والمقارنة، ولا تُتخذ نقطة انطلاق.

2. **Strict Layer Separation (الفصل الطبقي):**

   ```text
   LOCAL MEANING = ROOT CONTRIBUTION + FORM CONTRIBUTION + CONSTRUCTION CONTRIBUTION + PARTICIPANT ROLES + CONTEXTUAL EFFECT
   ```

   يُحظر إسناد أثر ناتج عن السياق أو الوزن الصرفي إلى النواة الجذرية.

3. **Epistemic Honesty (النزاهة المعرفية):** الحالات `LOCK_BLOCKED` و `SPARSE_EVIDENCE_CEILING` هي نتائج علمية ناجحة ومطلوبة عند تعذر الأدلة. يُحظر اختلاق المعاني لسد الفجوات.

4. **Anti-Circularity (حظر الاستدلال الدائري):** يُحظر:
   - افتراض معنى مسبق → تفسير الآيات بناءً عليه → استخدام الآيات المُفسَّرة كدليل لإثبات المعنى المسبق.
   - اختيار الجيران بناءً على التعريف المقترح → إثبات التعريف لأنه يختلف عن الجيران الذين اختيروا بناءً عليه.

---

## 2. Definitions & Key Terms

| Term (EN) | Term (AR) | Meaning |
| :--- | :--- | :--- |
| **Root Core** | `النواة الجذرية` | The minimal invariant semantic structure shared by all occurrences after stripping morphology and context |
| **Distinctive Residue** | `البقية المميزة` | Positive semantic feature(s) that differentiate the root from nearest neighbors |
| **Rejection Condition** | `شرط النقض` | Specific evidence that would invalidate the proposed Root Core |
| **Root Definition** | `التعريف الجذري` | Shortest, precise articulation of the Root Core |
| **Root Meaning** | `المعنى الجذري` | Explanatory elaboration clarifying perspective and focus |
| **Root Concept** | `المفهوم الجذري` | Broader conceptual structure (actors, relations, transformation) |
| **Local Meaning** | `المعنى الموضعي` | Specific interpretation in a specific verse (Form + Construction + Context) |

---

## 3. Multi-Dimensional Coverage (التغطية متعددة الأبعاد)

لا يُكتفى بحصر المواضع. **MUST** يُفصل تقييم التغطية إلى أبعاد:

| البعد | التعريف |
| :--- | :--- |
| `INDEX_COVERAGE` | حصر جميع المواضع والصيغ المستخرجة |
| `DEEP_ANALYSIS_COVERAGE` | المواضع التي خضعت فعلياً للتحليل الطبقي العميق |
| `FORM_COVERAGE` | الصيغ الصرفية الممثلة |
| `CONSTRUCTION_COVERAGE` | التراكيب النحوية الممثلة |
| `CONTEXT_DIVERSITY` | تنوع المجالات السياقية |
| `NEIGHBOR_COVERAGE` | الجيران الدلاليين الذين تمت مقارنتهم فعلياً |
| `UNRESOLVED_ITEMS` | الشواهد الشاذة أو المعارضة التي لم تُحسم |

**قاعدة:** لا يُسمح بمساواة `COLLECTED = ANALYZED = VALIDATED`. الفجوات يجب أن تُصرّح وتُؤثر في الحالة.

### التعامل مع الجذور كبيرة الحجم (Large Roots)

في الجذور التي تتجاوز 30 موضعاً، يُكتفى بـ `INDEX_COVERAGE` الكامل + عينة متنوعة للتحليل العميق، مع توثيق:
- معيار اختيار العينة.
- ما استُثني ولماذا.
- هل العينة تغطي التنوع السياقي والصرفي؟

---

## 4. Homonymy & Lexical Split (المشترك اللفظي والتشعب)

يُحظر فرض "وحدة مصطنعة" (Forced Unification).

إذا ظهرت إحدى الحالات التالية:
- `Homonymy`: تباين جذري بين الفروع لا يمكن جمعه في نواة واحدة.
- `Lexical Split`: تشعب دلالي واضح.
- `Root Identity Ambiguity`: شك في هوية الجذر.

**إجراء المطلوب:**
- تضييق `SCOPE` إلى فرع واحد.
- حفظ فرضيات متعددة (`H1`, `H2`, `C0`) وعزل أدلة كل نواة عن الأخرى.
- منع القفل (`LOCK_BLOCKED`) حتى يُحسم التباين أو يُقبل التعدد.

---

## 5. Advanced Analytical Protocols

### 5.1 Root Core Extraction

النواة الجذرية ليست:
- مرادفاً معجمياً سريعاً.
- معنى أشهر آية.
- نتيجة السياق أو الحكم الفقهي.
- قاسماً عاماً من نوع "حركة" أو "تغير" أو "علاقة".
- تركيباً بلاغياً جميلاً.

بل هي: **أصغر Claim دلالية موجبة يمكن إثباتها وتمييزها واختبارها ضمن Scope معلوم، ومميزة عن الجيران الأساسيين.**

### 5.2 Distinctive Residue (البقية المميزة)

السؤال الحاكم ليس فقط:
> "هل التعريف يغطي المواضع؟"

بل:
> "لماذا هذا الجذر تحديداً وليس جاره؟"

**قاعدة:** لا يُفرض عدد ثابت للجيران؛ المطلوب هم **الجيران الحاسمون لاختبار الادعاء** (`ESSENTIAL_NEIGHBORS`). الجيران التجميليون لا يُطلبون.

### 5.3 Differentiation Axes (محاور التفريد)

تُفعّل بحسب الحاجة، ولا تُطبق كلها إجبارياً:

| المحور | السؤال |
| :--- | :--- |
| `Event Type` | فعل، حالة، تحول، تحصيل، إزالة، إدراك؟ |
| `Agency` | يتطلب فاعلاً واعياً؟ |
| `Intentionality` | القصد جزء من الدلالة أم سياق؟ |
| `Participant Structure` | ما الأطراف التي يقبلها؟ |
| `Directionality` | انتقال، قرب، بعد، علو، سفل؟ |
| `Aspect/Phase` | بدء، استمرار، اكتمال، نتيجة؟ |
| `Result/Effect` | ما الأثر على الفاعل أو المفعول؟ |
| `Affected Entity` | ماذا يتغير في الشيء الواقع عليه الحدث؟ |
| `Syntax` | حروف الجر، التعدية، البناء؟ |
| `Morphological Distribution` | هل الخاصية ثابتة عبر الصيغ؟ |
| `Contextual Distribution` | أين يظهر اللفظ في القرآن؟ |
| `Collocation` | ما المصاحبات المتكررة؟ |
| `Scalarity/Intensity` | درجة، شدة، تكرار؟ |
| `Temporal Profile` | زمن الحدث؟ |

**قاعدة:** لا يُسمح باختراع فرق في محور لا يملك Evidence من Corpus.

### 5.4 Falsification (التكذيب)

كل فرضية يراد رفعها إلى `Claim` **MUST** تحتوي:

- `REJECTION_CONDITION`: شرط نصي دقيق لو تحقق يُسقط الفرضية.
- `SUPPORTING_EVIDENCE`: الشواهد المؤيدة.
- `COUNTEREVIDENCE`: الشواهد المعارضة أو المقاومة.
- `UNRESOLVED_CASES`: الحالات التي لم تُحسم.
- `FAILED_PREDICTIONS`: إن وجدت.

**ممنوع:** شرط دائري مثل:
> "نرفضها إذا ثبت أنها خاطئة."

بل الصحيح:
> "تُرفض الفرضية إذا ورد الجذر في آية تدل على [معنى محدد]."

---

## 6. Locking & Status Management

### 6.1 Official Statuses (الحالات الرسمية)

يجب استيراد الحالات من `official_statuses_ref`. فيما يلي القائمة المعتمدة حالياً (تخضع للتحقق من Authority النشطة):

| Status | When to Use |
| :--- | :--- |
| `UNKNOWN` | لم يبدأ التحليل، أو لا توجد بيانات كافية |
| `CANDIDATE_HYPOTHESIS` | فرضية قيد الاختبار، لم تستوفِ معايير القفل بالكامل |
| `SPARSE_EVIDENCE_CEILING` | الجذر يرد 1-2 مرة، لا يمكن استخلاص نواة مميزة دون الاعتماد المفرط على الخارج |
| `LOCK_BLOCKED` | **نتيجة منهجية صحيحة**: تعارض، فشل تفريد، شاهد معارض غير محلول، أو جار أساسي غير محسوم |
| `LOCK_INTERNAL_RESULT` | اجتازت جميع معايير القفل داخلياً |
| `REVALIDATION_REQUIRED` | نتيجة سابقة تأثرت بأدلة أو سياسات جديدة |

### 6.2 Lock Gate Criteria (معايير القفل)

القفل (`LOCK_INTERNAL_RESULT`) يتطلب تحقيق **جميع** المعايير التالية:

| المعيار | المطلوب |
| :--- | :--- |
| `SCOPE_STABILITY` | Scope واضح ومستقر |
| `COVERAGE` | تغطية مناسبة مع فجوات معلنة |
| `INVARIANCE` | الثابت لا يتغير بتغير المجال أو المشاركين |
| `LAYER_NEUTRALITY` | لا يبتلع مساهمة الصيغة أو السياق |
| `POSITIVE_CONTENT` | يذكر ما هي النواة، لا ما ليست عليه فقط |
| `DISTINCTIVENESS` | بقية موجبة أمام الجيران الأساسيين |
| `FALSIFIABILITY` | شرط نقض حقيقي |
| `PREDICTIVE_CONTENT` | اختبار تنبؤي غير دائري |
| `COUNTEREVIDENCE_HANDLING` | أقوى Counterevidence عُولج بصدق |
| `TRACEABILITY` | الأدلة والاعتماديات قابلة للحل |
| `NON_CIRCULARITY` | لا يعتمد على تعريف مفترض أو مرادف غير مستقرأ |

فشل معيار حاسم **لا يُعالج بزيادة الثقة أو تحسين الصياغة**.

---

## 7. Tooling & Fallback Strategy (الأدوات والتدهور)

- **What it proves vs. What it doesn't:** نجاح Validator صرفي/بنيوي يُثبت صحة البنية، **لا** يُثبت صحة الادعاء الدلالي للـ Root Core.
- **إذا كانت الأداة موجودة فعلاً**:
  - شغّلها، وسجل نتيجتها.
  - لا تدعِ أكثر مما تختبره.
- **إذا لم تكن الأداة موجودة**:
  - **ممنوع** القول: `VALIDATOR_PASSED`.
  - سجل `TOOL_UNAVAILABLE / NOT_VERIFIED`.
  - استخدم `FALLBACK` إن كان مصرحاً به صراحة في سياسة المشروع.
  - وإلا خفّض حالة الثقة أو امنع القفل.

**قاعدة ذهبية:** المحاكاة الداخلية لمنطق Validator هي للتفكير فقط، وليست Verification.

---

## 8. Operational Workflow (مسار العمل التنفيذي)

| المرحلة | الإجراء |
| :--- | :--- |
| **Phase 0: Handshake** | `AUTHORITY_PREFLIGHT` + تحديد `TARGET_CONTRACT` + تحميل الحالات وسياسة المصادر |
| **Phase 1: Corpus & Coverage** | فهرسة شاملة + تقييم الأبعاد السبعة للـ Coverage |
| **Phase 2: Structural Observation** | فصل الصرف، التركيب، المشاركين، السياقات دون إسقاطات دلالية |
| **Phase 3: Hypothesis Generation** | توليد `H1` (المرشحة)، `H2` (البديلة)، `C0` (الصفرية / لا نواة مميزة مؤهلة) |
| **Phase 4: Differentiation & Falsification** | تحديد `ESSENTIAL_NEIGHBORS` + تطبيق اختبارات الاستبدال والحدود + استخراج `DISTINCTIVE_RESIDUE` + البحث عن Counterevidence + صياغة `REJECTION_CONDITION` |
| **Phase 5: Locking & Dependency** | تطبيق Lock Gate + تعيين الحالة الرسمية + تسجيل الاعتماديات في `DEPENDENCY_LEDGER` (إن وُجد) |

---

## 9. Adversarial Pre-Delivery Check (قائمة التحقق العدائية)

**MUST** يمرر الوكيل هذه القائمة داخلياً قبل إصدار المخرج النهائي. إذا كانت الإجابة "نعم" لأي بند، يُلغى المخرج وتُعاد مراجعة التحليل:

| # | السؤال |
| :--- | :--- |
| 1 | هل بدأت التحليل بنسخ تعريف معجمي ثم بحثت له عن تأييد قرآني؟ |
| 2 | هل نسبت أثراً بلاغياً أو صرفياً إلى النواة الجذرية لتسهيل إثباتها؟ |
| 3 | هل اختلقت فرقاً بين الجيران بلا دليل موضوعي أو اختبار استبدال حقيقي؟ |
| 4 | هل عومل `LOCK_BLOCKED` كفشل، وحُولت الفرضية بالقوة لإرضاء الطلب؟ |
| 5 | هل تجاهلت `Counterexample` (شاهد معارض) أو خففت من شأنه لتمرير النتيجة؟ |
| 6 | هل التعريف المولد (Generic) فضفاض لدرجة انطباقه على عشرات الجذور الأخرى؟ |
| 7 | هل استخدمت دلالات الحروف أو حروف العطف كدليل استدلالي موجب ووحيد؟ |
| 8 | هل حولت غياب الشاهد عن السياق إلى حظر دلالي (`EXCLUDED`) بدلاً من (`UNKNOWN`)؟ |
| 9 | هل الادعاء الدلالي أوسع بكثير من نطاق التغطية (Coverage) المثبتة فعلياً؟ |
| 10 | هل اعتمدت تعريفاً جديداً لمجرد أن القديم نُقد، دون إعادة اختبار البديل؟ |
| 11 | هل تحول `ROOT_CORE_EXPLANATION` إلى Claim مستقلة غير مثبتة؟ |

---

## 10. Discovery vs Presentation (الاكتشاف مقابل العرض)

### Discovery Path (مسار البحث الداخلي)
```
Authority → Corpus → Observations → Classification → Hypotheses → Neighbors → Tests → Counterevidence → Validation → Lock/Block
```

### Presentation Path (مسار العرض النهائي)
```
Definition → Meaning → Concept → Distinctive Residue → Neighbors → Boundaries → Realizations → Evidence → Status
```

**قاعدة:** لا يُعرض سجل الاكتشاف كجواب نهائي. الجواب النهائي هو Artifact مصقول.

---

## 11. Presentation Schema (قالب العرض المعياري)

**يُخرج الوكيل النتيجة النهائية ملتزماً حرفياً بهذا القالب.**

في حالات المنع (`LOCK_BLOCKED` أو `SPARSE_EVIDENCE_CEILING`)، تُترك الحقول الدلالية فارغة وتُشرح أسباب المنع بالتفصيل.

```yaml
TARGET: "{الجذر / اللفظ}"
CONTRACT_TYPE: "[ROOT_CORE | LOCAL_MEANING | ...]"
OFFICIAL_STATUS: "[يُستدعى ديناميكياً من Registry المعتمد]"
CONFIDENCE: "[LOW | MODERATE | HIGH | UNRESOLVED]"

COVERAGE_PROFILE:
  INDEX_COVERAGE: "[العدد والصيغ المستخرجة]"
  DEEP_ANALYSIS_COVERAGE: "[نطاق التحليل الفعلي]"
  FORM_COVERAGE: "[الصيغ الممثلة]"
  CONSTRUCTION_COVERAGE: "[التراكيب الممثلة]"
  CONTEXT_DIVERSITY: "[وصف المجالات السياقية]"
  NEIGHBOR_COVERAGE: "[الجيران الذين تمت مقارنتهم]"
  UNRESOLVED_ITEMS: "[الشواهد الشاذة أو المعارضة]"

ABSTRACT_ROOT_CORE:
  "[أقل بنية مفهومية موجبة، مجردة من الوزن والسياق، وقابلة للتكذيب]"

ROOT_DEFINITION:
  "[أقصر صياغة دقيقة للنواة المثبتة]"

ROOT_MEANING:
  "[شرح زاوية الدلالة ومركز الثقل]"

ROOT_CONCEPT:
  "[البنية التصورية والعلاقات والثابت والمتغير]"

DISTINCTIVE_RESIDUE_AND_NEIGHBORS:
  SHARED_DOMAIN: "[المجال الدلالي المشترك]"
  vs_{الجار الأول}: "[الفرق الموجب المثبت]"
  vs_{الجار الثاني}: "[الفرق الموجب المثبت]"
  STATUS: "[حالة التفريد: RESOLVED | UNRESOLVED | PARTIAL]"

LAYER_SEPARATION:
  ROOT_CONTRIBUTION: "[ما يثبت يقيناً للجذر]"
  FORM_CONTRIBUTION: "[ما يُسند للوزن الصرفي]"
  CONSTRUCTION_CONTRIBUTION: "[ما يُسند للتركيب]"
  CONTEXTUAL_EFFECT: "[ما يُسند للسياق]"
  UNRESOLVED_ASSIGNMENT: "[ما لم يُحسم إسناده]"

FALSIFICATION_AND_EVIDENCE:
  REJECTION_CONDITION: "[الشرط النصي الدقيق الذي يُسقط الفرضية]"
  SUPPORTING_EVIDENCE: "[الشواهد المؤيدة]"
  COUNTEREVIDENCE: "[الشواهد المعارضة أو المقاومة]"
  UNRESOLVED_CASES: "[ما لم يُحسم]"

DEPENDENCY_AND_SCOPE:
  VALIDATION_SCOPE: "[الحدود التي تنتهي عندها صلاحية هذا التحليل]"
  UPSTREAM_DEPENDENCIES: "[النتائج أو الجذور السابقة التي اعتمد عليها]"
  REOPEN_CONDITION: "[المعطى الذي يُجبر النظام على إعادة فتح هذا الملف مستقبلاً]"
```

**إذا لم تثبت النواة:** يستخدم `NOT_ESTABLISHED` أو الحالة الرسمية المناسبة، ولا يُملأ `ABSTRACT_ROOT_CORE` بصياغة توهم الحسم.

---

## 12. Prohibited Patterns (الأنماط الممنوعة)

| ID | النمط | التعريف |
| :--- | :--- | :--- |
| `PM-01` | Dictionary-First | البدء بالمعجم ثم البحث عن تأييد |
| `PM-02` | Contextual Leakage | إدخال نتيجة السياق في تعريف الجذر |
| `PM-03` | Circular Confirmation | افتراض المعنى → تفسير الآيات → إثبات المعنى من التفسير |
| `PM-04` | Untested Replacement | اعتماد بديل لمجرد نقد القديم |
| `PM-05` | Counterfactual-as-Proof | "لو كان X لقال Y" |
| `PM-06` | Structural Overpromotion | تحويل `و` / `أو` / `رفع` إلى تعريف موجب للجذر |
| `PM-07` | Root/Form Conflation | نسبة خاصية الوزن إلى الجذر |
| `PM-08` | Generic Overextraction | تعريف يصلح لعشرات الجذور |
| `PM-09` | Frame Preselection | افتراض محور (ارتفاع، حركة) قبل التحليل |
| `PM-10` | Avoiding Block | تجاوز `LOCK_BLOCKED` لملء الفراغ |
| `PM-11` | Overclaiming | "بالتأكيد"، "الحقيقة القطعية" دون Status مؤهل |
| `PM-12` | Forced Unification | توحيد فرضيتين متعارضتين قسراً |
| `PM-13` | Neighbor Cherry-Picking | اختيار جيران يخدمون الفرضية فقط |
| `PM-14` | Coverage Inflation | مساواة `COLLECTED = ANALYZED = VALIDATED` |
| `PM-15` | Tool Simulation as Evidence | محاكاة Validator ثم الادعاء بنجاحه |
| `PM-16` | Status Invention | اختراع حالة غير معتمدة |
| `PM-17` | Silencing Counterevidence | حذف أو تضعيف الشاهد المعارض |
| `PM-18` | Presentation-as-Proof | جعل العرض الأنيق دليلاً على الصحة |

---

## 13. Reference Architecture (الهيكلة المرجعية)

للبقاء خفيفاً وقابلاً للصيانة، تُبنى المهارة على هذه الهيكلية:

```text
/lisan-v9/
├── SKILL.md                     # (هذا الملف - Runtime Kernel)
├── references/
│   ├── authority_policy.md      # سياسة السلطة والمصادر
│   ├── epistemology_hierarchy.md # تفصيل التسلسل المعرفي
│   ├── differentiation_axes.md  # محاور التفريد الموسعة
│   ├── lock_gate_criteria.md    # معايير القفل مع أمثلة
│   ├── evidence_ledger_schema.md # سجل الأدلة والاعتماديات
│   └── open_authority_questions.md # أسئلة السلطة المفتوحة
├── templates/
│   ├── root_result.yaml         # قالب العرض النهائي
│   └── distinction_card.yaml    # بطاقة التفريد
└── validators/
    ├── behavioral_tests.md      # اختبارات سلوكية
    └── adversarial_fixtures.md  # Fixtures للتحدي
```

---

## 14. القاعدة الختامية (The Final Rule)

> **الهدف ليس استخراج تعريف بأي ثمن، بل إنتاج أصغر Claim دلالية يمكن تتبعها واختبارها وتمييزها والدفاع عنها ضمن نطاق معلوم، مع القدرة الصريحة على رفضها إذا خالفت الأدلة. وكلما ازدادت الأدلة قوة، ازدادت الثقة؛ وكلما تعذرت، توقف القفل دون ندم.**

---

**Version 9.1.0 — FINAL**  
