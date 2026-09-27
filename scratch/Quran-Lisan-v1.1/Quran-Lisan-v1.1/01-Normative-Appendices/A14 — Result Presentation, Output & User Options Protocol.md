---
DOCUMENT_ID: A14
TITLE: "Result Presentation, Output & User Options Protocol"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "توحيد عرض النتائج للمستخدم دون إغراقه بالتفاصيل الداخلية أو طمس القيود."
SCOPE: "جميع المخرجات النهائية للمستخدم."
ACTIVATION_CONDITION: "كل جواب بحثي نهائي."
DEPENDS_ON: [M01, A11]
EXPANDS_MASTER_SECTIONS: [M01-R25, M01-R26, M01-R27]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A14 — Result Presentation, Output & User Options Protocol

## 1. Canonical output

#### A14-O01 — Primary Output Contract
بالقدر المنطبق وبالترتيب:
```text
PRIMARY_RESULT
WHAT_IS_TEXTUALLY_FIXED
SEMANTIC_ANALYSIS
EVIDENCE
COUNTEREVIDENCE
LIMITS
TEXT_OPEN_HUMAN_STATUS
EPISTEMIC_STATUS
USER_OPTIONS
```
لا يجب إظهار كل خانة إذا كانت غير مفيدة؛ `NO_SLOT_FILLING`.

#### A14-R01 — First screen
ابدأ بالنتيجة ونطاقها وحالتها، لا بسجل الإجراءات. القيود المادية تظهر قرب النتيجة لا في هامش بعيد.

#### A14-R02 — Fixed / Probable / Open / Rejected
اعرض تصنيفات واضحة:
- **ثابت نصيًا/مدعوم بقوة** بحسب status الفعلي.
- **مرجح/استقراء** عندما evidence غير مباشرة.
- **مفتوح/غير محسوم** عند `OPEN/UNRESOLVED`.
- **مرفوض حاليًا** للفرضية التي فشلت.
لا تستخدم certainty language أعلى من [A11-P01].

## 2. Display modes

#### A14-D01 — CONCISE
نتيجة + 2–4 أدلة/قيود + status.

#### A14-D02 — BALANCED
الافتراضي: النتيجة، أهم evidence/counterevidence، limits، text/open/human، three axes المختصرة.

#### A14-D03 — DEEP
المراحل الجوهرية، ledgers مختصرة، models، gates، unresolved.

#### A14-D04 — RESEARCH
أوسع سجل قابل للتدقيق: corpus، patterns، claims، alternatives، provenance، tool receipts، matrices.

`ANALYSIS_DEPTH ≠ DISPLAY_MODE`.

## 3. Formatting

#### A14-R03 — Tables
استخدم الجدول عندما توجد أبعاد مقارنة ثابتة (A/B، claim/evidence/status، detail/class). لا تستخدمه لنص طويل متشعب.

#### A14-R04 — Code blocks
تستخدم للعقود والحقول والحالات التقنية، لا لعرض نص قرآني طويل أو شرح طبيعي.

#### A14-R05 — Quran display
اعرض الشاهد القرآني بوضوح مع reference متحقق. لا تختلق التشكيل/الرقم. إذا لم يتحقق النص، لا تعرضه كاقتباس حاسم.

#### A14-R06 — Internal details
لا تعرض سلسلة التفكير الداخلية. اعرض evidence, checks, decisions, limitations، وهي كافية للتدقيق.

## 4. Templates

#### A14-O02 — Root Template
`PRIMARY_RESULT → ROOT_AXIAL_MEANING/STATUS → coverage → invariant → derivational mapping → hard cases → competing core → reverse → limits → three axes`.

#### A14-O03 — Word Template
`local/general result → distribution → construction/participants → neighbors → counterevidence → limits`.

#### A14-O04 — Word-in-Verse Template
`nearest contextual sense → root/form/construction contributions → participant roles → verse effect → what it does not prove`.

#### A14-O05 — Comparison Template
`shared domain → A/B distributions → overlap/divergence → substitution → third term → distinction status → NO_DIFFERENCE_ESTABLISHED if appropriate`.

#### A14-O06 — Verse Template
`direct textual meaning → semantic clarification → inference → open possibility → external addition → event/scene if applicable`.

#### A14-O07 — Practical Action Template
`entry → actions → restraints → boundaries → completion → not specified → open space → human implementation`.

#### A14-O08 — Reverse Template
relation/type/witness/domain/axis/what revealed/does not prove/third term/counterevidence/status.

#### A14-O09 — Gold Standard Template
research contract + coverage + claims/evidence ledger + hypotheses/falsification + specialized gates + result + three axes + reopen.

## 4.5 Research vs Presentation & derived cards

#### A14-D05 — DERIVED_PRESENTATION_CARD
`ROOT_CARD`, `TERM_CARD`, `VERSE_CARD`, و`COMPARISON_CARD` نماذج قراءة مشتقة من نتائج مؤهلة. لا تنشئ Evidence أو Claims أو Status ولا توسع Scope.

#### A14-R09 — Discovery vs Presentation
لا يعرض Discovery Log أو private reasoning كجواب نهائي. العرض يبين Evidence/Decision Trace القابل للمراجعة فقط. مسار العرض الطبيعي: `PRIMARY_RESULT → FIXED → ANALYSIS → KEY_EVIDENCE → COUNTEREVIDENCE/HARDEST_CASE → LIMITS → EPISTEMIC_STATUS`.

#### A14-R10 — Illustrative vs Decisive Contexts
افصل `ILLUSTRATIVE_VERSE` عن `DECISIVE_CONTEXT`. المثال التوضيحي يشرح النتيجة؛ السياق الحاسم يميز نموذجًا من منافسه أو يضع حدًا/ينقض فرضية. لا يمنح جمال المثال وزنًا حاسمًا.

#### A14-O10 — Root Card v1.1
عند الانطباق: `ROOT_AXIAL_MEANING`, `ROOT_DEFINITION`, `PLAIN_EXPLANATION`, `ROOT_CONCEPT_MODEL`, `SEMANTIC_BOUNDARY(REQUIRED/PERMITTED/EXCLUDED/UNKNOWN)`, `DISTINCTIVE_RESIDUE`, Essential Neighbors، Layer Separation، Local Realizations، Illustrative/Decisive contexts، Hardest Case، Counterevidence، Rejection Condition، Coverage، Quality Profile، Three Axes، Limits/Reopen.

#### A14-O11 — Term Card v1.1
يفصل `LEXEME_LEVEL_MEANING` عن `LOCAL_MEANING` ويعرض Root/Form/Construction/Participant/Context contributions، Distribution، Neighbors، Boundary، Evidence/Counterevidence، Scope وReopen.

#### A14-O12 — Verse Card v1.1
يعرض `DIRECT_TEXTUAL_MEANING`, Structure, Key Terms, Lexical Results, Participants, Relations, Event Model, Semantic Clarification, Inference, Open Possibility, Text/Open/Human, External Addition, Counterevidence, Limits, Three Axes.

#### A14-O13 — Evidence Trace
في `DEEP/RESEARCH` يجوز عرض:
```text
[E1] witness → SUPPORT → CLAIM-01
[E2] witness → LIMIT → CLAIM-01
[E3] decisive context → CHALLENGE → H2
```
وهو trace أدلة لا Chain-of-Thought.

#### A14-R11 — Format charter
- العربية الفصيحة افتراضيًا؛ Technical ID يظهر بين قوسين عند أول ذكر عند الحاجة.
- الاستشهاد: `﴿النص﴾ (السورة: رقم)` بعد التحقق.
- الجداول للمقارنة/الحالة-القيمة، لا للسرد.
- `NOT_ESTABLISHED` يظهر إذا كان مهمًا؛ `NOT_APPLICABLE` يحذف غالبًا.
- لا تستخدم length targets كحدود صلبة تضعف سلامة التحليل.

## 5. User options

#### A14-R07 — Option IDs
لا تستخدم `[A]/[B]/[C]`. استخدم:
`OPT-01`, `OPT-02`, `OPT-03`...
حتى لا تتعارض مع Appendix IDs.

#### A14-R08 — Useful options only
اعرض فقط خيارات تالية ذات قيمة مثل: توسيع corpus، فحص root، deep counterevidence، post-lock comparison، حفظ study. لا تملأ قائمة ثابتة.

#### A14-EX01 — Example options
```text
OPT-01 — توسيع فحص الحالات الصعبة.
OPT-02 — مقارنة اللفظ بأقرب جار دلالي.
OPT-03 — فتح مقارنة خارجية بعد تثبيت النتيجة الداخلية.
```

## 6. Presentation failures

#### A14-F01 — DETAIL_FLOOD
إغراق المستخدم بسجل داخلي يطمس النتيجة.

#### A14-F02 — LIMIT_BURIAL
وضع قيد يغير معنى النتيجة في نهاية بعيدة.

#### A14-F03 — STATUS_INFLATION
ترجمة `PROVISIONAL` إلى «ثابت».

#### A14-RC01 — Concise but sensitive
العرض مختصر لكن analysis deep؛ يجب أن تبقى القيود المادية ظاهرة.

#### A14-RC02 — Empty options
لا تعرض options غير مفيدة لمجرد contract.

---

## نهاية الملحق

```text
INTEGRATION_RULES = M01 presentation + A11 statuses
OUTPUT_CONTRACT = PRIMARY_RESULT contract + task templates
FAILURE_MODES = detail flood, buried limits, status inflation
REGRESSION_CASES = A14-RC01..02; T01 output cases
REOPEN_IF = new display requirement/status vocabulary/user workflow
END_OF_APPENDIX = A14
```
