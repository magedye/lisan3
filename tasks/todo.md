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
- [x] External immutable model-artifact handoff contract and fail-closed checks
- [x] Governance Review E2E root-cause classification and race-free assertion
- [x] R3 and V4 remain not started

Production model selection, inference, production vector population, API/UI,
EvidenceResolver, and hybrid orchestration are explicitly deferred.

Code candidate: `2449ac4db7102a0a62ae9622c6f668bb71602ef8`. Its clean detached
profile passed: 130 pytest tests, six Playwright journeys, production frontend
build, Ruff, Pyright (0 errors / 252 existing warnings), migration reversibility,
and 29/29 authority-critical R2 mutations killed. The next genuine dependency
is an accepted external model artifact + governed manifest + independent
model-review evidence; R3 and V4 remain deferred.
