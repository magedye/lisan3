# SUPPORTING SEMANTICS ROOT CORE FIREWALL REGRESSION

## العقد

- دلالات الحروف والأوزان مراجع مساعدة وليست دليلًا قرآنيًا أوليًا.
- لا يجوز لأي حقل أو نتيجة منها تعريف `Root Core` أو رفعه إلى حالة معتمدة.
- `ADOPTED_OPERATOR` يحتاج مساهمة مختبرة، ومرجع اعتماد صريحًا من المالك.
- بقاء سجل الحروف `entries: []` حالة صحيحة ومقصودة.

## الاختبارات السالبة

يشغّل `11_VALIDATION/validate_supporting_semantics_boundaries.py --self-test` حالتين مرفوضتين:

1. مدخل حرف يحتوي `root_core`.
2. مؤثر معلن `ADOPTED_OPERATOR` دون مرجع اعتماد المالك.

أي قبول لإحدى الحالتين فشل مغلق في الإصدار.
