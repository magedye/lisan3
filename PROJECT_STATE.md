# Lisanapp Project State

State context only. Canonical repository contracts and runtime evidence remain authoritative.

## Repository

- Root: `D:\APP\tafseer\lisanapp3`
- Branch: `main`
- R1 remediation baseline: `8a4a8884ac9b3ce353ed00c0948cf878ff8daa40`
- V3 remediation implementation commit: `1deab3251ac1dc53ef772d10f99c9fd32284e557`
- Independently reviewed V3 candidate: `6bb6505484dd649d092032a36d456f9f7fba5da1`
- V3 review provenance: fresh independent read-only review in a clean detached checkout of that exact SHA.
- Independently reviewed R1 candidate: `a0d10d7fd5ff8845d3071b7e68f1500f92fd9563`
- R1 review provenance: fresh focused independent read-only review in a clean detached checkout of that exact SHA.
- This state record is post-review administrative history. Any later state-only commit does not replace or extend either independently reviewed candidate.
- Remote publication: not authorized and not performed
- Owner-added untracked files are intentionally preserved and excluded from the candidate

## Gate State

- V3 implementation state: `V3_REMEDIATED`
- V3 independent state: `V3_INDEPENDENTLY_CONFIRMED`
- V3 confirmation applies only to: `6bb6505484dd649d092032a36d456f9f7fba5da1`
- V4 entry: `V4_ENTRY_UNBLOCKED_NOT_STARTED`
- R1: `R1_INDEPENDENTLY_CONFIRMED`
- R1 confirmation applies only to: `a0d10d7fd5ff8845d3071b7e68f1500f92fd9563`
- R2: `NOT_STARTED`
- R3: `NOT_STARTED`
- `V4_COMPLETE`, `TECHNICALLY_RELEASE_READY`, and `RELEASE_ACCEPTED` are not established.

No implementation thread claim may grant independent confirmation or release acceptance. The recorded V3 and R1 independent statuses above are review results, not implementation claims.

## Hybrid Retrieval Architecture

- Architecture state: `CANONICAL_APPROVED`
- Canonical reference: `docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`
- Activation Gate: `V3_INDEPENDENTLY_CONFIRMED — SATISFIED`
- V3 confirmation provenance remains limited to: `6bb6505484dd649d092032a36d456f9f7fba5da1`
- Execution order: `R1 → R2 → R3`
- Current retrieval phase: `R1_INDEPENDENTLY_CONFIRMED`
- R1 is independently confirmed only for its reviewed candidate; R2 and R3 remain `NOT_STARTED` pending separate owner authorization.
- The R1 graph is a SQLite-derived projection of governed state, rebuildable without mutating canonical sources. NetworkX is in-process and disposable; React Flow is a read-only Knowledge Explorer with a textual provenance fallback. No Vector, embeddings, Qdrant, Neo4j, RDF persistence, or graph server was introduced.

## Remediation Completed

- F1: restored canonical Alembic squash `80330541af56`, added reversible forward migration `f4c0a1b2c3d4`, and verified all 19 tables plus every model column from a fresh `base -> head` database. The dedicated migration-parity and E2E startup paths use Alembic rather than `Base.metadata.create_all()`.
- F4: separated source-role approval, artifact presence, expected canonical hash, hash verification, import validation, and production activation. Local/fixture hashes remain `UNVERIFIED` and cannot create production `VALIDATED` snapshots.
- F5: audit API is read-only; Purity and Internal Lock are derived from current DB evidence; forged/stale/manual GateReports cannot authorize locking, claim creation, isolation release, or publication; unsupported Purity dimensions remain `NOT_EVALUATED` and fail closed.
- F3: focused Cosmic Ray profiles cover registry admission, Corpus authority, and Gate authority. Latest implementation evidence has zero critical survivors; any retained survivor is documented as equivalent.
- Hypothesis: DB-backed generated properties exercise exact entity traceability, dependency binding, multi-entity isolation, gate sequencing, invalid audit mutation rejection, and AI non-authority.
- F6: runtime OpenAPI, canonical OpenAPI, and frontend TypeScript bindings are synchronized and reproducible; Schemathesis four-check profile and frontend production build pass.
- E2E: five Playwright journeys use the production Next.js frontend against FastAPI and isolated file-backed Alembic persistence; teardown leaves no repository Node child process.

## Independent V3 Evidence (Candidate-Bound)

- Fresh detached review command profile: 62 pytest tests passed; the five Playwright E2E journeys passed and left no Next start process.
- Fresh Alembic `base -> head`: `80330541af56 -> f4c0a1b2c3d4`; exact 19/19 model table and column parity.
- Schemathesis 4.25.0 on a live FastAPI server: all 32 operations, required four checks, 1,389 generated and passed; 0 failures; 0 errors.
- Cosmic Ray: Registry 116 total / 113 killed / 3 equivalent survivors; Corpus 99 / 99 killed / 0 survivors; Gates 164 / 163 killed / 1 equivalent survivor; 0 critical survivors.
- Ruff: pass. Pyright: 0 errors and 184 existing SQLAlchemy typing warnings.
- `npm ci` and production `npm run build`: pass. Runtime OpenAPI, both committed OpenAPI files, and regenerated frontend TypeScript bindings matched exactly.

## Unresolved Independent Status Axes

- AI profile: governed exploratory runtime only; fake/test-provider execution remains test evidence, not live-AI or methodology-eval verification.
- Corpus authority: no authority-bound expected canonical hash or production activation is currently evidenced for Tanzil/QAC; fixture/imported snapshots remain unverified and cannot enter production canonical knowledge.
- Promptfoo: `CONFIGURED_NOT_EXECUTABLE` (configuration exists; CLI and referenced runner are absent).
- pip-audit: `NOT_CONFIGURED_NOT_EXECUTED`.
- accessibility/axe profile: `NOT_CONFIGURED_NOT_EXECUTED`.

## V4 Entry Plan (Not Started)

- V4 is the release gate, run only on the actual release candidate; it is not granted by V3 confirmation.
- Establish the V4 candidate identity first, then execute the full project-defined verification, frontend/backend builds, tests, contracts, migrations, critical E2E, security/authorization checks, and accessibility/performance checks where executable.
- Apply the tooling adoption reference at execution time: full pytest, Hypothesis, Schemathesis, applicable Promptfoo suite, focused Cosmic Ray, Playwright, frontend build, OpenAPI/client sync, Ruff, type checking, pip-audit, npm audit, and accessibility checks. Selected Z3 invariants remain conditional on adoption.
- Resolve tool availability and applicability before classifying V4: Promptfoo requires a real applicable AI-eval target/baseline; pip-audit and npm audit require executable dependency-audit profiles; accessibility requires an executable baseline. Do not claim tool execution from installation or configuration alone.
- V4 completion remains blocked until its candidate-bound required evidence is executed and independently assessed. No V4 implementation, release publication, or release acceptance is authorized by this record.

## Sequencing

- The Hybrid Retrieval canonical contract is durable in Git, recognizes `V3_INDEPENDENTLY_CONFIRMED` and `R1_INDEPENDENTLY_CONFIRMED` as satisfied for their respective reviewed candidates, and orders work `R1 -> R2 -> R3`.
- It does not establish V4-before-R1 precedence. V4 must be performed on the later actual release candidate and is not a substitute for R1 acceptance.
- R1 is independently confirmed. R2 runtime implementation has not begun;
  only the separately authorized benchmark evaluation described below exists.
  R3 remains `NOT_STARTED`.

## R1 Implementation-Side Evidence

- Forward migration `b7e4c1d9a5f2` adds `KnowledgeNode` and `KnowledgeEdge` projection storage after the accepted migration head. Fresh migration/model parity passed.
- Blind Lab projection now selects only runs with a current valid Internal Lock Gate and a present `CLEAN` isolation state. Rebuild replaces the disposable graph, so pre-lock, contaminated, and newly ineligible sources have no persisted or NetworkX-visible projection while canonical records remain unchanged.
- The R1 canonical contract permits string-like opaque `provenance_ref` values and does not establish an R1 referential provenance registry. Edge origin, provenance presence, governed vocabulary, and candidate non-authority remain enforced and tested without adding a new provenance architecture.
- Root Alembic now imports the registered domain model metadata. Fresh `base -> head`, project parity, and `alembic check` all pass; no migration history changed.
- Clean Python resolution passes with `pydantic-ai-slim[openai]==2.33.0`, preserving the used Agent/TestModel/OpenAI runtime while avoiding the unused `web` extra that conflicted with the intentional `uvicorn==0.30.1` pin. Clean `npm ci` installed 480 packages and the production frontend build passed.
- Complete pytest: 81 passed. Focused R1 graph profile: 19 passed, including exact reachability, generated mixed eligibility, and adversarial stale/scope cases. Journey 6 passed against production Next.js, live FastAPI, and isolated file-backed Alembic SQLite.
- The repository-owned `run_r1_critical_mutations.py` deterministically selects 32 authority-critical mutations across eligibility, Gate/isolation checks, rebuild filtering, run/entity scope, dependency vocabulary, reachability, and presentation authority. Its exact-count and source-fingerprint checks fail closed on profile drift. The focused profile kills every non-equivalent critical mutation; the retained `CLEAN ==` to `CLEAN <=` survivor is equivalent because current Gate evaluation independently requires exact `CLEAN` isolation.
- Schemathesis 4.25.0 selected both R1 graph operations with the required four checks: 56 generated cases passed, 0 failures, 0 errors. Runtime OpenAPI, both committed OpenAPI files, and regenerated TypeScript bindings match exactly.
- Ruff passes for every Git-tracked Python file. Pyright reports 0 errors and 144 existing SQLAlchemy typing warnings.
- This implementation-side evidence does not by itself establish independent review, release readiness, R2/R3 activation, or V4 evidence; the separate candidate-bound R1 review result is recorded below.

## Independent R1 Evidence (Candidate-Bound)

- Reviewed candidate: `a0d10d7fd5ff8845d3071b7e68f1500f92fd9563`.
- A fresh focused read-only review in a clean detached checkout confirmed the change was limited to R1 regression/mutation verification and state artifacts, with no production, R2, or R3 behavior change.
- The exact reachability regression passed; the focused R1 graph suite passed 19 tests; relevant Blind Lab/isolation coverage passed 3 tests; Ruff passed; Pyright reported 0 errors.
- The reproducible R1 Cosmic Ray profile selected 32 authority-critical mutations from a 231-mutation universe: 31 killed, 1 independently equivalent survivor, and 0 non-equivalent critical survivors. The previously surviving `read:351 AddNot` reachability mutation was killed.
- Independent result: `R1_INDEPENDENTLY_CONFIRMED`. This result applies only to the reviewed candidate above and does not establish R2/R3 activation, V4 completion, technical release readiness, or release acceptance.

## R2 Benchmark Evidence and Stop Boundary

- R2 execution baseline: `3a8c77aea1b2b919ca817f9dce3d84e236006702` on `main`; owner files `check_db2.py` and `debug_proxy.py` remained untracked and untouched.
- The reproducible benchmark covers six separate embedding spaces, 30 candidate documents, 12 queries, all required case classes, explicit fixture/synthetic provenance, and non-authority labels.
- Evaluated exact revisions of multilingual E5 small, Arabic E5 NLI Matryoshka, and paraphrase multilingual MiniLM; each produced 384-dimensional normalized local CPU embeddings.
- Macro nDCG@3 was `0.687701`, `0.852049`, and `0.751876` respectively. No candidate satisfied every predeclared per-space threshold. `CLAIM` and `STRUCTURAL_PROFILE` had no qualifying model; the aggregate leader also failed the `ROOT_CANDIDATE` false-positive trap.
- Decision: `EMBEDDING_MODEL_SELECTION_BLOCKED`. No default/production model was selected and no thresholds or labels were changed after execution.
- Two complete cached executions produced byte-identical `results.json` evidence with runner + manifest + corpus input SHA-256 `2c6f22ff2ee31299c0342aa53d097fb1990880decabc56385920b1cb622b9d25` and result SHA-256 `DC2F6F6B353773BA2E1DDFAC618F51B8C21E401E2ED9A8B1A16E89CDCC575B56`.
- `sqlite-vec==0.1.9` is a development evaluation dependency only. Import compatibility with Python 3.12 / SQLite 3.49.1 was observed, but the R2 persistence/filter/rebuild/recovery/performance Spike was not executed after the authorized model-selection stop condition. Its status remains `APPROVED_FOR_EVALUATION`.
- No R2 migration, embedding persistence, vector runtime, API, UI, OpenAPI binding, Schemathesis, E2E, or mutation profile was implemented or claimed. R2 is `NOT_READY`; R3 and V4 remain `NOT_STARTED`.
- Durable evaluation report: `tools/governance-lab/reports/R2_VECTOR_BENCHMARK_DECISION.md`; machine-readable results: `tools/governance-lab/vector-benchmark/r2/results.json`.

## Exact Next Action

Independent architecture review of `EMBEDDING_MODEL_SELECTION_BLOCKED`: authorize an expanded candidate set, per-space model selection, or a governed benchmark/threshold revision. Then rerun the exact R2 benchmark before any default-model adoption or vector runtime implementation. Do not begin R3 or V4 implementation.
