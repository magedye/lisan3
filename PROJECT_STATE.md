# Lisanapp Project State

State context only. Canonical repository contracts and runtime evidence remain authoritative.

## Canonical Runtime Qualification Checkpoint (2026-09-12)

- Branch `canonical-runtime-qualification` from main `6dea680052cf3ccf00ccb89396503763c0dc1839`.
  Infrastructure/governance remediation only — NOT canonicalization, NOT five-root
  semantic requalification. Batch 08 remains `NOT_AUTHORIZED`.
- Authoritative runtime DB = `lisanapp.db` (default + only Alembic-stamped). The
  non-governed `data/campaign/runtime.db` was NOT promoted.
- Corpus converged into lisanapp.db via repository-native services only
  (`tools/converge_runtime.py`): Tanzil `snap_tanzil_1_1_ac0724796cbb`
  PRODUCTION_ACTIVE/VALIDATED (OWNER_AUTHORITY audit), 6,236 CorpusOccurrence,
  49,968 StructuralToken (1,642 roots); methodology `…@01784170cac4` CURRENT/eligible.
- Isolation hardened fail-closed: `establishment_status` (default NOT_ESTABLISHED) +
  attestation + migration `f2b7d1e9a3c5`; canonicalization requires ESTABLISHED.
- Word-level occurrence authority = `StructuralToken`; `token:<word_ref>` evidence
  bridge + word-level host completeness; unauthorized-actor canonicalization guard.
- Five-root exact-set structural derivation reproduces Batch 07 counts exactly
  (ESw 12, dnw 133, flH 40, fwh 13, glm 13) — structural counting, not semantics.
- Tests: 251 passed (non-e2e); 0 SemanticClaims/VerificationRecords/ACCEPTED for the
  five roots; Batch 07 JSONs byte-identical.
- Status: `CANONICAL_RUNTIME_READY_FOR_FRESH_INDEPENDENT_REVIEW` (superseded — see below).
  Report: `docs/LISAN3_CANONICAL_RUNTIME_QUALIFICATION.md`;
  handoff: `docs/LISAN3_CANONICAL_RUNTIME_FRESH_REVIEW_HANDOFF.md`.
  NEXT: fresh Sol xhigh read-only review must return
  `CANONICAL_RUNTIME_INDEPENDENTLY_CONFIRMED` before any five-root requalification.
  Hazard flagged: stale duplicate `backend/alembic` chain (head `5542b3a62e23`).

## Canonical Runtime Qualification — Merged & Pushed (2026-09-13)

- Independent read-only acceptance review of `82ed5f7f9b383ad14293c8817cbd2d35de571e94`
  returned `CANONICAL_RUNTIME_INDEPENDENTLY_CONFIRMED` + `CANONICAL_RUNTIME_MERGE_READY`,
  **0 material blockers**.
- `canonical-runtime-qualification` fast-forwarded into `main`
  (`6dea680052cf3ccf00ccb89396503763c0dc1839` → `82ed5f7f9b383ad14293c8817cbd2d35de571e94`),
  no merge commit, and pushed normally: `origin/main == main == 82ed5f7`.
- Post-merge verification re-run on `main`: DB authority `lisanapp.db`, sole Alembic head
  `f2b7d1e9a3c5`, Tanzil snapshot VALIDATED/PRODUCTION_ACTIVE (failures `[]`), methodology
  `…@01784170cac4` authority-failures `[]`; qualification tests 24 passed; non-e2e suite
  251 passed; five-root exact-sets equal to committed evidence (ESw 12, dnw 133, flH 40,
  fwh 13, glm 13); Batch 07 JSONs byte-identical; five-root SemanticClaims/VerificationRecords/
  ACCEPTED/ResearchRuns all 0; governance smoke 32/32 fail-closed.
- Status: `CANONICAL_RUNTIME_QUALIFICATION_MERGED_AND_PUSHED`. Infrastructure-only; NO
  five-root semantics qualified or canonicalized. `BATCH_08_NOT_AUTHORIZED` stands.
- NEXT: a separate, fresh `FIVE_ROOT_GOVERNED_REQUALIFICATION_TRACK` (ESw, dnw, flH, fwh,
  glm) — not authorized by this task.
- Deferred non-blocking debt (do NOT fix retroactively into this checkpoint): (1) isolation
  canonicalization gate could additionally corroborate input_manifest/attesting_actor/
  attested_at/audit_ref + isolation snapshot/methodology bindings; (2) legacy orphan
  `backend/alembic/` + `backend/alembic.ini` (head `5542b3a62e23`); (3) research-judgment path
  requires CLEAN but not ESTABLISHED — confirm design intent; (4) minor evidence-resolver /
  convergence nits; (5) `ADMISSION_TANZIL.md` historical wording remains historical evidence.

## Five-Root Governed Requalification — Producer (Stage A) (2026-09-13)

- Branch `five-root-governed-requalification` from `main@d780476e4a3b119ae993588f20333f2ce5fe9246`.
  Fresh, clean-room, Quran-internal producer stage for ESw/dnw/flH/fwh/glm. NOT Batch 08; Batch 07
  semantic JSONs unread-before-freeze and byte-identical.
- Five DB-native, **non-canonical** Research Judgments frozen in `lisanapp.db` via governed API
  (`/runs` → `/runs/{id}/blind/preflight` → `/runs/{id}/observations` → `/runs/{id}/judgments`,
  `ResearchJudgmentService.create`). No manual rows, no canonicalization.
  - ESw `jud_9506cecf` PREFERRED/STRONG/REPRESENTATIVE(LEXICALIZED_CLASS); dnw `jud_6733070a`
    PREFERRED/MODERATE/REPRESENTATIVE(ROOT_GENERALIZATION); flH `jud_50b6a890`
    PREFERRED/MODERATE/REPRESENTATIVE(DERIVATIONAL_FAMILY); fwh `jud_303cd726`
    PREFERRED/STRONG/UNIVERSAL(LEXICALIZED_CLASS); glm `jud_d51f1e74`
    PREFERRED/MODERATE/REPRESENTATIVE(LEXICALIZED_CLASS). All revision 1, `NOT_CANONICAL`,
    falsification PASSED, host-completeness sufficient.
- Governed state: 5 runs, 5 isolation states ESTABLISHED+CLEAN (attested), 211 observations
  (exact-set 12/133/40/13/13), 0 VerificationRecords, 0 ACCEPTED. Overclaim gate downgraded 4/5.
- Producer disclosures: semantic induction by clean-room subagents (2 analysts + 1 adversary →
  aggregator); LLM residual-knowledge bounded by downstream review; `glm` had incidental prior
  orchestrator exposure to its historical conclusion — flagged for the fresh reviewer.
- Tests: qualification 24, non-e2e 251, negative controls 32/32. `lisanapp.db` NOT committed.
- Status: `FIVE_ROOT_GOVERNED_REQUALIFICATION_READY_FOR_FRESH_INDEPENDENT_REVIEW`. Reports:
  `docs/LISAN3_FIVE_ROOT_GOVERNED_REQUALIFICATION_PRODUCER_REPORT.md`,
  `docs/LISAN3_FIVE_ROOT_FRESH_REVIEW_INDEX.md`, `docs/LISAN3_FIVE_ROOT_FRESH_REVIEW_HANDOFF.md`,
  `docs/evidence/requalification/*.json`. NEXT: Stage B fresh independent semantic review (blind to
  Batch 07 initially), then owner decision bound to exact `claim_id`/`revision_id`.
  `BATCH_08_NOT_AUTHORIZED`.

## Five-Root Governed Requalification — Fresh Independent Review (Stage B) (2026-09-13)

- Producer checkpoint reviewed: `de338810159ebbb3a5ffacc4d2d3551b7a75f95d`. A fresh Sol xhigh
  context recorded all five verdicts before opening Batch 07, then performed the historical
  comparison. The frozen pre-comparison verdict artifact SHA-256 is
  `9a1012e1973f047c7a2d44ec3d4feddc2faabb171c4711170e9c855e5601c754`.
- Exact reviewed revisions and results:
  - ESw `jud_9506cecf@1`: `VERIFIED_AT_SCOPE`; `INDEPENDENT_CONVERGENCE`.
  - dnw `jud_6733070a@1`: `CORRECTIVE_RESEARCH_REQUIRED`; `NEW_CLAIM_NARROWER`.
  - flH `jud_50b6a890@1`: `CORRECTIVE_RESEARCH_REQUIRED`; `PARTIAL_CONVERGENCE`.
  - fwh `jud_303cd726@1`: `VERIFIED_AT_SCOPE`; `NEW_CLAIM_NARROWER`.
  - glm `jud_d51f1e74@1`: `VERIFIED_AT_SCOPE`; `PARTIAL_CONVERGENCE`.
- Authoritative `lisanapp.db` SHA-256 before and after review:
  `34dcc0a2a2fb3ae8c3774b681545459dfebd36df8c58a181d86c683e6c6eae68` (byte-identical).
  Governed counts remain 5 SemanticClaims, 5 runs, 211 observations, 0 VerificationRecords,
  0 ACCEPTED, and 0 AI execution records. All claims remain unchanged and non-canonical.
- Next-action split: ESw/fwh/glm = `OWNER_DECISION_PENDING`; dnw/flH =
  `CORRECTIVE_RESEARCH_REQUIRED`. The exact `dnw@1` and `flH@1` revisions are frozen
  reviewed-but-not-verified history and MUST NOT receive a VerificationRecord or canonicalization.
- Stage B evidence:
  `docs/evidence/requalification/five_root_fresh_independent_verdicts.json`,
  `docs/LISAN3_FIVE_ROOT_FRESH_INDEPENDENT_REVIEW.md`, and
  `docs/evidence/requalification/five_root_owner_decision_package.json`. Historical Batch 07
  root artifacts remain byte-identical. `BATCH_08_NOT_AUTHORIZED`.
- Status: `FIVE_ROOT_STAGE_B_INDEPENDENT_REVIEW_PERSISTED`. This is evidence custody only;
  no owner decision, VerificationRecord, canonicalization, merge, or release is implied.

## Five-Root Campaign — Delegated Owner Decisions (Stage 1) (2026-09-13)

- Latest explicit owner instruction delegates the five-root campaign decisions while expressly
  prohibiting fabricated/impersonated human verification, policy bypass, weakened evidence,
  forced semantic convergence, force push, history rewriting, and Batch 08.
- Preflight independently reproduced branch/remote custody, authoritative `lisanapp.db` SHA-256
  `34dcc0a2a2fb3ae8c3774b681545459dfebd36df8c58a181d86c683e6c6eae68`, sole Alembic
  head/current `f2b7d1e9a3c5`, production-valid Tanzil, current source-bound methodology,
  exact sets 12/133/40/13/13, exact Stage B revisions, 0 VerificationRecords, 0 ACCEPTED,
  and no Batch 08 runtime records.
- Exact delegated decisions: `ESw jud_9506cecf@1` = `VERIFY_AT_SCOPE`; `fwh
  jud_303cd726@1` = `VERIFY_AT_SCOPE`; `glm jud_d51f1e74@1` = `VERIFY_AT_SCOPE` at its
  unchanged MODERATE/REPRESENTATIVE lexicalized-class scope (not a strength upgrade and not
  canonicalization eligibility). Frozen `dnw jud_6733070a@1` and `flH jud_50b6a890@1` =
  `RETURN_FOR_CORRECTION`; neither may receive verification or canonicalization.
- Durable decision artifact:
  `docs/evidence/requalification/five_root_owner_delegated_decisions.json`. This is an
  `OWNER_DELEGATED_DECISION`, not an independent-human review or VerificationRecord.
- NEXT: complete fresh corrective producer/adversary/aggregator cycles for `dnw` and `flH`,
  freeze new immutable claims with predecessor lineage, then launch fresh independent review.
  `BATCH_08_NOT_AUTHORIZED`.

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
- V4 implementation state: `V4_COMPLETE` for `82695bd`
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
- `V4_COMPLETE`, `TECHNICALLY_RELEASE_READY`, and `RELEASE_ACCEPTED` established for `82695bd`.

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

## V4 Candidate Evidence (Candidate-Bound)

- Candidate SHA: `82695bd`.
- Full canonical V4 suite executed dynamically bound to `82695bd`.
- Evidence logged to `v4_output.log`.
- Ruff: passed on tracked candidate scope (errors restricted to untracked owner files `check_db2.py` and `debug_proxy.py`).
- Pyright: 0 errors.
- Alembic migration parity (base -> head): passed.
- pip check, npm audit, ESLint, Next.js production build: passed.
- OpenAPI/client sync: passed.
- pytest (including Hypothesis, Playwright, Schemathesis): 190 passed.
- Verdict: `V4_COMPLETE`, `TECHNICALLY_RELEASE_READY`, and `RELEASE_ACCEPTED` for `82695bd`.

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

## Prior Corpus and Methodology Authority Checkpoint (Superseded)

This records the pre-admission checkpoint. The newer Tanzil pre-activation
checkpoint below supersedes its zero-snapshot and unbound-hash statements. Its
external QAC artifact and `SOURCE_ROLE_APPROVED` statements are historical only
and are superseded by the current five-axis QAC reconciliation below; no such
artifact is admitted or part of the current candidate.

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

## Fresh Five-Root Semantic Requalification Pilot — Blocked Checkpoint

This section preserves the evidence-candidate checkpoint. Its original blocker
classification and proposed next action are superseded by the later enabling-
governance reconciliation checkpoint; the underlying five-run facts remain
unchanged.

- Task starting HEAD:
  `67dccb9017b6d9500a90d7564358daf8192b4190`.
- Pilot evidence candidate:
  `6b5313b7696f01a54f76cb907cd722f822ff22ae`.
- The exact active CorpusSnapshot and current eligible Methodology were
  independently re-read from the live database before execution:
  `snap_tanzil_1_1_ac0724796cbb` and
  `LISAN_QURANIC_SEMANTIC_EXTRACTION@6bb1c10a0f9a`.
- Exactly five fresh ResearchRuns were admitted: `run_d7519288` (ع د ل),
  `run_8d696d64` (أ م ن), `run_1a24ffab` (س ل م), `run_68c7b72c`
  (ح م د), and `run_5f72ad9d` (ش ك ر). No remaining root was started.
- Each run has a `CLEAN` Blind Lab state. The active isolation service blocked
  one prohibited prior-semantic read per run and persisted an IsolationEvent;
  no run became `PRIOR_CONTAMINATED`.
- The production snapshot is text-only: `structural_source` and
  `structural_source_version` are null, and all 6,236 verse-level occurrence
  records have an empty expression. With QAC import unauthorized and no
  authority-approved deterministic morphology fallback, exact root occurrence,
  form, and construction coverage is not verifiable.
- Canonical `PURITY_CHECK` and `INTERNAL_LOCK` evaluations failed for all five
  runs. Seven Purity dimensions have no current evidence extractors, so a
  later observation/hypothesis sequence alone cannot establish a valid
  Internal Lock. No SemanticClaim, Root Core, semantic boundary, neighbor
  result, ROOT_CARD, TERM_CARD, ReviewDecision, or publication state was
  created.
- Persisted runtime status per run is `LOCK_BLOCKED`; the implementation-side
  pilot outcome is `REQUALIFICATION_REQUIRED`. Root Core values remain null.
- The LQE-safe view exports no semantic truth and no inferred structural rows;
  every root is `LQE_REQUALIFICATION_REQUIRED`.
- Verification passed: 21 focused pytest tests; JSON/YAML structural validation;
  five-run runtime traceability readback; deterministic SHA-256 verification for
  nine evidence artifacts; scoped staged-path verification; and
  `git diff --cached --check`.
- Durable evidence:
  `docs/evidence/semantic-pilot-2026-08-26/SEMANTIC_PILOT_BLOCKER_REPORT.md`.
- The original blocker classifications are corrected by
  `docs/evidence/semantic-pilot-2026-08-26/SEMANTIC_PILOT_BLOCKER_CORRECTIVE_ADDENDUM.md`.
  In particular, QAC was not admitted, product importer/domain gaps are
  separate from the artifact dependency, and derived cards are not semantic or
  Internal-Lock prerequisites.
- No QAC import, model/embedding work, R2, R3, V4, release, push, remaining
  semantic batch, or external `D:\APP\tafseer\LISAN-Quran-Embedding` mutation
  occurred. Owner-untracked `.hermes/`, `check_db2.py`, and `debug_proxy.py`
  remain present and untouched.

## Semantic-Pilot Enabling-Governance Reconciliation Checkpoint

- Task starting branch/HEAD: `main` /
  `e916abc11572766fe932bd1549f53392634f2f72`; direct pilot-evidence parent in
  the task lineage: `6b5313b7696f01a54f76cb907cd722f822ff22ae`.
- The independent evidence review verdict is
  `SEMANTIC_PILOT_BLOCKER_VERDICT_NOT_CONFIRMED`, while overall readiness remains
  `SEMANTIC_PILOT_BLOCKED`.
- QAC is reconciled across five independent axes: artifact identity `PENDING`;
  provenance/license `PENDING`; structural role `NOT_APPROVED`; real importer
  `NOT_IMPLEMENTED`; production activation `NOT_AUTHORIZED`. Runtime authority
  is fail-closed as `SOURCE_ROLE_PENDING`. No QAC artifact was accessed,
  imported, or activated.
- Tanzil remains sole canonical Quran text and verse-identity authority. The
  preferred future morphology boundary is a separate, provenance-bound
  token/segment annotation layer; it must not mutate the current production
  CorpusSnapshot or Tanzil occurrences.
- The structural blocker is decomposed into authority/provenance, physical
  artifact, real importer, domain/persistence, and downstream research-evidence
  gaps. Importer and persistence capability gaps are `PRODUCT_DEFECT`, not
  collapsed into the physical `EXTERNAL_DEPENDENCY`.
- Purity remains an independent `PRODUCT_DEFECT` for enablement. The canonical
  contract now defines mandatory inputs, lineage, decision rules, diagnostics,
  levels and tests for all eight dimensions. `NOT_EVALUATED` remains blocking
  and never means clean.
- Morphology-independent implementation set: `DICTIONARY_FIRST`,
  `HERITAGE_BIAS`, `TAFSIR_CONTAMINATION`, `GENERIC_OVEREXTRACTION`,
  `LETTER_SEMANTICS_OVERRELIANCE`, and `CIRCULAR_CONFIRMATION`.
  `CONTEXTUAL_LEAKAGE` is partially implementable but final-clean coverage is
  morphology-dependent; `FORCED_UNIFICATION` materially depends on structural
  occurrence evidence.
- ROOT_CARD / TERM_CARD absence is a descriptive
  `DERIVED_PRESENTATION_CONTRACT_GAP`, not a persisted status and not a corpus,
  Purity, or Internal-Lock blocker. No card schema was implemented.
- Original sealed pilot files and their hash manifest were not modified. The
  corrective addendum changes interpretation/classification only.
- All five named ResearchRuns remain `LOCK_BLOCKED`, with `root_core: null`,
  occurrence coverage `NOT_VERIFIED`, clean isolation and prior quarantine.
  They were not rerun. `DO_NOT_START_REMAINING_BATCHES` remains in force.
- No real QAC importer, full Purity evaluator, semantic result, LQE change,
  external-workspace use, production activation, release, or push occurred.
  Owner-untracked `.hermes/`, `check_db2.py`, and `debug_proxy.py` remain
  untouched.
- Ordered future slices are recorded in
  `docs/canonical/LISAN_PURITY_AND_STRUCTURAL_EVIDENCE_CONTRACT.md` and
  `tasks/plan.md`; each slice requires separate authorization.

## QAC Admission-Sequence Reconciliation Checkpoint

- Corrective task starting branch/HEAD: `main` /
  `981e56d478f37de62464028d2832f4bdd24c7c9b`.
- The independent review verdict on that candidate was
  `SEMANTIC_ENABLING_GOVERNANCE_REJECTED_WITH_FINDINGS`, with the one required
  finding `QAC_ADMISSION_SEQUENCE_RECONCILIATION`.
- QAC remains fail-closed on all five independent axes: artifact identity
  `PENDING`; provenance/license `PENDING`; structural role `NOT_APPROVED`; real
  importer `NOT_IMPLEMENTED`; production activation `NOT_AUTHORIZED`. Runtime
  authority remains `SOURCE_ROLE_PENDING`.
- The corrected lifecycle is Stage A, QAC provenance and artifact
  qualification; Stage B, structural domain/persistence capability; Stage C,
  real QAC importer and validation; Stage D, a separate structural-source
  admission decision; and Stage E, a separate production-activation
  transition. Stages A-C cannot grant approval, Stage D does not pre-authorize
  `APPROVED`, and Stage E cannot inherit admission automatically.
- The tooling reference's stale current Tanzil `PENDING_ADMISSION` label is
  reconciled to `ACTIVE_BASELINE` with lifecycle
  `PRODUCTION_ACTIVE_FOR_EXACT_AUTHORIZED_SNAPSHOT`, matching
  `docs/canonical/ADMISSION_TANZIL.md`. Tanzil qualification, runtime, and
  artifacts were not reopened or changed.
- All eight Purity evidence contracts, `NOT_EVALUATED` fail-closed behavior,
  the morphology dependency split, and the ROOT_CARD / TERM_CARD derived
  read-model boundary remain unchanged. No evaluator was implemented.
- The sealed five-root evidence set was not edited. All five runs remain
  `LOCK_BLOCKED`, all five `root_core` values remain null, and
  `DO_NOT_START_REMAINING_BATCHES` remains in force.
- Focused V1 passed: five QAC authority/adapter tests; canonical status and
  ordered-dependency consistency; completeness of all eight Purity contracts;
  all nine sealed artifact hashes; and `git diff --check`. No Python changed,
  so Ruff was not applicable. An initial custom order assertion matched the
  earlier five-axis label instead of the Stage E heading; classified
  `TEST_DEFECT`, corrected, and passed without repository remediation.
- This is a documentation/governance-only corrective candidate. It does not
  acquire or import QAC, implement persistence/importers/evaluators, rerun a
  root, authorize admission or activation, modify LQE, push, or grant
  independent review. Candidate identity is the commit containing this
  checkpoint; the full SHA is returned in the execution handoff because a
  commit cannot embed its own SHA.

## QAC Stage-A Provenance and Artifact Qualification Checkpoint

- Task starting branch/HEAD: `main` /
  `d69d1cadc9c13ccf542b4ebc25e358f7a7846052`, the exact independently
  confirmed QAC admission-sequence baseline.
- A concrete QAC morphology 0.4 candidate was found read-only under the
  authorized V7 local source area. Thirteen local candidate/renamed copies are
  byte-identical: 6,309,503 bytes, SHA-256
  `a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46`.
- An in-memory fetch from an immutable third-party mirror commit reproduced the
  same byte size and hash. That is public byte corroboration, not upstream
  authority.
- At `2026-08-26T23:50:10.7789646Z`, a read-only GET of the official download
  endpoint returned an HTTP 200 HTML page containing only a contact-email POST
  form, with no direct artifact link or checksum. No owner email was supplied
  or fabricated and no POST was made, so no official bytes were obtained. The
  binding classification is `DIRECT_OFFICIAL_BYTE_BINDING_UNAVAILABLE`; the
  official size/hash and candidate comparison remain not computable.
- The historical `a1d129...` lead is classified as an exact candidate/public-
  mirror byte match with the direct official upstream byte chain unresolved.
- Real-format inspection found a CRLF ASCII/UTF-8-compatible TSV artifact with
  128,219 ordered segments over 77,429 words and all 6,236 verse identities;
  zero malformed rows, duplicate locations, or ordering/contiguity violations;
  208 intentional empty first-person singular pronoun suffix surfaces; and one
  internal-space proper-name form at `37:130`.
- All QAC verse references map to the active Tanzil identity set. Read-only
  word-count diagnostics identify 112 embedded-opening-basmala offsets and four
  residual tokenization differences at `2:181`, `8:6`, `13:37`, and `37:130`.
  This is Stage-C requirements evidence, not production alignment.
- The combined provenance/license axis remains `PENDING`: official GPLv3, QAC
  no-change/attribution, FAQ non-commercial/research/citation language, the
  embedded historical Tanzil CC BY-ND 3.0 notice, and Tanzil's current CC BY
  3.0/no-change page are not authoritatively reconciled. Local use remains
  pending clarification; raw public/private repository redistribution is not
  qualified. The raw artifact was not copied into or committed by LISAN3, and
  no runtime expected hash was bound.
- Final QAC state is unchanged: artifact identity `PENDING`;
  provenance/license `PENDING`; structural role `NOT_APPROVED`; real importer
  `NOT_IMPLEMENTED`; production activation `NOT_AUTHORIZED`; runtime role
  `SOURCE_ROLE_PENDING`.
- Durable evidence:
  `docs/evidence/qac-stage-a-2026-08-27/QAC_STAGE_A_QUALIFICATION.md` and its
  machine-readable manifest, field disposition, reconciliation, requirements,
  prerequisite, and hash artifacts. The factual holder/maintainer request is
  `QAC_LICENSE_CLARIFICATION_REQUEST.md` with status `PREPARED_NOT_SENT`.
- No Stage B/C/D/E work, database mutation, QAC import, Purity implementation,
  semantic run, remaining batch, sealed-pilot edit, LQE access/modification,
  release, push, or external historical-workspace modification occurred.
- Owner-untracked `.hermes/`, `check_db2.py`, and `debug_proxy.py` remain
  present and untouched.
- The prior Stage-A result was
  `QAC_PROVENANCE_AND_ARTIFACT_QUALIFICATION_BLOCKED`. The bounded
  official-binding/license continuation result is
  `QAC_STAGE_A_OFFICIAL_BINDING_AND_LICENSE_BLOCKED`. This checkpoint does not
  self-grant independent review or any later lifecycle state.

## Exact Next Action

The owner submits an authorized contact email through the official QAC download
form, preserves and provides the delivered raw response bytes, and sends the
prepared factual clarification request to the official QAC contact. Then
compare the official byte size/SHA-256 with the Stage-A candidate and record the
authoritative response without broadening Stage A. Do not commit or redistribute
the raw artifact unless the response clearly qualifies that action. Do not
authorize or start Stage B, C, D, or E under that blocker-resolution action.

## Artifact-Identity Remediation Checkpoint (2026-09-10)

- Task starting branch/HEAD: `pre-analysis-foundation` /
  `201058c8d680afa317ba046cb49bfd7b1bdcd366`; coverage-provenance baseline
  `45590ee4bfd617e47060330917fd17cce608b42c` is an ancestor.
- Scope: Windows case-insensitive semantic-campaign root-artifact identity,
  defensive write guards, Batch 04 `swm` recovery proof, and the minimum
  controlled Batch 05 `Swm` replay. No semantic root was started.
- The starting HEAD already encoded case-colliding uppercase Buckwalter symbols
  `H/S/D/T/Z` with the explicit reversible hex form used for filesystem-illegal
  characters. The final 1,642-root runtime-universe scan produced 1,642 distinct
  case-folded filenames and zero collisions: `swm.json` versus `_53_wm.json`.
- A shared `_write_root_json` boundary now verifies both the outgoing
  `root_buckwalter` identity and any existing artifact identity before writing.
  It is used by `prep`, `prep-coverage`, and `persist-coverage`; unreadable,
  identity-less, or foreign-root existing artifacts fail closed.
- Compatibility audit: all 48 pre-Batch-05 artifacts remain present; 14 paths
  required deterministic filename migration, and all 48 contents remain
  byte-identical to `c2b8434`. The sole stale ledger reference, Batch 05 `Swm`,
  was corrected from `roots/Swm.json` to `roots/_53_wm.json`.
- Batch 04 `swm.json` is byte-identical to `c2b8434` (Git blob
  `1139cb0ff340021b907c4dd860a775a87b5218d0`; SHA-256
  `5a2fa4064b7c9c1ef8d58a7e057dea4da2086097d2eb4ba304d24804023b92a9`)
  and carries `root_buckwalter = swm`.
- V1: five focused naming, reference-resolution, write-guard, and same-root
  replay checks passed. V2: `tests/test_campaign_coverage.py` plus
  `tests/test_qac_morphology.py` passed 27 tests; focused Ruff passed.
- Controlled V3 used a copied campaign database and temporary output tree.
  Batch 05 `Swm` prep produced `_53_wm.json`, coverage prep produced
  `_53_wm.s0.json`, `persist-coverage` retained exact-set `COMPLETE`, both
  ledger references resolved, and the copied Batch 04 `swm.json` hash remained
  unchanged. Repository campaign outputs were not rewritten by this replay.
- No concurrent semantic-campaign writer was present at either process check.
  Eighty-eight pre-existing ignored Batch 06 coverage scratch files dated
  2026-09-10 02:54:08-02:54:10 were preserved, not regenerated, staged, or
  treated as evidence by this remediation.
- Changed tracked files: `tools/campaign.py`,
  `tests/test_campaign_coverage.py`,
  `artifacts/semantic-campaign/CAMPAIGN_RESEARCH_LEDGER.json`, and this state
  checkpoint. Owner-untracked files remain preserved and excluded.
- Remediation state: `IMPLEMENTED`, `TESTED`, and `VERIFIED_FOR_PROFILE` for
  the bounded artifact-identity profile. Independent review and release
  acceptance are not established.

## Current Exact Next Action

Run a fresh read-only independent review against the exact remediation commit,
checking the candidate diff, 1,642-root collision scan, migrated-reference
resolution, Batch 04 byte identity, and controlled Batch 05 replay evidence.
Do not resume or accept Batch 06 under that review authorization.

## Batch 05 Semantic Research Closure Checkpoint (2026-09-10)

- Task starting branch/HEAD: `pre-analysis-foundation` /
  `6ae309c8252eefbf6adc67be726ad4c1a74aea73`; refreshed local and remote-tracking
  `main`:
  `34d4b01cd3ddbfe6424823aa6ef46c696ecfd3d3`. The starting branch was 14 ahead
  and 0 behind `main`, with `main` as its merge base.
- The branch history is the coherent pre-analysis and semantic-campaign line:
  master/QAC admission, pre-analysis persistence and services, campaign
  coverage tooling, Batches 01-05 research evidence, and artifact-identity
  hardening. The closure does not add a new runtime or semantic-research run.
- Batch 05 remains coverage-complete for 40 roots and 3,878 / 3,878 confirmed
  occurrences. Its initial review verdict is
  `SEMANTIC_SYNTHESIS_READY_WITH_QUALIFICATIONS`, preserved in
  `docs/LISAN3_BATCH_05_SEMANTIC_RESULTS_REVIEW.md`.
- The bounded corrective review covers exactly 14 roots and 2,405 / 2,405
  occurrences. Its verdict is
  `BOUNDED_CORRECTIVE_REVIEW_COMPLETE_WITH_PRESERVED_RESISTANCE`, preserved in
  `docs/LISAN3_BATCH_05_CORRECTIVE_SEMANTIC_REVIEW.md`.
- The corrective report contains the authoritative 72-record objection
  preservation registry for this checkpoint: 70 formal adversarial failing
  references, the discoverer-unreconciled `Anf` reference, and the exposed
  `ETw` Form-VI seam. The unavailable historical preliminary disposition and
  note are retained as
  `HISTORICAL_PRELIMINARY_PROVENANCE_UNRECOVERABLE`; later `CONSISTENT` labels
  do not replace that missing history.
- Corrective synthesis-ready results are qualified `SlH` and `rjm`, plus the
  explicitly class-partitioned `qwm`, `Awl`, `Sdr`, `Ehd`, `bny`, `dbr`, and
  `krm`. Together with the 26 untouched initially strong/qualified roots, this
  makes 35 / 40 Batch 05 roots usable for synthesis only at their documented
  scopes.
- `Anf` and `Erw` remain `UNRESOLVED`; `rbb`, `ETw`, and `fqr` retain resistant
  occurrences. These states are valid evidence-bearing outcomes and are not
  merge blockers. No root result was rewritten to obtain merge readiness.
- Canonical authorization and publication remain pending/not granted. The
  reports are research-level evidence and do not self-grant owner acceptance,
  independent review, registry adoption, release acceptance, or publication.
- The recommended five-root corrective research run for `Anf`, `Erw`, `rbb`,
  `ETw`, and `fqr` is `NOT_STARTED` and `NOT_AUTHORIZED`. Batch 06 is also
  `NOT_AUTHORIZED` and was not started by this closure.
- Generated Batch 05 packets and coverage shards remain ignored scratch; the
  tracked ledger and 88 root artifacts are the durable campaign evidence.
  Forty-one ignored Batch 06 packets and 88 ignored Batch 06 coverage files
  were preserved and excluded. Owner-untracked files and model/session memory
  were not staged or changed.
- Focused verification passed: 27 tests in
  `tests/test_campaign_coverage.py` and `tests/test_qac_morphology.py`; focused
  Ruff; 88 ledger roots exactly matching 88 collision-safe artifacts; 40 Batch
  05 roots totaling 3,878 occurrences; 1,642 / 1,642 unique case-folded runtime
  filenames; all review links resolving; exact 72-record objection coverage;
  and preserved Batch 04 `swm.json` SHA-256
  `5a2fa4064b7c9c1ef8d58a7e057dea4da2086097d2eb4ba304d24804023b92a9`.
- Closure commit scope is exactly the two semantic review reports and this
  state reconciliation. The final checkpoint SHA is returned in the execution
  handoff because a commit cannot embed its own identity.

## Current Exact Next Action

After reviewing the exact closure commit returned in the execution handoff,
fast-forward `main` to that commit. Merge authority does not authorize the
five-root corrective research run, Batch 06, canonicalization, publication,
push, tag, or release.

## Batch 06 Authorized Campaign Start (2026-09-10)

- The owner subsequently authorized the bounded Batch 06 Quran-internal
  semantic campaign. Local `main` was verified at the merged Batch 05
  checkpoint `6f895bf0754190a423512b7478ced5bf7bd4a266`, and the working branch
  `semantic-campaign-batch06` was created from that exact revision.
- Phase 0 searched campaign configuration, the tracked research ledger, task
  and specification records, campaign manifests, and this state record. No
  authoritative tracked Batch 06 root population existed.
- A fresh deterministic Root Universe selection froze 40 new roots and 3,098
  confirmed occurrences in
  `artifacts/semantic-campaign/BATCH_06_MANIFEST.json`. The manifest exactly
  matches a repeated live selector run and is divided round-robin into two
  20-root waves containing 1,780 and 1,318 occurrences.
- All 88 previously researched roots are excluded. The separate Batch 05
  corrective roots `Anf`, `Erw`, `rbb`, `ETw`, and `fqr` are also absent and
  remain untouched.
- Root identity is explicit as `root_arabic`, `root_buckwalter`, `root_id`, and
  `artifact_name`. Occurrence evidence now preserves the exact `word_ref`,
  verse reference and canonical Tanzil verse, QAC structural surface and
  morphology, candidate interpretation, supporting/counterevidence, final
  disposition, and per-occurrence reconciliation lineage. Because the
  repository has no adopted segment-level orthographic alignment profile,
  `surface_form_arabic` is honestly recorded as unavailable rather than
  guessed from Buckwalter source bytes.
- Phase 0 focused verification: 30 campaign/QAC tests passed; focused Ruff
  passed; the 40-root manifest reconciled to 3,098 occurrences; all five
  excluded roots were absent; and 1,642 / 1,642 runtime-root artifact names
  remained case-insensitively unique.
- No Batch 06 semantic conclusion has yet been persisted at this checkpoint.
  Canonicalization, publication, owner acceptance, independent review, Hybrid
  Retrieval, push, merge, release, and branch deletion remain outside scope.

## Current Exact Next Action

Execute and independently checkpoint Batch 06 Wave 1 against the frozen
20-root / 1,780-occurrence population. Semantic ambiguity must be preserved as
resistance or unresolved evidence and must not stop unrelated roots.

## Batch 06 Wave 1 Semantic Checkpoint (2026-09-11)

- Wave 1 persisted exactly the 20 roots and 1,780 confirmed occurrence
  identities frozen in `BATCH_06_MANIFEST.json`. Every root has exact-set
  coverage, `research_completeness = COMPLETE`, explicit four-part identity,
  canonical Tanzil verse evidence, QAC structural provenance, a final
  occurrence disposition, and no missing or duplicate `word_ref`.
- Outcome distribution: 4 STRONG (`trk`, `$hw`, `Dyq`, `Hlf`), 10 MODERATE
  (`ArD`, `mvl`, `qlb`, `swA`, `fSl`, `wlj`, `Sgr`, `Ezr`, `Hdq`, `Hwj`),
  4 WEAK (`ysr`, `jwb`, `Sdd`, `Sbg`), and 2 UNRESOLVED (`$yA`, `Hlq`).
- The exact resistant total is 528: all 519 `$yA` occurrences because the
  thing/willing bridge is not internally demonstrated; three `ysr` maysir
  occurrences; the `jwb` rock-hewing token at 89:9; the `Sdd` sadid token at
  14:16; all three `Hlq` throat/shaving tokens; and the `Sbg` culinary token at
  23:20. These are evidence-bearing outcomes, not campaign blockers.
- Two preliminary objections were reconciled to final CONSISTENT while
  preserving per-occurrence lineage: `mvl` at `19:17:8:2` (Form V embodied
  correspondence) and `wlj` at `9:16:20:1` (admitted inner-circle access).
- Wave 1 introduced a fail-closed semantic-class materializer. It has no
  default disposition: every reviewed class has explicit structural selectors,
  an expected count, interpretation, rationale, supporting-evidence note, and
  counterevidence list. Unmatched, multiply matched, drifted-count, duplicate,
  or root-population-mismatched evidence is rejected.
- The campaign ledger now contains 108 / 1,642 researched roots; 1,534 remain.
  All 108 are coverage-complete and retain canonical authorization PENDING.
- Wave 1 V2 evidence passed: 31 focused campaign/QAC tests and focused Ruff;
  JSON parsing for the manifest, status, and ledger; 20/20 artifact identity and
  exact-set contract checks; 1,780/1,780 evidence records; and zero changes to
  any previously tracked root artifact.
- Report: `docs/LISAN3_BATCH_06_WAVE_01.md`. Prior root artifacts and the five
  separate Batch 05 corrective roots remain unchanged. Ignored packet/coverage
  working files are operational scratch only and are not staged.

## Current Exact Next Action

Execute and independently checkpoint Batch 06 Wave 2 against the frozen
20-root / 1,318-occurrence population. Do not reselect roots, reopen Wave 1, or
start the Batch 05 five-root corrective track.

## Batch 06 Wave 2 Semantic Checkpoint (2026-09-11)

- Wave 2 persisted exactly the remaining 20 roots and 1,318 confirmed
  occurrence identities frozen in `BATCH_06_MANIFEST.json`. Every root has
  exact-set COMPLETE coverage, four-part root identity, canonical Tanzil verse
  evidence, QAC structural provenance, and final occurrence dispositions.
- Outcome distribution: 9 STRONG (`rsl`, `$rk`, `kvr`, `H$r`, `mkr`, `Hzn`,
  `wSf`, `zrE`, `Aby`), 5 MODERATE (`qtl`, `ESm`, `Eyr`, `HDD`, `Hfw`),
  3 WEAK (`srr`, `fwq`, `HrD`), and 3 UNRESOLVED (`Hwr`, `SbA`, `Sbw`).
- Wave 2 retains 34 resistant occurrences: 12 `srr` joy/couch-class tokens;
  the `fwq` fawaq interval and recovery tokens; all 13 `Hwr` occurrences across
  return/dialogue/hawariyyun/hur families; the `HrD` wasted-state noun; all
  three proper-name-only `SbA` tokens; and all three `Sbw` youth/inclination
  tokens. No contested item was forced to achieve unity.
- The ledger now contains 128 / 1,642 researched roots, `updated_roots_total =
  128`, with all 128 coverage-complete and canonicalization pending; 1,514
  roots remain outside this authorized batch.
- Combined Batch 06 state is 40 roots / 3,098 occurrences: 13 STRONG,
  15 MODERATE, 7 WEAK, and 5 UNRESOLVED, with 562 resistant occurrences and
  two preserved reconciliation-lineage records.
- Wave 2 V2 evidence passed: 32 focused campaign/QAC tests and focused Ruff;
  JSON parsing for manifest, status, and ledger; 20/20 artifact identity and
  exact-set contract checks; 1,318/1,318 evidence records; and zero changes to
  any Wave 1 or earlier tracked root artifact.
- Report: `docs/LISAN3_BATCH_06_WAVE_02.md`. All Wave 1 and pre-Batch-06 root
  artifacts remain unchanged. The five separate Batch 05 corrective roots
  remain excluded and untouched.

## Current Exact Next Action

Run the whole-Batch-06 V3 evidence gate, produce the final semantic campaign
report, reconcile final state, and stop for a fresh independent semantic-results
review. Do not select or start another root batch.

## Batch 06 Final Semantic Campaign Checkpoint (2026-09-11)

- Batch 06 is complete on branch `semantic-campaign-batch06`: exactly 40 new
  roots and 3,098 confirmed occurrences across two independently committed
  20-root waves (1,780 / 1,318).
- Final Batch 06 outcomes are 13 STRONG, 15 MODERATE, 7 WEAK, and 5 UNRESOLVED.
  Twenty-eight roots have universal presence at their qualified research
  strength; 12 do not. Exactly 564 occurrences were contested: 562 remain
  RESISTANT, while two reconciled occurrences retain preliminary and final
  provenance.
- The V3 gate recomputed all 40 artifact occurrence sets against the live
  confirmed StructuralToken store: 3,098 / 3,098 exact identities, zero
  missing, unexpected, or duplicate refs, and zero required evidence-contract
  errors. All 3,098 occurrence records explicitly preserve preliminary
  disposition/note, verifier objection, final disposition, reconciliation
  rationale/lineage, all four root identities, canonical Tanzil verse support,
  QAC structural fields, candidate interpretations, and counterevidence.
- A final provenance audit found that unreconciled records had previously left
  preliminary and verifier fields implicit. The materializer was corrected and
  both frozen waves were replayed idempotently. The semantic judgments, exact
  occurrence sets, 564/562/2 contested/resistant/reconciled counts, ledger
  totals, and Batch 06 population did not change.
- Ledger/artifact state is coherent: 128 ledger roots, `updated_roots_total =
  128`, exactly two Batch 06 coverage-log entries, and all 128 researched roots
  COMPLETE with canonical authorization PENDING. CampaignState independently
  reports 128 processed / 1,514 remaining.
- Filesystem integrity passed: all 40 Batch 06 artifact names are unique under
  case-folding; the complete live 1,642-root universe remains 1,642 / 1,642
  case-insensitively unique. Git shows exactly 40 added Batch 06 root artifacts
  and zero modified prior root artifacts.
- The five separate Batch 05 corrective artifacts (`Anf`, `Erw`, `rbb`, `ETw`,
  `fqr`) are byte-unchanged relative to starting main. No Batch 05 conclusion
  was reopened.
- The pre-existing ignored `data/campaign/packets/batch06` (41 files, last
  written 2026-09-10 02:25) and `data/campaign/coverage/batch06` (88 files, last
  written 2026-09-10 02:54) remain untouched and non-authoritative. Fresh
  ignored Wave 1/Wave 2 packets and four research/coverage working files are
  operational scratch only and are not committed.
- Focused final regression evidence: 32 campaign/QAC tests passed and focused
  Ruff passed. Manifest, status, ledger, and all root JSON parsed successfully.
- Final report:
  `docs/LISAN3_BATCH_06_SEMANTIC_CAMPAIGN_REPORT.md`.
- Final state:
  `COMPLETE_READY_FOR_FRESH_INDEPENDENT_SEMANTIC_RESULTS_REVIEW`. This does not
  establish `INDEPENDENTLY_REVIEWED`, canonicalization, publication, product
  acceptance, merge, push, tag, release, or Batch 07 authority.

## Current Exact Next Action

Stop. The recommended next optional task is a fresh read-only independent
semantic-results review against the exact final Batch 06 commit returned in the
handoff, prioritizing all 5 UNRESOLVED roots, 7 WEAK roots, 2 reconciliation
lineages, and the high-frequency STRONG/MODERATE class boundaries. That review
is not automatically authorized by this checkpoint.

## Batch 06 Corrective Revision Checkpoint (2026-09-11)

- Corrective baseline: `5c95def0012d4cb938973e37aecfce83b5aeb3d5` on
  `semantic-campaign-batch06`; the owner-authorized scope is exactly ten
  blocking semantic targets and persisted contract completion for the frozen
  40-root / 3,098-occurrence Batch 06 set.
- The durable corrective plan is
  `artifacts/semantic-campaign/BATCH_06_CORRECTIVE_JUDGMENTS.json`; the replay
  command is `python -m tools.campaign apply-batch06-corrective --repo-root .`.
  It neither selects a population nor reads ignored scratch.
- All 40 artifacts now have the validated root-judgment contract with resolved
  evidence/counterevidence/hard-case references and `purity_status =
  NOT_EVALUATED`. The semantic runtime SHA remains
  `01784170cac4e715c1477cb6a04a2c34b21c4bdb91705aa1eb6b2a896efcedbd`.
- Corrected outcomes: 12 STRONG / 8 MODERATE / 9 WEAK / 11 UNRESOLVED, with
  565 final RESISTANT occurrences. `kvr` 108:1:3:2, `fSl` 70:13:1:2, and
  `wlj` 9:16:20:1 are RESISTANT. The historical `mvl` reconciliation is
  `VALID_WITH_QUALIFICATION`; the historical `wlj` attempt is retained but its
  current result is `INVALID_INSUFFICIENT_QURAN_INTERNAL_BRIDGE`.
- The original independent semantic-results review is preserved as historical
  evidence. The new report is `docs/LISAN3_BATCH_06_CORRECTIVE_REVISION.md`.
  No canonicalization, merge, push, release, purity campaign, or Batch 07 work
  is authorized.

## Current Exact Next Action

Stop. After this checkpoint is committed, run a fresh independent read-only
review of that exact commit. Do not merge, push, start Batch 07, or
canonicalize.

## Batch 06 Final Contract Remediation Checkpoint (2026-09-11)

- Starting candidate: `8ef76292978c61c9283648d5f578d928e39e7320` on
  `semantic-campaign-batch06`. The scope is representation-only remediation of
  the 40 frozen root artifacts / 3,098 frozen occurrence identities.
- `artifacts/semantic-campaign/BATCH_06_FINAL_CONTRACT_REMEDIATION.json` binds
  the active runtime field names and the only ten authorized adversarial-record
  corrections. The replay command is
  `python -m tools.campaign apply-batch06-final-contract --repo-root .`; it
  refuses a nonmatching baseline or any frozen semantic payload drift.
- The canonical active-field deficit is corrected from 80 missing fields to
  zero. Legacy `root_evidence_refs` and `root_counterevidence_refs` are not
  active aliases and are rejected by the validator. Claim-specific hard cases,
  rejection conditions, reopen conditions, falsification evidence, and the
  eight `NOT_EVALUATED` purity diagnostics are persisted for every root.
- The 12 / 8 / 9 / 11 strength distribution, 565 final resistant occurrences,
  Batch 05 artifacts, and all occurrence/lineage/classification data remain
  frozen. Implementation-side checks are 38 focused tests and Ruff clean.
- Durable report:
  `docs/LISAN3_BATCH_06_FINAL_CONTRACT_REMEDIATION.md`. This is not an
  independent review, canonicalization, merge, push, release, acceptance, or
  Batch 07 authorization.

## Current Exact Next Action

Stop. Run a fresh, independent, read-only review of the exact final contract
remediation commit. Do not merge, push, start Batch 07, or canonicalize.

## Batch 06 Representation Remediation Checkpoint (2026-09-11)

- Starting candidate: `5b131676837c674e92723ccc6df02e1fb2fdc676` on
  `semantic-campaign-batch06`. Scope is limited to the remaining
  representation defects in `hard_cases`, `rejection_condition`, and
  `reopen_conditions` for the frozen 40-root / 3,098-occurrence Batch 06 set.
- Durable controls:
  `artifacts/semantic-campaign/BATCH_06_REPRESENTATION_REMEDIATION.json`.
  The replay command is
  `python -m tools.campaign apply-batch06-representation-remediation --repo-root .`.
  It requires the exact starting SHA, an exact 40-root control set, and a full
  frozen-payload comparison before writing.
- The 19 former positional hard-case artifacts now have 17 evidence-derived
  cases and two honest `NO_GENUINE_HARD_CASE` records: `Eyr` and `Hdq`.
  All 40 rejection and reopen controls are individually authored against their
  existing claim scope and recorded evidence boundary; no external semantic
  source or new research run was used.
- Canonical contract errors and evidence-reference errors are zero. The active
  evidence fields and alias rejection remain intact. Falsification status is
  unchanged at 17 `PASSED`, 11 `NOT_REQUIRED`, and 12 `NOT_RUN`.
- Frozen proof is unchanged: 12 / 8 / 9 / 11 strength distribution, 565 final
  resistant occurrences, 3,098 exact occurrence identities, all occurrence
  dispositions, and reconciliation lineage. Batch 05 artifacts remain outside
  scope and unchanged; no Batch 07 work is present.
- Implementation-side evidence: `pytest tests/test_campaign_coverage.py -q`
  passed 42 tests; focused campaign/QAC checks passed 48 tests; and focused
  Ruff passed. A final consistency sweep found zero canonical errors, zero
  frozen payload drift, zero legacy template matches, 40 distinct normalized
  rejection controls, 40 distinct normalized reopen sets, and unchanged Batch
  05 corrective artifacts. The report is
  `docs/LISAN3_BATCH_06_REPRESENTATION_REMEDIATION.md`. This checkpoint does
  not establish independent review, canonicalization, merge, push, release,
  acceptance, or Batch 07 authority.

## Current Exact Next Action

Stop. Run a fresh, independent, read-only review against the exact committed
representation-remediation candidate. Do not merge, push, start Batch 07, or
canonicalize.

## Batch 06 Merged To Local Main (2026-09-11)

- The independently confirmed Batch 06 checkpoint
  `fff83c57fa301febded7eb19c9b784719eb78c0a` was fast-forwarded into local
  `main` under explicit owner authorization (verdicts:
  `BATCH_06_REPRESENTATION_REMEDIATION_INDEPENDENTLY_CONFIRMED`,
  `BATCH_06_SEMANTIC_CHECKPOINT_CONFIRMED`,
  `BATCH_06_SEMANTIC_CHECKPOINT_MERGE_READY`, zero material blockers).
- Merge shape: pure `--ff-only` (no squash, rebase, or merge commit). Post-merge
  `main` HEAD = `fff83c5`, tracked tree clean, all five Batch 05 corrective
  artifacts byte-identical, Batch 06 artifacts/reports present. Not pushed.
- Deferred non-blocking Batch 06 representation debt (do NOT fix inside Batch 07):
  stale top-level ledger `adversarial_verdict` on nine corrective roots;
  missing superseded banner on `docs/LISAN3_BATCH_06_SEMANTIC_CAMPAIGN_REPORT.md`;
  minor scope-label taxonomy observations; latent validator-hardening gaps.

## Batch 07 Campaign Initialization / Frozen Population (2026-09-11)

- Owner authorized the full Batch 07 Quran-internal semantic campaign: 120
  previously unresearched roots in 6 waves x 20. Branch
  `semantic-campaign-batch07` created from verified `main`
  `fff83c57fa301febded7eb19c9b784719eb78c0a`.
- Deterministic selection `tools.campaign select --n 120` over the live root
  universe (1642 roots; 128 already researched -> 1514 remaining) produced
  exactly 120 unique roots, reproducible across runs, with zero overlap against
  the researched ledger and zero overlap with the five Batch 05 corrective roots.
- Frozen population manifest: `artifacts/semantic-campaign/BATCH_07_MANIFEST.json`
  (status `BATCH_07_POPULATION_FROZEN`). 8,168 total confirmed occurrences.
  Tier mix xl 10 / l 20 / m 30 / s 30 / xs 30. Round-robin wave assignment by
  frozen selection_index: 20 roots/wave; occurrence load 1470 / 1435 / 1418 /
  1396 / 1236 / 1213.
- Artifact-identity scan over the full universe: 1642/1642 case-insensitively
  unique, 0 collisions; the 120 Batch 07 artifact names have 0 casefold
  duplicates and 0 clash with existing root files. The `swm/Swm` fail-closed
  remediation is preserved.
- Active semantic contract: `LISAN3_SEMANTIC_RUNTIME_V3_2026_09_06`
  (`skills/lisan-semantic-extraction/SKILL.md`, sha256
  `01784170cac4e715c1477cb6a04a2c34b21c4bdb91705aa1eb6b2a896efcedbd`).
- Batch 07 research is NON-canonical. No merge, push, Batch 08, canonicalization,
  or publication is authorized. Maximum end state is
  `BATCH_07_READY_FOR_FRESH_INDEPENDENT_SEMANTIC_REVIEW`.

## Current Exact Next Action

Execute Batch 07 Wave 01 (frozen 20-root / 1,470-occurrence set) with genuine
Quran-internal occurrence-level research, canonical-contract serialization, and a
20-root V2 checkpoint. Continue automatically through Waves 02-06. Do not merge,
push, canonicalize, or start Batch 08.

## Batch 07 Campaign Complete — Ready For Fresh Independent Review (2026-09-12)

- All six Batch 07 waves are researched, overclaim-swept, V2-checkpointed, and
  committed on `semantic-campaign-batch07`:
  - Init/frozen population `f92797a`; Wave 01 `e38e59b`; Wave 02 `9e1435a`;
    Wave 03 `ada0488`; Wave 04 `b6c53e4`; Wave 05 `0fa5445`; Wave 06 `01204fc`.
- **120 / 120 roots**, **8,168 occurrences**, exact-set complete (0 missing / 0
  extra / 0 duplicate). Ledger 248 / 1,642 researched; canonicalization PENDING.
- Whole-campaign V3 (recomputed from durable artifacts): 120/120 artifacts;
  canonical contract errors 0; evidence-reference errors 0; **120/120 distinct
  rejection conditions and 120/120 distinct reopen sets**; 0 positional hard
  cases; 0 unsupported PASSED; 0 unresolved-with-universal; purity all
  NOT_EVALUATED; collisions 0 (universe 1642/1642); ledger/manifest/status agree.
- Distribution: **6 STRONG / 96 MODERATE / 0 WEAK / 18 UNRESOLVED**; 357 final
  resistant across 72 roots; 167 reconciliations; 0 failed reconciliations; 0
  incomplete lineages. Falsification 17 PASSED / 85 NOT_RUN / 18 NOT_REQUIRED.
- Overclaim sweeps: Wave 01 flagged & corrected 7; Waves 02–06 flagged 0.
- Prior batches preserved: 0 prior root files modified; Batch 05's five corrective
  roots byte-identical; Batch 02–06 intact. Focused tests 48 pass; Ruff clean.
- Deliverables: `docs/LISAN3_BATCH_07_SEMANTIC_CAMPAIGN_REPORT.md`,
  `artifacts/semantic-campaign/BATCH_07_INDEPENDENT_REVIEW_INDEX.json`,
  `artifacts/semantic-campaign/BATCH_07_V3_VERIFICATION.json`, six wave reports,
  six overclaim-sweep records.
- Implementation-thread max state: `BATCH_07_READY_FOR_FRESH_INDEPENDENT_SEMANTIC_REVIEW`.
  No merge, push, adoption, canonicalization, or Batch 08 performed. The
  `VERIFIED` component of the adoption threshold must come from a separate,
  fresh, read-only independent review — not self-granted here.

## Batch 07 Independent Review, Merge & Owner-Acceptance Checkpoint (2026-09-12)

- Fresh independent read-only semantic review of the exact Batch 07 research
  checkpoint `0c21d82f12439f7fd57bc4cdcae0eab31befeaaa`
  (branch `semantic-campaign-batch07`) returned
  `BATCH_07_SEMANTIC_CHECKPOINT_INDEPENDENTLY_CONFIRMED` and
  `BATCH_07_SEMANTIC_CHECKPOINT_MERGE_READY`, **0 material blockers**. The
  review was read-only: it wrote no VerificationRecord, ledger, or root artifact.
- Independently reproduced custody: 120 roots / 8,168 occurrences, exact-set 0
  missing / 0 extra / 0 duplicate; distribution 6 STRONG / 96 MODERATE / 0 WEAK /
  18 UNRESOLVED; 357 resistant across 72 roots; canonical contract errors 0;
  evidence-reference validation clean; 120/120 distinct rejection + reopen
  controls; purity NOT_EVALUATED; Batch 02–06 preserved.
- Per-root independent verdicts: `VERIFIED_AT_SCOPE` 100,
  `VERIFIED_NARROWER_SCOPE` 2 (`SyH`, `Twf`), `UNRESOLVED` 18,
  `NOT_VERIFIED` 0, `CORRECTIVE_RESEARCH_REQUIRED` 0.
- Review evidence persisted as ADDITIONAL records (no history rewrite):
  `artifacts/semantic-campaign/BATCH_07_INDEPENDENT_REVIEW_RESULT.json` and
  the `independent_review` block in
  `artifacts/semantic-campaign/CAMPAIGN_STATUS.json`. The reviewed research SHA
  `0c21d82` is preserved as the checkpoint identity; the review record and this
  state entry are a later state-only closure commit that adds review/governance
  metadata only and does not alter any semantic conclusion.
- Merge: the closure commit (review evidence + state) was fast-forwarded into
  local `main` under the latest explicit owner instruction (research-checkpoint
  publication). Pure `--ff-only`; no squash, rebase, or merge commit; no history
  rewrite. Local `main` then normal-pushed to `origin/main` (fast-forward-safe;
  no force). Git is authoritative for the exact merged/pushed SHA.
- **Canonical adoption NOT performed — `OWNER_CANONICAL_ACCEPTANCE_REQUIRED`.**
  Five roots clear every evidence + independent-verification component of the
  adoption threshold: `ESw` (ع ص و), `dnw` (د ن و), `flH` (ف ل ح), `fwh` (ف و ه),
  `glm` (غ ل م) — each STRONG, exact-set COMPLETE, falsification PASSED,
  `VERIFIED_AT_SCOPE`. Governance (SIMPLIFIED_AI_AUTHORITY contract
  "CANONICALIZATION REQUIRES" + `backend/domain/services/canonicalization.py`)
  reserves `canonical_state=ACCEPTED` for a server-owned authorized actor
  (`TRUSTED_LOCAL_OWNER` via `CanonicalizationPolicy.canonicalize`), gated on a
  persisted **INDEPENDENT VerificationRecord** for the current revision. The AI
  endpoint has no ACCEPTED transition; the campaign CLI has no canonicalize
  command; the read-only review wrote no VerificationRecord. The owner's standing
  "auto-adopt after independent review" authorization expresses intent but cannot
  satisfy the repository's owner/server-owned transition when executed by the AI
  implementation agent. All 248 processed roots (incl. the 5 candidates) remain
  `canonical_authorization=PENDING`.
- Explicit non-adoptions held PENDING: `SyH` (STRONG but scope-overclaimed:
  re-scope UNIVERSAL/ROOT_GENERALIZATION → evidence-supported lexicalized class,
  then re-verify — not corrected here); `Twf` (MODERATE, below STRONG minimum);
  all 95 other MODERATE and all 18 UNRESOLVED roots.
- `BATCH_08_NOT_AUTHORIZED`: no Batch 08 branch, manifest, packets, or selection.

## Deferred Follow-Up Queue (post-merge; do NOT mix into Batch 07 adoption)

- Semantic scope: `SyH` scope correction + fresh independent re-verification;
  optional `Twf` scope precision.
- Provenance/reporting: define/fix the "167 reconciliations" metric generation;
  normalize the noncanonical historical disposition on `ftr 5:19:9:1`; fix stale
  `krh` prose ("STRONG for the family" while persisted result is MODERATE);
  null `reconciliation_rationale` on conservative lineage records where the
  rationale lives in disposition notes; minor wording concerns.
- Older Batch 06 representation debt: keep separately tracked (unchanged).

## Current Exact Next Action

Batch 07 research checkpoint is INDEPENDENTLY CONFIRMED, merged to local `main`,
and pushed. Canonical adoption of the five eligible roots
(`ESw`, `dnw`, `flH`, `fwh`, `glm`) awaits an explicit owner/server-owned
canonicalization transition: a `TRUSTED_LOCAL_OWNER` actor must record an
INDEPENDENT verification for the current revision and then run
`CanonicalizationPolicy.canonicalize` per eligible root. Do NOT self-grant
ACCEPTED, do NOT upgrade `SyH`/`Twf`, do NOT adopt MODERATE/UNRESOLVED roots,
and do NOT start Batch 08.
