# نموذج البيانات والذاكرة وقابلية التتبع

**الإصدار:** 1.0.0  
**الحالة:** `FINAL_REFERENCE_BASELINE / READY_FOR_IMPLEMENTATION`  
**التاريخ:** 2026-09-05

## 1. السجلات الدنيا P0
1. `SourceIdentity` — المصدر، الإصدار، الترخيص، provenance، hash، أدوار الحقول.
2. `CorpusSnapshot` — القطعة النصية المحددة وهوية الآيات.
3. `Occurrence` — الموضع، اللفظة، المطابقة، الغموض، الاستبعادات.
4. `ResearchRun` — الهدف، وحدة التحليل، الإصدارات، الحالة الإجرائية، snapshots.
5. `Observation` — ملاحظة مباشرة مع مصدر/أداة.
6. `EvidenceRelation` — علاقة ملاحظة/موضع بفرضية أو قرار: support/counter/constraint/neutral.
7. `Hypothesis` — النص/البنية، النطاق، البدائل، predictions، `RejectionCondition`.
8. `SemanticDecision` — القرار المرّجح/غير المحسوم، reasons منظمة، alternatives، revision lineage.
9. `ExecutionReceipt` — tool/model, inputs refs/hashes, outputs refs/hashes, error, duration, retry lineage, provider/config.
10. `CompletenessProfile` — denominators وفحص المواضع/الصيغ/التراكيب/الحالات الصعبة/الجيران/الاختبارات.

## 2. سجلات P1
- `LexicalUnitHypothesis`
- `LayerAttribution`
- `SemanticNeighborResult`
- `FalsificationRun`
- `SourceAccessEvent`
- `ExternalInfluence`
- `IndependentVerification`
- `ConfidenceAssessment` بعد وجود calibration_version.

## 3. Views دلالية
`RootConceptResult`, `LocalMeaningResult`, و`SemanticDifferenceResult` Views/aggregates فوق السجلات، وليست مصادر أدلة مستقلة.

## 4. حالات ResearchRun المبسطة
`CREATED → UNIT_RESOLVED → INTERNAL_DATA_READY → OBSERVED → HYPOTHESES_FROZEN → CHALLENGED → INTERNAL_DECISION_SNAPSHOTTED → [INDEPENDENT_VERIFIED] → [EXTERNAL_COMPARED/REVISED] → PRESENTED`

العودة مسموحة مع reason وrevision؛ لا overwrite صامت.

## 5. الذاكرة
- تفضيلات مستخدم.
- تاريخ تشغيل.
- فرضيات سابقة.
- قرارات سابقة مع evidence lineage.
- مصادر خارجية مفصولة.
أي recall سابق يولد hypothesis/reference، لا EvidenceRelation جديدًا إلا بعد إعادة التتبع.

## 6. سلسلة التتبع
`Decision → Hypotheses → EvidenceRelations → Observations → Occurrences/Artifacts → SourceIdentity`، وبالتوازي `Decision → FalsificationRuns/Completeness/Verification → ExecutionReceipts → protocol/model/tool revisions`.

## 7. إضافات v1.1 — طبقات المعرفة والبوابة التأسيسية

### أ. طبقات المعرفة الأربع
لا تُخزَّن «النتائج المقبولة» وحدها:
1. **قاعدة النتائج البحثية:** كل الجذور بما فيها `STRONG/MODERATE/UNRESOLVED/REJECTED`.
2. **قاعدة المعرفة المقبولة:** ما اجتاز الشروط وأصبح `ACCEPTED`.
3. **قاعدة تعلّم المنهج:** المشاكل والانحرافات والدروس والاقتراحات المكتشفة عبر الجذور.
4. **مجموعة التقييم الدلالي:** الحالات الصعبة والأمثلة المضادة ← اختبارات Regression دلالية.

الجذر غير المحسوم قد يكون أهم من السهل في تحسين المنهج، فلا تضيع قيمته.

### ب. فرضيات عبر الجذور (`Cross-root Hypotheses`)
أنماط لا تظهر إلا بعد دراسة عشرات الجذور (أثر صيغة مشترك عبر جذور، مساهمة تركيب مع حرف جر، أبعاد تفصل مجموعات الجيران، سياقات تُضخّم معنى الجذر) تُسجَّل **فرضيات لا حقائق تلقائية**، وتصير موضوع دورة بحث جديدة.

### ج. البوابة التأسيسية الخفيفة
كل `ResearchRun` يسجّل `foundational_profile_version` (مثل `FND-1.0`) إلى جانب `methodology_version`؛ يتحقق النظام من وجود النسخة واعتمادها فقط، بلا `FOUNDATION_GATE` ثقيلة (CTL-042). المرجع: [24_FOUNDATIONAL_PREMISES_AND_ASSUMPTIONS_CHARTER.md](24_FOUNDATIONAL_PREMISES_AND_ASSUMPTIONS_CHARTER.md).
