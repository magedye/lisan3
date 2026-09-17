# دليل Requirement → Test → Evidence → Acceptance

`acceptance/TRACEABILITY_MATRIX.csv` هو العقد الحاكم للتتبع. يوجد لكل FR/NFR اختبار واحد على الأقل.  
- `STATIC_EXECUTABLE`: يجب أن يمر داخل حزمة الإغلاق قبل التسليم.
- `IMPLEMENTATION_ACCEPTANCE`: يمر بعد وجود كود المنتج.
- `SEMANTIC_EVAL`: يقيم سلوك AI بالـRubric؛ لا يثبت صحة دلالية مطلقة.
- `CAPABILITY_PROTOCOL`: بروتوكول منصة خارجي مثل CAP-GO-01.

**P0 Prototype exit:** كل اختبار قابل للتطبيق لمتطلب `prototype_priority=P0` يجب أن PASS، وأي اختلاق آية/Tool أو تسرب مصدر محظور هو فشل حاسم، لا يعوضه نجاح بقية النقاط.
