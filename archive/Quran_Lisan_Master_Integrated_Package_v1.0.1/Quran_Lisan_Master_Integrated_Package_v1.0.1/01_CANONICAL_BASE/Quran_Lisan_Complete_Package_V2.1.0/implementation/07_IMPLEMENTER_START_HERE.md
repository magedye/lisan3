# ابدأ من هنا — دليل مطور V2

1. اقرأ `../00_PACKAGE_AUTHORITY.md` ثم `../01_PACKAGE_MAP_AND_START_HERE.md`.
2. اقرأ `../reference/03_METHODOLOGY_AND_EVIDENCE_CONSTITUTION.md` و`../research/01_FINAL_RESULT_AND_SEMANTIC_DERIVATION_CONTRACT.md`.
3. شغّل `python scripts/run_v2_acceptance.py`؛ يجب أن ينجح قبل كتابة المنتج.
4. اقتنِ Tanzil عبر `scripts/acquire_tanzil.py` أو ضع القطعة المعروفة ثم شغّل `scripts/validate_tanzil.py`.
5. استخدم Pydantic models في `contracts/python/quran_lisan_contracts` كمصدر العقود؛ لا تخترع حقولًا إضافية.
6. نفذ Tool Gateway وفق `contracts/tools/TOOL_REGISTRY.csv` وOpenAPI.
7. نفذ State Machine وفق `contracts/state-machine/research_run_transitions.json`.
8. أدخل Fixture `PROTOTYPE-SLM-01` فقط في النموذج الأول؛ لا توسع قبل البوابة أو قرار Phase جديد.
9. طبق Skills 01–13؛ Agent يختار Skill لكنه لا يغير منهجها.
10. في `LOCAL_MEANING`/تحليل الآية، نفذ `SemanticDerivationChain` بالترتيب الحاكم من الجذر إلى البيان النهائي.
11. شغّل الاختبارات من `acceptance/TEST_CATALOG.csv`؛ `SEMANTIC_EVAL` يستخدم Rubric سلوكيًا ولا يفترض معنى صحيحًا مسبقًا.
12. لا تعتمد Opal منسقًا حاكمًا حتى `CAP-GO-01` = PASS لكل P0؛ Python fallback هو الافتراضي الآمن.

إذا احتجت قرارًا غير موثق: أنشئ `SPEC_GAP` وتوقف عن الجزء المتأثر.
