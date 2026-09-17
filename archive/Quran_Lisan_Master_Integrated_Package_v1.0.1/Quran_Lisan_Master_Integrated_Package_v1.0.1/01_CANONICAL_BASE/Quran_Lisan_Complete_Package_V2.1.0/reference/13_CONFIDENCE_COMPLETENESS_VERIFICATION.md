# الثقة واكتمال البحث والتحقق المستقل

**الإصدار المدمج في V2:** 2.0.0  
**الحالة:** `V2_FINAL_COMPREHENSIVE_BASELINE / READY_FOR_BLIND_IMPLEMENTATION`  
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
