# Lisanapp Project State

State context only. Canonical repository contracts and runtime evidence remain authoritative.

## Repository

- Root: `D:\APP\tafseer\lisanapp3`
- Branch: `main`
- Tanzil production-activation implementation candidate:
  `a1d910f11735ec4ba0e9324dbb82b800efd485f6`
- UI governance-remediation implementation candidate:
  `43c27e6dd2393d24be21805b4b2ea42b78d15955`
- UI completion state: `IMPLEMENTED`, `TESTED`, `VERIFIED_FOR_PROFILE`, and
  `INDEPENDENTLY_REVIEWED` for the bounded UI Completion profile.
- UI independent-review provenance: product-behavior conclusions are bound to
  implementation candidate `43c27e6dd2393d24be21805b4b2ea42b78d15955`;
  the reviewed documentation checkpoint is
  `c3f1ffe1b44d632323ff706c2c83a91831e1c450`.
- Prior UI completion candidate `4a6ef34be5fd0916b9285deba96a27507bafac30`
  received the independent verdict `UI_COMPLETION_INDEPENDENT_REVIEW_FAILED`;
  documentation checkpoint `e0238aea767a8314463c4734a3d48c3a191e4850`
  records that pre-remediation state.
- R1 remediation baseline: `8a4a8884ac9b3ce353ed00c0948cf878ff8daa40`
- V3 remediation implementation commit: `1deab3251ac1dc53ef772d10f99c9fd32284e557`
- Independently reviewed V3 candidate: `6bb6505484dd649d092032a36d456f9f7fba5da1`
- V3 review provenance: fresh independent read-only review in a clean detached checkout of that exact SHA.
- Independently reviewed R1 candidate: `a0d10d7fd5ff8845d3071b7e68f1500f92fd9563`
- R1 review provenance: fresh focused independent read-only review in a clean detached checkout of that exact SHA.
- This state record is post-review administrative history. Its later
  state-only commit is not independently reviewed for product behavior and
  does not replace or extend any independently reviewed candidate.
- Remote publication: not authorized and not performed
- Owner-added untracked files are intentionally preserved and excluded from the candidate

## Gate State

- UI Completion profile: `IMPLEMENTED`, `TESTED`, `VERIFIED_FOR_PROFILE`,
  `INDEPENDENTLY_REVIEWED`
- UI Completion independent review applies only to:
  `43c27e6dd2393d24be21805b4b2ea42b78d15955`
- V3 implementation state: `V3_REMEDIATED`
- V3 independent state: `V3_INDEPENDENTLY_CONFIRMED`
- V3 confirmation applies only to: `6bb6505484dd649d092032a36d456f9f7fba5da1`
- V4 entry: `V4_ENTRY_UNBLOCKED_NOT_STARTED`
- R1: `R1_INDEPENDENTLY_CONFIRMED`
- R1 confirmation applies only to: `a0d10d7fd5ff8845d3071b7e68f1500f92fd9563`
- Stabilization remediation independent state:
  `STABILIZATION_REMEDIATION_INDEPENDENTLY_CONFIRMED`
- Stabilization confirmation applies only to owner-supplied candidate:
  `f202a1e703b8da97bb0df419c9149052758505cc`
- R2 benchmark: completed with `EMBEDDING_MODEL_SELECTION_BLOCKED`
- R2 model-agnostic infrastructure: implementation-side `IMPLEMENTED` and
  `TESTED` at `2449ac4db7102a0a62ae9622c6f668bb71602ef8`; independent review
  and complete R2 acceptance are not established
- Production embedding model: not selected; evaluated models remain `NOT_ADOPTED`
- Production vector retrieval: not established
- R2 completion and independent confirmation: not established
- R3: `NOT_STARTED`
- `V4_COMPLETE`, `TECHNICALLY_RELEASE_READY`, and `RELEASE_ACCEPTED` are not established.

No implementation thread claim may grant independent confirmation or release acceptance. The recorded V3 and R1 independent statuses above are review results, not implementation claims.

## Hybrid Retrieval Architecture

- Architecture state: `CANONICAL_APPROVED`
- Canonical reference: `docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`
- Activation Gate: `V3_INDEPENDENTLY_CONFIRMED — SATISFIED`
- V3 confirmation provenance remains limited to: `6bb6505484dd649d092032a36d456f9f7fba5da1`
- Execution order: `R1 → R2 → R3`
- Current retrieval phase: bounded model-agnostic R2 infrastructure checkpoint
- R1 is independently confirmed only for its reviewed candidate. The owner
  separately authorized bounded model-agnostic R2 infrastructure while model
  selection is deferred; R3 remains `NOT_STARTED`.
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
- Corpus authority: exact Tanzil 1.1 snapshot
  `snap_tanzil_1_1_ac0724796cbb` is `VALIDATED` and `PRODUCTION_ACTIVE` after
  governed owner-authorized activation. QAC artifact verification and
  real-format import remain pending and separate.
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
- R1 is independently confirmed. The separately authorized R2 benchmark and
  model-agnostic infrastructure checkpoint described below now exist; no
  production model/vector runtime exists. R3 remains `NOT_STARTED`.

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
- At that benchmark stop boundary, no R2 migration, embedding persistence,
  vector runtime, API, UI, OpenAPI binding, Schemathesis, E2E, or mutation
  profile had been implemented or claimed. The later model-agnostic
  infrastructure checkpoint is recorded separately below. R2 was `NOT_READY`;
  R3 and V4 remained `NOT_STARTED`.
- Durable evaluation report: `tools/governance-lab/reports/R2_VECTOR_BENCHMARK_DECISION.md`; machine-readable results: `tools/governance-lab/vector-benchmark/r2/results.json`.

## R2 Model-Agnostic Vector Infrastructure Evidence

- The benchmark above remains frozen and unchanged. Production model selection
  is delegated to `LISAN-Quran-Embedding`; no model weights, inference, default
  provider, or production vector population was added.
- Canonical R2 authority permits this bounded continuation because verified R1
  activates R2 and the R2 scope separately includes embedding-space contracts,
  sqlite-vec evaluation, index schema/lifecycle, provenance, and tests. Complete
  R2 acceptance remains unavailable without a qualifying adopted model.
- Reversible migration `c9e2a7f4b6d1` adds evaluation-only derived embedding
  persistence. Constraints admit only `BENCHMARK_ONLY` or
  `SYNTHETIC_EVALUATION` and reject production-eligible state.
- Provider-independent manifest/adapter contracts have no adapter
  implementation. Production handoff fails closed without a governed decision
  reference for the requested space.
- Deterministic rebuild, deletion/recovery, source/model/config invalidation,
  current/stale rejection, and all six embedding-space boundaries are tested.
- Blind Lab checks reject missing isolation, pre-lock, contaminated, ineligible,
  cross-run, and cross-space access. Blocked access does not mark contamination.
- `RetrievalCandidate` remains `VECTOR` / `CANDIDATE` /
  `DERIVED_DISCOVERY_NON_AUTHORITATIVE`; similarity is not confidence and no
  SemanticClaim, Gate, Internal Lock, review/publication state, or KnowledgeEdge
  is mutated.
- sqlite-vec v0.1.9 result: `SQLITE_VEC_EVALUATION_PASSED` for 5,000
  deterministic 32-dimensional synthetic vectors. Build was 0.627351 seconds;
  100-query p95 was 52.904200 ms under predeclared 5-second/100-ms limits.
  Canonical status remains `APPROVED_FOR_EVALUATION`.
- Pre-commit focused R2 profile: 30 passed; full pytest: 118 passed. Fresh
  migration parity, downgrade/re-upgrade, and `alembic check`: passed. Ruff:
  passed. Pyright: 0 errors and 144 existing SQLAlchemy-style warnings. pip
  check and `git diff --check`: passed.
- Authority-critical Cosmic Ray: 291 universe / 29 selected / 29 killed / 0
  survivors, bound to vector service SHA-256
  `3382eed7668bfcaa05c8c9ec77d57881987faab8f205aef80b14e3719edb2799`.
- Durable report:
  `tools/governance-lab/reports/R2_MODEL_AGNOSTIC_VECTOR_INFRASTRUCTURE.md`;
  Spike result: `tools/governance-lab/vector-spike/r2/results.json`.
- This is implementation-side evidence only. R2 is not independently confirmed
  or complete; no API/UI/R3/V4 work was performed.
- Coherent implementation commits are `a18e4615dd6581f61c01e6ca6a1fc298a4855f6c`,
  `4ab5d6f6d3f989bffe77b23f646c895afb462aca`, and candidate
  `c64d4531c918c47943b45423ee02d0fc501ad2f6`.
- Clean detached verification of candidate `c64d4531c918c47943b45423ee02d0fc501ad2f6`
  passed Ruff, Pyright (0 errors / 144 existing warnings), all 112 non-E2E
  tests, the live sqlite-vec Spike, the 29/29 critical mutation profile, the
  frozen-benchmark comparison, and final clean-worktree checks.
- Historical broad verification of `c64d453...` reached 117 passed with one
  Governance Review E2E race (`Revision: 1` observed before the async approval
  response) and an intermittent Next setup failure. That result remains
  candidate-bound history only; the signal is classified and corrected in the
  later model-independent checkpoint below.

## R2 Model-Independent Completion Checkpoint

- `2449ac4db7102a0a62ae9622c6f668bb71602ef8` hardens the external production
  handoff without selecting, loading, or integrating a model. The contract
  requires immutable artifact identity/hash, tokenizer/config hashes, model
  identity/dimension/normalization/spaces, Quran corpus binding, benchmark
  metrics, limitations/license, reproducibility/independent-review evidence,
  and Blind-Lab/provenance/exposure declarations.
- The future adapter boundary rejects missing/evaluation manifests, mismatched
  artifact bytes, unsupported model revision/dimension/space,
  normalization/configuration drift, stale manifests, unapproved Blind-Lab
  eligibility, unknown/prohibited provenance/exposure, and Quran corpus
  mismatch. All evidence uses synthetic manifests/artifact bytes only.
- LISAN3 does not import, locate, execute, or require the external research
  checkout. The manifest accepts only portable `artifact://` identifiers.
- The outstanding Governance Review E2E signal is classified `TEST_DEFECT`:
  the test raced its history request ahead of the async approval response. It
  now waits for the successful approval POST; product governance code was not
  changed.
- Fresh detached verification of `2449ac4...` used a physical `npm ci` inside
  the verification checkout after an external Junction was rejected by
  Turbopack. It passed production frontend build, Ruff, Pyright (0 errors / 252
  existing warnings), full pytest (130 passed), all six Playwright journeys,
  R2 migration reversibility/parity, and R2 Cosmic Ray (291 / 29 / 29 killed /
  0 survivors). `pip check` found no broken requirements and production-only
  `npm audit` reported zero vulnerabilities. Generated caches were moved outside
  before the final clean-Git check.
- This checkpoint does not select a model, permit production vector population,
  activate a provider, establish `R2_VERIFIED_FOR_PROFILE`, independently
  confirm R2, or begin R3/V4.
- User-requested readiness indicator (not a canonical lifecycle state):
  `LISAN3_MODEL_INDEPENDENT_WORK_COMPLETE`.

## Runtime and Golden UX Stabilization Checkpoint

- Implementation candidate:
  `b95894365e03e49c4a47ad4f489549b55fc34730`; status is implementation-side
  `IMPLEMENTED` and `TESTED`, not independently reviewed or release accepted.
- The active local DB failure was a pre-V3 database at legacy revision
  `5542b3a62e23` against the intentional canonical root squash. The DB state was
  `STALE_CONTEXT`; cwd-relative configuration and unconditional readiness were
  separately corrected as a `PRODUCT_DEFECT`. No DB was deleted or stamped.
- Backend and Alembic now share a deterministic repository-local SQLite target,
  operational readiness fails closed on revision/table/column mismatch, and
  startup instructions are reproducible from the root README.
- The Golden Arabic RTL shell and truthful Attention Center are wired to the
  existing Ask/Create Run interaction; `/audit` is now a production route over
  the existing read-only backend contract. No Stitch fixture state or remote
  prototype asset was introduced.
- Clean detached verification applied the full migration chain to a fresh DB,
  passed 134 pytest tests including seven Playwright journeys, Ruff, ESLint,
  frontend production build, `pip check`, and production `npm audit`; Pyright
  reported 0 errors and 145 existing warnings. Live backend readiness and all
  eight frontend routes returned HTTP 200; Chromium reported no console errors.
- Full durable evidence and inventories:
  `docs/LISAN3_STABILIZATION_CHECKPOINT.md`.
- R2 remains at the model-independent checkpoint; model selection/integration,
  R3, and V4 remain unstarted.

## Stabilization Review Remediation Confirmation

- Candidate: `f202a1e703b8da97bb0df419c9149052758505cc`, direct child of documentation
  checkpoint `643230b1ad883d1caaca6813f0d03a26b1e09621`.
- The owner supplied the fresh independent result
  `PASS — STABILIZATION_REMEDIATION_INDEPENDENTLY_CONFIRMED`. The result is
  bound only to the candidate above and is not extended by later UI commits.
- The found-claim UI and real Journey 7 now require all four independent axes:
  Epistemic, Review, Freshness, and Publication. A focused parameterized test
  fails separately if any axis is absent.
- The existing `/ask` found-claim response now converts its ORM result through
  the existing `SemanticClaimResponse` contract. This closes the HTTP 500
  exposed by the new real-data Journey 7 path without changing a schema,
  model, migration, or authority value.
- `UI_BACKEND_CONTRACT_MATRIX.md` is reconciled to the implemented/tested Home
  Ask/Create Run flow and read-only `/audit` behavior without claiming the
  unavailable Attention Center read model or full Golden/Stitch completion.
  Its stale R1 wording is corrected only for independently confirmed candidate
  `a0d10d7fd5ff8845d3071b7e68f1500f92fd9563`.
- The stabilization report now records the legacy inventory as 7 application
  tables plus `alembic_version`.
- Exact-SHA clean detached verification passed: focused UI 4, relevant pytest
  13, Journey 7 1, all Playwright journeys 7, full pytest 139, Ruff, ESLint,
  Next production build, `pip check`, `npm audit --omit=dev`, fresh Alembic
  base-to-head at `c9e2a7f4b6d1`, live backend/frontend smoke, and
  `git diff --check`. Pyright reported 0 errors and 144 existing warnings.
- No R2 service, model integration, migration, R3, or V4 artifact changed.
  Production model integration, R3, and V4 remain unstarted. Owner files
  `check_db2.py` and `debug_proxy.py` remain untracked and untouched.

## UI Completion Checkpoint

- Initial task HEAD: `9cb924fd7cac8c2106258881e3b2e7253cfd4268`.
- Exact implementation candidate:
  `4a6ef34be5fd0916b9285deba96a27507bafac30`.
- All 28 Golden/Stitch pairs are classified exactly once: 8 current
  executable, 7 inventory-time backend gaps resolved with minimal reads,
  0 blocked only by a model artifact, 1 blocked by R2 confirmation/R3, and
  12 reference-only or superseded.
- All eight current production routes use real backend contracts and explicit
  loading, empty, error, blocked, and domain-specific non-current states.
- Exact-candidate detached verification passed 130 non-E2E tests, all 8
  Playwright journeys, Ruff, ESLint, Next build, generated-contract parity,
  `pip check`, production `npm audit`, live route smoke, browser console review,
  desktop/tablet/mobile visual review, and `git diff --check`. Pyright reported
  0 errors and 160 warnings.
- Durable evidence: `docs/LISAN3_UI_COMPLETION_CHECKPOINT.md`,
  `docs/STITCH_PRODUCTION_COVERAGE_MATRIX.md`, and
  `docs/evidence/ui/`.
- No model work, production vector activation, EvidenceResolver, R3, V4,
  release action, or push was performed.

## UI Governance and Data-Integrity Remediation Checkpoint

- Starting checkpoint: `e0238aea767a8314463c4734a3d48c3a191e4850`;
  remediated implementation candidate:
  `43c27e6dd2393d24be21805b4b2ea42b78d15955`.
- One `ClaimReleasePolicy` now governs Ask, direct claim, provenance,
  reproduction, quality, history, legacy Explorer, aggregate projections,
  audit reads, workspace claims, and R1 graph projection/read. It derives
  release from an existing linked run, `CLEAN` isolation, and a dynamically
  valid current Internal Lock.
- `/ask` returns `INSUFFICIENT_EVIDENCE` before release and the governed claim
  only after release. Unique semantic, evidence, and audit markers are covered
  by negative and positive production-path regressions.
- `POST /runs` now rejects unknown snapshots and fails closed while canonical
  Corpus activation and a Methodology registry/fallback are unavailable. The
  UI exposes that unavailable state and offers no free-text authority inputs.
- No Steward command is currently registered as executable. Arbitrary input is
  persisted/audited as `UNSUPPORTED`; authority-bypassing input is persisted
  and audited as `REJECTED`; no fixed rules, `PASS`, or fake `SUCCESS` remain.
- SemanticClaim persistence and public schemas use only the four canonical
  axes. Migration `d4f7a2c8e901` deterministically reconciles known legacy/null
  values with before/after audit evidence, refuses unknown meaning, adds DB
  constraints, and supports a tested downgrade. Review rejection no longer
  mutates Publication.
- A stored QualityProfile is returned unchanged. Without one, only the
  deterministic methodological-purity derivation is identified as derived;
  all other metrics are unavailable/null and the frontend says so.
- Clean detached exact-SHA verification passed: full pytest 156, explicit
  Playwright 8, Ruff, Pyright with 0 errors and 177 existing warnings, ESLint,
  Next production build, OpenAPI/TypeScript regeneration parity, fresh
  Alembic/model parity at `d4f7a2c8e901`, `pip check`, production npm audit
  with 0 vulnerabilities, route smoke, and Git diff/status checks.
- The non-blocking Governance ARIA tab pattern was not touched and remains a
  separate UI-quality follow-up. No model integration, production vector,
  R2/R3, V4, release, push, or `LISAN-Quran-Embedding` work was performed.
- Durable evidence: `docs/LISAN3_UI_GOVERNANCE_REMEDIATION_CHECKPOINT.md`.

## Independent UI Completion Review (Candidate-Bound)

- Independent verdict: `INDEPENDENTLY_REVIEWED`, bound to implementation
  candidate `43c27e6dd2393d24be21805b4b2ea42b78d15955` and reviewed documentation
  checkpoint `c3f1ffe1b44d632323ff706c2c83a91831e1c450`.
- The review confirmed closure of the claim-release/Blind Lab bypass, Steward
  fabricated success, Run Builder invalid authority admission,
  noncanonical/coupled status-axis behavior, and manufactured Quality metrics.
  Detailed candidate-bound evidence remains in
  `docs/LISAN3_UI_GOVERNANCE_REMEDIATION_CHECKPOINT.md`.
- The Governance ARIA tab issue remains an optional, non-blocking UI-quality
  follow-up and does not reopen the completed UI Completion profile.
- This review does not establish `TECHNICALLY_RELEASE_READY`, `V4_COMPLETE`,
  `RELEASE_ACCEPTED`, production embedding-model adoption, production vector
  retrieval, R2 completion or confirmation, or R3 completion. Existing V3 and
  R1 independent-review provenance and all other phase states remain unchanged.
- The administrative documentation commit that records this verdict is not
  independently reviewed for product behavior.

## Prior Corpus and Methodology Authority Checkpoint (Superseded for Tanzil)

This records the pre-admission checkpoint. The newer Tanzil pre-activation
checkpoint below supersedes its zero-snapshot and unbound-hash statements.

- Starting HEAD: `28d355653a915016b179e223852f2b978dc44605`;
  implementation candidate:
  `382c7aefdde8cf5fde160b98fe3b705384ddadbb`.
- Read-only external reconciliation verified the Tanzil Uthmani 1.1 candidate
  at 6,236 verses, 1,334,737 bytes, and SHA-256
  `ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af`.
  The external CANON-001 manifest explicitly does not grant LISAN3 production
  activation, so no authority was transferred into this repository.
- The QAC morphology v0.4 candidate was verified at 6,309,503 bytes and
  SHA-256
  `a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46`.
  It remains auxiliary structural evidence only; its semantic/gloss/ontology
  fields are excluded, and the current LISAN3 QAC importer does not validate
  the real tab-separated artifact format.
- The live LISAN3 database still has zero CorpusSnapshots and zero ResearchRuns.
  Tanzil and QAC remain `SOURCE_ROLE_APPROVED`; neither has a LISAN3-bound
  expected hash, validated import, or `PRODUCTION_ACTIVE` activation.
- Migration `e8b3f6a1c204` adds a durable Methodology revision registry and seeds
  `LISAN_QURANIC_SEMANTIC_EXTRACTION@6bb1c10a0f9a`, bound to the governing
  skill source and SHA-256
  `43c0a40b3f465fa95695607c2de838effd07946966c57ad15275d0051e92a288`.
  Provenance fields are immutable; lifecycle and eligibility remain separately
  mutable for future retirement or revocation.
- ResearchRun admission now requires both a production-valid CorpusSnapshot and
  a current, eligible, source-matching Methodology revision. The live Run Builder
  remains unavailable only because no production-active CorpusSnapshot exists.
- Full affected verification passed: 146 non-E2E tests, affected Playwright
  Journey 1, Ruff, Pyright with 0 errors and 177 existing warnings, ESLint,
  Next production build, OpenAPI regeneration parity, Alembic base-to-head and
  model parity, and live readiness. A clean detached checkout of the exact
  candidate passed 15 focused tests, Ruff, clean Git status, and contract hash
  parity.
- The prior requalification Corpus blocker therefore remains. No pilot or
  remaining batch may start; any later Corpus activation closes only that
  blocker and still requires a fresh pilot rerun and separate authorization.
- No UI Completion workstream, LQE implementation, model integration, R3, V4,
  release, push, or external repository mutation was performed. Owner artifacts
  `.hermes/`, `check_db2.py`, and `debug_proxy.py` remain untouched.

## Tanzil Governed Pre-Activation Checkpoint (Superseded by Activation)

- Task starting HEAD:
  `29e5e1a75df6ee5c2a7d797b915a29cf512ab798`.
- Final implementation candidate:
  `69d0a27b2a2ca99d8c62dcf6344f42de51c17175`.
- Coherent implementation lineage:
  `eafa60f4666a334ed9ac85061548166277b67790`,
  `3da42df9d3d89d0d52e7cba18602d5834c26a2d5`, and the final candidate above.
- LISAN3 authority binds Tanzil Uthmani 1.1 at 1,334,737 bytes and SHA-256
  `ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af`.
  The strict UTF-8/LF artifact is preserved without normalization.
- The authority-bound identity index reconciles 114 surahs and exactly 6,236
  unique, complete, ordered verse identities to exact physical artifact lines.
- Live snapshot `snap_tanzil_1_1_ac0724796cbb` records
  `SOURCE_ROLE_APPROVED`, `ARTIFACT_PRESENT`, `HASH_VERIFIED`, and
  `IMPORT_VALIDATED`; `validation_status=PENDING` and
  `activation_status=CANONICAL_ACTIVATION_PENDING` remain deliberate.
- The live snapshot has exactly 6,236 deterministic non-fixture occurrences.
  Exact re-import reused the snapshot and created no competing rows.
- External CANON-001 reconciliation is limited to
  `CANON_001_ARTIFACT_IDENTITY_MATCH_CONFIRMED`; no external governance state
  or activation was imported.
- Live Alembic head is `c4d8b7e2a913`. Live `POST /runs` returned HTTP 503
  for the pre-activation snapshot and left the ResearchRun count at zero.
- Final exact-SHA clean verification passed 35 affected tests, all tracked
  Python Ruff checks, Pyright with 0 errors and 177 warnings, `pip check`, fresh
  migration plus `alembic check`, artifact/index hashes, `git diff --check`,
  and clean candidate status. The first detached Pyright invocation was an
  environment defect because that worktree had no local `.venv`; binding
  Pyright to the repository interpreter resolved imports and passed.
- The Tanzil artifact/provenance/hash/import part of the requalification Corpus
  blocker is resolved. Production-active Corpus authority remains blocked, and
  pilot/remaining-batches authorization remains separate. No requalification
  batch was started and `DO_NOT_START_REMAINING_BATCHES` was not changed.
- QAC remains an auxiliary morphology/syntax candidate with semantic, gloss,
  and ontology fields excluded from semantic authority. Its real TSV importer
  remains future work and was not made a Tanzil dependency.
- Durable decision evidence:
  `docs/evidence/corpus/TANZIL_PRE_ACTIVATION_DECISION_EVIDENCE.md`.
- This historical boundary was superseded only by the separately authorized
  exact-snapshot production activation recorded below.
- Owner-untracked `.hermes/`, `check_db2.py`, and `debug_proxy.py` remain
  present and untouched.

## Tanzil Production Activation Checkpoint

- Task starting HEAD: `4fe63673bd9a7057ce87b43d8bb2aa6e0f34a5c3`.
- Activation implementation candidate:
  `a1d910f11735ec4ba0e9324dbb82b800efd485f6`.
- Immediate live re-verification passed for the exact 1.1 artifact hash/size,
  114-surah/6,236-verse identity index, 6,236 deterministic non-fixture
  occurrences, absence of a competing active snapshot, current Methodology,
  and `CURRENT` schema at `c4d8b7e2a913`.
- Live snapshot `snap_tanzil_1_1_ac0724796cbb` is now `VALIDATED` and
  `PRODUCTION_ACTIVE`. It is the only production-active snapshot.
- Audit `aud_tanzil_production_activation_ac0724796cbb` records actor
  `OWNER_AUTHORITY`, timestamp `2026-08-26T16:52:00.806969Z`, prior/new state,
  reason, exact artifact/index evidence, and decision reference.
- Production-path `POST /runs` persisted `run_3410bc36`; unknown authority
  identifiers remained rejected. Live `/attention` and the real browser showed
  only the exact governed Corpus/Methodology pair.
- The prior `BLOCKED_CORPUS_PENDING` requirement is resolved. No semantic pilot
  or remaining batch was started; `DO_NOT_START_REMAINING_BATCHES` remains in
  force pending separate owner authorization.
- QAC is unchanged and remains separate. No QAC import, model/embedding work,
  R2, R3, V4, release, push, or external LQE mutation occurred.
- Durable evidence:
  `docs/evidence/corpus/TANZIL_PRODUCTION_ACTIVATION_EVIDENCE.md`.
- This is implementation-side activation evidence; it does not establish
  independent review, V4 completion, technical release readiness, or release
  acceptance.

## Exact Next Action

Obtain separate owner authorization for a fresh semantic requalification pilot
rerun against the exact active snapshot. Do not start the pilot or any remaining
root batch under this activation authorization; preserve
`DO_NOT_START_REMAINING_BATCHES`.
