# ملف التنفيذ المرجعي — Implementation Profile v1

**الإصدار:** 1.0.0  
**الحالة:** `FINAL_REFERENCE_BASELINE / READY_FOR_IMPLEMENTATION`  
**التاريخ:** 2026-09-05

## 1. الهدف
هذا الملف يزيل التخمين عن التقنية الأساسية للنسخة الأولى دون تحويل أدوات التجريب إلى سلطة منهجية.

## 2. المحرك المستقل
- Runtime: **Python 3.12**.
- Contracts: **Pydantic v2** مع strict/extra-forbid في الحدود الحاكمة.
- Store/index: **SQLite + FTS5**.
- Persistence access: تنفيذ بسيط؛ يجوز SQLAlchemy 2/Alembic إذا بدأ schema durable متعدد الجداول، لكن لا يُنشأ نموذج Lisan3 كاملًا.
- Tool/API boundary: **FastAPI** لعرض الأدوات الحتمية لـGem/Opal/clients؛ routes رقيقة بلا منطق دلالي.
- No Pydantic AI في baseline إلا إذا فشل Gem/Opal في model/tool execution القابل للتدقيق أو احتجنا server-side verifier.

## 3. النص
Tanzil Uthmani 1.1، Hafs an Asim، hash `ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af`. تحفظ bytes canonical؛ مفاتيح البحث مشتقة ومنفصلة.

## 4. البيانات البنيوية في Prototype
لجذر النموذج الأول فقط: annotation set محدودة ومراجعة، مع occurrence id، segmentation/root/lemma/form والحقول التركيبية الضرورية فقط، source/provenance/ambiguity. لا ينسخ QAC fixture runtime. قبل التوسع: `STRUCT-SOURCE-QUALIFICATION` إلزامي.

## 5. الذكاء
- Primary reasoning surface: Gemini/Gem أو نموذج آخر خلف ProviderProfile.
- Gem: conversational research UI.
- Opal: experimental workflow/agent layer after CAP-GO-01.
- fallback orchestrator: Python engine state machine/simple workflow؛ لا LangGraph baseline.

## 6. Scope أول Prototype
- root واحد متوسط التنوع.
- semantic neighbor واحد.
- complete exact occurrence inventory.
- held-out hard cases.
- internal induction only → semantic decision → optional blind challenge → immutable internal snapshot → one controlled external comparison.

## 7. معايير خروج Prototype
- zero fabricated verse/tool claims.
- every decisive statement has EvidenceRelation.
- layer attribution is reviewable.
- at least one serious competing hypothesis unless genuinely none exists with reason.
- falsification executed and receipts present.
- completeness profile shows denominators and gaps.
- UNRESOLVED is a valid result.
- no numeric probability marketed before calibration.
