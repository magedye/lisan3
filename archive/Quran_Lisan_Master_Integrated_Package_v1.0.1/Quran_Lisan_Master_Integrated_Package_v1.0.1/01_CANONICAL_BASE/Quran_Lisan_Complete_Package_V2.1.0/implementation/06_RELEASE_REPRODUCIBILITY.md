# إعادة إنتاج إصدار V2

## بيئة الهدف
- Python Runtime المستهدف: 3.12.
- Pydantic v2 لعقود البيانات.
- FastAPI لعقد Tool Gateway/OpenAPI.

## خطوات التحقق والإغلاق
```bash
python scripts/run_v2_acceptance.py
python scripts/build_release_v2.py
python scripts/validate_package.py
```
بعد إنشاء DOCX الموحد وتشغيل QA البيئي، يعاد بناء manifest/hashes ثم ينشأ ZIP النهائي وبصمة SHA-256 جانبية، ثم يفك الأرشيف في مجلد مؤقت ويعاد التحقق من hashes والاختبارات الثابتة.

## قاعدة DOCX
يسجل renderer وإصداره وOS والخطوط وعدد الصفحات الناتج وحكم الفحص البصري في `release-evidence/docx/`. الحكم هو `DOCX_VISUAL_QA_PASS_IN_RECORDED_ENVIRONMENT` ولا يدعي ثبات عدد الصفحات في Microsoft Word أو أي Renderer آخر.
