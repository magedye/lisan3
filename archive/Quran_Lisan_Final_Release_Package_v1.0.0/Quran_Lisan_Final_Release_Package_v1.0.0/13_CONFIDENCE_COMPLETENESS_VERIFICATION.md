# الثقة واكتمال البحث والتحقق المستقل

**الإصدار:** 1.0.0  
**الحالة:** `FINAL_REFERENCE_BASELINE / READY_FOR_IMPLEMENTATION`  
**التاريخ:** 2026-09-05

## 1. الفصل الإلزامي
- **قوة النتيجة/الثقة:** مدى تفضيل الحكم بعد الأدلة والبدائل والنقض.
- **اكتمال البحث:** ماذا كان مؤهلًا للفحص وماذا فُحص.
- **التحقق المستقل:** نوع وحالة إعادة الفحص بمسار مستقل.
لا تدمج في رقم واحد.

## 2. قبل المعايرة
الإصدار 1.0 **لا يسمح بعرض 0–100% كاحتمال موثوق**. تستخدم فئات وصفية مثل: `WEAK / MODERATE / STRONG` مع component report، أو `UNRESOLVED`. كل وزن/threshold سابق مرشح تجريبي فقط.

## 3. مكونات قوة النتيجة المرشحة
coverage، derivational/form consistency، layer separation، hard cases، falsification resistance، alternatives margin، distinctive evidence، explanatory economy، source integrity، failed predictions.

## 4. CompletenessProfile
يجب إظهار denominators: indexed vs deeply analyzed occurrences؛ eligible vs covered forms؛ constructions؛ context clusters؛ neighbors؛ hard cases؛ mandatory tests؛ exclusions/ambiguity. Sampling يوسم ولا يعامل Full Coverage.

## 5. Rejection conditions والفشل المغلق
- دليل من مصدر محظور داخل INTERNAL_ANALYSIS: يبطل صفة «داخلي» للمسار المتأثر.
- source/hash/occurrence identity غير قابلة للتحقق: يوقف الادعاء المعتمد عليها.
- fabricated tool use/no receipt: يرفض الادعاء التنفيذي.
- counterexample حاسم يحقق rejection condition: تعاد صياغة/ترفض الفرضية.
- غياب فرق عن جار: لا يبطل النتيجة تلقائيًا؛ يبقى فرق غير محسوم ويؤثر في القوة.

## 6. التحقق المستقل
مشغلات غير رقمية معتمدة: طلب المستخدم، قرار جوهري/قابل لإعادة الاستخدام، تقارب بدائل، شك تلوث، hard case غير محلول، تغيير نموذج/Skill/مصدر مؤثر. الأنواع: deterministic، context-blind Agent، model-diverse، human review، held-out cases.

## 7. خطة المعايرة
اجمع labeled/reviewed cases أولًا، سجل component predictions ونتائج المراجعة/التعديل، ثم اختبر calibration وBrier/reliability أو مقياس مناسب قبل تفعيل النسب. كل نموذج ثقة يحمل `calibration_version`.

## 8. إضافات v1.1 — ملف الثقة متعدد الأبعاد (تسعة محاور)
تفصيلٌ لمكونات §3 في ملف عرضٍ ثابت، لا نسبة يختارها النموذج بذاته:
1. `Coverage` — اكتمال التغطية.
2. `Structural Reliability` — موثوقية بيانات الجذر والصيغة.
3. `Cross-occurrence Consistency` — قدرة المفهوم على تفسير المواضع المختلفة.
4. `Layer Separation` — نجاح فصل الجذر عن الصيغة والتركيب والسياق.
5. `Neighbor Differentiation` — التمييز عن الجيران.
6. `Counterevidence Burden` — حجم الأدلة المعارضة.
7. `Falsification Survival` — الصمود للدحض.
8. `Holdout Performance` — الأداء على مواضع محجوبة لم تُستخدم في بناء الفرضية.
9. `Independent Verification` — حالة التحقق المستقل.

الحكم النهائي: `STRONG / MODERATE / WEAK / UNRESOLVED` مع مبرر صريح. التحويل إلى 0–100% لا يتم إلا بعد `calibration_version` معتمد (يوافق CTL-021/CTL-036). ملاحظة رابطة: `Cross-occurrence Consistency` مرتبط مباشرة بشرط الحضور الكوني ([05](05_ROOT_CONCEPT_CONTRACT.md) §11) — موضع معارض واحد يمنع `STRONG`.
