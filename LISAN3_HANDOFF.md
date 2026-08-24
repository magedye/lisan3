# LISAN3 — Project Handoff & Continuity Brief

**Purpose:** Start a new ChatGPT conversation/workspace/project named **LISAN3** without losing the verified context, architectural decisions, governance boundaries, current blockers, or execution order of `Lisanapp3`.

**Filesystem project root:** `D:\APP\tafseer\lisanapp3`

> **Important:** `LISAN3` is the new conversation/workspace name. Do **not** rename the filesystem repository or change its Git boundary unless the owner explicitly authorizes it.

> **Current continuity status:** V3 is independently confirmed only for
> `6bb6505484dd649d092032a36d456f9f7fba5da1`; V4 is
> `V4_ENTRY_UNBLOCKED_NOT_STARTED`; and R1/R2/R3 are `NOT_STARTED`. Historical
> remediation findings below are preserved as evidence, not current gate state.

---

## 1. Mission

Lisanapp is a **local, single-user, governed Quranic semantic research application**.

It is not a generic chatbot, ordinary RAG system, or direct semantic editor.

Its central goal is to support disciplined Quranic semantic research through:

- Canonical Corpus evidence
- Observations
- Hypotheses
- semantic-neighbor analysis
- Counterevidence
- Falsification
- Gate evaluation
- Review / Governance
- Audit / Provenance
- Reproducibility
- AI-assisted research under strict non-authoritative boundaries

The governing principle is:

> **Research before answer. Evidence before acceptance. Retrieval and AI may discover candidates, but they do not decide Quranic semantic truth.**

---

## 2. Repository Identity

### Dedicated repository

Repository root:

`D:\APP\tafseer\lisanapp3`

This is intentionally a **dedicated nested Git repository**, separate from the legacy parent repository:

`D:\APP\tafseer`

The parent repository must not be used as the revision identity for Lisanapp.

### Current independently reviewed candidate

- Branch: `main`
- Candidate reviewed: `6bb6505484dd649d092032a36d456f9f7fba5da1`
- V3 remediation implementation: `1deab3251ac1dc53ef772d10f99c9fd32284e557`
- Earlier candidate `4ac9e0721e612febdcc7df79a09a1b1aa2c47232` and baseline `0e5f256deede286252c299aa2541ea5a8a6b0753` are historical reference points.

These SHAs are historical reference points only.
**At the beginning of a new session, always re-establish current Git identity from the repository itself.**

Run first:

```powershell
cd D:\APP\tafseer\lisanapp3
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git log -5 --oneline
```

Do not assume the Handoff SHA is still HEAD after later work.

---

## 3. Current Verified Project Gate

The earlier `V3_NOT_CONFIRMED` / `V4_ENTRY_BLOCKED` review findings are
historical. A fresh independent read-only review subsequently established:

`V3_INDEPENDENTLY_CONFIRMED`

for candidate `6bb6505484dd649d092032a36d456f9f7fba5da1`.

Current V4 state is:

`V4_ENTRY_UNBLOCKED_NOT_STARTED`

R1, R2, and R3 remain `NOT_STARTED`.

The implementation thread must not self-grant:

- `V3_INDEPENDENTLY_CONFIRMED`
- `INDEPENDENTLY_REVIEWED`
- `TECHNICALLY_RELEASE_READY`
- `RELEASE_ACCEPTED`

---

## 4. Validated V3 Blocking Findings

The latest independent review established the following material gaps.

### F1 — Alembic migration integrity — CRITICAL

A fresh `alembic upgrade head` created only **7 tables while the current model required 19**.

Missing durable tables included:

- `corpus_snapshots`
- `audit_logs`
- `review_decisions`
- `quality_profiles`
- `dependency_records`
- `hypotheses`
- `essential_neighbors`
- `governance_rules`
- `rule_revisions`
- `change_proposals`
- `steward_commands`
- `isolation_events`

`Base.metadata.create_all()` in tests was masking migration drift.

Required remediation:

- forward migrations above current head
- fresh DB `base → head`
- migration/model parity integration test
- reconcile stale migration documentation/history

### F2 — No real Browser E2E — CRITICAL

The five Playwright journeys used `page.request` as an HTTP client.

They were valid API/integration tests, but not:

`Browser → production Next.js UI → FastAPI → test persistence`

Required remediation:

- real `page.goto`
- locators
- click/fill/select where applicable
- visible-state assertions
- production frontend
- file-backed isolated test SQLite
- five canonical journeys:
  1. Governed Research
  2. Blind Lab / Prior Contamination
  3. Claim Traceability
  4. Governance Change
  5. Steward

### F3 — Critical mutation survivors — CRITICAL

Mutation testing exposed test gaps capable of weakening:

- Freshness admission, including `REVALIDATION_REQUIRED`
- Corpus snapshot validation state
- Review revision currency

Multi-entity query/filter tests also need strengthening.

Any remaining critical surviving mutant blocks independent V3 confirmation.

### F4 — Corpus validation boundary — HIGH

A Corpus snapshot could be persisted as:

`validation_status="VALIDATED"`

while:

`canonical_text_hash="UNKNOWN"`

Required remediation:

separate and enforce:

- source-role approval
- physical artifact presence
- hash verification
- import validation
- production activation

Fixtures must never masquerade as production canonical artifacts.

### F5 — Methodological Purity — HIGH

Current Purity behavior was largely cosmetic.

Some dimensions were hard-coded as `EVALUATED_CLEAN`, while others were only shallow heuristics.

Required behavior:

- real evaluation where supported
- explicit `NOT_EVALUATED`-type state where unsupported
- no “not evaluated = clean”
- enforce canonical Purity blocking behavior in admission/publication where required
- purity score must never imply epistemic truth

Canonical dimensions include:

1. Dictionary-First
2. Contextual Leakage
3. Heritage Bias
4. Tafsir Contamination
5. Forced Unification
6. Generic Overextraction
7. Letter Semantics Overreliance
8. Circular Confirmation

### F6 — Slice G API contract conformance — HIGH

Schemathesis found **34 unique failures** against the reviewed candidate, including response-schema and undocumented-status problems across Slice G endpoints.

Affected areas include:

- Knowledge Explorer
- Quality / Purity
- Reproduction Manifest
- Audit
- History
- Provenance
- AI trace

Required remediation:

- classify each failure by root cause
- fix implementation/schema/status documentation correctly
- regenerate OpenAPI
- regenerate frontend TS types
- rebuild frontend
- rerun Schemathesis

### Additional verification weakness

The independent review also found:

- one trivial Hypothesis property
- one Hypothesis property with no assertions

Replace decorative properties with meaningful domain invariants.

---

## 5. Historical V3 Remediation and Current Engineering Priority

The following was the completed V3 remediation sequence:

# `V3 Remediation`

Order:

```text
F1 Migration integrity
→ F2 Real Browser E2E
→ F3 Critical mutation gaps
→ F4 Corpus validation invariant
→ F5 Purity + Purity Gate
→ F6 Slice G contract conformance
→ meaningful Hypothesis properties
→ full V3 candidate verification
→ clean committed candidate SHA
→ fresh independent read-only V3 review
```

The current next engineering priority is a separately authorized R1 Knowledge
Graph Foundation work package. It is activation-allowed after V3 confirmation,
but remains `NOT_STARTED`; this handoff does not authorize it. Do not begin V4
until an actual release candidate is established.

---

## 6. Current Architecture

The approved baseline remains:

**Local Single-User Modular Monolith**

### Backend

- Python 3.12
- FastAPI
- Pydantic v2
- SQLAlchemy 2
- Alembic
- SQLite
- Pydantic AI

### Frontend

- Next.js App Router
- TypeScript
- Tailwind CSS
- Radix UI
- CSS Logical Properties / Arabic RTL
- OpenAPI-generated TypeScript contracts

### Verification

- pytest / httpx
- Hypothesis
- Ruff
- Pyright
- Playwright
- Schemathesis
- Cosmic Ray
- Promptfoo — configured but not yet executed

### Deliberately absent

Do not add without explicit governed decision:

- login/auth/JWT/Keycloak
- Redis
- Celery
- Kafka
- microservices
- Kubernetes
- separate Graph server
- separate Vector server during current baseline

---

## 7. AI Runtime Boundary

AI is a **first-class exploratory analytical runtime**, but never semantic authority.

Current maximum supported claim:

`TESTED_WITH_FAKE_PROVIDER`

The project currently uses Pydantic AI with a test/fake provider profile.

The AI may support:

- hypothesis generation
- candidate neighbor generation
- counterevidence suggestions
- differentiation axes
- falsification support
- synthesis

AI must never independently grant:

- Gate PASS
- Internal Lock
- canonical semantic acceptance
- review approval
- publication authority

Keep:

`Promptfoo = CONFIGURED_NOT_EXECUTED`

unless actual runtime evidence changes it.

Live AI provider activation is not part of the current R1 preparation priority.

---

## 8. Corpus Boundary

Source-role direction:

- Tanzil: canonical Quran text candidate
- QAC: auxiliary morphology/syntax candidate
- QAC semantic ontology: not semantic authority

Current artifact state remains:

`CORPUS_ARTIFACT_VERIFICATION_PENDING`

until physical artifacts are securely verified by exact provenance/version/hash.

Do not silently upgrade fixture/stub evidence to production canonical status.

---

## 9. Four Independent Status Axes

Keep the four axes independent.

### Epistemic

- `OBSERVATION`
- `HYPOTHESIS`
- `TESTED`
- `SUPPORTED`
- `LOCK_BLOCKED`
- `LOCK_INTERNAL_RESULT`
- `REJECTED`
- `UNRESOLVED`

### Review

- `NOT_REVIEWED`
- `REVIEW_REQUIRED`
- `IN_REVIEW`
- `APPROVED`
- `REJECTED`
- `OWNER_DECISION_REQUIRED`

### Freshness

- `CURRENT`
- `STALE`
- `INVALIDATED`
- `REVALIDATION_REQUIRED`

### Publication

- `PRIVATE_WORKING`
- `REVIEWABLE`
- `PUBLISHABLE`
- `PUBLISHED`
- `WITHDRAWN`

Do not reintroduce unofficial persisted statuses such as `NOT_ESTABLISHED`.

Presentation language may differ where canonically allowed, but persistence/transition values must come from the official authority.

---

## 10. Blind Lab Invariant

Blind Lab isolation is a core epistemic boundary.

Before internal lock, forbidden prior semantic material must not leak through:

- raw APIs
- AI context
- Knowledge Graph
- Vector indexes
- cached embeddings
- external search indexes
- old claims/definitions

A blocked access attempt should remain distinguishable from actual contamination.

Do not automatically mark a run contaminated merely because a forbidden read was blocked.

---

## 11. Google Stitch Role

Google Stitch remains the **Golden Design / Interaction Reference**.

It is not backend/domain authority.

Authority order for UX work:

```text
Owner instruction
→ UX Constitution
→ canonical product/contracts
→ approved Stitch / design reference
→ production frontend implementation
```

Material redesigns may be prototyped in Stitch.

Ordinary:

- bug fixes
- backend binding
- accessibility corrections
- loading/error states
- contract synchronization

do not require a mandatory Stitch round trip.

Production frontend remains Next.js/TypeScript.

---

## 12. New Canonical Hybrid Retrieval Architecture

The owner has saved the canonical document:

`docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`

Status:

`CANONICAL — APPROVED / EXECUTION_GATED`

Its governing principle:

> **Retrieval discovers candidates. Evidence resolves them. Governance decides what can become governed knowledge.**

The architecture introduces future:

### R1 — Knowledge Graph Foundation

- SQLite graph projection
- `KnowledgeNode`
- `KnowledgeEdge`
- governed graph vocabulary
- NetworkX analysis
- React Flow Knowledge Explorer
- provenance
- rebuildability

### R2 — Vector Discovery

- embedding benchmark
- separate embedding spaces
- `sqlite-vec` Spike
- derived vector index
- candidate neighbor discovery
- candidate counterevidence discovery
- provenance

### R3 — Governed Hybrid Retrieval

```text
Exact Retrieval
+
Vector Discovery
+
Graph Retrieval
        ↓
RetrievalCandidate Set
        ↓
EvidenceResolver
        ↓
Pydantic AI Runtime
        ↓
Hypothesis / Differentiation
        ↓
Counterevidence / Falsification
        ↓
GateReport
```

### Activation gate

R1/R2/R3 MUST NOT begin until:

`V3_INDEPENDENTLY_CONFIRMED`

---

## 13. Hybrid Retrieval Authority Boundary

Always preserve:

```text
Vector similarity ≠ semantic evidence
Graph connectivity ≠ semantic truth
AI proposal ≠ canonical claim
Retrieval score ≠ epistemic confidence
```

Graph and Vector outputs are:

`DERIVED / DISCOVERY`

Canonical/structural exact retrieval remains the source-resolution path.

A Vector/Graph candidate must pass through source resolution, research evaluation, counterevidence/falsification, Gates, and Governance before it can influence governed knowledge.

---

## 14. Hybrid Retrieval Tool Decisions

Current intended statuses:

- NetworkX → `ADOPT_NEXT_AFTER_V3`
- React Flow / `@xyflow/react` → `ADOPT_NEXT_AFTER_V3`
- sqlite-vec → `APPROVED_FOR_EVALUATION`
- Embedding model → `TO_BE_SELECTED_BY_BENCHMARK`
- Qdrant Embedded/Local → `CONDITIONAL_LATER`
- Qdrant Server → `DO_NOT_ADOPT_NOW`
- Neo4j → `DO_NOT_ADOPT_NOW`
- RDFLib → `APPROVED_FOR_EVALUATION`
- RDF/OWL → `CONDITIONAL_LATER`
- Protégé → `LAB_ONLY`
- Haystack/LlamaIndex → `CONDITIONAL_LATER`, external-source retrieval only
- LangChain → `DO_NOT_ADOPT_NOW`
- Prolog → `DO_NOT_ADOPT_NOW`

Do not change these statuses from agent preference alone.

---

## 15. Embedding Policy

Do not select an embedding model by popularity or intuition.

R2 requires a reproducible benchmark with:

- known close candidates
- known non-neighbors
- difficult lexical distinctions
- contextual outliers
- candidate counterevidence
- false-positive traps

Use measurable evaluation such as:

- Recall@K
- Precision@K
- MRR
- nDCG@K
- False Positive Rate

Do not use one universal embedding space for everything.

Potential spaces include:

- `VERSE_CONTEXT`
- `STRUCTURAL_PROFILE`
- `HYPOTHESIS`
- `CLAIM`
- `ROOT_CANDIDATE`
- `EXTERNAL_RESEARCH`

Cross-space similarity must fail closed unless explicitly defined.

---

## 16. Knowledge Graph Policy

The graph is a **derived projection**, not a second canonical database.

Initial persistence remains SQLite.

NetworkX is in-process analysis, not persistence.

Do not adopt Neo4j now.

Every graph edge must retain origin/provenance, conceptually distinguishing:

- `DOMAIN_PROJECTION`
- `GOVERNED_ASSERTION`
- `DISCOVERY_CANDIDATE`

Candidate graph relations must never be rendered as established canonical knowledge.

---

## 17. Documentation Reconciliation Status

The post-V3 documentation reconciliation makes the Hybrid Retrieval contract
durable and cross-referenced before R1. Verify its exact commit and current
working tree before relying on this statement.

The task requires reconciliation of:

- `docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md`
- `docs/canonical/LISAN_TOOLING_ADOPTION_REFERENCE.md`
- `docs/canonical/UI_BACKEND_CONTRACT_MATRIX.md`
- optional `docs/canonical/LISAN_DOMAIN_MODEL.md`
- root/scoped `AGENTS.md`
- optional `.agents/skills/lisan-hybrid-retrieval/SKILL.md`
- `PROJECT_STATE.md`
- current durable implementation plan
- optional concise reference from `PROMPT/1.MD`

### Important

At the beginning of LISAN3:

1. inspect Git history;
2. inspect the above files;
3. verify that the canonical reconciliation commit and references are present;
4. reconcile any later drift before continuing;
5. do not implement R1/R2/R3 without a separately authorized bounded task.

---

## 18. Canonical Documents to Read First

At the start of any substantial work, read applicable `AGENTS.md` first, then resolve canonical references from the repository.

Important known documents include:

- `AGENTS.md`
- `docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md`
- `docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`
- `docs/canonical/LISAN_TOOLING_ADOPTION_REFERENCE.md`
- `docs/canonical/UI_BACKEND_CONTRACT_MATRIX.md`
- Lisan UX Constitution / implementation reference
- active semantic runtime skill
- official registries/schemas/contracts
- `PROMPT/1.MD`
- `PROJECT_STATE.md`

Treat `PROJECT_STATE.md` as resumable context, not authority.

Do not trust stale implementation reports over repository/runtime evidence.

---

## 19. Agent Execution Discipline

For every engineering task:

```text
Authority
→ bounded goal
→ acceptance map
→ minimal implementation
→ executed evidence
→ adversarial self-review
→ state update
→ precise claim
```

Maintain these distinctions:

```text
installed
≠ configured
≠ executed
≠ passed
≠ verified
≠ independently reviewed
≠ release accepted
```

Prefer `PARTIAL` / `NOT_VERIFIED` over unsupported completion claims.

Preserve unrelated user work.

Do not silently rewrite canonical history.

---

## 20. Model / Agent Selection Policy

### Default implementation

Use:

**Terra — high — Plan→Execute**

for:

- feature implementation
- remediation
- migrations
- tests
- frontend/backend integration
- refactors with clear acceptance criteria

### Mechanical work

Use:

**Luna**

for:

- inventories
- formatting
- low-risk documentation cleanup
- simple repetitive edits
- classification
- mechanical bulk changes

### Independent / high-risk reasoning

Use:

**Sol — high/xhigh — fresh read-only**

for:

- independent candidate review
- release/V4 audit
- architecture conflict
- semantic authority conflict
- security-critical review
- ambiguous root cause after ordinary debugging
- high-risk cross-system decisions

---

## 21. MoA Policy in Hermes

Use Multi-Agent / MoA only when it materially improves reasoning.

Good MoA triggers:

- ambiguous architecture
- difficult unresolved root cause
- semantic/epistemic authority conflict
- security-sensitive decision
- embedding-model benchmark interpretation
- major technology migration choice
- adversarial design review with genuine competing hypotheses

Do not use MoA for routine implementation.

Never let multiple agents write overlapping repository changes in parallel.

Preferred pattern:

```text
MoA independent analyses
        ↓
one aggregator
        ↓
one implementation agent
```

When a future LISAN3 task would materially benefit from MoA, explicitly tell the owner before execution and recommend the appropriate Hermes preset.

---

## 22. First Actions in the New LISAN3 Conversation

The first agent should NOT begin coding immediately.

Perform:

### Step 1 — Git identity

Run:

```powershell
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git log -5 --oneline
```

### Step 2 — Read governance

Read applicable:

- root/scoped AGENTS
- canonical platform reference
- Hybrid Retrieval architecture contract
- tooling reference
- UX authority
- active semantic skill
- PROJECT_STATE

### Step 3 — Reconcile actual current state

Determine whether:

- the post-V3 documentation reconciliation commit and canonical references are present;
- V3 confirmation remains bound to `6bb6505484dd649d092032a36d456f9f7fba5da1`;
- current tree is clean;
- current candidate SHA changed;
- PROJECT_STATE matches repository evidence.

### Step 4 — Choose exactly one current task

Current priority is R1 preparation only through a separately authorized
work package. R2 and R3 remain phase-gated.

### Step 5 — Do not infer

If repository evidence and this handoff differ:

**repository authority + executed evidence win.**

Record the discrepancy rather than forcing the repository to match this document.

---

## 23. Recommended First Prompt for LISAN3

Use this as the first substantive instruction in the new conversation:

> Work on `D:\APP\tafseer\lisanapp3`.
>
> Treat `LISAN3_HANDOFF.md` as continuity context, not as a substitute for repository authority.
>
> First perform a read-only resume:
> 1. establish Git root/branch/full HEAD/working-tree state;
> 2. read applicable AGENTS and canonical references;
> 3. verify whether the Hybrid Retrieval documentation reconciliation task has already been completed;
> 4. inspect PROJECT_STATE against actual Git/runtime evidence;
> 5. confirm the candidate-bound V3 confirmation and current R1 state;
> 6. identify any discrepancy between this handoff and the repository.
>
> Do not modify the repository during this first resume pass.
>
> Return:
> - current candidate identity;
> - canonical authority map;
> - actual V3 status;
> - Hybrid Retrieval reconciliation status;
> - current blockers;
> - exact recommended next task;
> - whether the next task needs a single agent or Hermes MoA.
>
> Do not begin V4 or R1/R2/R3 unless the repository proves `V3_INDEPENDENTLY_CONFIRMED`.

---

## 24. Handoff State Summary

At the time this Handoff was created:

```text
Project:
Lisanapp3 / new conversation name LISAN3

Repository:
D:\APP\tafseer\lisanapp3

Independently reviewed V3 SHA:
6bb6505484dd649d092032a36d456f9f7fba5da1

Independent V3 verdict:
V3_INDEPENDENTLY_CONFIRMED

V4:
V4_ENTRY_UNBLOCKED_NOT_STARTED

Current priority:
Post-V3 documentation reconciliation, then separately authorized R1

AI:
TESTED_WITH_FAKE_PROVIDER

Corpus:
ARTIFACT_VERIFICATION_PENDING

Hybrid Retrieval architecture:
CANONICAL_APPROVED

Hybrid Retrieval activation:
V3_INDEPENDENTLY_CONFIRMED — SATISFIED

Current Retrieval Phase:
R1_NOT_STARTED

Future order:
R1 Knowledge Graph
→ R2 Vector Discovery
→ R3 Governed Hybrid Retrieval
```

---

# Final Continuity Rule

Do not restart Lisan from first principles.

Do not trust old completion claims blindly.

Resume from:

**canonical authority + current Git revision + current runtime evidence.**

The immediate objective after confirming the documentation candidate is a
separately authorized R1 Knowledge Graph Foundation work package. Preserve the
R1 → R2 → R3 order and do not treat retrieval outputs as semantic authority.
