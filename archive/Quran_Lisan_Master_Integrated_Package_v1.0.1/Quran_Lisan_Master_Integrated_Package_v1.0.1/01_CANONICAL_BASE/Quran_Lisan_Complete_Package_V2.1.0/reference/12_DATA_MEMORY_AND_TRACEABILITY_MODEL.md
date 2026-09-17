# نموذج البيانات والذاكرة وقابلية التتبع

**الإصدار المدمج في V2:** 2.0.0  
**الحالة:** `V2_FINAL_COMPREHENSIVE_BASELINE / READY_FOR_BLIND_IMPLEMENTATION`  
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
