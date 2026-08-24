# Implementation Plan: R2 Vector Discovery

## Overview

Implement only R2 candidate discovery on the verified R1 baseline. The vector
layer is derived, rebuildable, run-scoped, embedding-space-scoped, and
non-authoritative. Model adoption follows a reproducible Arabic-focused
benchmark; sqlite-vec remains an evaluation until the recorded Spike evidence
satisfies the canonical R2 acceptance criteria.

## Architecture Decisions

- Preserve the local FastAPI/SQLAlchemy/SQLite modular monolith; no vector
  server, microservice, Qdrant, or R3 EvidenceResolver.
- Keep provenance in a normal SQLAlchemy table and nearest-neighbor data in a
  disposable sqlite-vec virtual table keyed by embedding ID.
- Fail closed on run, Blind Lab eligibility, embedding space, source revision,
  model revision, configuration, and index revision mismatches.
- Return typed `RetrievalCandidate` results marked `VECTOR`, `CANDIDATE`, and
  `DERIVED_NON_AUTHORITATIVE`; never persist them as KnowledgeEdges.
- Use fixture/synthetic benchmark labels only as evaluation data, never as
  Quranic semantic authority.

## Task List

### Phase 1: Benchmark and evaluation contract

- [x] Task 1: Add a provenance-bearing R2 benchmark corpus, exact model
  revisions, deterministic metrics, and predeclared selection thresholds.
- [x] Task 2: Execute all candidate models per embedding space and record the
  benchmark decision without forcing a winner.

### Checkpoint: Benchmark

- [x] Corpus schema validation and reproducibility test pass.
- [x] Recall@K, Precision@K, MRR, nDCG@K, and FPR are reported per space.

### Phase 2: Derived vector foundation

- [ ] Task 3: Add the reversible R2 migration, embedding provenance model,
  sqlite-vec loader, and rebuild lifecycle.
- [ ] Task 4: Add run/space-scoped neighbor and counterevidence discovery with
  stale/model/config rejection and Blind Lab fail-closed policy.

### Checkpoint: Backend

- [ ] Focused model/service/API tests and Hypothesis invariants pass.
- [ ] Migration from zero, parity, deletion survival, and deterministic rebuild pass.

### Phase 3: Contracts and UI

- [ ] Task 5: Add explicit R2 schemas/routes/errors and regenerate OpenAPI plus
  TypeScript bindings.
- [ ] Task 6: Add the bounded Arabic RTL candidate-discovery surface with
  provenance and non-authority labels, then cover it in Playwright.

### Checkpoint: Integration

- [ ] R2 Schemathesis operations pass the four required checks.
- [ ] Browser journey passes with clean candidate/discovery semantics.

### Phase 4: Hardening and candidate

- [ ] Task 7: Add and execute the authority-critical R2 mutation profile.
- [ ] Task 8: Record sqlite-vec compatibility/performance/recovery evidence,
  review the change across correctness/readability/architecture/security/
  performance, and fix only required R2 findings.
- [ ] Task 9: Run the complete R2 phase profile, update PROJECT_STATE from
  executed evidence, commit the exact candidate, and repeat verification from
  a clean detached worktree.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Benchmark labels become semantic authority | High | Explicit fixture/synthetic provenance and non-authority schema fields |
| Cached vector leaks pre-lock or cross-run material | High | Run-scoped queries, current eligibility checks, stale purge on rebuild, adversarial tests |
| sqlite-vec extension is unavailable in migration/runtime | High | Pinned package, connection loader, fresh-resolution/migration checks, explicit recovery result |
| Model/config drift silently changes results | High | Exact model revision/config hash and fail-closed current-profile matching |
| Similarity appears as confidence | High | `similarity_score` only, authority notice, no confidence field, UI wording tests |
| R2 relation enters R1 graph truth | High | No KnowledgeEdge writes and graph-count/non-mutation tests |

## Open Questions

- `EMBEDDING_MODEL_SELECTION_BLOCKED`: no candidate qualified in every space.
  Independent architecture review must authorize an expanded model set,
  per-space model choice, or a governed benchmark/threshold revision.
