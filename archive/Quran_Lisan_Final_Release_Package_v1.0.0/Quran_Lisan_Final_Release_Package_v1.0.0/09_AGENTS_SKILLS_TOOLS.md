# الوكلاء والمهارات والأدوات

**الإصدار:** 1.0.0  
**الحالة:** `FINAL_REFERENCE_BASELINE / READY_FOR_IMPLEMENTATION`  
**التاريخ:** 2026-09-05

## 1. التعريف
- **Skill / مهارة:** كيف تنفذ مهمة منهجية حساسة.
- **Agent / وكيل:** ماذا ينفذ ومتى وبأي ترتيب ضمن صلاحياته.
- **Tool / أداة:** فعل حقيقي قابل للتحقق يصدر إيصال تنفيذ.

## 2. الوكلاء المعتمدون في النواة
- `AG-01 Research Orchestrator & Semantic Decision Agent`: يدير البحث ويملك الترجيح.
- `AG-02 Adversarial Challenge Agent`: يحاول إسقاط الفرضيات مع فصل سياقه قدر الإمكان.
- `AG-03 Source Contamination Reviewer`: يفحص التسرب الظاهر/غير المتتبع ولا يدعي كشف المعرفة البارامترية يقينًا.
- `AG-04 Independent Blind Verifier`: مشروط بالمشغلات؛ لا يرى الحكم الأول.
- `AG-05 Output & Terminology Reviewer`: يصحح البيان والمصطلح، ولا يغير القرار الدلالي بذاته.

لا ننشئ Collector/Context Agents مستقلين افتراضيًا؛ تكون تلك وظائف Skills/Tools ما لم يثبت أن فصلها يضيف استقلالًا أو دقة قابلة للقياس.

## 3. المهارات v1.0
1. `SK-01 Analysis Unit Resolution`
2. `SK-02 Quran Occurrence Collection`
3. `SK-03 Derivational Family Analysis`
4. `SK-04 Morphological Form Analysis`
5. `SK-05 Root Concept Extraction`
6. `SK-06 Local Meaning Analysis`
7. `SK-07 Construction Analysis`
8. `SK-08 Semantic Neighbor Comparison`
9. `SK-09 Distinctive Feature Discovery`
10. `SK-10 Competing Hypothesis Generation`
11. `SK-11 Falsification & Counterevidence`
12. `SK-12 Source Contamination Review`
13. `SK-13 Result Synthesis`

لكل Skill: purpose, input contract, allowed context, allowed tools, prohibited evidence, steps, outputs, uncertainty behavior, stop condition, verification, version/hash.

## 4. الأدوات الحتمية الدنيا
- `get_occurrences`
- `get_verse`
- `get_context`
- `get_structural_annotation`
- `get_derivational_family`
- `get_collocations`
- `validate_evidence_refs`
- `calculate_completeness_profile`
- `create_internal_snapshot`
- `record_source_access`
- `record_execution_receipt`
- `apply_source_role_policy`
- `retrieve_external_sources` — غير متاحة في INTERNAL_ANALYSIS.

لا توجد أداة حتمية تحكم «المعنى الصحيح»؛ التحقق الحتمي يثبت الهوية/البيانات/التغطية/السجل، بينما الدعم الدلالي قرار مفسر.

## 5. الاستقلال
نصف مسارًا بأنه مستقل فقط إذا سجل نوع الاستقلال: `CONTEXT_BLIND`, `MODEL_DIVERSE`, `DETERMINISTIC_CHECK`, `HUMAN_REVIEW`, أو مزيج. Same-model agreement لا يساوي دليلًا مستقلًا.

## 6. إضافات v1.1 — مهمة حملة الاكتشاف والمعايرة
تُضاف مهمة تشغيلية للوكيل المنسق `AG-01`:
> **`LISAN Semantic Discovery & Methodology Calibration Campaign`**

أهدافها: إنشاء حصر مؤهل للجذور؛ اختيار عينة متنوعة منهجيًا؛ تطبيق منهج لسان القرآن كاملًا على كل جذر؛ تخزين النتيجة والأدلة والدحض والثقة؛ اكتشاف مشاكل المنهج من واقع التطبيق وتحويلها إلى **اقتراحات منهجية مصنّفة لا تعديلات تلقائية**؛ بناء قاعدة متنامية من النتائج المقبولة؛ بناء مجموعة تقييم دلالية؛ التوسع تدريجيًا بجودة مؤهلة.

تلتزم المهمة بقاعدة تجميد المنهج داخل الدفعة (CTL-041) ومانع التوسع البنيوي (CTL-043)، وتسجّل `foundational_profile_version` لكل تشغيل (CTL-042). التفاصيل في [16_IMPLEMENTATION_STANDARDS_AND_ROADMAP.md](16_IMPLEMENTATION_STANDARDS_AND_ROADMAP.md) و[12_DATA_MEMORY_AND_TRACEABILITY_MODEL.md](12_DATA_MEMORY_AND_TRACEABILITY_MODEL.md).
