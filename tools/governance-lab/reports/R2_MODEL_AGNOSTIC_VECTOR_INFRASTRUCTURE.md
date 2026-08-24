# R2 Model-Agnostic Vector Infrastructure Evidence

This report records a bounded R2 implementation checkpoint. It is evaluation
and implementation evidence, not semantic authority, independent review,
production-model adoption, complete R2 verification, R3 activation, or release
acceptance.

## Canonical continuation verdict

Bounded model-agnostic R2 continuation is permitted.

- Owner instruction is the highest active authority and explicitly authorizes
  only this continuation while deferring production model selection.
- `LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md` Section 34 activates R2
  after R1 verification. R1 is independently confirmed for
  `a0d10d7fd5ff8845d3071b7e68f1500f92fd9563`.
- Section 34 separately places embedding-space definitions, the sqlite-vec
  Spike, index schema/lifecycle, provenance, and tests inside R2 scope.
- Section 34 acceptance item 2 still requires a qualifying adopted model.
  Therefore the independent infrastructure slices may proceed, but
  `R2_VERIFIED_FOR_PROFILE` cannot be claimed while model selection is blocked.
- Sections 23 and 35 reserve EvidenceResolver and hybrid orchestration for R3;
  neither is implemented here.

No canonical document was changed to manufacture permission.

## Frozen benchmark

The benchmark remains unchanged and valid evidence:

- decision: `EMBEDDING_MODEL_SELECTION_BLOCKED`;
- runner + manifest + corpus input SHA-256:
  `2c6f22ff2ee31299c0342aa53d097fb1990880decabc56385920b1cb622b9d25`;
- result SHA-256:
  `DC2F6F6B353773BA2E1DDFAC618F51B8C21E401E2ED9A8B1A16E89CDCC575B56`;
- all three evaluated model revisions remain `NOT_ADOPTED`;
- thresholds, labels, judgments, model results, and machine-readable evidence
  were not modified or rerun.

## Exact model-agnostic scope implemented

- six canonical embedding-space identities;
- deterministic, provider-independent model manifest and configuration hash;
- adapter protocol only, with no implementation or inference;
- production handoff guard requiring a governed decision reference and an
  explicitly authorized space;
- typed synthetic/benchmark vector input and `RetrievalCandidate` contracts;
- reversible Alembic/SQLAlchemy `semantic_embeddings` evaluation schema;
- deterministic run/space rebuild and complete derived-state deletion;
- source/model/config/index provenance and explicit lifecycle state;
- stale model/config invalidation and stale-query rejection/exclusion;
- run, space, source eligibility, Internal Lock, and Blind Lab enforcement;
- sqlite-vec integration and evaluation-only candidate query;
- isolated sqlite-vec correctness, persistence, recovery, and performance Spike.

No model weights, downloads, inference implementation, default model,
production provider, production vector population, production-active index,
API, UI, OpenAPI change, TypeScript binding, R3 artifact, or V4 work exists.

## Governed external artifact handoff

Future production integration is contract-only and repository-independent.
`GovernedModelArtifactManifest` requires an immutable `artifact://` reference,
artifact/tokenizer/config SHA-256 values, model ID/revision/dimension,
normalization, supported spaces, Quran snapshot/version/hash, benchmark metrics,
known limitations, license, reproducibility evidence, independent model-review
evidence, and Blind-Lab/provenance/exposure declarations. It cannot name a
checkout path, import research Python, invoke training, load weights, or select
a provider.

The later governed integration must construct decision-bound
`GovernedModelArtifactRequirements` from accepted authority records, verify the
exported artifact bytes before loading anything, and reject a missing/evaluation
manifest, hash mismatch, unsupported revision/dimension/space, incompatible
normalization/configuration, stale time window, unapproved Blind-Lab state,
unknown/prohibited provenance or exposure, and mismatched Quran corpus binding.
All current checks use synthetic artifact bytes and manifests only.

`LISAN-Quran-Embedding` remains an external artifact producer. LISAN3 has no
runtime path, source, Git, virtual-environment, or experiment-file dependency
on that checkout.

## Deferred `LISAN-Quran-Embedding` responsibilities

The separate research track owns:

- governed production model selection;
- any governed per-space model decision;
- exact model artifact and revision provenance;
- preprocessing/configuration handoff;
- benchmark evidence sufficient to change a model from `NOT_ADOPTED`;
- a governed manifest decision reference that satisfies the production handoff;
- the evidence that must exist before LISAN3 may begin production vector
  population and complete R2 acceptance.

The current adapter boundary fails closed without that handoff.

## Persistence and evaluation boundary

`semantic_embeddings` is schema/evaluation infrastructure only. Database and
ORM constraints permit only `BENCHMARK_ONLY` or `SYNTHETIC_EVALUATION`, require
`production_eligible = false`, require explicit source/run/space/model/config
provenance, and reject invalid current/stale combinations.

Existence of this table does not imply model adoption or a production-active
vector index. Complete deletion leaves canonical source records untouched.

## sqlite-vec result

Result: `SQLITE_VEC_EVALUATION_PASSED`.

Canonical adoption status remains `APPROVED_FOR_EVALUATION`.

Executed profile:

- Python 3.12.10, SQLite 3.49.1, sqlite-vec v0.1.9;
- 5,000 deterministic `SYNTHETIC_EVALUATION` vectors;
- 32 float32 dimensions, 100 queries, top-k 10;
- predeclared limits: build <= 5 seconds and query p95 <= 100 ms;
- observed build: 0.627351 seconds;
- observed query mean: 33.911764 ms;
- observed query p95: 52.904200 ms;
- persistence after reopen, filtered run/space query, provenance linkage,
  deterministic query, rebuild equivalence, deletion, model/config invalidation,
  invalid-dimension rejection, rollback, and recovery all passed.

Runner SHA-256:
`291D72ABBC3B50A54C139F30BDC44885470C82A91DE223899174E93700A700AB`.

Result SHA-256:
`E1776C6E18171886C0369DAFF607BB53CFA2FDF8C092FBD92359924D3D8F8F8E`.

This result does not imply `EMBEDDING_MODEL_SELECTED`, sqlite-vec production
adoption, or R2 completion.

## Embedding-space and isolation results

- Every vector record and query carries one of the six canonical spaces.
- A manifest not authorizing the requested space is rejected.
- Persistence/query filters require exact run and space; generated Hypothesis
  tests exercised every canonical space.
- Cross-run and cross-space candidates are not returned.
- Missing run/isolation, pre-lock access, contaminated runs, and ineligible
  sources fail closed.
- Blocked access creates neither vector state nor contamination state/event.
- A run that becomes ineligible cannot query its formerly eligible vector state.
- Stale or mismatched model/config state is rejected or excluded.
- Rebuild removes vectors omitted because sources were removed/ineligible.

## RetrievalCandidate and R1 separation

Candidates are typed `VECTOR` / `CANDIDATE` /
`DERIVED_DISCOVERY_NON_AUTHORITATIVE`. Distance and similarity are retrieval
metadata only; the contract has no confidence, Gate, epistemic, review,
publication, or graph-promotion field.

Rebuild, query, deletion, and blocked-access tests preserve SemanticClaim axes
and do not create or mutate KnowledgeEdges. No `DOMAIN_PROJECTION` or
`GOVERNED_ASSERTION` is produced. The independently confirmed R1 candidate and
its provenance remain unaffected.

## Verification evidence

- pre-commit focused R2 contract/persistence/lifecycle/Spike profile: 30 passed;
- pre-commit full pytest against the same tracked implementation content: 118
  passed;
- fresh Alembic `base -> head` model/table/column parity: passed;
- R2 downgrade to `b7e4c1d9a5f2`, re-upgrade to head, and `alembic check`: passed;
- Ruff across every Git-tracked Python file: passed;
- Pyright: 0 errors, 144 existing SQLAlchemy-style warnings, no new R2 warnings;
- pip check: no broken requirements;
- `git diff --check`: passed;
- authority-critical Cosmic Ray profile: 291-universe / 29 selected / 29
  killed / 0 survivors, source SHA-256
  `3382eed7668bfcaa05c8c9ec77d57881987faab8f205aef80b14e3719edb2799`.
- clean detached candidate `c64d4531c918c47943b45423ee02d0fc501ad2f6`:
  Ruff passed; Pyright reported 0 errors / 144 existing warnings; all 112
  non-E2E tests passed; the live sqlite-vec Spike passed; all 29 selected
  critical mutations were killed; the frozen benchmark was unchanged; and the
  checkout remained clean;
- clean detached verification of code candidate
  `2449ac4db7102a0a62ae9622c6f668bb71602ef8`: fresh lockfile dependencies,
  frontend production build, Ruff, Pyright (0 errors / 252 existing warnings),
  full pytest (130 passed), all six Playwright E2E journeys, migration parity,
  and the R2 critical Cosmic Ray profile (291 universe / 29 selected / 29
  killed / 0 survivors) passed. `pip check` found no broken requirements and
  production-only `npm audit` reported zero vulnerabilities. The detached
  checkout had no Git changes after moving generated verification caches outside
  it.

Schemathesis and OpenAPI/TypeScript regeneration remain inapplicable because no
API or OpenAPI contract endpoint was added.

## Governance Review E2E signal

Classification: `TEST_DEFECT`.

The governing service already increments `active_revision` and persists the
new immutable revision in its approval transaction. The E2E test clicked the
async approval handler and immediately queried history, allowing `Revision: 1`
to be observed before the `POST .../approve` response completed. The test now
waits for that exact successful POST response before querying history. Focused
and full browser suites pass; no product governance behavior was weakened or
changed.

## Interim state and remaining dependency

- R2 benchmark: completed;
- production embedding-model selection: blocked/deferred;
- model-agnostic infrastructure: `IMPLEMENTED` and `TESTED` in code candidate
  `2449ac4db7102a0a62ae9622c6f668bb71602ef8`, pending independent review;
- immutable external-model handoff boundary: ready and fail-closed; it does not
  activate a model or production vector state;
- production embedding model: not selected;
- R2: not independently confirmed and not complete;
- R3: `NOT_STARTED`;
- V4: `NOT_STARTED`.

User-requested readiness indicator (not a canonical lifecycle state):
`LISAN3_MODEL_INDEPENDENT_WORK_COMPLETE`.

Exact next action: obtain an accepted `LISAN-Quran-Embedding` exported model
artifact + manifest + independent model-review evidence. Then construct the
governed decision requirements, verify the artifact without source-checkout
coupling, integrate it into R2, run complete R2 acceptance, and request one
fresh independent R2 review. Do not begin R3.

## Official sqlite-vec implementation sources

- Python loading and float32 serialization:
  https://alexgarcia.xyz/sqlite-vec/python.html
- vec0 persistence and metadata-filtered KNN:
  https://alexgarcia.xyz/sqlite-vec/features/vec0.html
- API stability warning and distance functions:
  https://alexgarcia.xyz/sqlite-vec/api-reference.html
