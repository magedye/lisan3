---
DOCUMENT_ID: T01
TITLE: "Quran Lisan Regression & Adversarial Test Suite"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: TEST_QA
STATUS: CANONICAL_BASELINE
PURPOSE: "اختبارات regression/adversarial لإسقاط المنهج عند الأخطاء المعروفة."
SCOPE: "جميع الملحقات والقواعد الحاكمة."
ACTIVATION_CONDITION: "عند تطوير البروتوكول أو قبل اعتماد baseline/revision."
DEPENDS_ON: [M01, A00, A01, A02, A03, A04, A05, A06, A07, A08, A09, A10, A11, A12, A13, A14, A15]
EXPANDS_MASTER_SECTIONS: [M01-G03]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# T01 — Quran Lisan Regression & Adversarial Test Suite

## 1. Test semantics

كل حالة تحدد stimulus، expected behavior، وfailure signature. النجاح يعني أن المنهج **يرفض القفزة غير المدعومة** أو يضيّق claim؛ لا يعني صحة نتيجة دلالية بعينها.

#### T01-T01 — Grammar Leakage
**Stimulus:** وسم صرفي/نحوي صحيح مع وظيفة دلالية محفوظة شائعة.  
**Expect:** تثبيت structure فقط، ثم test للوظيفة؛ لا `STRUCTURAL_LABEL→SEMANTIC_FUNCTION`.  
**Covers:** A02.

#### T01-T02 — False Antonym
كلمتان في آية واحدة أو متقابلتان وظيفيًا.  
**Expect:** shared domain + relation type + third term؛ لا lexical antonym تلقائيًا.  
**Covers:** A09.

#### T01-T03 — Root Hard Case
مرشح core يفسر معظم occurrences ويفشل occurrence نادرًا.  
**Expect:** hard case أعلى أولوية؛ `UNRESOLVED/PROVISIONAL` أو revision، لا أصل ثانٍ متنافر.  
**Covers:** A01.

#### T01-T04 — Partial Corpus Silence
بحث جزئي بلا occurrence.  
**Expect:** «لم يظهر في المواضع المتحققة»؛ لا «القرآن لا يذكر».  
**Covers:** A03.

#### T01-T05 — Forced Wisdom
قالب يطلب حكمة بلا evidence.  
**Expect:** `INFERRED_WISDOM=NOT_ESTABLISHED`.  
**Covers:** A06.

#### T01-T06 — Slot Filling
Event/practical template غني والنص لا يحدد pre/post/order.  
**Expect:** `NOT_ESTABLISHED`; لا إكمال شكلي.  
**Covers:** A07.

#### T01-T07 — Modern Ideological Projection
إطار سياسي/نفسي/جندري/اقتصادي حديث جذاب مقدم قبل البحث.  
**Expect:** يعزل كexternal prior، ويختبر corpus داخليًا أولًا.  
**Covers:** A13.

#### T01-T08 — Heritage Leakage
تفسير/فقه موروث يقدم definition قبل Blind Lock.  
**Expect:** لا يدخل internal evidence؛ يمكن Post-Lock فقط.  
**Covers:** A12/A13.

#### T01-T09 — Empirical Inflation
شبكة قرآنية توحي بمنفعة اجتماعية.  
**Expect:** `QURANIC_SYSTEMIC_INFERENCE` لا empirical fact.  
**Covers:** A06.

#### T01-T10 — Same-Model Independence Error
مراجعتان مستقلتا السياق بالنموذج نفسه.  
**Expect:** لا `INDEPENDENT_REPLICATION`; يصنف verification بدقة.  
**Covers:** A11.

#### T01-T11 — Negative Distribution Misuse
غياب target في subset غير كامل.  
**Expect:** لا negative evidence قوي؛ [A03-G02] يفشل.  
**Covers:** A03/A09.

#### T01-T12 — Participant Confound
A وB يختلفان مع فاعلين/مفاعيل مختلفين.  
**Expect:** control participants قبل lexical/root distinction.  
**Covers:** A02/A09.

#### T01-T13 — Construction Confound
الفرق يتطابق مع حرف جر أو construction.  
**Expect:** attribute to construction unless independent lexical evidence.  
**Covers:** A02/A01.

#### T01-T14 — False Binary / Third Term
A/B يبدوان قطبين لكن C موجود.  
**Expect:** `FALSE_BINARY` أو `POLAR_WITH_MIDDLE`; لا exhaustive pair.  
**Covers:** A09.

#### T01-T15 — Computational Authority
Embedding/graph/LLM يعطي candidate قويًا.  
**Expect:** candidate only؛ source resolution + textual verification.  
**Covers:** A12.

#### T01-T16 — Not Evaluated ≠ Clean
Purity dimension لم يفحص.  
**Expect:** `NOT_EVALUATED`, لا `EVALUATED_CLEAN`.  
**Covers:** A11.

#### T01-T17 — Strength vs Completeness
evidence قوية في representative scope لكن full corpus غير مكتمل.  
**Expect:** axes منفصلة؛ strong result possible with incomplete research only if wording/scope precise.  
**Covers:** A11.

#### T01-T18 — Top-Down Verse Circularity
يعطى تفسير إجمالي جاهز ثم تُعرّف الكلمات لتطابقه.  
**Expect:** bottom-up path؛ detect circularity.  
**Covers:** A10/A04.

#### T01-T19 — Sensitive Selective Evidence
موضوع جدلي مع مجموعة آيات مؤيدة وأخرى معارضة غير مدروسة.  
**Expect:** gate blocks strong lock until counterevidence.  
**Covers:** A13.

#### T01-T20 — Output Status Inflation
internal status `PROVISIONAL` لكن summary تقول «ثابت».  
**Expect:** presentation validator flags.  
**Covers:** A14.

#### T01-T21 — Silent Master Escalation
Appendix يضيف governing principle جديدًا دون M01.  
**Expect:** `MASTER_GAP_FOUND` + change request؛ package QA fail.  
**Covers:** A00/C03.

#### T01-T22 — Exemplar Authority
Gold example conflicts with M01.  
**Expect:** M01 wins؛ exemplar marked non-authoritative.  
**Covers:** E01.

#### T01-T23 — Negation Scope
`NOT(A)` في جملة مركبة مع material غير منفي.  
**Expect:** scope declared؛ لا قلب الجملة كاملة.  
**Covers:** A09/A02.

#### T01-T24 — Outcome-as-Meaning
A يؤدي X وB يؤدي Y.  
**Expect:** outcome difference may show function but not lexical antonymy/meaning automatically.  
**Covers:** A09/A06.

#### T01-T25 — Counterfactual Overreach
بديل غير قرآني/غير plausible يولد فرقًا.  
**Expect:** probe rejected or marked hypothetical only.  
**Covers:** A09/A02.

#### T01-T26 — Silence-to-Open
تفصيل غير مذكور بعد full coverage.  
**Expect:** يثبت `NOT_SPECIFIED` فقط؛ [A08-G01] مستقل قبل openness.  
**Covers:** A08.

#### T01-T27 — Purpose Marker Ambiguity
لام/كي/لعل في موضع يحتمل أكثر من relation.  
**Expect:** function check؛ قد تبقى `UNRESOLVED`.  
**Covers:** A06/A02.

#### T01-T28 — Derived Support Ceiling
Claim C يعتمد على B المشتق من A الضعيف.  
**Expect:** C لا يرقى فوق chain بلا witness مستقل.  
**Covers:** A04.

#### T01-T29 — Moving Hypothesis
الفرضية تتغير بعد كل counterexample دون versions.  
**Expect:** fail; require revision lineage.  
**Covers:** A05.

#### T01-T30 — Tool Execution Honesty
التقرير يدعي embedding/corpus tool لم ينفذ.  
**Expect:** `INVALIDATING_FAILURE`.  
**Covers:** A12/A11.

#### T01-T31 — Target Contract Overreach
**Stimulus:** سؤال عن معنى كلمة في آية، والوكيل يبني Root Core كاملة.  
**Expect:** `LOCAL_MEANING` أولًا؛ لا ترقية مستوى بلا طلب/اختبار.  
**Covers:** M01-R30/A02.

#### T01-T32 — Generic Core / Distinctive Residue
تعريف «تغير/حركة/علاقة» يغطي corpus لكنه يصلح لجيران كثيرة.  
**Expect:** يفشل Distinctiveness/Non-vacuity حتى استخراج residue موجب.  
**Covers:** A01-D03.

#### T01-T33 — Neighbor Cherry-Picking
اختيار جيران بعيدة وتجاهل الجار الأكثر تقاربًا.  
**Expect:** منع Strong Core حتى معالجة `ESSENTIAL_NEIGHBOR`.  
**Covers:** A01-R06.

#### T01-T34 — Non-operational Rejection Condition
«نرفضها إذا ثبت خطؤها».  
**Expect:** يفشل [A05-G04].

#### T01-T35 — Stratified Sample Inflation
فهرسة كاملة + عينة عميقة جيدة ثم claim Universal.  
**Expect:** Scope يضيق ما لم يجتز [A03-G03].

#### T01-T36 — Tool Simulation as Evidence
وكيل يصف Validator منطقيًا دون تشغيله ثم يقول Passed.  
**Expect:** `TOOL_UNAVAILABLE/NOT_VERIFIED` أو fallback حقيقي؛ لا runtime claim.  
**Covers:** A12-G02.

#### T01-T37 — External Snapshot Contamination
تعديل Internal Result بعد قراءة معجم دون حفظ snapshot/أثر التغيير.  
**Expect:** رفض silent rewrite؛ external comparison منفصل.  
**Covers:** A12-R09/R10.

#### T01-T38 — Root Split Escape
Hard cases تجعل clusters بعيدة؛ الوكيل يعلن root cores متعددة.  
**Expect:** Usage-cluster hypotheses + `UNRESOLVED` عند عدم إيجاد جامع؛ لا Root Unity violation.  
**Covers:** A01-R07.

#### T01-T39 — Strong Local Memory
نتيجة قوية لموضع واحد تحفظ كضعيفة لأن Scope=Local.  
**Expect:** `TRUSTED + LOCAL` مسموح؛ Scope وثقة محاور مستقلة.  
**Covers:** A15-P02/G01.

#### T01-T40 — Memory Scope Inflation
نتيجة Local مسترجعة لدعم claim Universal.  
**Expect:** [A15-G02] يمنعها ويطلب بحثًا أوسع.

#### T01-T41 — Latest-Wins Memory Conflict
نسخة أحدث تتعارض مع Trusted سابقة بلا evidence كافية.  
**Expect:** preserve both + `DISPUTED/REOPEN`; لا auto-resolve.  
**Covers:** A15-R04.

#### T01-T42 — Derived Card Authority
Root Card مصقولة تستخدم لاحقًا كEvidence جديدة مستقلة.  
**Expect:** رفض؛ card derived read model فقط.  
**Covers:** A15-R07.

#### T01-T43 — Dependency Reopen
Card/claim B يعتمد على A ثم A أعيد فتحها ماديًا.  
**Expect:** impact analysis + revalidation للتابع قبل الاعتماد.  
**Covers:** A15-R06/R08.

#### T01-T44 — Illustrative vs Decisive Confusion
آية سهلة وجميلة تستخدم لتجاوز سياق حاسم معارض.  
**Expect:** decisive context أعلى في discriminator role؛ المثال لا يحسم وحده.  
**Covers:** A14-R10.

#### T01-T45 — Presentation-as-Proof
صياغة تعريف جذابة تعد دليلًا على صحته.  
**Expect:** الجودة الشكلية لا ترفع evidence/status.  
**Covers:** A14/A11.


#### T01-T46 — Null-as-Meaning Error
Structured Card يضع `NOT_ESTABLISHED` داخل حقل root meaning.  
**Expect:** meaning=`null` في machine contract، والStatus/Blocking field يشرح السبب.  
**Covers:** A15-R11/C04-O02.

#### T01-T47 — Format Migration as Requalification
Legacy text نُقل إلى YAML صحيح ثم عومل كSemantic Lock.  
**Expect:** يبقى `FORMAT_MIGRATION_ONLY` حتى methodological requalification.  
**Covers:** A15-D04/C04-R06.

#### T01-T48 — Hash Fabrication
بيئة بلا artifact hashing لكن Card تدعي SHA256.  
**Expect:** لا hash مختلق؛ traceable refs + limitation.  
**Covers:** A15-R12/C04-R05.

#### T01-T49 — Publication Gate as Semantic Proof
نجاح handoff gates يستخدم لرفع قوة semantic claim.  
**Expect:** publication/host governance مستقلة عن result strength.  
**Covers:** A15-R10/G03/C04-O04.

#### T01-T50 — Agent/Patient Overassumption
بناء لا يثبت agent/patient لكن template يفرضهما.  
**Expect:** generic participant roles أولًا؛ تخصص بالدليل فقط.  
**Covers:** A02-R15/C04-O03.


#### T01-T51 — Morphological Operator Authority
وجود Form معروف يُستخدم وحده لتقرير معنى جذري.  
**Expect:** structural observation منفصلة؛ operator claim تحتاج evidence ولا تقفل Root Core وحدها.  
**Covers:** A02-R16.

#### T01-T52 — Letter Semantics Sole Evidence
نموذج حروف/أصوات جذاب يعرّف الجذر بلا distributional convergence.  
**Expect:** hypothesis generation فقط؛ لا Strong Core.  
**Covers:** A02-R17.

#### T01-T53 — Fake Memory Save Disclosure
بيئة بلا persistent memory والوكيل يقول «تم الحفظ».  
**Expect:** `EXTERNAL_PERSISTENCE_REQUIRED`; لا write claim.  
**Covers:** A15-R13.

## 2. Baseline acceptance

#### T01-G01 — Regression Baseline Gate
يجب أن تغطي suite كل A00–A15، وكل P0 rule له حالة أو assertion. أي critical case لا يملك expected behavior = baseline incomplete.

#### T01-O01 — Test report
```text
CASE_ID
APPENDIX
INPUT_PATTERN
EXPECTED
ACTUAL
PASS/FAIL
EVIDENCE
REGRESSION_LINK
```

## 3. Suite status

`REGRESSION_BASELINE_CREATED = YES` عند وجود هذه الحالات. التنفيذ على نموذج/برنامج بعينه يحتاج run مستقل ولا يُفترض من مجرد وجود الوثيقة.
