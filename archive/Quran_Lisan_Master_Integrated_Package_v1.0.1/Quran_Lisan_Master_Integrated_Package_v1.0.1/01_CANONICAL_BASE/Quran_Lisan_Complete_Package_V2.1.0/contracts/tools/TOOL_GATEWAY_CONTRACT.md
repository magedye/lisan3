# عقد Tool Gateway — بوابة الأدوات

- كل طلب/استجابة يطابق Pydantic/JSON Schema.
- أي حقل مجهول يرفض `422 VALIDATION_ERROR`.
- كل تنفيذ ناجح أو فاشل ينشئ `ExecutionReceipt` مملوكًا للخادم، عدا `record_tool_execution` الذي يخزن receipt موجودًا بصورة append-only.
- الأدوات القراءة/الحساب idempotent (إعادة الطلب بنفس المدخلات لا تنشئ أثرًا دلاليًا جديدًا)، بينما سجل التنفيذ يمنع تكرار `receipt_id`.
- `retrieve_external_sources` محظور في `INTERNAL_ANALYSIS` ويجب أن يفشل مغلقًا بـ`SOURCE_POLICY_DENIED` أو `EXTERNAL_STAGE_NOT_OPEN`.
- Tool لا يصدر حكمًا دلاليًا. الحسابات الحتمية لا تتحول إلى Evidence إلا بعلاقة `EvidenceRelation` صريحة.
