# سياسة المصدر وFixture

1. **Tanzil** هو النص المرجعي للنسخة الأولى بعد مطابقة SHA/size/6236 records؛ لا تطبيع على bytes المرجعية.
2. **QAC fixture** مصدر خارجي بنيوي مؤقت للاختبارات فقط. حقول root/form/locator قابلة للاستخدام في Fixture؛ أي gloss/ontology/semantic label ممنوع من الدليل الداخلي.
3. **Synonyms Dataset** تقييم خارجي فقط ولا يدخل الدليل القرآني.
4. عند غياب source role (دور مصدر) صريح أو عدم القدرة على إثبات phase/field authorization، `fail closed` (فشل مغلق).
5. `SourceAccessEvent` يسجل ALLOWED/DENIED؛ لا يكفي أن يقول النموذج إنه لم يستخدم مصدرًا.
6. إغلاق النتيجة الداخلية ينشئ `InternalSnapshot` immutable؛ أي مقارنة خارجية revision منفصلة.
