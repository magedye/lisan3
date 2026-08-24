# Implementation Plan: R2 Model-Agnostic Vector Infrastructure

## Overview

Continue only the R2 infrastructure that remains valid while production
embedding-model selection is deferred to `LISAN-Quran-Embedding`. Preserve the
frozen benchmark decision, use only synthetic/evaluation vectors, keep every
derived result non-authoritative, and stop before R3 or V4.

## Authority Decision

- Canonical R2 activation follows verified R1; the recorded R1 candidate is
  independently confirmed and the owner has separately authorized this bounded
  R2 continuation.
- The canonical R2 scope separately names embedding-space definitions,
  sqlite-vec evaluation, index schema/lifecycle, provenance, and tests. Those
  slices can be implemented without satisfying the full R2 acceptance item that
  requires an adopted model.
- `R2_VERIFIED_FOR_PROFILE` remains unavailable while model selection is
  blocked. No production model, production vector population, API/UI retrieval
  path, EvidenceResolver, hybrid orchestration, R3, or V4 is in scope.

## Architecture Decisions

- Persist only derived evaluation records through SQLAlchemy/Alembic. Their
  schema makes synthetic/benchmark provenance, run, embedding space, model
  identity, source revision/hash, configuration hash, index revision, and stale
  state explicit.
- Keep the production model handoff as a provider-independent protocol and
  manifest-validation boundary. No adapter implementation, weights, inference,
  download, default model, or production provider is introduced.
- Fail closed when a governed model decision reference is absent from a
  production manifest request.
- Use `sqlite-vec==0.1.9` only in an isolated technical Spike with deterministic
  synthetic vectors. The Spike result cannot change its canonical
  `APPROVED_FOR_EVALUATION` status.
- Every query is explicitly run- and embedding-space-scoped. Cross-space,
  cross-run, stale, ineligible, contaminated, or pre-lock access is rejected.
- Return typed candidates labeled `VECTOR`, `CANDIDATE`, and
  `DERIVED_DISCOVERY_NON_AUTHORITATIVE`; similarity/distance is retrieval
  metadata, never confidence.

## Task List

### Phase 1: Authority and frozen evidence

- [x] Confirm canonical permission for bounded model-agnostic R2 continuation.
- [x] Preserve the benchmark thresholds, labels, judgments, model results, and
  `EMBEDDING_MODEL_SELECTION_BLOCKED` decision unchanged.

### Phase 2: Contracts and persistence

- [x] Add provider-independent embedding-space, manifest, adapter, evaluation
  vector, and typed `RetrievalCandidate` contracts.
- [x] Add a reversible Alembic migration and derived evaluation-vector model
  with fail-closed provenance and lifecycle constraints.

### Checkpoint: Contract and migration

- [x] Focused schema/manifest negative paths pass.
- [x] Fresh Alembic `base -> head`, downgrade/upgrade, model parity, and
  `alembic check` pass.

### Phase 3: Lifecycle and isolation

- [x] Implement deterministic evaluation-only rebuild, deletion/recovery,
  model/config invalidation, and stale-vector exclusion.
- [x] Enforce Blind Lab eligibility, source eligibility, run isolation,
  embedding-space isolation, and candidate non-authority.

### Checkpoint: Infrastructure

- [x] Focused pytest and Hypothesis invariants pass.
- [x] Canonical source and R1 graph/claim state remain unchanged under vector
  rebuild, query, deletion, and blocked access.

### Phase 4: sqlite-vec Spike and evidence

- [x] Execute isolated synthetic-vector persistence, filtered KNN,
  deterministic ordering, reopen/recovery, deletion, invalidation, and local
  performance checks.
- [x] Record the exact `SQLITE_VEC_EVALUATION_PASSED` or blocker result without
  promoting sqlite-vec or selecting a model.

### Phase 5: Candidate checkpoint

- [x] Run Ruff, Pyright, full pytest, migration checks, affected mutation
  checks where justified, and adversarial code review.
- [x] Update the durable R2 governance report and `PROJECT_STATE.md`, create
  coherent commit(s), and verify the exact SHA in a clean detached worktree.

Candidate `c64d4531c918c47943b45423ee02d0fc501ad2f6` passed the bounded detached
R2 profile. Its historical broader attempt reached 117 passed before the
Governance Review E2E race was classified; Phase 6 below is the superseding
model-independent completion checkpoint.

### Phase 6: Model-independent completion checkpoint

- [x] Extend the existing manifest boundary into a portable, immutable external
  artifact handoff with all required model, corpus, provenance, Blind-Lab,
  benchmark, reproducibility, and independent-review fields.
- [x] Test every required fail-closed handoff rejection without loading a model.
- [x] Classify and correct the Governance Review E2E signal as a test race.
- [x] Verify code candidate `2449ac4db7102a0a62ae9622c6f668bb71602ef8` in a
  clean detached checkout: full pytest/E2E, frontend build, migration profile,
  Ruff, Pyright, and critical mutation profile.

R3 remains `NOT_STARTED`; V4 remains release-candidate-bound and is not run.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Evaluation tables imply model adoption | High | Evaluation-only provenance and production-ineligible constraints |
| Cached vectors bypass Blind Lab | High | Current lock/isolation checks on rebuild and every query |
| Cross-space similarity becomes a universal score | High | Explicit enum plus fail-closed equality validation and negative tests |
| Model/config drift silently reuses vectors | High | Exact manifest fingerprint and stale invalidation |
| Candidate score mutates semantic authority | High | Typed non-authority contract and canonical-state immutability tests |
| sqlite-vec pre-v1 behavior drifts | Medium | Pin 0.1.9, verify actual loaded version, isolate the Spike, retain fallback removal path |

## Remaining External Dependency

`LISAN-Quran-Embedding` owns governed production model selection, exact model
artifact/revision handoff, per-space decision if approved, and the later
benchmark evidence that can populate a production-governed vector state. The
exact remaining dependency is an accepted immutable exported artifact + governed
manifest + independent model-review evidence, not the research checkout.
