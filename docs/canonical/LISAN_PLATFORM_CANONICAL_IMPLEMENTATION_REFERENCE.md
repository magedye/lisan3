# Lisanapp Canonical Implementation Reference

*See the [Tooling Adoption Reference](./LISAN_TOOLING_ADOPTION_REFERENCE.md) for canonical rules regarding allowed tools and frameworks.*

Hybrid Retrieval, Knowledge Graph, Vector Discovery, EvidenceResolver, and
their AI Runtime integration are governed by
[`LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`](./LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md).

## Product Mission
Transform the current materials into a single governed, maintainable, testable Lisan application implementation that connects the already-designed Stitch Golden UX to a real governed backend and semantic runtime.

## Authority Hierarchy & Ownership
- **Governance**: Owned by authoritative domain models and registries. Changes require explicit rule revisions via Change Proposals and Impact Analyses.
- **UX**: Owned by the UX Constitution v4.0 and the Stitch Golden Prototype (visuals).
- **Semantic Runtime**: Owned by the Canonical Runtime Skill (`skills/lisan-semantic-extraction/SKILL.md`).
- **Application Backend**: Owned by the Python/FastAPI codebase.
- **Application Frontend**: Owned by the Next.js/React codebase.

## Application Architecture
- **Type**: Modular Monolith.
- **Backend**: Python, FastAPI, SQLite, SQLAlchemy, Pydantic v2.
- **Frontend**: Next.js, TypeScript, Tailwind CSS, CSS Logical Properties (RTL), Radix UI.
- **API Boundary**: RESTful JSON over OpenAPI with typed frontend clients.
- **Identity & Authorization**: Trusted local single-user context. Domain invariants and state transitions enforce authority constraints (e.g. Steward role logic) without a JWT or User database.

## Governance & Status Model
The four status axes remain completely independent:
1. **Epistemic Status** (e.g., `LOCK_BLOCKED`, `NOT_ESTABLISHED`)
2. **Review Status** (e.g., `NOT_REVIEWED`, `INDEPENDENTLY_REVIEWED`)
3. **Freshness Status** (e.g., `CURRENT`, `STALE`)
4. **Publication Status** (e.g., `PRIVATE_WORKING`, `PUBLISHED`)

## Provenance & Reproducibility Model
All semantic changes must trace back through:
- Claim → Evidence → Artifact → Research Run → Corpus Snapshot → Methodology Revision.
- A deterministic Reproduction Manifest can be generated from the backend.

## Change-Control Policy
- **Workflow vs Epistemic States**: Workflow progression (e.g., analysis stage) never automatically grants epistemic lock or publication authority.
- **Governance Rules**: Existing governing revisions cannot be mutated in place. New revisions must be created, triggering transitive invalidation assessments.

## Methodology Revision Authority
- The active methodology source is `skills/lisan-semantic-extraction/SKILL.md`.
- Every ResearchRun-eligible revision is an immutable registry record bound to
  the source path and SHA-256, its authority reference, allowed use, and its
  independent `CURRENT` or `RETIRED` lifecycle state.
- Identity, provenance, source binding, and allowed use cannot be mutated after
  insert; only lifecycle and eligibility may change to retire or revoke future use.
- ResearchRun admission accepts only a present, `CURRENT`, explicitly eligible
  registry revision whose source bytes still match the recorded SHA-256.
- A source change requires a new registry revision. Retiring or revoking a
  revision prevents future run admission without rewriting historical runs.

## Canonical Corpus Pre-Activation Authority

- `docs/canonical/ADMISSION_TANZIL.md` owns the LISAN3 Tanzil source identity,
  exact version, immutable artifact/index references, expected hashes, format,
  provenance, and pre-activation lifecycle boundary.
- A caller-supplied matching hash is parsing evidence only. Import validation
  requires the authority-bound expected hash to exist before bytes are read and
  verified.
- The canonical text layer preserves every admitted verse record byte-for-byte
  after strict UTF-8 decoding. It performs no Unicode normalization.
- The governed importer reconciles the artifact to the authority-bound 114-surah,
  6,236-identity index, then persists one deterministic snapshot identity and
  one deterministic occurrence identity per verse. An exact retry verifies and
  reuses that state; it cannot create a competing snapshot.
- `IMPORT_VALIDATED`, `VALIDATED`, and `PRODUCTION_ACTIVE` are distinct. Import
  validation does not grant production activation, and ResearchRun admission
  continues to require a separately production-active snapshot.
- QAC remains an optional auxiliary morphology/syntax candidate. Tanzil
  canonical-text import does not inherit QAC semantic/gloss/ontology fields and
  does not depend on a real-format QAC importer.

### Tooling and Verification

Lisanapp uses strict evidence-based verification. Test coverage is divided into standard unit tests (`pytest`), randomized invariant checking (`hypothesis`), property-based contract checking (`schemathesis`), bounding mutation checking (`cosmic-ray`), and canonical journeys (`playwright`).

## 8. Migration Policy

The current Alembic migration history (e.g., `80330541af56_initial_schema.py`) represents an intentional squash of the Lisanapp database schema at the V3 milestone.
All subsequent schema changes MUST be generated as incremental, reversible Alembic migrations layered on top of this initial squash.
Direct modification of the initial migration file is prohibited.

## AI Semantic Runtime
Lisanapp is an AI-assisted governed Quranic semantic research application. AI serves as a primary exploratory and analytical runtime (proposing, exploring, comparing, challenging, synthesizing, explaining). AI is NOT an authority source, canonical corpus, validator, gate, review authority, or publication authority.

- **AI Proposals vs. Evidence**: AI output is strictly a proposal until resolved against canonical contracts, evidence validators, and Gate logic. AI output must NEVER be converted directly into `authoritative semantic truth`, `LOCK_INTERNAL_RESULT`, or `PUBLISHED`.
- **Relationship with Semantic Skill**: The active Canonical Runtime Skill (`skills/lisan-semantic-extraction/SKILL.md`) governs the AI agent's instructions.
- **Relationship with Canonical Corpus**: AI must not use its private memory as canonical Quranic evidence. The canonical Corpus supplies all textual evidence.
- **Structured-Output Requirements**: All AI proposals entering the governed application must be parsed and validated through Pydantic schemas. Malformed outputs must fail safely.
- **Tool-Use Rules**: The model may only access truly available tools via a controlled Dispatcher. Simulated tools are never reported as executed.
- **Blind Lab AI-Context Isolation**: Before valid Internal Lock, the `AIContextBuilder` strictly isolates the AI model's context. Forbidden semantic artifacts (Owner answers, previous Root Cores, non-admitted dictionaries, post-lock comparisons) are strictly excluded from the prompt payload.
- **Provenance & Reproducibility**: AI usage must be traceable via an `AIExecutionRecord` that persists provider, model identity, tool actions, evidence refs, skill version, and structured outputs. Hidden chain-of-thought is explicitly NOT persisted as an artifact.
- **Provider Independence & Degraded Mode**: The domain layer uses a generic provider abstraction (e.g., `ModelProvider`). When no live model is available, the application remains fully operational, preserving existing deterministic data without inventing semantics.
