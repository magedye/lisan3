# سياسة Migration والتوافق

1. `schema_version` يتبع Semantic Versioning (إصدار دلالي): major للكسر، minor للإضافة المتوافقة، patch للتصحيح غير الكاسر.
2. لا تعدل البيانات durable يدويًا عند بدء قاعدة متعددة الجداول؛ استخدم migration مرقمة (يوصى Alembic مع SQLAlchemy إذا اعتمدت تلك الطبقة).
3. قارئ V2 يرفض major غير معروف وunknown fields على boundaries.
4. أي تغيير في مصدر النص، Skill مؤثرة، SourceRoleProfile، أو calibration model يسجل impact ويحدد النتائج التي تحتاج إعادة تقييم؛ لا rewrite صامتًا.
5. `supersedes_id` يربط revisions السجلية؛ historical record يبقى قابلًا للقراءة.
6. API contract يعلن version؛ أي breaking change يحتاج `/v3` أو تفاوض إصدار صريح.
