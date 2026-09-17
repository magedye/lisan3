# سجل القرارات النهائية وبوابات ما بعد الإصدار

**الإصدار المدمج في V2:** 2.0.0  
**الحالة:** `V2_FINAL_COMPREHENSIVE_BASELINE / READY_FOR_BLIND_IMPLEMENTATION`  
**التاريخ:** 2026-09-05

## 1. القرارات النهائية
| المعرف | القرار | الحالة |
| --- | --- | --- |
| DR-001 | المشروع مستقل عن Lisan3. | ACCEPTED |
| DR-002 | الاستقراء القرآني الداخلي هو المسار الأول. | ACCEPTED |
| DR-003 | AI يملك الترجيح الدلالي ولا يملك اختراع الدليل أو اليقين المطلق. | ACCEPTED |
| DR-004 | الفصل الطبقي بين الجذر/الوحدة المعجمية/الصيغة/التركيب/السياق إلزامي. | ACCEPTED |
| DR-005 | البدائل والنقض والحالات الصعبة أولية في النتيجة. | ACCEPTED |
| DR-006 | اختلاف المبنى يحفز البحث عن فرق ولا يثبت الفرق بذاته. | ACCEPTED |
| DR-007 | الذاكرة السابقة فرضية/مرجع وليست دليلًا بذاتها. | ACCEPTED |
| DR-008 | strength/completeness/independent verification مستقلة. | ACCEPTED |
| DR-009 | Skill=كيف، Agent=ماذا/متى، Tool=تنفيذ حقيقي. | ACCEPTED |
| DR-010 | البنية الهجينة ذات المحرك المستقل هي المعمارية النهائية المنطقية. | ACCEPTED |
| DR-011 | Gem واجهة مستهدفة؛ Opal طبقة workflow تجريبية مشروطة بـCAP-GO-01 ولا يحمل أي منهما SSOT. | ACCEPTED |
| DR-012 | الأوزان/العتبات الرقمية غير معتمدة حتى calibration. | ACCEPTED |
| DR-013 | المصطلحات الحاكمة جزء من المنهج الإصْداري. | ACCEPTED |
| DR-014 | العملية: التحليل الدلالي الاستقرائي؛ النتيجة: معنى/مفهوم مرجح؛ العرض: البيان الدلالي. | ACCEPTED |
| DR-015 | المفهوم الجذري كيان منظم والنواة الدلالية محتواه المركزي. | ACCEPTED |
| DR-016 | blind verification مشروط لا دائم. | ACCEPTED |
| DR-017 | exact/FTS first؛ vector/graph discovery مرشح لا Evidence/Confidence. | ACCEPTED |
| DR-018 | النص الأول: Tanzil Uthmani 1.1 Hafs, SHA-256 ac0724...667af، 6236 آية؛ لا تعدد قراءات في MVP. | ACCEPTED |
| DR-019 | QAC الحالي لا يعاد استخدامه Runtime؛ MVP يستخدم structural annotation محدودة موثقة، ومصدر scalable يحتاج qualification Gate. | ACCEPTED |
| DR-020 | البيان النبوي الصحيح مصدر خارجي ذو أولوية خاصة في comparison فقط افتراضيًا، وأثره مقيد بنطاقه. | ACCEPTED |
| DR-021 | runtime baseline: Python 3.12 + Pydantic v2 + SQLite/FTS5 + FastAPI Tool Gateway. | ACCEPTED |
| DR-022 | Pydantic AI مشروط فقط إذا لم تكف Gem/Opal أو احتجنا server-side model/tool orchestration. | ACCEPTED |
| DR-023 | لا يعاد استخدام Lisan3 Purity/Internal Lock، four-axis statuses، Steward، publication workflow. | ACCEPTED |
| DR-024 | أول إثبات منتج: root واحد + semantic neighbor واحد + held-out hard cases. | ACCEPTED |
| DR-025 | same-model multi-agent agreement لا يسمى independent evidence. | ACCEPTED |

## 2. بوابات لاحقة لا تمنع بدء التنفيذ
| المعرف | البوابة | القرار الافتراضي حتى الحسم |
| --- | --- | --- |
| GQ-001 | مصدر صرف/نحو واسع النطاق | لا توسيع corpus؛ استخدم MVP structural set فقط حتى qualification. |
| GQ-002 | calibration weights/thresholds | فئات وصفية + components؛ لا percentages للمستخدم. |
| GQ-003 | Gem/Opal production ownership | CAP-GO-01؛ عند الفشل Python engine owns orchestration. |
| GQ-004 | vector/graph | ممنوع adoption حتى benchmark يثبت recall/use-case gap. |
| GQ-005 | multi-reading | Hafs profile only حتى owner phase decision. |
| GQ-006 | multi-user/publication | single-researcher baseline؛ مؤجل. |
