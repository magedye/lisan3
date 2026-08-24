# R2 Model-Agnostic Vector Infrastructure Checklist

- [x] Canonical continuation permission established
- [x] Frozen benchmark and `EMBEDDING_MODEL_SELECTION_BLOCKED` preserved
- [x] Embedding-space and model-handoff contracts
- [x] Evaluation-only migration and model parity
- [x] Deterministic rebuild, deletion/recovery, and stale invalidation
- [x] Cross-space, cross-run, source, and Blind Lab rejection
- [x] Typed `RetrievalCandidate` non-authority boundary
- [x] Isolated sqlite-vec correctness/performance Spike
- [x] Focused Hypothesis and authority-negative tests
- [x] Full pytest, Ruff, Pyright, and migration checkpoint
- [x] Durable governance report and PROJECT_STATE update
- [x] Coherent candidate commit and clean detached exact-SHA R2 verification
- [x] R3 and V4 remain not started

Production model selection, inference, production vector population, API/UI,
EvidenceResolver, and hybrid orchestration are explicitly deferred.

Candidate: `c64d4531c918c47943b45423ee02d0fc501ad2f6`. The bounded detached R2
profile passed. Exact-SHA full-suite green is not claimed because the broader
run had one out-of-scope Governance Review E2E failure.
