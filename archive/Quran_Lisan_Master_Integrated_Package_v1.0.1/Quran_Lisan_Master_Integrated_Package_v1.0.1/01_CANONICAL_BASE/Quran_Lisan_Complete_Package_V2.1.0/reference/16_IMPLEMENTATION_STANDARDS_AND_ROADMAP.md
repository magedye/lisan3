# معايير التنفيذ وخارطة الطريق

**الإصدار المدمج في V2:** 2.0.0  
**الحالة:** `V2_FINAL_COMPREHENSIVE_BASELINE / READY_FOR_BLIND_IMPLEMENTATION`  
**التاريخ:** 2026-09-05

## 1. ملف التنفيذ المرجعي
التفاصيل التقنية الملزمة في `21_IMPLEMENTATION_PROFILE_V1.md`. المبدأ: build deterministic core first, then AI orchestration.

## 2. المرحلة 0 — Preflight + Capability Proof
- تثبيت Tanzil artifact/hash/index.
- إنشاء project methodology/terminology/schema versions.
- تنفيذ `CAP-GO-01` لـGem/Opal: tool authorization/receipts, structured export, run IDs, resume, branching, source-stage controls, internal snapshot, retry lineage.
- إذا فشل أي P0: Opal يصبح مختبر/واجهة غير حاكمة ويملك Python orchestrator المسار الحاكم.

## 3. المرحلة 1 — One-root Research Loop
- Python 3.12 deterministic engine.
- Pydantic v2 contracts.
- SQLite + FTS5 store/index.
- FastAPI Tool Gateway.
- manual/verified minimal structural annotation for selected root; no QAC runtime.
- records P0 العشرة.
- Skills الأساسية + Agent رئيسي + adversarial challenger.
- internal snapshot → optional external comparison.

**خروج:** تقرير واحد قابل لإعادة التشغيل دون fabricated evidence، مع alternatives/falsification/completeness.

## 4. المرحلة 2 — Structural source and repeatability
- qualify a scalable morphology/syntax source: license, exact artifact, field roles, importer, alignment, ambiguity.
- expand eval set across roots/forms.
- fake/live provider separation.
- retry/resume and regression suite.

## 5. المرحلة 3 — Gem/Opal integration if capability proof passes
- Gem conversational interface.
- Opal workflow/Agent routing only for boundaries it can export/enforce.
- no state duplicated without one system-of-record ID.

## 6. المرحلة 4 — calibration + external comparison
- benchmark confidence components.
- enable numeric scores only after calibration acceptance.
- controlled tafsir/dictionary/prophetic-explanation comparison with influence lineage.

## 7. المرحلة 5 — Expansion by evidence
Only after measured need: vector discovery, graph projection, multi-provider routing, local model, richer UI, multi-reading support, multi-user/publication.

## 8. ممنوعات التنفيذ
- no LangGraph + Opal dual orchestration initially.
- no vector/graph server before benchmark.
- no QAC fixture adapter reuse.
- no full Lisan3 governance/status/publication stack.
- no silent model-memory fallback.
- no hard-coded confidence percentages from prior discussions.
