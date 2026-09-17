# V7.1 Mandatory Production Readiness Regressions

الحالة: `ACTIVE / EXECUTABLE` عبر `11_VALIDATION/scripts/run_v7_regressions.py` وبوابة الحزمة.

| ID | السلوك المحمي | Expected behavior |
|---|---|---|
| V71-01 | Cumulative workflow | observations/H1-H2-C0 ثم Freeze ثم memory |
| V71-02 | Pre-Freeze protection | يرفض `REFERENCE_OPENED_TOO_EARLY` |
| V71-03 | Post-Freeze reuse | يقبل Claim قوية مع status/scope/provenance |
| V71-04 | External sovereignty | يرفض external semantic source داخل الاستقراء |
| V71-05 | Dependency propagation | يعيد downstream transitively |
| V71-06 | Markdown result | يرفض Run بلا `<RUN_ID>_CUMULATIVE_RESULT.md` |
| V71-07 | Mandatory sections | يفرض الأقسام 0–13 |
| V71-08 | Arabic terminology | يفرض الاسم العربي والمعرف والشرح |
| V71-09 | Public provenance | يرفض `PUBLISHABLE` بلا حقول المصدر |
| V71-10 | Public/research consistency | يرفض mismatch غير موسوم |
| V71-11 | LOCK_BLOCKED | يقيد claim ولا يوقف workflow |
| V71-12 | Operator scope | يمنع application أوسع من evidence scope |
| V71-13 | Independent audit | يبقى معزولًا وغير حاجب للإنتاج |
| V71-14 | Gloss leakage | يسمح بالحقل البنيوي ويمنع استخدام Gloss |
| V71-15 | Canon consistency | يمنع current-state `CANON_PENDING` بعد admission |
| V71-16 | Package integrity | Manifest/checksums/links/versions/schemas/authority |

هذه المجموعة Regression وValidator refinement؛ لم تنشئ Rule ID جديدًا.
