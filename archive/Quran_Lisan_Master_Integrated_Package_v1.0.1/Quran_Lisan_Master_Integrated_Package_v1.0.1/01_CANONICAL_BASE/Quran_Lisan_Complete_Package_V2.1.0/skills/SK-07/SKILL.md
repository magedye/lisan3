# SK-07 — تحليل المعنى الموضعي

**الإصدار:** 2.0.0  
**الحالة:** ACCEPTED  
**المتطلبات:** FR-012

## الهدف
تحليل المعنى الموضعي وفق دستور V2 وعقوده التنفيذية والبحثية.

## المدخلات
exact occurrence + root hypothesis + form/construction/context

## السياق المسموح
- في `INTERNAL_ANALYSIS`: Tanzil/البيانات البنيوية المصرح بها، ملاحظات التشغيل الحالي، وعقود المشروع فقط.
- لا تستخدم نتائج سابقة كدليل؛ يمكن أن تكون فرضية تشغيلية إذا أعيد تتبع أصلها.

## الأدوات المسموحة
TL-02|TL-03|TL-04|TL-06

## الخطوات الإلزامية
1. تحقق من وحدة التحليل والمرحلة وسياسة المصدر.
2. استدع الأدوات اللازمة وسجل `ExecutionReceipt`; لا تدع تنفيذًا بلا receipt.
3. افصل observation (الملاحظة) عن hypothesis (الفرضية) وعن evidence relation (علاقة الدليل).
4. طبق الفصل الطبقي الملائم للمهمة، وسجل الغموض والفجوات بدل ملئها تخمينًا.
5. أنشئ المخرج المنظم، ثم تحقق منه ضد schema قبل تسليمه للمنسق.

## المخرجات
local meaning hypotheses + layer map

## حالات الفشل/عدم الحسم
الجذر لا يكفي وحده؛ يجب إظهار مساهمة الطبقات وعدم الحسم

## شرط التوقف
تتوقف المهارة عند تحقق عقد مخرجها أو عند ظهور نقص يمنع تنفيذ خطوة إلزامية. لا تكرر حلقة اعتراض بلا اختبار جديد قابل للتتبع.

## التحقق
- schema validation.
- source-policy validation.
- evidence-reference validation عند وجود ادعاء.
- receipt presence للأدوات/النماذج المؤثرة.

## ممنوعات
- Chain-of-thought (سلسلة التفكير الداخلية الخاصة) ليست Artifact مطلوبًا؛ نحفظ أسبابًا موجزة قابلة للمراجعة فقط.
- لا يتحول retrieval similarity أو موافقة نموذج ثان إلى دليل دلالي بذاته.


## V2 — SemanticDerivationChain إلزامية
لا تصدر Local Meaning قبل بناء السلسلة بالترتيب: root → general inflection/derivation → lexeme/root relation → general form → general construction → local form → local construction/roles → context → local meaning → final statement. أي مرحلة غير منطبقة توسم صراحة ولا تحذف لتجاوزها.
