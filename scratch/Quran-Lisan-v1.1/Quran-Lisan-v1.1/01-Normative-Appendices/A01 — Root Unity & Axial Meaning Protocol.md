---
DOCUMENT_ID: A01
TITLE: "Root Unity & Axial Meaning Protocol"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "تعريف واختبار واعتماد المعنى المحوري الواحد للجذر القرآني."
SCOPE: "دراسات الجذر وكل ادعاء يرقّي معنى إلى مستوى ROOT."
ACTIVATION_CONDITION: "RESEARCH_TARGET=ROOT أو ادعاء ROOT_AXIAL_MEANING."
DEPENDS_ON: [M01, A02, A03, A04, A05]
EXPANDS_MASTER_SECTIONS: [M01-P03, M01-D01, M01-R05, M01-R06, M01-G01]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A01 — Root Unity & Axial Meaning Protocol

## 1. المبدأ والتعريف

#### A01-P01 — Root Unity
للجذر القرآني معنى محوري واحد يمثل الأصل/النواة/الأساس الدلالي، ويبقى حاضرًا وفاعلًا في جميع المشتقات والصيغ والاستعمالات. اختلاف السطح لا يبرر أصولًا متنافرة؛ بل يختبر أولًا أثر الاشتقاق والصيغة والتركيب والمشاركين والسياق والخطاب.

#### A01-D01 — ROOT_AXIAL_MEANING
`ROOT_AXIAL_MEANING` هو أقل بنية دلالية إيجابية، مشتركة، لازمة، مميزة، غير فارغة، قادرة على تفسير العائلة بعد فصل آثار الطبقات الأخرى.

`ALIASES = {الجذر الدلالي، الأصل، الأصل الدلالي، النواة، النواة الدلالية، الأساس، الأساس الدلالي، المعنى المحوري، المفهوم الجذري}`

`ROOT_LETTERS` = الحروف الجذرية، ولا تساوي المفهوم الدلالي.

#### A01-D02 — Root status
```text
ROOT_CORE_STATUS =
  CANDIDATE
  | PROVISIONAL
  | STRONGLY_SUPPORTED
  | UNRESOLVED
  | REJECTED
```
`STRONGLY_SUPPORTED` لا يعني حقيقة نهائية؛ بل اجتيازًا قويًا للبوابة ضمن coverage معلن.

#### A01-R01 — Local realization
```text
ROOT_AXIAL_MEANING
→ DERIVATIONAL_EFFECT
→ FORM_EFFECT
→ CONSTRUCTION_EFFECT
→ PARTICIPANT_EFFECT
→ CONTEXT/DISCOURSE_EFFECT
→ LOCAL_MEANING
```
أي فرق يمكن تفسيره بطبقة أدنى لا يُرفع إلى الجذر. [A02-G01]

## 2. Mental Activation Description

#### A01-R02 — Mental activation
بعد استقرار النواة يجوز وصفها بأنها التصور الأساسي المرتبط بالمادة قبل إضافات الاستعمال. هذا وصف phenomenological للنتيجة لا مصدر إثبات.

#### A01-T01 — Mental Activation Guard
إذا كان سبب قبول النواة «هذا أول ما يتبادر» دون corpus، فالنتيجة `REJECTED_AS_EVIDENCE`. يجوز للتبادر فقط إنشاء `CANDIDATE`.

#### A01-R03 — Anti-prior rule
التعليم، الاستعمال المعاصر، المعجم، والموروث قد تؤثر في التبادر. لذلك لا يدخل التبادر في وزن الإثبات إلا بقدر ما يعاد اختباره نصيًا.

## 3. Corpus prerequisites

#### A01-G01 — ROOT_AXIAL_MEANING_ACCEPTANCE_GATE
لا تنتقل الحالة إلى `STRONGLY_SUPPORTED` حتى تحقق الشروط الآتية أو يُسجل سبب صريح لعدم الانطباق. فشل شرط جوهري يعيد النواة إلى `PROVISIONAL/UNRESOLVED/REJECTED`.

### 3.1 سلامة corpus

#### A01-T02 — ROOT_IDENTITY_VERIFIED
**الاختبار:** تحقق من نسبة كل target إلى الجذر/lemma والصيغة وعدم خلط جذور أو homographs بنيويًا.  
**نجاح:** كل occurrence المستخدم في الإثبات له هوية متحققة أو مستبعد معلل.  
**فشل:** occurrence غير متحقق يسند claim جوهريًا.

#### A01-T03 — CORPUS_COVERAGE_SUFFICIENT
**الاختبار:** قارن `CLAIM_SCOPE` مع [A03-G01].  
**نجاح:** التغطية تكفي للادعاء ولا توجد كتلة غير محللة قد تقلب النتيجة.  
**فشل:** claim شامل من عينة سهلة أو indexed غير analyzed.

#### A01-T04 — FORM_AND_USAGE_DIVERSITY_COVERED
**الاختبار:** تغطية الصيغ، الأنواع الصرفية، التراكيب، المشاركين، المجالات، والاستعمالات النادرة.  
**نجاح:** لا تعتمد النواة على cluster واحد.  
**فشل:** غياب شكل أو مجال مادي من التحليل.

### 3.2 ماهية النواة

#### A01-T05 — POSITIVE_INVARIANT
النواة يجب أن تقول ما يوجد، لا أن تكون مجرد «ليس كذا».  
**نجاح:** خاصية إيجابية قابلة للرصد عبر الأسرة.  
**فشل:** تعريف سلبي أو دائري مثل «X هو ما ليس Y».

#### A01-T06 — UNIVERSAL_PRESENCE
**الاختبار:** لكل استعمال validated، حدد أين وكيف تعمل النواة.  
**نجاح:** حضور فعلي لا مجرد إمكانية لغوية لإقحام العبارة.  
**فشل:** استعمال صعب لا يظهر فيه core إلا بتأويل اعتباطي.

#### A01-T07 — NECESSITY
**الاختبار:** احذف النواة من تفسير occurrence؛ هل تفسره الصيغة/التركيب/السياق وحدها؟  
**نجاح:** إزالة النواة تفقد قيدًا لازمًا متكررًا.  
**فشل:** النواة زخرفية يمكن حذفها من كل التفسيرات.  
يرتبط بـ`CORE_NECESSITY_TEST`.

#### A01-T08 — DISTINCTIVENESS
**الاختبار:** قارن بأقرب الجذور/الألفاظ في المجال.  
**نجاح:** core يفسر فرقًا مستقرًا.  
**فشل:** تعريف يصلح لعدد كبير من الجذور بلا تمييز.  
يرتبط [A09-T08] بالحد البعيد وnear-neighbor.

#### A01-T09 — MINIMALITY
**الاختبار:** احذف كل مكوّن من تعريف core بالتتابع.  
**نجاح:** لا يبقى في التعريف إلا ما يلزم للتغطية والتمييز.  
**فشل:** تفاصيل سياقية أو نتائج أو مشاركون داخل core بلا ضرورة.

#### A01-T10 — NON_VACUITY
**الاختبار:** هل يمكن للنواة توليد توقعات أو استبعاد نماذج؟  
**نجاح:** لها محتوى falsifiable.  
**فشل:** صياغة عامة مثل «وجود علاقة ما/حصول شيء» لا تستبعد شيئًا.

### 3.3 القدرة التفسيرية

#### A01-T11 — DERIVATIONAL_EXPLAINABILITY
لكل موضع سجل مسار الاشتقاق.  
**نجاح:** يمكن تفسير local meaning عبر core + الطبقات دون قفزة غير معللة.  
**فشل:** يلزم معنى مستقل لا صلة له بالنواة أو مجاز ad hoc.  
الحالة الجزئية: `DERIVATION_PATH_STATUS = PARTIALLY_EXPLAINED`.

#### A01-T12 — LAYER_ATTRIBUTION_CLEAN
**الاختبار:** مرر الفرق عبر [A02-G01].  
**نجاح:** ما ينتمي للصيغة/التركيب/المشارك/السياق لا يُحمل على core.  
**فشل:** leakage من layer إلى root.

#### A01-T13 — CROSS_FORM_STABILITY
**الاختبار:** افحص الأفعال، الأسماء، المصادر، الصفات، والمشتقات ذات الصلة.  
**نجاح:** invariant يستمر رغم تغير form.  
**فشل:** core لا يعمل إلا في صيغة واحدة.

#### A01-T14 — CONTEXTUAL_ROBUSTNESS
**الاختبار:** افحص المجالات والسياقات المتباينة.  
**نجاح:** لا يتغير core بتغير story/law/argument/local discourse، وإن تغير realization.  
**فشل:** يحتاج تعريفًا جديدًا لكل domain.

### 3.4 الاختبار المعارض

#### A01-T15 — HARDEST_CASE_SURVIVAL
**الاختبار:** اختر أصعب occurrence قبل القفل.  
**نجاح:** يفسره النموذج بلا ترقيع جوهري.  
**فشل:** hard case يعارض core؛ لا يُعزل في sense جديد بلا برهان.

#### A01-T16 — COMPETING_CORE_TEST
**الاختبار:** صغ أفضل core منافس إن وجد وقارنه على التغطية والاقتصاد والتمييز.  
**نجاح:** المرشح يتفوق بالدليل، لا بالتفضيل.  
**فشل:** competitor يفسر corpus بالمثل أو أفضل؛ الحالة `PROVISIONAL/UNRESOLVED`.

#### A01-T17 — PREDICTIVE_POWER
**الاختبار:** جمّد core ثم اختبر holdout أو occurrence لم يدخل في بنائه.  
**نجاح:** توقع صحيح لمكونات أو حدود.  
**فشل:** لا يتنبأ بشيء أو يفشل بوضوح. [A05-G02]

#### A01-T18 — REVERSE_COHERENCE
**الاختبار:** اسأل ما الحدود/المقابلات التي يتنبأ بها core ثم اختبرها عبر [A09-G01].  
**نجاح:** Reverse يضيّق core أو يؤكده دون تعريفه وحده.  
**فشل:** core يستلزم binaries أو negation patterns لا تدعمها الشبكة.

#### A01-T19 — NO_CIRCULARITY
**الاختبار:** افحص graph الأدلة.  
**نجاح:** core مدعوم observations مستقلة، لا بإعادة قراءة الشواهد بمعناه ثم عدّها إثباتًا له.  
**فشل:** `CIRCULAR_CONFIRMATION`. [A04-F02]

## 4. أسلوب الحكم على البوابة

#### A01-R04 — Gate decision
```text
IF corpus_identity fails → BLOCKED/UNRESOLVED
IF positive/universal/necessity fails materially → REJECTED or UNRESOLVED
IF explanatory tests incomplete → PROVISIONAL
IF all material tests pass and counterevidence addressed → STRONGLY_SUPPORTED
```
لا تستخدم متوسطًا رقميًا لتعويض فشل جوهري.

#### A01-O01 — Root evidence card
```yaml
ROOT_RESEARCH:
  root_letters:
  root_axial_meaning:
  aliases_used: []
  coverage_profile:
  invariant_constraints: []
  derivational_paths: []
  hard_cases: []
  competing_cores: []
  reverse_constraints: []
  gate_results: {}
  counterevidence: []
  status:
  result_strength:
  research_completeness:
  independent_verification:
  reopen_if: []
```

## 4.5 التفريد والجيران وشرط النقض

#### A01-D03 — DISTINCTIVE_RESIDUE
`DISTINCTIVE_RESIDUE` هو أقل خاصية أو مجموعة خصائص دلالية **موجبة** تبقى بعد فصل أثر الصيغة والتركيب والمشاركين والسياق، وتفسر لماذا استُعمل هذا الجذر بدل أقرب جيرانه. هو اختبار لصلاحية `DISTINCTIVENESS` لا كيان دلالي مستقل ولا نواة ثانية.

شروطه: `POSITIVE + MINIMAL + ROOT_COMPATIBLE + LAYER_NEUTRAL + NEIGHBOR_DISCRIMINATING + FALSIFIABLE`.

#### A01-R06 — ESSENTIAL_NEIGHBORS
لا يفرض عدد ثابت للجيران. يصنف الجار إلى `ESSENTIAL_NEIGHBOR` إذا كان إسقاطه يجعل ادعاء التمييز غير مختبر. لكل جار حاسم يسجل: `SHARED_DOMAIN`, الخاصية المشتركة، الفرق الموجب، `LAYER_OF_DIFFERENCE`, الشاهد المميز، Counterevidence، وRejection Condition.

يمنع `NEIGHBOR_CHERRY_PICKING`: اختيار جيران سهلة وترك الجار الذي ينافس النواة فعليًا.

#### A01-T20 — OPERATIONAL_REJECTION_CONDITION
قبل ترقية النواة إلى `STRONGLY_SUPPORTED` يجب أن يكون لها شرط نقض تشغيلي وفق [A05-G04]. يجب أن يحدد ما الملاحظة التي، إذا ظهرت بعد ضبط الصيغة/التركيب/السياق، ستؤدي إلى `REJECT`, `NARROW_SCOPE`, `REOPEN`, أو منع الترقية.

#### A01-R07 — Usage-cluster safeguard
إذا ظهرت clusters استعمالية متباعدة فلا تُحوّل تلقائيًا إلى `MULTIPLE_ROOT_CORES`. تعامل معها كـ`USAGE_CLUSTER_HYPOTHESES` واختبر: هوية الجذر، Layer Attribution، وأعمق Positive Invariant. إذا لم يثبت الجامع فالحالة `UNRESOLVED` وفق مبدأ Root Unity.

#### A01-O02 — ثلاث طبقات عرض لنواة واحدة
عند ثبوت النواة يمكن اشتقاق ثلاث صيغ عرض من **نفس** `ROOT_AXIAL_MEANING`:
- `ROOT_DEFINITION`: أقصر صياغة دقيقة.
- `ROOT_MEANING_EXPLANATION`: شرح زاوية الدلالة ومركز الثقل.
- `ROOT_CONCEPT_MODEL`: تمثيل تصوري للمشاركين والعلاقة/الحالة والثابت والمتغير.

هذه طبقات Presentation ولا تنشئ Claims مستقلة ولا تسمح بإدخال أثر سياقي إلى الجذر.

## 5. Hard Cases & Failure Modes

#### A01-F01 — FORCED_UNIFICATION
إنقاذ core فضفاض جدًا لمجرد الحفاظ على الوحدة. العلاج: `UNRESOLVED`.

#### A01-F02 — FORCED_POLYSEMY
اختراع أصول متنافرة عند أول شاهد صعب. العلاج: فصل layers والعودة للبوابة.

#### A01-F03 — CONTEXTUAL_LEAKAGE
إدخال أثر المشارك/التركيب/السياق في core.

#### A01-F04 — NEGATIVE_CORE
تعريف الجذر بنفي مقابل فقط.

#### A01-F05 — ORNAMENTAL_CORE
core غير ضروري يمكن حذفه دون خسارة تفسيرية.

#### A01-F06 — VACUOUS_CORE
core عام لا يميز ولا يتنبأ.


#### A01-F07 — NEIGHBOR_CHERRY_PICKING
إثبات Distinctiveness عبر جيران مختارة لخدمة الفرضية مع تجاهل جار حاسم.

#### A01-F08 — MULTIPLE_CORE_ESCAPE
الهروب من Hard Case بإعلان أصول دلالية متعددة بدل اختبار Root Identity وLayer Attribution والنواة الأعمق.

## 6. Regression cases

#### A01-RC01 — Rare derivation
صيغة نادرة تبدو خارجة عن core؛ يجب أن تؤدي إلى `UNRESOLVED` أو revision لا أصل ثانٍ تلقائيًا.

#### A01-RC02 — Context confound
زوج occurrences يختلفان في participant/construction؛ يجب ألا يُنسب الفرق للجذر قبل control.

#### A01-RC03 — Attractive mental activation
تعريف شديد التبادر لكنه يفشل في corpus؛ يجب رفضه.

#### A01-RC04 — Too broad invariant
تعريف يغطي الجميع لكنه يغطي neighbor roots كذلك؛ يفشل distinctiveness.

#### A01-RC05 — Reverse-only definition
تقابل قوي في موضع واحد؛ لا يجوز استخدامه وحده لتعريف core.


#### A01-RC06 — Essential-neighbor failure
النواة تبدو مميزة أمام جيران بعيدة لكنها تنهار أمام أقرب جار. المتوقع: تخفيض/إعادة صياغة النواة لا تجاهل الجار.

#### A01-RC07 — Cluster split temptation
تظهر مجموعتان استعماليتان بعيدتان. المتوقع: `USAGE_CLUSTER_HYPOTHESES` + فحص أعمق؛ لا إعلان أصلين دلاليين.

## 7. Reopen

#### A01-R05 — Reopen conditions
أعد فتح النتيجة عند: occurrence جديد/مصَحّح، root identity correction، hard case غير مفسر، competitor أقوى، coverage gap مادي، layer attribution جديد، reverse contradiction، أو كشف circularity.

---

## نهاية الملحق

```text
INTEGRATION_RULES = M01 Root Unity + A02/A03/A04/A05
OUTPUT_CONTRACT = ROOT_RESEARCH card + ROOT_CORE_STATUS
FAILURE_MODES = forced unification/polysemy, leakage, vacuity, circularity
REGRESSION_CASES = A01-RC01..A01-RC05; T01 root cases
REOPEN_IF = new corpus/hard case/competitor/layer/reverse contradiction
END_OF_APPENDIX = A01
```
