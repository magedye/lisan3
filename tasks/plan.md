# Semantic-Pilot Enabling Governance Plan

## Goal and boundary

Reconcile QAC authority, correct the sealed five-root pilot blocker
classification through an additive record, define evidence contracts for all
eight mandatory Purity dimensions, and leave an implementation-ready plan.
This candidate does not activate or import QAC, implement Purity evaluators or
card schemas, mutate runtime data, rerun roots, or authorize remaining batches.

## Dependency order

```text
authority reconciliation
    -> blocker correction
    -> structural and Purity contracts
    -> implementation slices
    -> focused verification
    -> exact-SHA independent review
```

## Task 1: Reconcile QAC authority

**Acceptance criteria:**

- Canonical and machine-readable records agree that artifact identity and
  provenance are pending, structural use is not approved, the real importer is
  not implemented, and production activation is not authorized.
- The proposed structural-only field boundary and prohibited semantic fields
  are explicit without granting evidence authority.
- Tanzil remains the sole Quran text and verse-identity authority.

**Verification:** focused authority tests, canonical-reference consistency
search, Ruff on the affected Python module, and `git diff --check`.

**Dependencies:** None.

## Task 2: Correct the sealed pilot blocker state

**Acceptance criteria:**

- The original pilot report and its recorded hash remain unchanged.
- An additive corrective record decomposes authority, artifact, importer,
  domain/persistence, and research-evidence gaps.
- ROOT_CARD and TERM_CARD are classified only as a derived presentation
  contract gap, never as a semantic or Internal Lock blocker.

**Verification:** recompute the original nine artifact hashes and inspect the
corrective record against current gate code.

**Dependencies:** Task 1.

## Task 3: Define structural and Purity contracts

**Acceptance criteria:**

- All eight mandatory dimensions define inputs, lineage, decision rules,
  diagnostics, dependency level, fixtures, and negative tests.
- `NOT_EVALUATED` remains blocking and can never equal clean.
- Morphology-independent and morphology-dependent evaluator slices are exact.
- The future annotation layer is separately provenance-bound and cannot mutate
  or replace Tanzil text authority.

**Verification:** dimension-name parity with `PURITY_DIMENSIONS`, completeness
checks for every contract section, and focused documentation validation.

**Dependencies:** Tasks 1 and 2.

## Task 4: Persist current state and implementation slices

**Acceptance criteria:**

- PROJECT_STATE identifies the corrected current blocker state and preserves
  `LOCK_BLOCKED`, null Root Cores, quarantine, and
  `DO_NOT_START_REMAINING_BATCHES`.
- The future work is split into eight independently reviewable slices; no slice
  is treated as authorized by this plan.

**Verification:** state-to-canonical cross-check and scoped Git inspection.

**Dependencies:** Tasks 1-3.

## Checkpoint: Candidate review readiness

- [x] Focused V1/V2 checks pass.
- [x] Original sealed evidence hashes still match.
- [x] Only authorized paths are staged.
- [x] Owner-untracked files remain untouched.
- [x] One coherent candidate commit is created and not pushed.
- [x] Independent review remains a later exact-SHA gate.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Pending QAC is accidentally promoted | Use existing `SOURCE_ROLE_PENDING`; require a later explicit admission decision. |
| Historical evidence is silently rewritten | Keep every hashed pilot artifact byte-identical and add a corrective record. |
| Purity contracts become cosmetic | Require resolvable lineage, diagnostics, fixtures, and negative tests per dimension. |
| Structural annotations replace Tanzil | Use a separate annotation entity bound to Tanzil `verse_ref` and independent source provenance. |

## Open authority boundary

No QAC artifact acquisition, hash binding, source-role approval, import,
activation, pilot rerun, or remaining-root work is authorized by this plan.
