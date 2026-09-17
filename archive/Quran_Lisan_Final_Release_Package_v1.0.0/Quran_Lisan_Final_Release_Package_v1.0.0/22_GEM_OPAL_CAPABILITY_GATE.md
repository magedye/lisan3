# CAP-GO-01 — اختبار قدرة Gem/Opal

**الإصدار:** 1.0.0  
**الحالة:** `FINAL_REFERENCE_BASELINE / READY_FOR_IMPLEMENTATION`  
**التاريخ:** 2026-09-05

## سبب وجود البوابة
Opal/Gems from Google Labs منصة تجريبية متغيرة؛ لذلك لا يحملان نواة الثقة ما لم يثبتا خصائص قابلة للتصدير والاختبار.

## الاختبارات P0
1. Tool allowlist يمكن فرضها ولا يدعي الوكيل Tool غير متاح.
2. يمكن ربط Tool execution بسجل server-owned receipt أو معرف يعاد قراءته.
3. structured output يمكن التحقق منه خارج المنصة ورفض unknown fields.
4. stable run/artifact IDs يمكن export/readback.
5. resume بعد فقد الجلسة دون فقد lineage.
6. branch competing hypotheses ثم join دون overwrite.
7. INTERNAL_ANALYSIS يمنع external comparison tools/indexes.
8. internal snapshot غير قابل للتعديل قبل فتح external stage.
9. retry/failure lineage لا يكرر SemanticDecision.
10. model/config/memory influence قابل للتسجيل بالقدر الذي تسمح به المنصة.

## القرار
- PASS لكل P0 → يجوز لـOpal أن يكون orchestrator واجهةً للحلقة، مع بقاء system of record في المحرك.
- أي FAIL/PARTIAL P0 → المحرك المستقل يملك orchestration الحاكم؛ Opal يبقى prototype/UX/optional agent surface.

## قيود حالية موثقة
حتى 2026-09-05: Gems from Google Labs powered by Opal ميزة تجريبية؛ الإنشاء/التحرير web/computer/English مع حساب شخصي، بينما Agent Mode يوفر Memory وRouting وأدوات مثل Search/Code. لذا هذا Gate ليس اختياريًا.
