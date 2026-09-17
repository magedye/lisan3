# العقود التنفيذية

الحزمة `quran_lisan_contracts` هي المصدر البرمجي لعقود v1.0.1. تستخدم `extra="forbid"` لمنع الحقول المجهولة على الحدود، وتحافظ على revision وإصدار schema. شغّل:

```bash
python scripts/generate_schemas.py
python scripts/validate_contracts.py
```

الهدف Runtime هو Python 3.12. تمت كتابة العقود لتكون متوافقة مع Python >=3.12، بينما بيئة إنشاء الحزمة مسجلة في تقرير الإغلاق.
