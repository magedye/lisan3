---
DOCUMENT_ID: A10
TITLE: "Bottom-Up Verse Analysis & Scene Reconstruction Protocol"
VERSION: 1.1
BASE_PROTOCOL: QURAN_LISAN_V1.1
DOCUMENT_CLASS: NORMATIVE_APPENDIX
STATUS: CANONICAL_BASELINE
PURPOSE: "بناء معنى الآية من أسفل إلى أعلى وفصل طبقات المعنى وإعادة بناء المشهد دون اختراع."
SCOPE: "تحليل آية أو مقطع محلي."
ACTIVATION_CONDITION: "RESEARCH_TARGET=VERSE أو passage يحتاج synthesis."
DEPENDS_ON: [M01, A01, A02, A04, A07]
EXPANDS_MASTER_SECTIONS: [M01-R19, M01-D03]
DOES_NOT_OVERRIDE: M01
SUPERSEDES: "Legacy foundation material as mapped in Migration Report"
---

# A10 — Bottom-Up Verse Analysis & Scene Reconstruction Protocol

## 1. Canonical order

#### A10-R01 — Bottom-Up Verse Analysis
```text
STRUCTURE
→ KEY TERMS
→ LEXICAL RESULTS
→ LAYER ATTRIBUTION
→ PARTICIPANTS
→ RELATIONS
→ EVENT MODEL
→ CONTEXT
→ VERSE SYNTHESIS
```
يمكن إدخال distribution/competing models/falsification حيث يلزم، لكن لا يبدأ التحليل بتفسير إجمالي جاهز ثم يجعل الكلمات تثبته.

#### A10-G01 — Verse Entry Gate
قبل synthesis: نص الآية ومرجعها متحققان، key references/resolution آمنة، claims lexical الأساسية لها evidence status، والنطاق local معلن.

## 2. Structure

#### A10-R02 — Structural pass
حدد الجملة، condition، agent/patient، attachments، pronouns، negation، exception، order، temporality، وboundaries. أي عنصر unresolved يبقى كذلك.

#### A10-R03 — Key Terms
للمفردات المحورية استخدم نتائج lexical/root مستقلة عندما يكون الادعاء يتجاوز local observation؛ لا تستخرج root core من الآية وحدها.

## 3. Layers of verse meaning

#### A10-D01 — DIRECT_TEXTUAL_MEANING
ما يبنيه النص مباشرة بعد تحقق بنيته.

#### A10-D02 — SEMANTIC_CLARIFICATION
ما تضيفه دراسة الألفاظ وتوزيعها إلى فهم اللفظ في الموضع.

#### A10-D03 — INFERENCE
نتيجة مركبة غير ملفوظة مباشرة لكنها مدعومة بسلسلة معلنة.

#### A10-D04 — OPEN_POSSIBILITY
قراءة يسمح بها النص لكنها غير مثبتة وحدها.

#### A10-D05 — EXTERNAL_ADDITION
معلومة من خارج القرآن/Blind result، لا تدمج في الداخلي.

#### A10-R04 — No layer collapse
لا تعرض inference كـdirect، ولا external addition كـQuranic meaning.

## 4. Scene reconstruction

#### A10-O01 — Scene Model
```text
ACTORS =
OBJECTS =
LOCATION =
CONSTRAINTS =
ACTION =
PROBLEM =
CHANGE =
RESULT =
UNSUPPORTED_FIELDS =
```

#### A10-G02 — Scene Evidence Gate
لا تُنشئ actor motive، mental state، pre-state، causal link، hidden object، أو post-state بلا evidence. الحدث المتصور ليس دليلًا إضافيًا.

#### A10-R05 — Dialogue
في الحوار: حدد speaker/addressee/question/response/non-response/reference shift قبل inference pragmatic.

#### A10-R06 — Repeated narrative
عند تكرر الحدث، لا تصنع «نسخة مركبة» تمحو differences؛ استخدم differences كcontrastive evidence محتمل.

## 5. Context

#### A10-R07 — Local before broad
السياق المحلي يحدد relation، ثم يوسع إلى passage/surah/network فقط إذا كان ذلك مطلوبًا ومتحققًا.

#### A10-R08 — Context does not redefine lexical core
الوظيفة الحجاجية أو السردية لا تصبح تلقائيًا semantic component للفظ.

## 6. Synthesis

#### A10-O02 — Verse Synthesis
```yaml
VERSE_RESULT:
  direct_textual_meaning:
  semantic_clarification:
  inference:
  open_possibility:
  external_addition:
  participants:
  relations:
  event_model:
  scene:
  counterevidence:
  what_the_verse_does_not_prove:
  epistemic_status:
```

#### A10-F01 — TOP_DOWN_CIRCULARITY
تفسير جاهز → meanings → same verse confirms.

#### A10-F02 — SCENE_FILLING
إكمال المشهد بعناصر متوقعة غير مذكورة.

#### A10-F03 — LEXICAL_OVERLOAD
تحميل اللفظ بكل وظيفة الآية.

#### A10-RC01 — Ambiguous pronoun
مرجع حاسم غير محسوم → synthesis narrowed.

#### A10-RC02 — Event result without cause
sequence/result لا يثبت cause/purpose.

---

## نهاية الملحق

```text
INTEGRATION_RULES = M01 verse rules + A01/A02/A04/A07
OUTPUT_CONTRACT = VERSE_RESULT
FAILURE_MODES = top-down circularity, scene filling, lexical overload
REGRESSION_CASES = A10-RC01..02; T01 verse cases
REOPEN_IF = reference resolution/new lexical result/context evidence
END_OF_APPENDIX = A10
```
