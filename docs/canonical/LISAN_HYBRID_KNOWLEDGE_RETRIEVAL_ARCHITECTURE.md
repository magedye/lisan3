# Lisan Hybrid Knowledge Retrieval Architecture Contract

> **Semantic-governance amendment — 2026-09-06:** this document continues to
> govern retrieval, projection, and EvidenceResolver boundaries. Any reference
> below to four status axes, Purity/Lock Gates, or Internal Lock is historical
> and is superseded by `SIMPLIFIED_AI_AUTHORITY_AND_GOVERNANCE_CONTRACT.md`.
> Retrieval outputs remain non-authoritative; current admission uses the single
> server-owned canonicalization policy.

**Document ID:** `LISAN-HKR-ARCH`
**Version:** `1.0`
**Status:** `CANONICAL — APPROVED / EXECUTION_GATED`
**Scope:** Lisanapp Knowledge Graph, Vector Discovery, Hybrid Retrieval, and integration with the Golden UX
**Repository:** `D:\APP\tafseer\lisanapp3`

---

# 0. Authority and Purpose

This document is the canonical architectural contract for all work involving:

- Knowledge Graph;
- Vector / Embedding retrieval;
- hybrid retrieval;
- Knowledge Explorer;
- semantic-neighbor candidate discovery;
- candidate counterevidence discovery;
- graph-based dependency exploration;
- retrieval integration with the AI Semantic Runtime;
- provenance of retrieval-derived candidates.

It does not replace:

- the Lisan UX Constitution;
- canonical Quranic methodology;
- active registries/schemas;
- Semantic Runtime Skill;
- governance contracts;
- Corpus admission contracts.

It defines how retrieval technologies are allowed to operate **under those authorities**.

If an implementation, prototype, old proposal, report, model output, or fixture conflicts with this document or a higher authority, the higher authority wins.

---

# 1. Governing Architectural Principle

Lisan uses three fundamentally different categories:

```text
Canonical / Governed Truth
        ↓
Derived Retrieval & Discovery
        ↓
AI-assisted Research
```

They MUST NOT be conflated.

The governing rule is:

> **Retrieval discovers candidates. Evidence resolves them. Governance decides what can become governed knowledge.**

Therefore:

```text
Vector similarity ≠ semantic evidence

Graph connectivity ≠ semantic truth

AI proposal ≠ canonical claim

Retrieval score ≠ epistemic confidence
```

---

# 2. Canonical Authority Boundary

The following remain authoritative within their defined roles:

```text
Canonical Corpus
Official Registries
Canonical Methodology
Schemas / Contracts
Governed Evidence
Gate Evaluation
Review / Publication Rules
Audit / Provenance
```

The following are always derived or advisory unless separately admitted through canonical governance:

```text
Vector embeddings
Vector similarity results
Graph projections
Graph traversal results
Graph centrality
AI-generated candidates
Clustering
Nearest-neighbor recommendations
External-source retrieval
```

Derived outputs must never silently acquire canonical authority.

---

# 3. Current Lisanapp Baseline

The target remains a:

**Local Single-User Modular Monolith**

Current architectural baseline:

```text
Lisanapp
│
├── Next.js / TypeScript Frontend
│
├── FastAPI Application
│
├── Pydantic Domain Contracts
│
├── Pydantic AI Runtime
│
├── SQLAlchemy / Alembic
│
├── SQLite
│
├── Governed Research Runtime
│
├── Blind Lab
│
├── Evidence / Counterevidence
│
├── Gate Evaluation
│
├── Governance / Steward
│
└── Audit / Provenance
```

Do not introduce a distributed architecture merely to support Graph or Vector retrieval.

No new server is required for R1–R3.

---

# 4. Execution Gate

This architecture is approved, but execution remains gated by the active phase.

The initial activation prerequisite for R1 is:

`V3_INDEPENDENTLY_CONFIRMED`

That prerequisite is satisfied only for the independently reviewed candidate
`6bb6505484dd649d092032a36d456f9f7fba5da1`. R1 is therefore eligible for a
separately authorized work package; this contract does not itself authorize
implementation. R2 remains gated by R1 verification, and R3 remains gated by
R1 and R2 verification.

Agents may maintain this contract, reconcile related documentation, prepare
acceptance criteria, prepare non-production benchmark datasets, and prepare
ADR proposals. They MUST NOT use R1–R3 as justification to expand unrelated
work or bypass the phase order.

---

# 5. Relationship to Google Stitch and the Golden UX

## 5.1 Stitch Role

Google Stitch remains:

- a visual reference;
- an interaction reference;
- a Golden UX prototype;
- a user-testing/design exploration asset.

It is NOT:

- semantic authority;
- backend authority;
- API authority;
- lifecycle authority;
- canonical status authority;
- production frontend source code.

## 5.2 Authority Order for UI Work

For UX/frontend behavior:

```text
Owner instruction
        ↓
UX Constitution
        ↓
Canonical product/contracts
        ↓
Approved Design System / Golden Stitch reference
        ↓
Production frontend implementation
```

## 5.3 UI Change Rule

Material UX redesigns SHOULD be reconciled against the Golden prototype and may be prototyped in Stitch first.

However, the following do NOT require a mandatory Stitch round trip:

- backend data binding;
- bug fixes;
- accessibility fixes;
- contract synchronization;
- loading/error states required by real runtime behavior;
- implementation corrections that do not alter approved UX intent.

Do not create unnecessary design drift by forcing every code change through Stitch.

## 5.4 Production Code Rule

Stitch HTML/CSS exports are reference artifacts.

Do not copy them verbatim as production architecture.

Production UI remains implemented using the approved Next.js/TypeScript design system.

---

# 6. Target Retrieval Architecture

The approved target is:

```text
                        Lisan UI
                           │
                  Governed Application
                           │
       ┌───────────────────┼────────────────────┐
       │                   │                    │
 Exact Retrieval     Vector Discovery      Graph Retrieval
       │                   │                    │
 SQLite / Corpus       sqlite-vec         SQLite Projection
       │                   │              + NetworkX analysis
       └───────────────────┼────────────────────┘
                           │
                     Candidate Set
                           │
                    Evidence Resolver
                           │
                   Pydantic AI Runtime
                           │
            Hypothesis / Differentiation
                           │
          Counterevidence / Falsification
                           │
                       GateReport
                           │
                  Governed Knowledge
```

This architecture is called:

**Governed Hybrid Semantic Retrieval**

---

# 7. Layer 1 — Exact Retrieval

Exact Retrieval is the primary evidence-resolution path.

It operates over admitted canonical/structural data.

Examples:

- surah/ayah identity;
- canonical text;
- root;
- lemma;
- form;
- morphology;
- construction;
- syntax;
- CorpusOccurrence;
- admitted ObservationArtifacts;
- governed Evidence references.

Exact Retrieval may resolve an actual canonical source reference.

Vector and Graph results cannot override Exact Retrieval.

If a derived candidate conflicts with admitted Corpus evidence:

**Corpus evidence governs.**

---

# 8. Layer 2 — Vector Discovery

Vector Search exists for:

**candidate discovery**, not semantic adjudication.

Permitted use cases include:

- candidate semantic-neighbor discovery;
- candidate counterevidence discovery;
- outlier/context discovery;
- clustering for exploratory analysis;
- research-artifact retrieval;
- external-research retrieval in permitted source profiles.

It MUST NOT directly:

- define Root Core;
- establish Distinctive Residue;
- pass a Gate;
- create canonical Evidence;
- assign official status;
- publish knowledge;
- resolve a semantic dispute.

---

# 9. Vector Storage Decision

## Initial decision

`sqlite-vec`

Status:

`APPROVED_FOR_EVALUATION`

Target adoption after successful R2 Spike:

`ADOPTED_FOR_LOCAL_VECTOR_INDEX`

if acceptance criteria pass.

Reason:

- preserves local-first architecture;
- preserves one primary SQLite database;
- avoids separate Vector server;
- fits current corpus scale;
- provides a migration path later.

## Upgrade path

Only evaluate stronger infrastructure when evidence demonstrates need.

Preferred progression:

```text
sqlite-vec
    ↓
Qdrant Embedded / Local
    ↓
Qdrant Server only if deployment requirements demand it
```

Do not adopt Qdrant Server prematurely.

---

# 10. Vector Data Contract

Use a derived index conceptually equivalent to:

```text
SemanticEmbedding

id
entity_type
entity_id
embedding_space
embedding_model
embedding_model_revision
source_revision
source_hash
vector
created_at
index_revision
```

The Vector index is rebuildable.

Deleting the complete vector index MUST NOT delete canonical knowledge.

Changing:

- model;
- model revision;
- preprocessing;
- source revision;

must make the relevant index stale and trigger rebuilding.

---

# 11. Separate Embedding Spaces

Do not assume one embedding space is meaningful for every Lisan entity.

Evaluate separate spaces such as:

```text
VERSE_CONTEXT
STRUCTURAL_PROFILE
HYPOTHESIS
CLAIM
ROOT_CANDIDATE
EXTERNAL_RESEARCH
```

Vectors from incompatible spaces MUST NOT be compared directly.

A numerical similarity result must always identify:

- embedding space;
- model;
- revision;
- source revision.

Do not create one universal semantic score.

---

# 12. Embedding Model Selection

No embedding model is canonically approved yet.

Status:

`TO_BE_SELECTED_BY_BENCHMARK`

The agent MUST NOT choose an embedding model because:

- it is popular;
- it is from the same AI provider;
- it performs well on English benchmarks;
- it “looks semantically good” in a few examples.

The benchmark SHOULD evaluate suitable:

- Arabic models;
- multilingual models;
- local/open models;
- hosted models where allowed.

Local-first options receive preference when quality is competitive.

---

# 13. Embedding Benchmark

R2 MUST include a reproducible benchmark before model adoption.

Use a governed evaluation dataset containing appropriate examples of:

- known close candidates;
- known non-neighbors;
- difficult lexical distinctions;
- contextual outliers;
- candidate counterevidence;
- false-positive traps.

Evaluate using metrics such as:

```text
Recall@K
Precision@K
MRR
nDCG@K
False Positive Rate
```

Also perform qualitative adversarial review.

Do not use a vague criterion such as:

> “these verses look close”

as the adoption gate.

The benchmark dataset itself does not become semantic authority.

---

# 14. Top-K Rule

Vector retrieval may use configurable:

`top_k`

for retrieval efficiency.

This MUST NOT become a methodology rule such as:

> “the nearest five vectors are the five semantic neighbors.”

Essential semantic neighbors are determined by governed research methodology.

Vector retrieval only proposes candidates.

---

# 15. Layer 3 — Knowledge Graph

The Knowledge Graph is a **derived graph projection of governed domain state**.

It is not a second canonical database.

Canonical domain records remain the source.

The graph projection may be deleted and rebuilt.

---

# 16. Graph Persistence

Initial storage:

**SQLite**

Use derived projection tables conceptually similar to:

```text
KnowledgeNode

node_id
entity_type
entity_id
entity_revision
projection_revision
created_at
```

and:

```text
KnowledgeEdge

edge_id
source_node_id
edge_type
target_node_id
edge_origin
edge_status
provenance_ref
valid_from_revision
invalidated_at
```

`source_node_id` and `target_node_id` must reference graph nodes.

Because `entity_id` may identify heterogeneous domain entities, do not falsely declare a relational FK to multiple unrelated domain tables.

Application/domain validation resolves the corresponding entity.

---

# 17. Graph Edge Authority

Every edge must identify its origin.

Use categories conceptually equivalent to:

```text
DOMAIN_PROJECTION
GOVERNED_ASSERTION
DISCOVERY_CANDIDATE
```

Examples:

### DOMAIN_PROJECTION

Derived directly from existing governed records:

```text
CLAIM → EVIDENCE
CLAIM → RESEARCH_RUN
RUN → CORPUS_SNAPSHOT
CLAIM → GATE_REPORT
CLAIM → DEPENDENCY
```

### GOVERNED_ASSERTION

An explicitly governed relationship that has passed its applicable process.

### DISCOVERY_CANDIDATE

AI/vector/graph-generated research suggestion.

A `DISCOVERY_CANDIDATE` edge MUST NOT be shown as canonical knowledge.

---

# 18. Canonical Graph Vocabulary

Graph relationship vocabulary must be versioned and governed.

Initial candidates include:

```text
OCCURS_IN
SUPPORTS
CHALLENGES
DEPENDS_ON
DERIVED_FROM
USES_CORPUS
USES_METHODOLOGY
EVALUATED_BY
INVALIDATED_BY
GENERATED_IN
NEIGHBOR_OF
DISTINGUISHED_FROM
```

Do not add arbitrary edge types from free-form AI output.

`NEIGHBOR_OF` and `DISTINGUISHED_FROM` require explicit status/origin because they may represent:

- discovery candidate;
- current hypothesis;
- governed result.

---

# 19. NetworkX Decision

`NetworkX`

Status:

`ADOPT_NEXT_AFTER_V3`

Role:

in-process graph analysis over SQLite-derived projection.

Permitted tasks include:

- dependency reachability;
- neighborhood analysis;
- cycle detection;
- connected-components analysis;
- invalidation impact exploration;
- path analysis.

NetworkX is not persistence.

Do not use it as the canonical database.

---

# 20. Graph Database Decision

Do NOT introduce Neo4j currently.

Status:

`DO_NOT_ADOPT_NOW`

Re-evaluate only when evidence shows that SQLite projection + NetworkX cannot meet:

- scale;
- traversal complexity;
- performance;
- maintainability requirements.

A visual graph does not imply the need for a Graph Database.

---

# 21. React Flow Decision

`@xyflow/react`

Status:

`ADOPT_NEXT_AFTER_V3`

Role:

production visualization of graph read models.

Primary UX target:

**Knowledge Explorer**

It may also support:

- dependency visualization;
- provenance;
- invalidation paths;
- semantic-neighbor candidates.

React Flow does not own graph authority.

Charts/graphs must retain textual or tabular alternatives where required by UX/accessibility contracts.

---

# 22. Candidate Evidence Contract

Vector and Graph discovery MUST produce explicit candidate objects.

Use a concept such as:

```text
RetrievalCandidate

candidate_id
candidate_type
source_layer
entity_ref
source_revision
score_or_path
retrieval_reason
provenance
status
```

`source_layer` must identify:

```text
EXACT
VECTOR
GRAPH
EXTERNAL
```

For VECTOR results include:

- embedding model;
- embedding revision;
- similarity score.

For GRAPH results include:

- graph path/edge refs;
- graph projection revision.

A RetrievalCandidate is NOT canonical Evidence.

---

# 23. Evidence Resolver

R3 introduces a canonical application boundary:

`EvidenceResolver`

Its purpose is to convert a candidate into a resolvable research input where justified.

Conceptual flow:

```text
RetrievalCandidate
        ↓
EvidenceResolver
        ↓
Canonical/Structural Source Lookup
        ↓
Resolved Artifact
        ↓
Evidence / Counterevidence candidate
        ↓
Research evaluation
```

Only source-resolved artifacts may participate in governed Evidence/Gate paths according to canonical contracts.

---

# 24. AI Runtime Integration

Pydantic AI receives retrieval results as research candidates.

The AI context must explicitly distinguish:

```text
CANONICAL_EVIDENCE
STRUCTURAL_EVIDENCE
VECTOR_CANDIDATE
GRAPH_CANDIDATE
EXTERNAL_CANDIDATE
```

Model instructions must state:

> Vector similarity and graph relationships are discovery aids. They are not semantic authority. Resolve important claims against admitted Corpus, Evidence, methodology, and governed contracts before using them in a semantic conclusion.

AI MUST NOT:

- convert candidate similarity directly into Evidence;
- infer Gate PASS from retrieval score;
- treat Graph path as semantic proof;
- hide candidate provenance;
- merge candidate and canonical evidence labels.

---

# 25. Blind Lab Integration

All retrieval layers must obey Blind Lab source policy.

Pre-lock AI/retrieval may access only sources permitted for the active Blind Lab profile.

If dictionaries, tafsir, previous definitions, or external research are forbidden before lock:

- Vector index must not leak them;
- Graph projection must not expose them;
- AI tools must not query them;
- cached embeddings must not become a bypass.

Blind Lab isolation applies to **derived indexes as well as raw source APIs**.

This is a mandatory security/epistemic invariant.

---

# 26. Purity Integration

Vector Search MAY assist Purity evaluation, particularly:

- Heritage Bias candidate detection;
- similarity to external dictionary definitions;
- possible Tafsir contamination.

But:

```text
high similarity ≠ contamination proven
```

Vector results produce candidate Purity findings requiring policy-defined evaluation.

Exact Retrieval remains required where deterministic source comparison is possible.

Purity Gate behavior remains governed by canonical Purity policy.

---

# 27. Graph Integration with Invalidation

The graph projection may accelerate:

`transitive impact discovery`

but canonical invalidation MUST remain derived from authoritative dependency records.

Before Graph results can drive invalidation:

- graph projection must be proven equivalent to canonical dependency relationships for the supported profile.

Graph-only inferred relationships must not invalidate governed knowledge automatically.

---

# 28. Provenance Requirements

Every derived retrieval result must be traceable.

At minimum record:

### Vector

```text
entity
embedding model
model revision
embedding space
source revision/hash
index revision
similarity score
retrieval timestamp
```

### Graph

```text
source node
target node
edge type
edge origin
projection revision
provenance refs
path if traversal-derived
```

The UI must be able to distinguish:

> “This came from Vector candidate discovery.”

from:

> “This relationship exists in governed dependency records.”

---

# 29. Knowledge Explorer Integration

The Golden Knowledge Explorer will be backed by real graph read models.

Frontend behavior must preserve:

- current four status axes;
- relationship types;
- provenance access;
- filtering;
- stale/revalidation states;
- textual/table fallback.

Do not let visual proximity of graph nodes imply semantic proximity unless explicitly labeled.

---

# 30. Semantic Differentiation Lab Integration

Vector Search may populate:

**Candidate Neighbors**

The UI must label them as candidates.

For each candidate, governed analysis must still perform:

- Shared Domain analysis;
- differentiation axes;
- substitution probe;
- boundary tests;
- Counterevidence;
- Falsification;
- Gate evaluation.

Vector score must never substitute for Distinctive Residue.

---

# 31. External Research

External books, dictionaries, linguistic research and future RAG sources are outside the canonical Corpus.

If external retrieval is introduced later:

- keep its index logically separable;
- record source role;
- enforce Blind Lab policy;
- label candidate provenance;
- never silently mix it with Quranic Corpus embeddings.

Frameworks such as Haystack or LlamaIndex remain:

`CONDITIONAL_LATER`

for external-source retrieval only.

They are not the core Lisan semantic architecture.

---

# 32. RDF / OWL / Protégé

These are not part of R1–R3 production runtime.

Current status:

```text
RDFLib: APPROVED_FOR_EVALUATION
RDF/OWL: CONDITIONAL_LATER
Protégé: LAB_ONLY
```

Future permitted use:

```text
Governed Lisan Data
       ↓
Derived Graph Projection
       ↓
RDF Export
       ↓
OWL / Protégé / SPARQL interoperability
```

Ontology reasoning must not invent new Quranic semantic authority.

---

# 33. Phase R1 — Knowledge Graph Foundation

Activation:

after `V3_INDEPENDENTLY_CONFIRMED`.

## Goal

Provide a real governed graph projection supporting Knowledge Explorer and dependency analysis.

## Scope

R1 includes:

- canonical Graph Vocabulary;
- KnowledgeNode;
- KnowledgeEdge;
- projection service;
- projection rebuild;
- NetworkX analysis;
- backend read models/APIs;
- React Flow integration;
- provenance;
- tests.

## R1 Acceptance

Must prove:

1. graph projection is rebuildable;
2. deleting graph projection does not delete canonical knowledge;
3. every graph edge has origin/provenance;
4. canonical dependency projection matches source records;
5. graph traversal cannot mutate canonical knowledge;
6. candidate semantic relations are not represented as established edges;
7. Knowledge Explorer uses real backend graph data;
8. textual/table fallback exists;
9. migration/model parity passes;
10. relevant Browser E2E passes.

Completion state:

`R1_VERIFIED_FOR_PROFILE`

not release acceptance.

---

# 34. Phase R2 — Vector Discovery

Activation:

after R1 verification.

## Goal

Provide safe candidate discovery.

## Scope

R2 includes:

- benchmark dataset;
- embedding model evaluation;
- embedding-space definitions;
- sqlite-vec Spike;
- index schema;
- index lifecycle/rebuild;
- candidate-neighbor discovery;
- candidate-counterevidence discovery;
- provenance;
- UI labels;
- tests.

## R2 Acceptance

Must prove:

1. benchmark is reproducible;
2. adopted model wins/qualifies under documented metrics;
3. vector index is rebuildable;
4. canonical knowledge survives complete vector-index deletion;
5. source/model revisions are recorded;
6. incompatible embedding spaces cannot be compared;
7. candidates are visibly labeled;
8. candidates cannot enter canonical Evidence without resolution;
9. Blind Lab cannot leak forbidden indexed sources;
10. performance is acceptable for representative local data.

Completion state:

`R2_VERIFIED_FOR_PROFILE`.

---

# 35. Phase R3 — Hybrid Retrieval

Activation:

after R1 and R2 verification.

## Goal

Combine Exact, Vector and Graph retrieval under one governed resolver.

## Required flow

```text
Query / Research Need
        ↓
Exact Retrieval
Vector Candidate Discovery
Graph Candidate Retrieval
        ↓
RetrievalCandidate Set
        ↓
EvidenceResolver
        ↓
AI Semantic Runtime
        ↓
Hypothesis / Differentiation
        ↓
Counterevidence / Falsification
        ↓
GateReport
```

## R3 Acceptance

Must prove:

1. Exact/Vector/Graph results retain source-layer labels;
2. exact canonical evidence cannot be overridden by similarity;
3. AI context preserves authority labels;
4. vector/graph candidates cannot directly pass Gates;
5. candidate provenance survives end-to-end;
6. EvidenceResolver resolves or rejects candidates deterministically where possible;
7. Hybrid Retrieval improves candidate discovery against the R2 benchmark or equivalent governed eval;
8. negative/adversarial cases exist;
9. Browser E2E covers affected Golden workflows;
10. no new authority lifecycle is introduced.

Completion state:

`R3_VERIFIED_FOR_PROFILE`.

---

# 36. Tooling Decisions

| Component | Decision |
|---|---|
| Canonical persistence | SQLite |
| Graph projection storage | SQLite |
| Graph analysis | NetworkX — `ADOPT_NEXT_AFTER_V3` |
| Graph UI | React Flow — `ADOPT_NEXT_AFTER_V3` |
| Vector store | sqlite-vec — `APPROVED_FOR_EVALUATION` |
| Vector upgrade | Qdrant Embedded/Local — `CONDITIONAL_LATER` |
| Qdrant Server | `DO_NOT_ADOPT_NOW` |
| Neo4j | `DO_NOT_ADOPT_NOW` |
| Embedding model | `TO_BE_SELECTED_BY_BENCHMARK` |
| RDFLib | `APPROVED_FOR_EVALUATION` |
| RDF/OWL | `CONDITIONAL_LATER` |
| Protégé | `LAB_ONLY` |
| Haystack/LlamaIndex | `CONDITIONAL_LATER`, external research only |
| LangChain | `DO_NOT_ADOPT_NOW` |
| Prolog | `DO_NOT_ADOPT_NOW` |

Do not modify these statuses without a governed architecture/tooling decision.

---

# 37. Verification Strategy

Use the project V0–V4 cadence.

Within R1–R3:

### V1

Focused unit/property/static checks.

### V2

Phase sub-boundary integration:

- migrations;
- API;
- projection/index;
- provenance;
- frontend contract sync.

### V3-style phase checkpoint

At R1/R2/R3 closure:

- affected backend suite;
- Hypothesis invariants;
- Ruff;
- Pyright;
- migrations;
- OpenAPI;
- frontend build;
- contract testing;
- Browser E2E;
- applicable adversarial tests.

Do not automatically rerun full release verification during every retrieval phase.

---

# 38. Adversarial Invariants

At minimum test:

```text
Vector candidate ⇒ never canonical Evidence directly

Graph discovery candidate ⇒ never governed relation automatically

Index deletion ⇒ canonical knowledge unchanged

Embedding model change ⇒ affected index becomes stale

Forbidden Blind Lab source ⇒ no retrieval path exposes it

Vector similarity ⇒ never Gate PASS

Graph path ⇒ never semantic lock

Candidate provenance ⇒ always retained

Cross-embedding-space comparison ⇒ rejected

Fixture candidate ⇒ never production canonical admission
```

Use property/stateful tests where useful.

---

# 39. Prohibited Architectural Patterns

Do NOT:

- create a second authoritative knowledge database;
- use vector similarity as semantic confidence;
- use graph centrality as semantic importance;
- automatically accept nearest neighbors;
- automatically create semantic edges from AI output;
- mix external-source vectors with canonical Corpus vectors without source separation;
- bypass Blind Lab using cached indexes;
- adopt Neo4j/Qdrant Server merely because Graph/Vector features exist;
- introduce microservices for retrieval;
- allow UI to write graph/vector-derived canonical knowledge directly;
- let Stitch prototype data become production truth.

---

# 40. Documentation Synchronization

This contract is the single canonical source for Hybrid Retrieval architecture.

Other documents MUST reference it rather than duplicate it.

The executing agent must reconcile the following:

## 40.1 Platform Reference

Update:

`docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md`

Add one concise reference:

> Hybrid retrieval, Knowledge Graph, Vector Discovery and EvidenceResolver architecture are governed by `LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`.

Do not duplicate this document.

## 40.2 Tooling Reference

Update:

`docs/canonical/LISAN_TOOLING_ADOPTION_REFERENCE.md`

Reconcile tool statuses with Section 36.

Do not maintain conflicting statuses.

## 40.3 UI / Backend Matrix

Update:

`docs/canonical/UI_BACKEND_CONTRACT_MATRIX.md`

Map affected Golden capabilities:

- Knowledge Explorer;
- Semantic Differentiation Lab;
- Purity;
- Provenance;
- Dependency Explorer;
- relevant Ask Lisan/research tooling.

Mark the mappings as:

`R1 — PLANNED / ACTIVATION_ALLOWED_POST_V3`

and:

`R2/R3 — PLANNED`

until their predecessor phase has been verified.

## 40.4 Domain Model

If:

`docs/canonical/LISAN_DOMAIN_MODEL.md`

exists, add only the derived retrieval concepts and reference this contract.

Do not duplicate complete schemas before implementation.

## 40.5 PROJECT_STATE

Record:

```text
Hybrid Retrieval Architecture:
CANONICAL_APPROVED

Activation Gate:
V3_INDEPENDENTLY_CONFIRMED — SATISFIED

Current Retrieval Phase:
R1_NOT_STARTED
```

PROJECT_STATE remains non-authoritative.

---

# 41. AGENTS Enforcement

Root `AGENTS.md` must reference this document under Canonical References:

`docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`

Do not copy its rules into AGENTS.

Scoped backend/frontend AGENTS files may state:

> For Graph, Vector, Knowledge Explorer, retrieval, or hybrid-search changes, read and follow `LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`.

This establishes just-in-time policy loading while keeping root AGENTS small.

---

# 42. Repository Skill

Create a small repo-scoped execution skill if the active agent environment supports repository skills:

`.agents/skills/lisan-hybrid-retrieval/SKILL.md`

The skill MUST NOT duplicate this architecture.

Its procedure should only:

1. read applicable AGENTS policy;
2. read this canonical contract;
3. verify V3 activation gate;
4. identify R1/R2/R3 current phase;
5. build acceptance-to-evidence map;
6. implement only current phase;
7. run focused verification;
8. perform adversarial self-review;
9. update PROJECT_STATE.

If repository skills are unsupported, AGENTS + canonical-reference enforcement is sufficient.

---

# 43. Change Control

Any future proposal that changes one of these decisions requires an explicit governed change:

- Graph becoming authoritative;
- Vector results becoming Evidence directly;
- changing SQLite Graph storage to Graph DB;
- changing sqlite-vec to external Vector service;
- selecting an embedding model;
- merging embedding spaces;
- changing CandidateEvidence authority;
- enabling external indexes inside Blind Lab;
- adopting RDF/OWL as runtime inference;
- changing R1→R2→R3 ordering.

Do not implement such changes from agent preference alone.

---

# 44. Completion and Claim Discipline

Agents must distinguish:

```text
DOCUMENT_APPROVED
IMPLEMENTED
TESTED
VERIFIED_FOR_PROFILE
TECHNICALLY_RELEASE_READY
INDEPENDENTLY_REVIEWED
RELEASE_ACCEPTED
```

This document being canonical does not mean R1–R3 are implemented.

Likewise:

```text
sqlite-vec installed ≠ Vector Discovery verified

NetworkX installed ≠ Knowledge Graph verified

React Flow rendered ≠ governed graph correct

Embedding generated ≠ semantic discovery valid
```

---

# 45. Current Decision

Effective immediately:

```text
Architecture:
APPROVED

Authority:
CANONICAL

R1 activation state:
V3_GATE_SATISFIED / R1_ALLOWED

R2/R3 activation state:
PHASE_GATED

Execution order:
R1 → R2 → R3
```

R1 remains `NOT_STARTED` until an owner separately authorizes its bounded work
package. No agent may use this architecture contract to bypass the phase order
or expand unrelated work.

---

# 46. Final Rule

> **Lisan uses exact retrieval to resolve evidence, vector retrieval to discover possible similarity, graph retrieval to expose governed relationships and candidate paths, and AI to coordinate research. None of those mechanisms independently determines Quranic semantic truth.**

All derived discovery must eventually return to:

```text
Corpus
→ Evidence
→ Counterevidence
→ Falsification
→ Gates
→ Governance
```

before it can influence governed knowledge.
