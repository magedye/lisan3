# البنية المنطقية المستهدفة

**الإصدار المدمج في V2:** 2.0.0  
**الحالة:** `V2_FINAL_COMPREHENSIVE_BASELINE / READY_FOR_BLIND_IMPLEMENTATION`  
**التاريخ:** 2026-09-05

## 1. القرار المعماري النهائي للإصدار 1.0
البنية **هجينة ومقسمة السلطة**:
- الذكاء الاصطناعي: الاستقراء، بناء الفرضيات، المقارنة، النقض، والترجيح الدلالي.
- المحرك المستقل: النص، الهوية، الاسترجاع الدقيق، صلاحيات المصادر، العقود، سجلات التنفيذ، الأدلة، الاكتمال والحسابات الحتمية.
- Gem/Opal: واجهة/تنسيق قابلان للاستبدال ولا يحملان الحقيقة الوحيدة.

## 2. الرسم
```text
الباحث
  │
  ├─ Gem / واجهة بديلة
  │        │
  │        ▼
  │   Orchestrator
  │   (Opal إذا اجتاز CAP-GO-01، وإلا المحرك المستقل)
  │        │
  │   ┌────┴─────────────────────────┐
  │   ▼                              ▼
  │ Skills                     Agents/Reviewers
  │   │                              │
  │   └──────────┬───────────────────┘
  │              ▼
  │          Tool Gateway
  │              │
  │   ┌──────────┼───────────┬──────────────┐
  │   ▼          ▼           ▼              ▼
  │ Quran     Structure   Evidence/Run   Execution Receipts
  │  Text       Layer        Store
  │   └──────────┼───────────┴──────────────┘
  │              ▼
  │      Deterministic Core Engine
  │              │
  │              ▼
  └──────── Semantic Decision + بيان دلالي
```

## 3. المكونات الإلزامية P0
1. Versioned methodology + terminology.
2. `SourceIdentity` و`CorpusSnapshot`.
3. exact `Occurrence` index.
4. minimal `StructuralAnnotation` مع غموض ومصدر.
5. `ResearchRun`.
6. `Observation`.
7. `EvidenceRelation`.
8. `Hypothesis` + `RejectionCondition`.
9. `SemanticDecision`.
10. `ExecutionReceipt` لكل أداة/نموذج.
11. `CompletenessProfile` متعدد الأبعاد.
12. Tool Gateway مع allowlist وسياسة مصدر.
13. Skills الإصدارية.
14. Agent/Orchestrator واحد افتراضي + adversarial challenger.
15. Internal snapshot ثم External comparison revision.

## 4. المكونات P1
- LexicalUnitHypothesis / semantic branches.
- LayerAttribution.
- SemanticNeighborResult.
- FalsificationRun.
- SourceAccessEvent / ExternalInfluence.
- IndependentVerification.
- calibrated confidence model بعد benchmark.

## 5. ما لا يدخل النواة الأولى
- Lisan3 four-axis status/publication/Steward/governance proposal machinery.
- Purity/Internal Lock gate كاملًا.
- QAC adapter الحالي.
- vector server، graph database، six embedding spaces، LangGraph، DSPy، external RAG framework.
- numeric confidence weights غير المعايرة.

## 6. استرجاع البيانات
`Exact/FTS first`. يستخدم SQLite/FTS5 أو مكافئ حتمي للنص والهوية والمواضع. vector/graph، إن أضيفا لاحقًا، ينتجان `RetrievalCandidate` فقط ولا ينشئان Evidence أو Confidence.

## 7. استقلال المنهج عن المزود
كل عقد/تعريف/Skill/Schema محفوظ خارج Gem/Opal وبإصدار. تغيير المزود أو الواجهة لا يغير نتيجة تاريخية صامتًا.
