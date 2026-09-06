# LISAN3 — Owner Request 01 Completion Report

**verdict**: `PRE_ANALYSIS_FOUNDATION_AUTONOMOUSLY_QUALIFIED`
**base SHA**: `34d4b01cd3ddbfe6424823aa6ef46c696ecfd3d3`
**candidate SHA**: `7594fb455839ca8d88c9437149fdd5d5c8d8142f`  ·  **branch**: `pre-analysis-foundation` (local; main untouched)
**handoff**: `artifacts/semantic-campaign/PHASE_1_HANDOFF.json`
**mode executed**: Master Admission → Phase 0A → Phase 0B adversarial review → Phase 0C remediation → Calibration Readiness Qualification.

## 1. Verdict
Qualified. Every accepted pre-analysis owner directive is enforced (deterministically where possible), the descriptive knowledge base is persisted and reusable, and all 14 readiness conditions are met. The large campaign is NOT started (that is Request 02) and remains data-gated on QAC morphology.

## 2. Base / 3. Candidate identity
Base `34d4b01` (main). Candidate `7594fb45` on local branch `pre-analysis-foundation` (§18: local checkpoint; not merged to main).

## 4. Files changed
9 modified (`.gitignore`, `AUTHORITY_MAP.md`, `REUSE_CANDIDATE_REGISTER.md`, `backend/domain/models.py`, `schemas.py`, `main.py`, `services/canonicalization.py`, `services/research_judgment.py`, `services/ai_context.py`); 14 added (5 services/modules, 2 migrations, 3 test files, 3 docs, 1 fixture, this report + handoff). See the commit.

## 5. Structures reused (no duplication)
`CorpusSnapshot`/`CorpusOccurrence`, `QACAdapter`, `derive_completeness`, `CanonicalizationPolicy`, `BlindLabIsolationService`/`IsolationState`, `MethodologyRevision` immutability, `ChangeProposal`/`RuleRevision`/`AuditLog` governed capture, `EssentialNeighbor`, `VerificationRecord`, `AIContextBuilder`, `Hypothesis`.

## 6. Structures created
`StructuralToken` (persisted descriptive facts), `ExternalHypothesisRecord` (unified register), `CampaignState` (checkpoint/resume); services `RootDescriptiveProfileService`, `RootUniverseService`, `StructuralFixtureLoader`, `ExternalHypothesisService`, `CampaignStateService`; `Hypothesis.origin` marker.

## 7. Structures removed/merged
None removed. `MULTIPLE_LEXICAL_UNITS` confirmed to have no active code path (nothing to neutralize). Phase 0A's transient 3-level model was superseded by the 4-level persisted model (single coherent implementation, not a duplicate).

## 8. Descriptive knowledge status
Persisted, deterministic, reusable, meaning-free. Counts are pure-Python aggregates over `structural_tokens`; identical rows → byte-identical profile across sessions; no LLM in the fact path.

## 9. RootDescriptiveProfile evidence
`test_r01_pre_analysis_capabilities.py`: fixture load → 140 tokens for س ل م; profile reproducible across a fresh session; four knowledge levels distinct; no structural field mislabelled DIRECT; double-count across extraction versions prevented.

## 10. Root semantic unity evidence
Exact-set universal coverage (no majority — `test_5`); a UNIVERSAL ROOT_CONCEPT is blocked at acceptance by any unresolved case (`test_4`) or any eligible counterexample occurrence (`test_4b`); counterevidence never satisfies coverage (coverage basis = supporting evidence only). `ROOT_SEMANTIC_UNITY = NON_NEGOTIABLE`.

## 11. Foundational profile
`docs/FOUNDATIONAL_PROFILE_DRAFT.md` — 10 accepted-only premises, 6 governed fields each (statement/authority/scope/methodological_effect/misapplication_risk/review_trigger), `DRAFT / NON_GATING`, with an explicit OPEN appendix.

## 12. External hypothesis support
Unified register: 6 claim types, RULE_CLAIM vs AUTHOR_APPLICATION, full test lifecycle, **no** confidence/authority/canonical field; Jabal helper (high priority = tested early, no bonus). `Hypothesis.origin` is write-once; external candidates are excluded from the blind internal context (`test_7`, `test_7b`, `test_7c`).

## 13. Isolation mechanism
Lightest sufficient: reused blind-lab isolation + a write-once `Hypothesis.origin` marker + exclusion of external-origin hypotheses from the AI context. No permanent dual-lane lifecycle (SUP-008 deliberately avoided).

## 14. Governance simplification
None needed — no new gate/status axis was added; the two-state model (`research_state`/`canonical_state`) is preserved. The new stores are data tables, not workflow gates. `MULTIPLE_LEXICAL_UNITS` audit found nothing to remove.

## 15. Methodology refinements made
Root-unity enforcement hardened (counterexample/coverage-basis fix) — a reproducible correctness fix, regression-tested, within the non-negotiable invariant (not a change to it).

## 16. Regression / eval cases added
`test_phase0a_pre_analysis_foundation.py` (13 cases: 10 mandatory + counterexample + origin-write-once + blind-exclusion), `test_r01_pre_analysis_capabilities.py` (11 cases), `test_r01_migration.py` (round-trip). Total new ≈ 25.

## 17. Exact tests and results
`pytest tests --ignore=tests/e2e` → **179 passed**. Migration `b3d6e2f8c150` round-trip validated (single head, additive, reversible). Ruff clean on all changed files. (One pre-existing, unmodified file `test_ai_governance_simplification.py` carries a prior import-order lint; untouched per scope.)

## 18. Calibration readiness
14/14 readiness conditions QUALIFIED (see handoff `readiness_gate`), verified by 5-lens Phase 0B adversarial review + Phase 0C remediation.

## 19. Remaining nonblocking limitations
- Unity-gate deterministic cross-check of declared unresolved vs confirmed StructuralToken set → Request 02 (percentage bypass already impossible).
- `tokens_from_qac` feature-parsing robustness → when QAC is admitted.
- `CampaignState.current_batch` reserved for the Request 02 batch runner.

## 20. Irreducible blockers
**QAC morphology corpus absent** (`SOURCE_ROLE_PENDING`, license unreconciled, artifact external/uncommitted). This blocks a full-Quran Root Universe and real per-root structural profiles — an external-data/licensing dependency not resolvable by the runtime. Capabilities are qualified against the bundled `slm` fixture; the blocker is recorded in the handoff. This does not block the foundation; it gates full-scale Request 02 execution.
