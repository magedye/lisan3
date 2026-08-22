# LISAN_TOOLING_ADOPTION_REFERENCE.md

## Lisanapp — Tooling, Frameworks & Reuse Adoption Reference

### Purpose

هذا المرجع يحدد الأدوات والمشاريع المعتمدة أو المرشحة للاستخدام في **Lisanapp**، ومتى يسمح باستخدام كل منها، وما الدور المحدد لها.

الهدف:

- منع تضخم المكدس التقني.
- منع تكرار وظائف موجودة بأدوات متعددة.
- ضمان استخدام الأدوات في طبقتها الصحيحة.
- منع تحويل أداة مساعدة إلى مصدر سلطة معرفية.
- تسهيل قرارات الوكلاء في مراحل التنفيذ والاستئناف.
- الحفاظ على Lisanapp كتطبيق محلي بسيط من نوع **Modular Monolith**.

---

# 1. حالات الاعتماد

استخدم الحالات التالية حرفياً:

| الحالة | المعنى |
|---|---|
| `ACTIVE_BASELINE` | معتمد ومستخدم في المشروع الآن |
| `ADOPT_NEXT` | معتمد مبدئياً ويجب إدخاله عند الوصول إلى مرحلته |
| `APPROVED_FOR_EVALUATION` | يسمح بعمل Spike/تقييم قبل الاعتماد النهائي |
| `CONDITIONAL_LATER` | لا يستخدم إلا إذا تحقق Trigger واضح |
| `LAB_ONLY` | يستخدم للاختبار/التقييم ولا يدخل Runtime الإنتاجي |
| `PENDING_ADMISSION` | مصدر/أداة مرشحة تحتاج Admission رسمي قبل اعتمادها |
| `DO_NOT_ADOPT_NOW` | لا تستخدم حالياً إلا بقرار معماري جديد |

---

# 2. قاعدة حاكمة

وجود أداة في هذا المرجع لا يجعلها Authority.

الترتيب دائماً:

```text
Canonical Requirements / Methodology / Governance
        ↓
Registries / Schemas / Contracts
        ↓
Lisan Domain Rules
        ↓
Runtime Skills
        ↓
Tools / AI / Validators
```

الأداة:

- تنفذ،
- تختبر،
- تساعد،
- تقترح،
- أو تتحقق من خاصية محددة،

لكنها لا ترفع سلطة Claim ولا تمنح حالة معرفية خارج العقد الرسمي.

---

# 3. Application Core — معتمد الآن

## 3.1 Python 3.12 + project-local `.venv`

**Status:** `ACTIVE_BASELINE`

### Role

بيئة Backend وSemantic Runtime.

### Use

- FastAPI backend.
- AI runtime.
- validators.
- corpus adapters.
- testing.
- governance lab.

### Rule

استخدم `.venv` محلية للمشروع.

لا تتطلب تثبيت Python عالمي جديد إذا كان `py.exe` يوفر Runtime صالحاً.

---

## 3.2 FastAPI

**Status:** `ACTIVE_BASELINE`

### Role

Application/API boundary للتطبيق المحلي.

### Use

- Commands.
- Queries.
- UI read models.
- ResearchRun APIs.
- Blind Lab.
- Semantic Runtime integration.
- Governance.
- Audit.
- serving built frontend assets في النسخة المحلية النهائية.

### Do not use for

- تعريف الحقيقة الدلالية.
- تخزين Domain logic داخل route handlers.

اجعل Routes رقيقة.

---

## 3.3 Pydantic v2

**Status:** `ACTIVE_BASELINE`

### Role

Canonical runtime validation boundary.

### Use

- API contracts.
- Semantic artifacts.
- Hypothesis.
- Evidence.
- Counterevidence.
- GateReport.
- RejectionCondition.
- AI structured outputs.
- Corpus contracts.

### Rule

استخدم typed schemas و`extra="forbid"` حيث يجب منع حقول غير مصرح بها.

لا تعتمد keyword filters كبديل للعقد البنيوي.

---

## 3.4 SQLAlchemy 2

**Status:** `ACTIVE_BASELINE`

### Role

Persistence abstraction.

### Use

- ResearchRun.
- artifacts.
- checkpoints.
- evidence.
- semantic results.
- audit.
- AIExecutionRecord.
- governance records.

---

## 3.5 Alembic

**Status:** `ACTIVE_BASELINE`

### Role

Versioned database schema migration.

### Rule

لا تعدّل schema الإنتاجية يدوياً.

كل تغيير durable يمر عبر migration قابلة للتتبع.

---

## 3.6 SQLite

**Status:** `ACTIVE_BASELINE`

### Role

قاعدة البيانات المحلية الأساسية.

### Rationale

Lisanapp حالياً:

- local,
- single-user,
- modular monolith.

لذلك لا توجد حاجة حالية لـPostgreSQL server.

### Reconsider only if

ظهرت حاجة مثبتة إلى:

- multi-user concurrency،
- remote centralized deployment،
- operational scale لا يناسب SQLite.

---

# 4. Frontend — معتمد الآن

## 4.1 Next.js App Router + React + TypeScript

**Status:** `ACTIVE_BASELINE`

### Role

Production implementation of the Stitch Golden UX.

### Rule

Stitch هو visual/interaction reference.

لا تنسخ `code.html` كمعمارية إنتاجية.

---

## 4.2 Tailwind CSS

**Status:** `ACTIVE_BASELINE`

### Role

Styling/design implementation.

### Use

مع:

- design tokens،
- CSS Logical Properties،
- native RTL.

---

## 4.3 Radix UI

**Status:** `ACTIVE_BASELINE`

### Role

Accessible UI primitives.

### Use

خصوصاً:

- Dialogs.
- Drawers.
- Menus.
- Tabs.
- Popovers.
- controlled interactive components.

لا تجعل تصميم Radix الافتراضي يحل محل Golden Design System.

---

## 4.4 CSS Logical Properties

**Status:** `ACTIVE_BASELINE`

### Role

RTL-first layout.

Prefer:

`margin-inline`

`padding-inline`

`inset-inline`

بدلاً من duplicating left/right CSS.

---

## 4.5 openapi-typescript

**Status:** `ACTIVE_BASELINE`

### Role

Generate frontend TypeScript API contract definitions from real FastAPI OpenAPI.

### Rule

```text
Backend contract
→ OpenAPI
→ generated TS types
```

لا تعدّل generated file يدوياً.

---

## 4.6 React Flow / `@xyflow/react`

**Status:** `ADOPT_NEXT`

### Stage

Knowledge Explorer / Dependency Graph.

### Role

عرض:

- semantic relationships،
- dependencies،
- invalidation paths،
- provenance relationships.

### Rule

Graph is a read/interaction view.

Graph database is not required.

Provide textual/table alternative.

---

## 4.7 Recharts

**Status:** `ADOPT_NEXT`

### Stage

Quality / Coverage / Analytics.

### Rule

لا تستخدم الرسوم وحدها لنقل حالة معرفية.

كل chart رئيسي له text/table representation.

---

# 5. AI Semantic Runtime

## 5.1 Pydantic AI

**Status:** `ADOPT_NEXT`

### Priority

**High**

### Stage

Before advancing deeply into AI-enabled Slices D–G.

### Role

Infrastructure for the in-process governed semantic research agent.

Use for:

- model invocation,
- typed structured outputs,
- agent instructions,
- tools,
- provider abstraction,
- retries around output validation,
- controlled dependency/context injection.

### Intended pipeline

```text
ObservationArtifacts
      ↓
Pydantic AI Agent
      ↓
Structured Proposal
      ↓
Pydantic Validation
      ↓
Lisan Domain Validation
      ↓
Evidence Resolution
      ↓
Gate Evaluation
```

### Important

Pydantic AI does NOT replace:

- Lisan Domain Model,
- Semantic Skill,
- Gate logic,
- Evidence system,
- Corpus,
- Governance.

It is infrastructure beneath them.

---

## 5.2 `Fake/TestModelProvider`

**Status:** `ADOPT_NEXT`

### Role

Deterministic AI tests.

### Use

When:

- API credentials are unavailable,
- CI must be reproducible,
- testing error/invalid output paths.

### Rule

Never classify fake-model execution as live AI verification.

---

## 5.3 LiteLLM

**Status:** `CONDITIONAL_LATER`

### Trigger

Adopt only if Lisan actually needs:

- multiple model providers,
- provider routing,
- fallback chains,
- unified usage accounting,
- provider switching beyond what Pydantic AI provides cleanly.

### Preferred integration

Library/SDK inside monolith.

### Avoid

A separate LiteLLM Proxy service unless demonstrated operational need exists.

---

## 5.4 DSPy

**Status:** `CONDITIONAL_LATER`

### Stage

After:

- AI runtime is stable,
- semantic eval dataset exists,
- meaningful regression corpus exists.

### Role

Optimize AI programs/instructions against explicit metrics.

Use for improving:

- Hypothesis generation,
- differentiation,
- counterevidence search,
- governed synthesis.

### Prerequisite

A trustworthy benchmark first.

Do NOT optimize against subjective “looks better” judgments.

---

## 5.5 LangGraph

**Status:** `DO_NOT_ADOPT_NOW`

### Reason

Lisan already has:

- ResearchRun,
- stages,
- persistence,
- checkpoints,
- resume.

Adding LangGraph now creates a second workflow/state system.

### Reconsider only if

Agent orchestration becomes sufficiently complex that the existing ResearchRun orchestration demonstrably cannot manage it cleanly.

---

## 5.6 Instructor

**Status:** `DO_NOT_ADOPT_NOW`

### Reason

Structured-output validation is already covered by:

- Pydantic,
- Pydantic AI.

Avoid redundant abstraction.

---

# 6. Quranic Corpus & Linguistic Data

## 6.1 Tanzil Quran Text

**Status:** `PENDING_ADMISSION`

### Priority

**High**

### Stage

Resolve current production Canonical Corpus `CONTRACT_GAP`.

### Proposed role

Primary local Quran text dataset candidate.

Use for:

- verse identity,
- canonical text snapshot,
- reproducible CorpusSnapshot,
- checksums,
- offline research.

### Admission required

Before calling it canonical:

- verify source/version,
- inspect license/terms,
- record file hashes,
- establish Corpus identity,
- document admission decision.

### Rule

Popularity does not automatically make a source authoritative.

---

## 6.2 Quranic Arabic Corpus — QAC

**Status:** `PENDING_ADMISSION`

### Priority

**High**

### Proposed role

Auxiliary structural/morphological source.

Use candidate data for:

- root,
- lemma,
- POS,
- morphology,
- syntax/treebank,
- structural relationships.

### Authority boundary

QAC structural annotation may become admitted structural evidence after review.

QAC semantic ontology must NOT automatically become Lisan semantic authority.

External semantic content remains subject to Source Role Policy.

---

## 6.3 Quran Foundation Content API

**Status:** `CONDITIONAL_LATER`

### Proposed use

- secondary verification,
- metadata,
- optional content adapter,
- comparison/reference.

### Do not use as

mandatory runtime dependency for a local-first application unless needed.

---

# 7. Search / Retrieval

## 7.1 SQLite indexes + FTS5

**Status:** `ADOPT_NEXT`

### Role

Primary local retrieval where appropriate.

Use for:

- exact/root/lemma searches,
- text lookup,
- metadata filtering,
- local research indexing.

Prefer deterministic search for canonical Quran evidence.

---

## 7.2 Qdrant / Vector DB

**Status:** `DO_NOT_ADOPT_NOW`

### Reason

Canonical Quran retrieval is:

- small,
- structured,
- exact,
- morphology-sensitive.

Vector similarity must not replace exact Evidence resolution.

### Reconsider for

external literature / candidate discovery only.

---

## 7.3 LlamaIndex / Haystack

**Status:** `CONDITIONAL_LATER`

### Stage

External research-source layer only.

Potential use for:

- books,
- papers,
- dictionaries,
- linguistic literature.

### Constraint

Must remain separable from Blind Lab and Source Role Policy.

Do not make either framework the Lisan core architecture.

---

# 8. Core Testing

## 8.1 pytest

**Status:** `ACTIVE_BASELINE`

### Role

Primary backend/unit/integration test framework.

Use at:

- V1,
- V2,
- V3,
- V4.

---

## 8.2 httpx / FastAPI TestClient

**Status:** `ACTIVE_BASELINE`

### Role

API/integration testing.

---

## 8.3 Hypothesis

**Status:** `ADOPT_NEXT`

### Priority

**Very High**

### Stage

Now — as domain invariants expand.

### Use

Property-based testing of:

- schemas,
- transitions,
- Gate rules,
- isolation,
- ResearchRun states.

Use `RuleBasedStateMachine` for lifecycle testing.

Examples of invariants:

```text
failed critical gate ⇒ never internal lock

PRIOR_CONTAMINATED ⇒ never internal lock

Steward command ⇒ never semantic truth directly

publication transition ⇒ never silently changes epistemic status

review transition ⇒ never silently changes freshness
```

Use Hypothesis to discover action sequences and edge cases rather than relying only on manually chosen scenarios.

---

## 8.4 Playwright

**Status:** `ADOPT_NEXT`

### Stage

When each vertical slice has real frontend/backend integration.

### Role

Critical E2E journeys:

1. Governed Research
2. Governance Change
3. Claim Traceability
4. Steward
5. Prior Contamination

Do not use Playwright as a substitute for domain tests.

---

## 8.5 Vitest + Testing Library

**Status:** `ADOPT_NEXT`

### Role

Frontend components and UI state behavior.

Particularly:

- status components,
- Inspector,
- Steward Drawer,
- empty/error/loading states.

---

## 8.6 axe-core / accessibility testing

**Status:** `ADOPT_NEXT`

### Stage

Frontend stabilization / V3.

### Role

Automated accessibility baseline.

Do not claim WCAG compliance solely because Axe passes.

---

# 9. API & Contract Quality

## 9.1 Schemathesis

**Status:** `ADOPT_NEXT`

### Priority

High after API stabilizes.

### Stage

V2/V3.

### Role

Property/fuzz testing generated from OpenAPI.

Use to discover:

- malformed values,
- boundary cases,
- status injection,
- missing validation,
- undocumented 5xx,
- contract inconsistencies.

---

## 9.2 Spectral

**Status:** `CONDITIONAL_LATER`

### Role

OpenAPI governance/linting.

Potential Lisan-specific rules:

```text
No direct /set-status endpoints.

Governed mutations must document failure states.

GateReport must expose gate_code.

Versioned canonical entities must expose revision.

Canonical write actions must use explicit commands.
```

Adopt after API conventions become stable enough to justify enforcement.

---

# 10. Governance & Methodology Lab

These tools TEST policies.

They do not become product Authority.

Create conceptually:

```text
tools/governance-lab/
```

---

## 10.1 Promptfoo

**Status:** `ADOPT_NEXT`

### Priority

**Very High once live AI begins**

### Stage

AI Runtime integration onward.

### Role

AI evals and adversarial methodology tests.

Create suites for:

- FM-01 Dictionary-First
- FM-02 Contextual Leakage
- FM-03 Circular Confirmation
- FM-06 Structural Overpromotion
- FM-08 Generic Overextraction
- FM-10 Avoiding Block
- FM-12 Forced Unification
- FM-13 Neighbor Cherry-Picking
- FM-14 Coverage Inflation
- FM-15 Tool Simulation as Evidence
- FM-16 Status Invention
- FM-17 Silencing Counterevidence
- FM-18 Presentation-as-Proof

Also test:

- prompt injection,
- prior contamination,
- model overreliance,
- instructions attempting to override methodology.

Target the actual Lisan API/agent, not only raw models.

Use CI only after baseline evals become stable enough to set meaningful gates.

---

## 10.2 Z3

**Status:** `CONDITIONAL_LATER`

### Priority

High for selected constitutional invariants.

### Stage

After status/gate/governance models stabilize.

### Role

Formal consistency checks.

Examples:

Prove no valid state satisfies:

```text
critical_gate_failed AND internal_lock
```

```text
prior_contaminated AND internal_lock
```

```text
review_rejected AND published
```

```text
invalidated_dependency AND freshness_current
```

Use only for high-value finite/logical invariants.

Do not formally model the entire application.

---

## 10.3 Cosmic Ray

**Status:** `ADOPT_NEXT`

### Stage

Hardening after critical domain tests exist.

### Role

Focused mutation testing.

Targets:

- Gate evaluator.
- Isolation policy.
- status transitions.
- Steward invariants.
- publication/registry admission.

### Purpose

Answer:

> If a developer weakens a critical rule, will our tests actually fail?

Do not mutation-test the entire repository initially.

---

## 10.4 CUE

**Status:** `APPROVED_FOR_EVALUATION`

### Stage

When canonical registries/configuration files increase.

### Potential role

Validate:

- YAML/JSON registries,
- methodology configuration,
- gate definitions,
- source policies,
- cross-file constraints.

### Relationship

Pydantic remains runtime validation.

CUE may become offline/canonical-artifact validation.

Adopt only if it provides real value beyond existing schemas.

---

## 10.5 OPA / Rego

**Status:** `LAB_ONLY`

### Stage

Policy engineering experimentation.

### Potential use

Independently encode and test selected governance rules.

### Do not

Introduce OPA as production runtime policy engine now.

### Trigger for reconsideration

Large, frequently changing policy set that becomes difficult to maintain safely in Python/domain contracts.

---

## 10.6 TLA+ / TLC

**Status:** `CONDITIONAL_LATER`

### Stage

Only if lifecycle/state transitions become substantially more complex.

### Potential role

Model checking:

- analysis lifecycle,
- review/publication,
- invalidation/revalidation.

### Default

Prefer Hypothesis + selected Z3 checks first.

---

# 11. AI Evaluation / Optimization

## 11.1 Promptfoo

Primary tool for:

**Evaluation before optimization.**

Do not optimize prompts before the benchmark exists.

---

## 11.2 DSPy

Use after Promptfoo/regression datasets provide a stable target metric.

Sequence:

```text
Canonical behavior
→ Test cases
→ Promptfoo baseline
→ Stable metrics
→ DSPy optimization
→ Regression verification
```

Never:

```text
DSPy optimization
→ decide afterward what “good” means
```

---

# 12. Observability

## 12.1 Native `AIExecutionRecord`

**Status:** `ADOPT_NEXT`

### Priority

High.

### Role

Product-native AI provenance.

Store:

- provider,
- model,
- skill revision,
- context policy revision,
- tool executions,
- artifact refs,
- execution status.

This is the primary production trace.

---

## 12.2 Arize Phoenix

**Status:** `CONDITIONAL_LATER / LAB_ONLY`

### Stage

AI evaluation/debugging.

### Use if

native trace becomes insufficient for development analysis.

Do not make the production app dependent on Phoenix.

---

## 12.3 Langfuse

**Status:** `CONDITIONAL_LATER / LAB_ONLY`

Same policy as Phoenix.

Select at most one external observability tool if a real need emerges.

Do not add both by default.

---

# 13. Static quality and security

## 13.1 Ruff

**Status:** `ADOPT_NEXT`

### Role

Python linting/format/static hygiene.

Use in V1/CI.

---

## 13.2 mypy or Pyright

**Status:** `ADOPT_NEXT`

### Rule

Choose one primary Python type checker.

Do not run multiple overlapping type-checking regimes without reason.

---

## 13.3 pip-audit

**Status:** `ADOPT_NEXT`

### Stage

V3/V4.

### Role

Python dependency vulnerability review.

---

## 13.4 npm audit

**Status:** `ADOPT_NEXT`

### Stage

V3/V4.

### Role

Frontend dependency review.

Do not automatically upgrade major packages solely to silence audit output without impact analysis.

---

# 14. Explicitly Not Adopted Now

The agent MUST NOT introduce these without demonstrated need and explicit architectural justification:

| Tool / Project | Current decision |
|---|---|
| LangGraph | `DO_NOT_ADOPT_NOW` |
| Instructor | `DO_NOT_ADOPT_NOW` |
| Qdrant | `DO_NOT_ADOPT_NOW` |
| Neo4j | `DO_NOT_ADOPT_NOW` |
| Redis | `DO_NOT_ADOPT_NOW` |
| Celery | `DO_NOT_ADOPT_NOW` |
| Kafka | `DO_NOT_ADOPT_NOW` |
| Keycloak | `DO_NOT_ADOPT_NOW` |
| JWT/Auth system | `DO_NOT_ADOPT_NOW` |
| Dify as platform base | `DO_NOT_ADOPT_NOW` |
| Open WebUI as platform base | `DO_NOT_ADOPT_NOW` |
| Flowise as platform base | `DO_NOT_ADOPT_NOW` |
| Kubernetes | `DO_NOT_ADOPT_NOW` |

Absence from the runtime is intentional simplification, not a missing feature.

---

# 15. Tool Adoption by Project Phase

## Phase A — Current Foundation / Slice A–C

Use:

```text
FastAPI
Pydantic
SQLAlchemy
Alembic
SQLite
pytest
httpx
Next.js
TypeScript
Tailwind
Radix UI
openapi-typescript
```

Add immediately:

```text
Hypothesis
Ruff
type checker
```

---

## Phase B — AI Runtime

Adopt:

```text
Pydantic AI
Fake/Test Model Provider
AIExecutionRecord
Promptfoo
```

Continue:

```text
Pydantic
pytest
Hypothesis
```

---

## Phase C — Canonical Corpus

Evaluate/admit:

```text
Tanzil
QAC
```

Optional:

```text
Quran Foundation API
```

Use SQLite/FTS indexes for local retrieval.

---

## Phase D — Slices D–G

Adopt as needed:

```text
React Flow
Recharts
Playwright
Vitest / Testing Library
```

Continue AI/Domain evaluation.

---

## Phase E — Governance Hardening

Adopt:

```text
Schemathesis
Cosmic Ray
Promptfoo full methodology suite
```

Evaluate:

```text
Z3
Spectral
CUE
```

---

## Phase F — AI Optimization

Only after benchmark maturity:

```text
DSPy
```

Optional if demonstrated:

```text
LiteLLM
Phoenix OR Langfuse
```

---

## Phase G — Release Gate

Use:

```text
full pytest suite
Hypothesis
Schemathesis
Promptfoo applicable suite
focused Cosmic Ray evidence
Playwright E2E
frontend production build
OpenAPI/client sync
Ruff
type checking
pip-audit
npm audit
accessibility checks
```

Selected Z3 formal invariants if adopted.

---

# 16. Governance Lab Recommended Structure

Use a project structure conceptually like:

```text
tools/
└── governance-lab/
    ├── properties/
    │   └── hypothesis/
    │
    ├── ai-evals/
    │   └── promptfoo/
    │
    ├── formal/
    │   └── z3/
    │
    ├── contracts/
    │   ├── schemathesis/
    │   └── spectral/
    │
    ├── mutation/
    │   └── cosmic-ray/
    │
    ├── policy-experiments/
    │   ├── cue/
    │   └── opa/
    │
    └── reports/
```

Do not put experimental tool files into canonical directories.

---

# 17. Rule/Policy Change Verification Pipeline

Where practical, a major methodology/governance rule change should pass:

```text
Change Proposal
      ↓
Canonical impact analysis
      ↓
Schema / Registry validation
      ↓
Existing regression tests
      ↓
Hypothesis properties/state machine
      ↓
AI methodology evals
      ↓
Selected formal invariant checks
      ↓
Focused mutation testing
      ↓
Affected integration/E2E tests
      ↓
Human review
      ↓
New canonical revision
```

Not every trivial edit requires every expensive layer.

Use claim-appropriate verification.

---

# 18. Tool selection rule for agents

Before adding any new dependency, the executing agent MUST answer:

1. What current requirement does this tool satisfy?
2. Is that requirement already satisfied by an approved tool?
3. Is it production runtime or test/lab-only?
4. What new operational complexity does it introduce?
5. What is the removal/fallback path?
6. Does it affect authority, evidence, isolation, or reproducibility?
7. Is the adoption trigger in this reference satisfied?

If the answer is unclear:

**do not add the tool.**

Record an evaluation proposal instead.

---

# 19. Priority shortlist

If execution time is constrained, prioritize in this order:

### Immediate

1. Pydantic AI
2. Hypothesis
3. Promptfoo
4. Canonical Corpus evaluation: Tanzil
5. QAC structural adapter evaluation
6. Ruff + Python type checking

### Before V3

7. Schemathesis
8. Playwright
9. Cosmic Ray
10. accessibility testing

### Selected hardening

11. Z3
12. Spectral
13. CUE

### Later optimization

14. DSPy
15. LiteLLM
16. Phoenix OR Langfuse

### Only if complexity proves necessary

17. OPA/Rego runtime
18. TLA+
19. LangGraph
20. Vector/Graph databases

---

# 20. Final principle

The Lisan tooling strategy is:

> **Use mature tools for infrastructure, testing, validation, AI execution, and data access; keep Lisan-specific epistemology, authority, semantic methodology, evidence rules, Gate logic, Blind Lab behavior, and governance under explicit Lisan contracts.**

Never rebuild commodity infrastructure without reason.

Never outsource Lisan's canonical methodology to a generic framework.