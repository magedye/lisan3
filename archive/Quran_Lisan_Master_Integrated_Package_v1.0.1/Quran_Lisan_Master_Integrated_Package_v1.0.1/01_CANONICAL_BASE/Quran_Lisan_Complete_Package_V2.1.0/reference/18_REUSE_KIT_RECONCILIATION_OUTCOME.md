# تقرير مصالحة NEW_LISAN_PROJECT_REUSE_KIT

**الإصدار المدمج في V2:** 2.0.0  
**الحالة:** `V2_FINAL_COMPREHENSIVE_BASELINE / READY_FOR_BLIND_IMPLEMENTATION`  
**التاريخ:** 2026-09-05

## 1. مصدر المصالحة
- Lisan3 reviewed HEAD: `5667528297f4f0f3e4b245fa47cec60e992f1798`.
- حزمة الوكيل: 50 مرشحًا؛ `ADAPT`=24, `REUSE_AS_IS`=12, `REFERENCE_ONLY`=5, `OPEN_QUESTION`=3, `DO_NOT_REUSE`=6.
- قاعدة القرار: الاحتفاظ بما يحسن سلامة المصدر/الدليل والفصل والنقض والتتبع دون إعادة حوكمة Lisan3 الثقيلة.

## 2. النتيجة العامة
- تم تبني/تكييف كل P0 المفيد منهجيًا: analysis unit, layering, rejection conditions, counterevidence, coverage vector, lexical branches, exact source identity, field roles, Blind Lab concepts, ResearchRun lite, execution receipts, strict schemas, Tool Gateway, exact retrieval, EvidenceResolver boundary, hypothesis freeze/influence log, terminology.
- تم رفض نقل Purity/Internal Lock monolith، four-axis status، Steward، publication/release cards، LangGraph، وQAC fixture runtime.
- vector/graph/embedding spaces بقيت deferred/candidate-only.
- Gem/Opal بقيت واجهات/تنسيق مشروطة بسبب غياب إثبات Lisan3 وبسبب كون Opal حاليًا تجربة Google Labs.

## 3. المصفوفة الكاملة
| ID | Candidate | Kit Class | Final disposition | Priority |
|---|---|---|---|---|
| C01 | Resolve analysis unit before research | ADAPT | ADOPTED_ADAPTED | P0 |
| C02 | Quran-internal induction first | REUSE_AS_IS | ADOPTED | P0 |
| C03 | Layered local-meaning equation | REUSE_AS_IS | ADOPTED | P0 |
| C04 | Observation → Interpretation → Hypothesis → Claim | ADAPT | ADOPTED_ADAPTED | P0 |
| C05 | H1/H2/C0 competing set | ADAPT | ADOPTED_ADAPTED | P0 |
| C06 | Distinctive residue | ADAPT | ADOPTED_ADAPTED | P1 |
| C07 | Operational rejection condition | REUSE_AS_IS | ADOPTED | P0 |
| C08 | Counterevidence + unresolved cases + failed predictions | REUSE_AS_IS | ADOPTED | P0 |
| C09 | Multidimensional coverage | ADAPT | ADOPTED_ADAPTED | P0 |
| C10 | Stratified sampling with declared limits | REUSE_AS_IS | ADOPTED | P1 |
| C11 | Semantic branches and no forced unity | ADAPT | ADOPTED_ADAPTED | P0 |
| C12 | Definition/Meaning/Concept separation | ADAPT | ADOPTED_ADAPTED | P1 |
| C13 | Byte-bound Quran/corpus identity | REUSE_AS_IS | ADOPTED | P0 |
| C14 | Source role and field-level admission | REUSE_AS_IS | ADOPTED | P0 |
| C15 | Exact Tanzil/QAC lifecycle statuses | REFERENCE_ONLY | REFERENCE/DEFERRED | P2 |
| C16 | Token/segment structural annotation boundary | ADAPT | ADOPTED_ADAPTED | P0 |
| C17 | Blind Lab source isolation | ADAPT | ADOPTED_ADAPTED | P0 |
| C18 | Blocked access ≠ actual contamination | REUSE_AS_IS | ADOPTED | P1 |
| C19 | Pretrained-knowledge contamination control | OPEN_QUESTION | RISK_CONTROL_ADOPTED; ABSENCE_NOT_CLAIMED | P0 |
| C20 | Post-analysis external comparison | ADAPT | ADOPTED_ADAPTED | P0 |
| C21 | Persistent ResearchRun | ADAPT | ADOPTED_ADAPTED | P0 |
| C22 | AI execution record | ADAPT | ADOPTED_ADAPTED | P0 |
| C23 | Strict structured contracts with Pydantic | REUSE_AS_IS | ADOPTED | P0 |
| C24 | Pydantic AI | ADAPT | ADOPTED_ADAPTED | P1 |
| C25 | Deterministic fake/test provider | REUSE_AS_IS | ADOPTED | P1 |
| C26 | Controlled ToolDispatcher | ADAPT | ADOPTED_ADAPTED | P0 |
| C27 | Provider abstraction and degraded mode | ADAPT | ADOPTED_ADAPTED | P1 |
| C28 | SQLite local persistence | ADAPT | ADOPTED_ADAPTED | P1 |
| C29 | Exact/FTS retrieval first | REUSE_AS_IS | ADOPTED | P0 |
| C30 | Vector results as candidates | ADAPT | ADOPTED_ADAPTED | P1 |
| C31 | Six separate embedding spaces | OPEN_QUESTION | CAPABILITY_GATE/DEFERRED | P2 |
| C32 | Benchmark-before-model adoption | ADAPT | ADOPTED_ADAPTED | P1 |
| C33 | Rebuildable graph projection | REFERENCE_ONLY | REFERENCE/DEFERRED | P3 |
| C34 | NetworkX analysis | REFERENCE_ONLY | REFERENCE/DEFERRED | P3 |
| C35 | EvidenceResolver boundary | ADAPT | ADOPTED_ADAPTED | P0 |
| C36 | Typed RetrievalCandidate | REUSE_AS_IS | ADOPTED | P1 |
| C37 | Lisan3 Purity/Internal Lock gates as a whole | DO_NOT_REUSE | REJECTED | P0 |
| C38 | Four independent official status axes | DO_NOT_REUSE | REJECTED | P1 |
| C39 | Steward role/command authority | DO_NOT_REUSE | REJECTED | P3 |
| C40 | Governance proposals + transitive invalidation | REFERENCE_ONLY | REFERENCE/DEFERRED | P2 |
| C41 | Publication/review workflow | DO_NOT_REUSE | REJECTED | P3 |
| C42 | Promptfoo methodology eval concept | ADAPT | ADOPTED_ADAPTED | P1 |
| C43 | Hypothesis/property/mutation/contract test stack | REFERENCE_ONLY | REFERENCE/DEFERRED | P2 |
| C44 | Initial hypothesis freeze + influence log | ADAPT | ADOPTED_ADAPTED | P0 |
| C45 | Six-layer result package | ADAPT | ADOPTED_ADAPTED | P1 |
| C46 | Legacy release/public/card authority fields | DO_NOT_REUSE | REJECTED | P3 |
| C47 | Gem conversational interface | OPEN_QUESTION | ADOPTED_AS_INTERFACE_WITH_CAPABILITY_LIMITS | P0 |
| C48 | Opal workflow/orchestration | ADAPT | ADOPTED_CONDITIONALLY_CAP-GO-01 | P0 |
| C49 | LangGraph/second workflow system | DO_NOT_REUSE | REJECTED | P3 |
| C50 | Governed terminology system | ADAPT | ADOPTED_ADAPTED | P0 |

## 4. أهم التغييرات على v0.9
1. Source identity أصبح field-level/stage-level لا source label فقط.
2. EvidenceRelation وExecutionReceipt وCompletenessProfile أصبحت سجلات P0.
3. أضيف LexicalUnitHypothesis/no-forced-unity إلى قلب المفهوم الجذري.
4. أضيف hypothesis freeze + external influence lineage.
5. exact/FTS first أصبح قرارًا نهائيًا؛ vector/graph deferred.
6. QAC runtime الحالي رفض؛ structural qualification صار Gate مستقل.
7. Lisan3 governance الثقيلة رفضت صراحةً.
8. Opal خُفِّض من منصة متوقعة إلى orchestration experimental capability-gated.

## 5. أثر Google الحالي على القرار
وفق التوثيق الرسمي المراجع في 2026-09-05، Gems from Google Labs powered by Opal ميزة تجريبية، إنشاء/تحريرها حاليًا عبر الويب وعلى الكمبيوتر وبالإنجليزية ومع حساب Google شخصي، وOpal Agent Mode يدعم routing/memory/tools. لذلك لا يجوز جعل Opal system-of-record أو نقطة إنفاذ وحيدة؛ يظل المحرك المستقل الحاكم.
