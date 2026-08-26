# Tanzil Production Activation Evidence

Activation timestamp: `2026-08-26T16:52:00.806969Z`

## Authorized identity and live prerequisites

- Starting HEAD: `4fe63673bd9a7057ce87b43d8bb2aa6e0f34a5c3`.
- Owner-authorized pre-activation candidate:
  `69d0a27b2a2ca99d8c62dcf6344f42de51c17175`.
- Activation implementation commit:
  `a1d910f11735ec4ba0e9324dbb82b800efd485f6`.
- Snapshot: `snap_tanzil_1_1_ac0724796cbb`.
- Source/version: `TANZIL_QURAN_UTHMANI` / `1.1`.
- Artifact: `data/corpus/tanzil/tanzil-uthmani-1.1.txt`, `1,334,737`
  bytes, SHA-256
  `ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af`.
- Live reparse and identity-index reconciliation passed for 6,236 unique,
  complete, ordered verse identities across 114 surahs. The 6,236 persisted
  non-fixture occurrences matched the exact artifact text and deterministic
  occurrence IDs. No competing production-active snapshot existed.
- Methodology
  `LISAN_QURANIC_SEMANTIC_EXTRACTION@6bb1c10a0f9a` remained `CURRENT`,
  source-matching, and ResearchRun-eligible.
- Live schema was `CURRENT` at Alembic head `c4d8b7e2a913`.

## Governed transition and audit

The `TanzilProductionActivationService` reused the governed pre-activation
importer to verify the artifact and occurrences, then atomically transitioned:

```text
validation_status: PENDING -> VALIDATED
activation_status: CANONICAL_ACTIVATION_PENDING -> PRODUCTION_ACTIVE
```

The only production-active snapshot after transition is
`snap_tanzil_1_1_ac0724796cbb`.

Audit record:

- ID: `aud_tanzil_production_activation_ac0724796cbb`
- Action: `AUTHORIZE_TANZIL_PRODUCTION_ACTIVATION`
- Actor: `OWNER_AUTHORITY`
- Timestamp: `2026-08-26T16:52:00.806969Z`
- Decision reference:
  `docs/canonical/ADMISSION_TANZIL.md#owner-production-activation-decision`
- Evidence: prior/new lifecycle states, owner reason, artifact path/version/
  byte size/hash, identity-index path/hash, verification revision, 114 surahs,
  6,236 verses, and `IMPORT_VALIDATED` are persisted in `new_state`.

CANON-001 remains limited to
`CANON_001_ARTIFACT_IDENTITY_MATCH_CONFIRMED`; no external governance state was
imported.

## ResearchRun and Run Builder evidence

- A real production-path `POST /runs` returned HTTP 200 and persisted
  `run_3410bc36`, bound to the exact active snapshot and eligible methodology.
- Unknown Corpus and unknown Methodology requests returned HTTP 422.
- Focused integration tests prove inactive Corpus, retired/ineligible
  Methodology, and later authority revocation fail closed with HTTP 503.
- Live `/attention` returned `available=true`, no blockers, and exactly one
  Corpus/Methodology choice: the authorized pair above.
- The affected Playwright Journey 1 passed. A separate live Chrome DevTools
  readback rendered only those two governed choices, returned HTTP 200 for
  `/api/attention` and `/api/ask`, and reported no console warnings or errors.
  No second ResearchRun was started through the browser.

## Negative activation and bounded state

Focused tests reject wrong hash, missing artifact, fixture-only state,
incomplete import, stale occurrence rows, wrong source/version, competing
active snapshot, non-pending lifecycle, ineligible Methodology, reactivation,
and a lookalike snapshot ID.

The prior `BLOCKED_CORPUS_PENDING` requirement is factually resolved by this
exact LISAN3 production activation. Semantic execution remains separately
gated: no pilot or remaining batch was started, and
`DO_NOT_START_REMAINING_BATCHES` remains in force until separate owner
authorization.

QAC is unchanged: it remains an auxiliary morphology/syntax candidate; its
real-format TSV import is not implemented, and semantic/gloss/ontology content
remains excluded from semantic authority. Tanzil activation does not activate
or complete QAC.

No semantic batch, QAC import, model/embedding work, R2, R3, V4, release, push,
or external LQE mutation was performed.
