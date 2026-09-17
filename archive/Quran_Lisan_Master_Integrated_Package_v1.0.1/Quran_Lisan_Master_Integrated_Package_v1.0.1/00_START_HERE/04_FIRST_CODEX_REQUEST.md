# LISAN3 — Phase 0A: Master Admission & Pre-Analysis Foundation

## المهمة والهدف
اعمل مباشرة على مستودع LISAN3 الحالي. هدف هذه المهمة **ليس تحليل الجذور دلاليًا**، بل إدخال حزمة `Quran_Lisan_Master_Integrated_Package_v1.0.0` إلى المشروع بصورة محافظة، والتحقق من التوافق، وتنفيذ التوجيهات المالكية المقبولة بعد V2.1 التي يجب أن تسبق التحليل الواسع.

نحتاج هذه المرحلة لأن الحملة الدلالية الواسعة يجب أن تبدأ من حقائق قابلة للتحقق، وسلطة موحدة، وتتبّع يمنع ضياع الأفكار، لا من إعادة اكتشاف الأعداد والبنية داخل LLM في كل RootRun.

## Model / Reasoning / Mode
- **Model:** أقوى نموذج Codex متاح وموثوق في بيئتك.
- **Reasoning:** High / Very High.
- **Mode:** Plan → Execute → Verify. لا تتوقف عند التوصيات.

## 0. Source of truth
استخدم ترتيب السلطة داخل `00_START_HERE/00_MASTER_AUTHORITY.md`.
V2.1 الموجود داخل الحزمة قاعدة كانونية محفوظة، والدلتا المقبولة بعده فقط تملك الأولوية في مواضع التعارض الموثقة.
لا تجعل `03_PRE_ANALYSIS/` حاكمًا لمجرد أنه موجود؛ عناصره OPEN ما لم يعتمدها المالك.

## V0 — Preflight
قبل أي تعديل سجل:
- HEAD SHA / branch / worktree status.
- الملفات غير المتعقبة/المعدلة وحيازتها.
- ما إذا كانت V2.1 أو أجزاء منها موجودة بالفعل في المستودع.
- status الحالي لحلقة governed capture.
- status الحالي لمصدر القرآن، root/morphology/structure data.
- status الحالي لعقود RootResearch/Confidence/External comparison.
- أي عمل سابق لتبسيط الحوكمة؛ لا تعِده إن كان منجزًا.

Preserve all unrelated user work. No reset/clean.

## V1 — Master admission without duplication
1. لا تنسخ الحزمة عشوائيًا إلى عدة مواضع.
2. حدد الموضع الحاكم الحالي للمراجع في LISAN3 وادمج **بالحد الأدنى**.
3. إذا كان محتوى V2.1 موجودًا بالفعل ومتكافئًا، لا تكرره؛ سجل mapping/hash فقط.
4. احتفظ بالمصادر/الحزم الأصلية كأرشيف غير حاكم إذا احتاج المشروع حفظها.
5. أنشئ/حدّث Authority pointer واحدًا يوضح current source of truth.

## V2 — Governed intent capture
نفذ أو تحقق من وجود حلقة:
`CAPTURE → ATOMIZE → CLASSIFY → MAP → DISPOSITION → VERIFY`.
- Owner directive لا يساوي assistant proposal.
- Proposal غير مالكي لا يصبح Accepted بلا approval ref.
- Accepted item لا يبقى بلا target أو rationale.
- أعد استخدام بنية المشروع الحالية إن كانت تكفي؛ لا تنشئ سجلًا موازيًا بلا حاجة.

## V3 — Descriptive knowledge foundation (أولوية تنفيذية)
نفذ مبدأ «المعرفة قبل الاجتهاد» بأخف بنية مناسبة.

### المطلوب
قدرة حتمية/قابلة لإعادة الإنتاج على استخراج أو استرجاع **Root Descriptive Profile** من المصادر المعتمدة يتضمن -حيث تتوفر البيانات المؤهلة-:
- root identity + source/provenance;
- total confirmed/eligible occurrences;
- occurrence refs;
- forms/derivations/inflections and counts;
- repeated constructions/particles/relations where deterministic/qualified;
- structural disagreements/uncertainties;
- source version / extraction version;
- verification state.

### قاعدة الثقة في البيانات
افصل على الأقل بين:
- direct textual fact;
- qualified structural annotation;
- disputed/unresolved structural annotation.
لا تقل إن تحليلًا صرفيًا «حقيقة نصية» لمجرد أنه في قاعدة بيانات.

### reuse first
افحص `CorpusSnapshot`, `Occurrence`, morphology/context/tools أو ما يقابلها في LISAN3 وأعد استخدامها. لا تضف جداول أو services جديدة إلا إذا أثبت gap فعلي.

### لا تفعل
لا تستنتج معنى الجذر في هذه المرحلة.
لا تستخدم LLM لإنتاج أعداد يمكن للكود/المصدر حسابها.

## V4 — Universal root meaning presence contract
ادمج التوجيه المالكي الحالي في موضع المنهج/العقد والاختبارات بأقل تغيير:
- معنى الجذر المقبول يجب أن يظهر أثره في كل occurrence ثابت الانتماء.
- موضع واحد معارض يمنع قبول root-wide concept الحالي.
- unresolved structural attribution لا يُخفى.
- لا تستخدم majority threshold بدل الشمول.
- الشمول لا يكفي بلا distinctiveness/falsifiability.

### Compatibility
لا تقم mass rename لكل schema/status القديم. عالج فقط السلوك/النص الذي يتعارض فعليًا.
إذا كان `MULTIPLE_LEXICAL_UNITS` أو ما يعادله يستخدم لتبرير غياب جامع لجذر واحد ثابت، غيّر هذا السلوك. إذا كان له استعمال تقني آخر مشروع (مثل نزاع نسبة تاريخية مثبت)، وثق الفرق بدل الحذف الأعمى.

## V5 — Terminology clarity delta
طبق التوجيه في **النصوص الحاكمة الجديدة والمخرجات البشرية** دون refactor شكلي واسع:
- قلل «دلالة» عندما يكون المقصود أوسع/أضيق وغير واضح.
- تجنب «الوحدة المعجمية» كحل دلالي غامض.
- حافظ على internal IDs/code tokens إذا كان تغييرها لا يضيف قيمة أو يكسر التوافق.
- قدّم Terminology Delta واقتراحات لأي تغيير أكبر يحتاج قرار مالك.

## V6 — External hypothesis testing support
نفذ الحد الأدنى المتوافق مع التوجيه المالكي:
- External hypothesis can be ROOT_CORE / FORM_EFFECT / LETTER_EFFECT / CONSTRUCTION_EFFECT / METHOD_RULE.
- provenance + source claim + test plan + result required.
- محمد حسن جبل: root core candidate عالي الأولوية إذا توفر نص موثق، دون سلطة أو bonus confidence.
- افصل rule claim عن application claim.
- لا يوجد `Scholar said X → methodology changed`.
- لا تصف External Hypothesis Test بأنه Blind Internal Discovery.

**لا تعتمد Full dual-lane lifecycle كتعقيد دائم إلا إذا كان لازمًا لإنفاذ هذا الفصل؛ إذا أمكن بآلية أخف فاستخدمها وسجل القرار.**

## V7 — Foundational premises draft, not silent adoption
لأن ضرورة توضيح المرتكزات قبل التحليل مقترح مالكي مهم لكن بنيته النهائية لم تُعتمد بالكامل:
- استخرج من السلطة الحالية فقط المرتكزات التي هي بالفعل قرارات/نصوص حاكمة.
- أنشئ `FOUNDATIONAL_PROFILE_DRAFT` قصيرًا مع: statement, source/authority, methodological effect, risk if misapplied, review trigger.
- لا تخترع five-layer taxonomy أو تحولها إلى Gate دون قرار.
- قدم ما يحتاج Owner decision منفصلًا.

## V8 — Readiness & calibration prep
جهز فقط ما يلزم لإثبات أن المشروع أصبح قادرًا على بدء Calibration لاحقًا:
- root descriptive profile demo/fixture from qualified data;
- deterministic coverage check;
- root universality acceptance test fixture;
- capture/traceability test;
- external hypothesis provenance/isolation test;
- no uncalibrated numeric confidence test.

لا تبدأ الحملة الواسعة ولا تنتج Root Concept بحثيًا حقيقيًا إلا إن احتاج اختبارًا اصطناعيًا/fixture.

## V9 — Tests and regression
شغل الاختبارات الحالية والمتأثرة. أضف فقط اختبارات تغلق تغييرات هذه المهمة.
يجب أن تثبت على الأقل:
1. direct text facts ليست model-generated;
2. structural uncertainty preserved;
3. accepted root concept cannot pass with one confirmed unexplained occurrence;
4. external hypothesis cannot masquerade as blind discovery;
5. assistant proposal cannot become owner accepted silently;
6. unrelated current behavior remains green.

## Stop / scope
- لا UI redesign.
- لا تغيير corpus identity.
- لا migration واسعة لمجرد التنظيف.
- لا push/merge/tag/release.
- لا حذف تاريخ أو حزم مصدر.
- إذا تعارضت نسخة مشروع أحدث مع هذه الحزمة، لا تحسم بصمت: قدم evidence + authority resolution.

## التقرير النهائي
أعد:
1. verdict;
2. base/candidate identity;
3. authoritative files admitted/mapped;
4. reused vs newly added structures;
5. descriptive knowledge capability;
6. root-universality implementation;
7. terminology changes (human-facing vs internal compatibility);
8. external hypothesis support;
9. foundational draft/open decisions;
10. tests exact results;
11. changed paths;
12. complexity added/removed;
13. remaining blockers before Calibration;
14. owner decisions genuinely required;
15. unrelated work untouched.

الحكم المستهدف فقط إذا أثبتته الأدلة:
`MASTER_ADMITTED_AND_PRE_ANALYSIS_FOUNDATION_QUALIFIED`

ولا تستخدم `READY_FOR_LARGE_SCALE_ROOT_ANALYSIS` في هذه المهمة.
