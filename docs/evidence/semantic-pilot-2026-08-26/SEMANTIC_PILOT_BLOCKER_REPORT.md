# Fresh Five-Root Semantic Requalification Pilot — Blocker Report

Date: 2026-08-26
Starting HEAD: `67dccb9017b6d9500a90d7564358daf8192b4190`
Readiness: `SEMANTIC_PILOT_BLOCKED`

## Active authority

- CorpusSnapshot: `snap_tanzil_1_1_ac0724796cbb`
- Source/version: `TANZIL_QURAN_UTHMANI` / `1.1`
- Corpus SHA-256: `ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af`
- Corpus lifecycle: `VALIDATED` / `PRODUCTION_ACTIVE`; non-fixture
- Corpus extent: 6,236 verse records across 114 surahs
- Methodology: `LISAN_QURANIC_SEMANTIC_EXTRACTION@6bb1c10a0f9a`
- Methodology revision: `git-blob:6bb1c10a0f9a09bf9a59c29c45e2252efc9832fb`
- Active skill: `skills/lisan-semantic-extraction/SKILL.md`
- Active skill SHA-256: `43c0a40b3f465fa95695607c2de838effd07946966c57ad15275d0051e92a288`
- Allowed use: `QURAN_INTERNAL_CUMULATIVE_RUN`

The live schema was `CURRENT` at Alembic head `c4d8b7e2a913`. The live admission projection exposed exactly the snapshot and methodology above with no blockers.

## Bounded execution result

| Root | ResearchRun | Runtime status | Occurrence coverage | Semantic result | Root Core | Boundary / neighbors / falsification | Traceability | ROOT_CARD / TERM_CARD | LQE use |
|---|---|---|---|---|---|---|---|---|---|
| ع د ل | `run_d7519288` | `LOCK_BLOCKED` | `FAIL` — root occurrences not authority-resolvable | `REQUALIFICATION_REQUIRED` | `null` | `NOT_VERIFIED` | Run/Corpus/method/isolation/Gates resolve | Not produced | `LQE_REQUALIFICATION_REQUIRED` |
| أ م ن | `run_8d696d64` | `LOCK_BLOCKED` | `FAIL` — root occurrences not authority-resolvable | `REQUALIFICATION_REQUIRED` | `null` | `NOT_VERIFIED` | Run/Corpus/method/isolation/Gates resolve | Not produced | `LQE_REQUALIFICATION_REQUIRED` |
| س ل م | `run_1a24ffab` | `LOCK_BLOCKED` | `FAIL` — root occurrences not authority-resolvable | `REQUALIFICATION_REQUIRED` | `null` | `NOT_VERIFIED` | Run/Corpus/method/isolation/Gates resolve | Not produced | `LQE_REQUALIFICATION_REQUIRED` |
| ح م د | `run_68c7b72c` | `LOCK_BLOCKED` | `FAIL` — root occurrences not authority-resolvable | `REQUALIFICATION_REQUIRED` | `null` | `NOT_VERIFIED` | Run/Corpus/method/isolation/Gates resolve | Not produced | `LQE_REQUALIFICATION_REQUIRED` |
| ش ك ر | `run_5f72ad9d` | `LOCK_BLOCKED` | `FAIL` — root occurrences not authority-resolvable | `REQUALIFICATION_REQUIRED` | `null` | `NOT_VERIFIED` | Run/Corpus/method/isolation/Gates resolve | Not produced | `LQE_REQUALIFICATION_REQUIRED` |

`REQUALIFICATION_REQUIRED` above is the owner-requested implementation-side outcome, not a value persisted into an Epistemic axis. The official persisted run outcome is `LOCK_BLOCKED`. No `NOT_ESTABLISHED` value was persisted.

## Canonical blockers

### 1. Exact occurrence and morphology evidence is unavailable

The production snapshot is an exact, governed Quran text source, but its 6,236 `CorpusOccurrence` records are verse-level records. Runtime readback established:

- `structural_source = null`
- `structural_source_version = null`
- every distinct `CorpusOccurrence.expression` value is the empty string
- the record contract exposes only snapshot ID, expression, verse reference, and text

Therefore the runtime cannot deterministically resolve which tokens belong to any of the five roots, nor their lemma, form, construction, or participant structure. Orthographic guessing or model memory would not meet the active skill's verified-evidence requirements.

QAC is admitted only as an auxiliary structural-source candidate with `ARTIFACT_VERIFICATION_PENDING` and `CANONICAL_ACTIVATION_PENDING`. Its real-format import is not implemented, and this pilot explicitly did not authorize QAC import. No other authority-approved deterministic morphology fallback exists.

Failure class: `EXTERNAL_DEPENDENCY`.
Execution mode: `NO_VALID_FALLBACK`.

### 2. Current Internal Lock is structurally fail-closed

The canonical `PURITY_CHECK` evaluated each run and returned `FAILED`. With no Observation or Hypothesis artifacts, all eight dimensions are `NOT_EVALUATED`. More importantly for later execution, the current evaluator implements a clean/sequence check only for `DICTIONARY_FIRST`; its other seven dimensions are always emitted as `NOT_EVALUATED` because their evidence extractors are unsupported.

The canonical `INTERNAL_LOCK` consequently returned `FAILED` for each run because the current Purity record did not pass. The backend correctly refused to make a `SemanticClaim` available without a current valid Internal Lock.

Failure class: `PRODUCT_DEFECT`. The fail-closed behavior is correct; the missing evaluator capability is the blocker.

### 3. No accepted ROOT_CARD / TERM_CARD contract exists

The active semantic skill supplies the result presentation template used by the five `*-result.yaml` files. The accepted runtime contracts contain no ROOT_CARD or TERM_CARD schema/validator. Since cards are derived read models and cannot originate semantic claims, none were invented.

Failure class: `AUTHORITY_CONFLICT` at the requested presentation boundary.

## Blind Lab and prior quarantine

Each run has a persisted `CLEAN` IsolationState. A prohibited prior-semantic read was attempted through the active isolation service and was blocked for each run. Five corresponding `IsolationEvent` records have `was_blocked=true`; none changed isolation to `PRIOR_CONTAMINATED`.

No prior card, Root Core, neighbor decision, semantic result, Knowledge Graph result, vector result, dictionary, or legacy research file was loaded. The blocked read is evidence of enforced quarantine, not contamination.

The ح م د and ش ك ر runs were created independently. Neither produced a hypothesis or semantic result, so no cross-root comparison occurred.

## Gate and acceptance summary

- Corpus binding: `PASS` for all five.
- Methodology binding and source hash: `PASS` for all five.
- Blind Lab/quarantine enforcement: `PASS` for all five.
- Gate computation validity: `PASS`; actual `PURITY_CHECK` and `INTERNAL_LOCK` outcomes are `FAILED` for all five.
- Exact occurrence coverage: `FAIL` for all five.
- Morphology, constructions, context diversity, hypotheses, semantic boundary, neighbor differentiation, counterevidence, falsification, and unresolved-branch analysis: `NOT_VERIFIED` for all five.
- Status correctness and blocker traceability: `PASS` for all five.
- LQE-safe derivation: `PASS`; the structural-mining view deliberately exports empty structural arrays and no semantic truth.

The complete per-root matrix is in `acceptance-matrix.json`. No overall percentage was computed.

## Artifact boundaries

- The five YAML results follow the active skill's blocked-result presentation shape. Semantic fields are `null` and do not masquerade as research conclusions.
- `pilot-manifest.json` is an operational evidence manifest, not a competing semantic-result schema.
- `lqe-structural-mining.json` exposes no Root Core, definition, neighbor truth, label, or confidence.
- No `SemanticClaim`, ReviewDecision, ROOT_CARD, TERM_CARD, publication artifact, model artifact, QAC artifact, or LQE repository mutation was created.

## Exact next task

Perform a fresh independent read-only review of the exact pilot evidence candidate. If the blocker verdict is accepted, obtain a separate owner decision for a bounded enabling scope that (1) admits or explicitly approves a deterministic root/morphology source and (2) implements evidence-backed evaluators for all mandatory Purity dimensions. Do not restart these five runs or start remaining batches until that enabling candidate is independently reviewed.
