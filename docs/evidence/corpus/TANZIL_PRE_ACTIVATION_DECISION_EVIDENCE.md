# Tanzil Pre-Activation Decision Evidence

Evidence timestamp: `2026-08-26T16:01:38.564773Z`

## Artifact identity

- Source: `TANZIL_QURAN_UTHMANI` / Tanzil Quran Text (Uthmani)
- Version: `1.1`
- Repository artifact:
  `data/corpus/tanzil/tanzil-uthmani-1.1.txt`
- Format: `TANZIL_UTHMANI_1_1_ONE_VERSE_PER_LINE_UTF8_LF`
- Size: `1,334,737` bytes
- Expected SHA-256:
  `ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af`
- Actual SHA-256:
  `ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af`
- Identity index:
  `data/corpus/tanzil/quran-verse-index-v1.0.json`
- Identity-index SHA-256:
  `0d0a2273e82ebb0d9848ccbf831f1bb297c0fb255413c5aeb299bbfaf2bbc967`

## Import and identity evidence

- Parser result: strict UTF-8, no BOM, LF-only, final LF, embedded Tanzil 1.1
  marker, exact byte-size/hash, and real one-verse-per-line records passed.
- Identity reconciliation: exactly 114 surahs and 6,236 unique, complete,
  ordered `surah:ayah` identities passed; stored verse text matches the exact
  corresponding artifact line without normalization.
- Snapshot: `snap_tanzil_1_1_ac0724796cbb`
- Persisted occurrences: `6,236`
- First occurrence: `occ_tanzil_1_1_001_001` / `1:1`
- Last occurrence: `occ_tanzil_1_1_114_006` / `114:6`
- Fixture state: `false`
- Exact re-import: snapshot reused, no competing snapshot or new occurrences.
- CANON-001 reconciliation:
  `CANON_001_ARTIFACT_IDENTITY_MATCH_CONFIRMED` (artifact identity only).

## Lifecycle boundary

Reached:

```text
SOURCE_ROLE_APPROVED
→ ARTIFACT_PRESENT
→ EXPECTED_HASH_BOUND
→ HASH_VERIFIED
→ IMPORT_VALIDATED
→ CANONICAL_ACTIVATION_PENDING
```

The compact `validation_status` remains `PENDING`. Live production-validation
readback reports exactly:

- `canonical admission is not production-active`
- `snapshot is not production-active`

`POST /runs` returned HTTP 503 against this snapshot and the current governed
methodology revision; the live ResearchRun count remained zero.

## Verification evidence

- V1: 22 focused authority/parser/import/lifecycle tests passed.
- Reversible fresh-DB migration and model/constraint parity passed.
- Live schema: expected and actual Alembic head `c4d8b7e2a913`, no missing
  model tables or columns.
- Ruff passed; Pyright reported 0 errors (178 SQLAlchemy-style warnings).
- Negative coverage includes missing/wrong/truncated/extra/malformed artifact,
  encoding and normalization corruption, wrong source/version/count, duplicate,
  missing, and impossible identities, caller-self-declared hash, fixture
  impersonation, premature import validation, and premature activation.

## Remaining decision boundary

The Tanzil artifact/provenance/hash/import portion of the requalification
Corpus blocker is resolved. The production-active Corpus blocker remains, and
remaining-batches authorization remains separate. QAC real-format import and
its semantic-field quarantine boundary are unchanged.

`PRODUCTION_ACTIVATION_NOT_GRANTED`
