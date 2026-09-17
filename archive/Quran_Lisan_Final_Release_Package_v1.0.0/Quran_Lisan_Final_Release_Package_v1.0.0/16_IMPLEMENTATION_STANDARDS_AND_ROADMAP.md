# معايير التنفيذ وخارطة الطريق

**الإصدار:** 1.0.0  
**الحالة:** `FINAL_REFERENCE_BASELINE / READY_FOR_IMPLEMENTATION`  
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

## إضافات v1.1 — حملة الاكتشاف والمعايرة

### أ. وحدة العمل = الجذر
تُتخذ **وحدة العمل الأساسية الجذر** لا المفردة؛ يبحث النظام داخله كل المشتقات والصيغ والتراكيب والمواضع، فينتج أصلٌ دلالي قابل لإعادة الاستعمال في عشرات الأسئلة اللاحقة.

### ب. مراحل التوسع
| المرحلة | الغرض |
| --- | --- |
| مسح شامل | حصر جميع الجذور المؤهلة وتصنيفها بلا بحث دلالي عميق |
| عينة معايرة | 8–12 جذرًا متنوعة جدًا لاختبار المنهج |
| مراجعة المنهج | جمع المشاكل والدروس دون تغيير المنهج أثناء الدفعة |
| دفعة توسع | 20–30 جذرًا |
| دفعات واسعة | ~50 جذرًا أو ما تسمح به الموارد |
| استكمال | حتى نفاد الجذور المؤهلة أو ظهور مانع منهجي عام |

**القاعدة الحاكمة (CTL-041):** لا تتغير المنهجية أثناء الدفعة الواحدة. تُسجَّل المشكلة ويُقترح حلها، وبعد اكتمال الدفعة يُنشأ `Methodology Revision` ثم تُعاد جذور مرجعية (sentinels) للتأكد من عدم التراجع.

### ج. اختيار الجذور بمحفظة متنوعة (لا بالتكرار وحده)
تُبنى محفظة بحسب: عدد المواضع، عدد المشتقات، تنوع الصيغ، تنوع التراكيب، تنوع المشاركين، قرب الجيران، احتمال تعدد أصول المعنى، صعوبة فصل الجذر عن السياق، جودة البيانات البنيوية، وجود مواضع صعبة. تشمل أول دفعة سهلًا ومتوسطًا وصعبًا، قليل وكثير المواضع.

**مانع توسع بنيوي (CTL-043):** إن لم يكن مصدر تحديد الجذور والصيغ مؤهلًا، يُسجَّل مانع توسع بنيوي ولا تُخمَّن الجذور من الذاكرة.

(المهمة التشغيلية في [09_AGENTS_SKILLS_TOOLS.md](09_AGENTS_SKILLS_TOOLS.md)؛ طبقات المعرفة في [12_DATA_MEMORY_AND_TRACEABILITY_MODEL.md](12_DATA_MEMORY_AND_TRACEABILITY_MODEL.md).)
