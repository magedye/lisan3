# Quran Lisan v1.1 — Migration & Reconciliation Report

`REPORT_TYPE = HISTORICAL_PROVENANCE_AND_RECONCILIATION`  
`TARGET_BASELINE = QURAN_LISAN_V1.1`

> هذه الوثيقة هي الموضع الوحيد في الحزمة الذي يسمح بالإشارات الفعالة إلى أرقام الإصدارات التاريخية. جميع الوثائق التشغيلية والمعيارية الأخرى تعتمد v1.1 فقط؛ تُذكر v1.0 وما قبلها هنا تاريخيًا لتتبع lineage.

## 1. Legacy Foundation Sources

| Legacy file | Bytes | SHA256 |
|---|---:|---|
| `Quran Lisan Appendix  Reverse v7.2 .md` | 41678 | `0c2752d0d085e16fc30c6b3032e01a4ccc5b6eade0cab0a1e8d80887af906d72` |
| `Quran Lisan Appendix  Tools v7.md` | 47306 | `1aa1c59c7f90085b636d6cb773d84ee39970637566f8dd6e40a6e078e8ffcf25` |
| `Quran Lisan v7.1 — Master Protocol.md` | 118100 | `94ded5f3a0fdb28882914fc5cf88cc401ede3335fc33382bc6273377239b6a24` |
| `Quran Lisan v7.1 — Review & Hardening Memo.md` | 1973 | `c4dce1a609cd0faa959c293549c99fedd037d6b07c166b7bae312942ee82f755` |
| `Quran Lisan v7.1 — Runtime Kernel.md` | 8474 | `f2c1d6cd1b1853e9531da84a2a583dd5836f38aa1335f773f99ec41f74b94d2b` |
| `Quran Lisan v7.2  Appendix Master Research Question Matrix.md` | 33561 | `0650ab70b1bc7279781bc25e3313001b181b6eb44ced0c341f31c41f85eef7eb` |

## 2. File-to-file migration map

### 2.1 `Quran Lisan v7.1 — Master Protocol.md`
موزع إلى:
- M01: القواعد العليا، authority، Root Unity، evidence discipline، Blind Lab، epistemic model.
- A01: Root Unity/core tests.
- A02: structural/grammar/morphology/distribution/participants.
- A03: coverage/absence/citation integrity.
- A04: Claim Evidence Ledger/atomicity/derived support.
- A05: freeze/prediction/holdout/falsification/competitors.
- A06: purpose/result/function/benefit/wisdom/worldly impact.
- A07: event/practical/attentional/transformation.
- A08: text/open/human/silence.
- A10: bottom-up verse/scene.
- A11: three axes/failure/purity/completeness/internal lock.
- A12: source roles/tools/post-lock.
- A13: sensitive topics.
- A14: output/templates/options.
- C01/C02: operational kernel/cards.
- T01: protocol regression suite.

### 2.2 `Quran Lisan v7.1 — Review & Hardening Memo.md`
أُدخلت قراراته كقيود معيارية:
- modern ideological projection → A13.
- no chain-of-thought dependency → M01/C01/A14.
- inferred wisdom lock & purpose marker check → A06.
- textual silence correction → A03+A08.
- purpose/result overlap → A06.
- grammar/morphology firewall، no-slot-filling، causal/teleological guards، claim atomicity، derived support ceiling، absence gate، external metadata guard، empirical effect guard، mental-state projection → الملحقات المختصة.

### 2.3 `Quran Lisan v7.1 — Runtime Kernel.md`
أعيد بناؤه في C01 دون جعله authority أعلى من M01. بقي صغيرًا، مع `CORE_KERNEL + APPLICABLE_MODULES` وPre-output gate.

### 2.4 `Quran Lisan Appendix Reverse v7.2.md`
أصبح A09. حُفظت العائلات والاختبارات والبوابات والسجل والمخرجات وأمثلة failure/regression، مع إزالة قسم تاريخ التغييرات من النسخة التشغيلية وإبقائه هنا فقط.

### 2.5 `Quran Lisan v7.2 Appendix Master Research Question Matrix.md`
أصبح R02 مرجعًا كاملًا للأسئلة. حافظت الأسئلة على كونها مرجعية لا mandatory slot-filling، وربطت بـA01–A14.

### 2.6 `Quran Lisan Appendix Tools v7.md`
المحتوى الداخلي كان معنونا `Quran Lisan Tools v7.3`، ولذلك عومل بوصفه المصدر الأدواتي الأحدث في legacy set. أصبح A12، وحُفظت عائلات corpus/root/construction/relations/discourse/scene/computation/validation، مع إضافة Tool Activation Registry الموحد المطلوب في v1.0.

## 3. Reconciliation decisions

### MR-D01 — Root Unity contradiction
**Legacy tension:** Master v7.1 أعلن Root Unity مسلّمة منهجية؛ Tools v7.3 صاغه في موضع باعتباره «فرضية قابلة للنقض».  
**Resolution:**  
- `ROOT_UNITY = METHODOLOGICAL_AXIOM` في Quran Lisan.  
- `ROOT_AXIAL_MEANING` المحدد لكل جذر = research hypothesis/finding قابل للاختبار والنقض وقد يبقى `UNRESOLVED`.  
هذا يحفظ المبدأ الحاكم ويمنع تحصين core المرشح من النقد.

### MR-D02 — Antonym acceptance
**Legacy tension:** Master v7.1 احتوى صياغة مبكرة تسمح بإثبات التقابل بشروط دعم أضعف («واحد على الأقل»)، بينما Reverse v7.2 شدد الشروط الضرورية.  
**Resolution:** A09 يعتمد شروطًا ضرورية: domain، relation classification، participant/construction control، alternatives/third-term/counterevidence/scope/direct cross-check. مؤشرات coupling/parallelism وغيرها داعمة وليست بدائل.

### MR-D03 — Mental activation
أُزيل أي احتمال لاعتبار التبادر test إثبات. أصبح `candidate generator / post-discovery description` فقط في A01.

### MR-D04 — Silence vs Open Space
دُمجت Hardening corrections: إثبات عدم التحديد/الغياب يخضع A03 أولًا، ثم فتح المجال يخضع بوابة مستقلة A08. `NOT_SPECIFIED ≠ TEXTUAL_OPEN_SPACE`.

### MR-D05 — Structure/semantics firewall
جميع التسميات النحوية/الصرفية/البلاغية أصبحت structural observations أولًا. semantic function تحتاج distribution/context test في A02.

### MR-D06 — Purpose stack
فُصلت رسميًا `EXPLICIT_PURPOSE / EXPLICIT_RESULT / SUPPORTED_FUNCTION / SUPPORTED_BENEFIT / INFERRED_WISDOM`; marker لا يحسم function. overlap يسمح `SAME_TEXTUAL_BASIS`.

### MR-D07 — Epistemic axes
احتفظ الفصل الصارم: `RESULT_STRENGTH ≠ RESEARCH_COMPLETENESS ≠ INDEPENDENT_VERIFICATION`; مراجعة same-model ليست independent replication.

### MR-D08 — Computational tooling
حُسمت سلطة الأدوات: retrieval/embeddings/graphs/LLM تولد candidates ولا تمنح Quranic evidence أو lock. أضيف contract موحد لكل أداة.

### MR-D09 — Display modes
Legacy `EXECUTIVE/BALANCED/DEEP/EXHAUSTIVE` أعيدت إلى النظام المطلوب في baseline:
`CONCISE/BALANCED/DEEP/RESEARCH`. الفرق في البحث/العرض بقي محفوظًا.

### MR-D10 — User option IDs
أزيلت `[A]...[L]` التشغيلية لتجنب التصادم مع Appendix IDs، واعتمد `OPT-01...`.

### MR-D11 — Formal pause behavior
حُفظ مفهوم checkpoint والاستئناف، لكن لم يعد «طلب A/B» قاعدة معيارية للحزمة. عند حدود التنفيذ يحفظ checkpoint/partial verified state ولا يدعي completion. هذا سلوك تشغيلي لا مبدأ دلاليًا.

### MR-D12 — Version reset
v7.x تُعامل provenance تاريخي فقط؛ baseline الجديد `QURAN_LISAN_V1.1` وليس continuation numbering.

## 4. Rules removed or downgraded

| Legacy item | Disposition | Reason |
|---|---|---|
| «شرط دعم واحد يكفي» لبعض تقابلات antonym | REMOVED | superseded by hardened Reverse necessary conditions |
| dictionary antonym as Blind-Lab authority | REMOVED | violates internal source isolation |
| POS sameness as necessary opposition condition | REMOVED | not semantically necessary |
| automatic purpose from grammatical label | REMOVED | structural label ≠ semantic function |
| automatic open space from silence | REMOVED | corrected by Hardening; separate gate required |
| automatic independence from repeated model review | REMOVED | violates verification semantics |
| forced template slot completion | REMOVED | `NOT_ESTABLISHED/NOT_APPLICABLE` are valid |
| fixed count of competitors/patterns | REMOVED | encourages artificial completion |
| old interactive [A]-[L] options | SUPERSEDED | replaced by `OPT-NN` |
| historical “what changed” sections inside active appendices | MOVED HERE | old versions may appear only in provenance |

## 5. Terminology normalization

- `ROOT_AXIAL_MEANING` = canonical technical identifier.
- root core/origin/nucleus/base/axial concept = aliases, not separate fields.
- `ROOT_LETTERS` remains distinct.
- `TEXTUAL_REQUIREMENT / NOT_SPECIFIED / TEXTUAL_OPEN_SPACE / HUMAN_IMPLEMENTATION / IMPORTED_SACRALIZATION` standardized.
- `CONCISE/BALANCED/DEEP/RESEARCH` standardized display modes.
- Cross references standardized as `[DOC-TYPE##]`.

## 6. New v1.0 appendices introduced to close real gaps

- A00 Governance/Registry/Dependency/Traceability.
- A14 Presentation/User Options.
- R01 Controlled Vocabulary.
- R03 Coverage/Cross-Reference Matrix.
- C03 Style/IDs/Composition Guide.
- T01 unified regression suite.
- MANIFEST + QA report.

هذه إضافات حوكمية/تنظيمية ضرورية للحزمة، لا قواعد دلالية مخترعة تناقض المصادر.

## 7. OPEN_DECISIONS

`NONE_BLOCKING_FOR_V1.1_BASELINE`.

قرارات بحثية مؤجلة وليست package blockers:
- تنفيذ Gold Standard studies الكاملة للجذور/المقارنات المدرجة في E01.
- أي benchmark لأدوات computational discovery يخص تطبيقًا بعينه ولا يدخل baseline المنهجي نفسه.

## 8. Legacy accounting

`ALL_LEGACY_FILES_ACCOUNTED_FOR = YES`.

كل source إما نُقل محتواه إلى ملف معياري/مرجعي/تشغيلي، أو نُقلت عناصره التاريخية إلى هذا التقرير، أو أُزيلت قاعدة لأنها نُسخت بصياغة أحدث موثقة أعلاه.

## v1.1 Hardening Integration — 2026-09-19

### المصادر الإضافية التي تمت دراستها
- `QURAN LISAN v1.1 — Persistent Agent Bootstrap, Research Runtime & Semantic Memory Protocol`.
- `Prompt For QURAN LISAN v1.2` (إعادة هيكلة tiered للـruntime، لا مصدر سلطة أعلى).
- `Lisan Quranic Semantic Extraction — Revised Skill`.
- `Lisan Quranic Semantic Extraction — Executive Protocol`.
- `Final-root-template` reference materials.
- `QURAN LISAN v2` agent prompt synthesis produced during reconciliation.

### أفكار دُمجت
1. `TARGET_CONTRACT` واختيار أضيق Analysis Unit.
2. `DISTINCTIVE_RESIDUE` بوصفه اختبار تمييز لا نواة مستقلة.
3. `ESSENTIAL_NEIGHBORS` بدل أعداد ثابتة/جيران تجميليين.
4. `OPERATIONAL_REJECTION_CONDITION` مع search space/method/confound/decision effect.
5. Coverage متعددة الأبعاد وstratified discovery sampling.
6. Research Record / Qualified Result / Derived Card separation.
7. Tool Reality، execution modes، deterministic/manual fallbacks، no fake validator claims.
8. Internal Result Snapshot قبل المقارنة الخارجية.
9. Illustrative Verse vs Decisive Context.
10. Semantic Boundary = `REQUIRED / PERMITTED / EXCLUDED / UNKNOWN` مع منع exclusion من الغياب وحده.
11. Semantic Memory governance بمحاور مستقلة: reliability/scope/conflict/lifecycle.
12. Dependency tracking + derived strength ceiling + revalidation on material upstream reopening.
13. Output cards and format charter مع Evidence Trace دون كشف private reasoning.
14. Multi-dimensional quality profile دون Overall Score افتراضي.

### أفكار لم تُعتمد كما وردت بسبب التعارض
- `Homonymy/Lexical Split/Multiple Root Cores` كحل نهائي داخل المنهج: **مرفوضة كقاعدة حاكمة** لأنها تتعارض مع `ROOT_UNITY`. حُفظت فقط كـ`USAGE_CLUSTER_HYPOTHESES` أو challenge للنواة الحالية؛ وعند تعذر الجامع تكون النتيجة `UNRESOLVED`.
- أي threshold عددي ثابت مثل «أكثر من 30 occurrence يكفي معه sampling»: لم يعتمد؛ استبدل بقاعدة sampling قائمة على diversity/materiality والـclaim scope.
- أي Status Registry خاص بمشروع/برنامج مضيف: لم يتحول إلى status معياري في Quran Lisan. أبقيت حالات المنهج الأصلية، مع السماح لـ`HOST_STATUS` منفصلًا.
- `ABSTRACT_ROOT_CORE` كنواة إضافية: لم يعتمد ككيان مستقل؛ تم تحويله إلى `ROOT_DEFINITION / ROOT_MEANING_EXPLANATION / ROOT_CONCEPT_MODEL` المشتقة من `ROOT_AXIAL_MEANING` الواحد.

### أثر التوافق
`v1.1` إصدار hardening تراكمي متوافق دلاليًا مع v1.0؛ لا يغير مبدأ Root Unity ولا سلطة القرآن ولا Blind Lab، لكنه يشدد شروط التفريد، النقض، الحفظ، traceability وعرض النتائج.

### إضافات تم التقاطها مباشرة من Final-root-template بعد فحص الحزمة
- `CUMULATIVE_RESEARCH_RECORD` كـartifact بحثي كامل ومصدر اشتقاق للعرض.
- `ROOT_CARD/TERM_CARD` كـ`DERIVED_READ_MODEL` بلا سلطة بحثية مستقلة.
- Machine schema: معنى غير مؤهل = `null`، وسبب المنع في status/blocking fields.
- `FORMAT_MIGRATION_ONLY ≠ METHODOLOGICAL_REQUALIFICATION`.
- deterministic derivation receipts وupstream snapshot/result hashes عند توفرها فعليًا.
- `STATUS_ONLY / CONTROLLED_CONCISE / EVIDENCE_TRACE / FULL_RESEARCH_REF` كمستويات rendering للبطاقات، منفصلة عن Display Modes الحوارية.
- Publication Handoff gates منفصلة عن الصحة الدلالية والقبول البشري.
- أدوار participants عامة أولًا؛ لا يفترض `AGENT/PATIENT` بلا دليل.
