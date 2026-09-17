# CAP-GO-01 — بروتوكول اختبار قدرة Gem/Opal

**الحالة:** `NOT_EXECUTED`.

لكل اختبار من العشرة:
1. سجل `environment`: المنصة، نوع الحساب، build إن ظهر، التاريخ، model/mode.
2. ابدأ من Fixture محدد في `fixtures/CAP_GO_FIXTURES.json`.
3. نفذ الخطوات المرقمة في `TEST_STEPS.md`.
4. خزّن screenshots/exports/receipts في `evidence/<test-id>/`.
5. احكم PASS/FAIL/PARTIAL حسب معيار الاختبار؛ PARTIAL يعامل كFAIL لـP0.
6. تحقق من التقرير ضد `RESULT_SCHEMA.json`.

**القرار:** PASS لجميع الاختبارات العشرة فقط يسمح لـOpal أن يكون orchestrator (منسق) الحلقة. وإلا يبقى Python fallback هو المنسق الحاكم، ويمكن استخدام Opal كواجهة/Prototype فقط.
