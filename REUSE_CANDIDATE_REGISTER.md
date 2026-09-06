# Reuse Candidate Register

*Target: `LISAN_LEGACY_REUSE_DELTA_KIT_v1.0/`*

Classification Options:
- `ADMIT_AS_IS`
- `ADAPT_AND_ADMIT`
- `REFERENCE_ONLY`
- `QUARANTINE`
- `SUPERSEDED`
- `REJECT`

## Assessment Queue
- `schemas/`: `ADAPT_AND_ADMIT` (Serve as baseline for new Pydantic v2 models, not used as raw JSON schemas directly)
- `contracts/`: `REFERENCE_ONLY` (Currently empty)
- `steward-contracts/`: `REFERENCE_ONLY` (Currently empty)
- `regression-cases/`: `ADAPT_AND_ADMIT` (Will be translated into pytest and E2E behavioral tests)
- `behavior-golden-tests/`: `REFERENCE_ONLY` 
- `authority-candidates/`: `REFERENCE_ONLY`
- `methodology-candidates/`: `REFERENCE_ONLY`
- `skill-source-candidates/`: `SUPERSEDED` (Migrated to canonical skills)

## Master Package v1.0.1 admission (2026-09-06)

Governed by `docs/canonical/ADMISSION_MASTER_PACKAGE_V1_0_1.md` (hash-bound; no
file copied into the tracked tree).

- `02_CURRENT_OWNER_DIRECTIVES/` (INT-* accepted directives): `ADMIT_AS_IS`
  (governing delta over V2.1; realized in code/docs per the admission map).
- `05_REGISTRIES/{MASTER_POST_V2_1_INTAKE,…CHANGE_PROPOSALS,…OPEN_QUESTIONS}.csv`:
  `ADMIT_AS_IS` as the archived governed-capture backlog. `INT-BOOT-001` is
  realized at runtime by `ChangeProposal(status)` + `RuleRevision(approved_by)` +
  `AuditLog` + the Steward boundary; no parallel registry is created.
- `05_REGISTRIES/MASTER_SUPERSESSION_MAP.csv`: `REFERENCE_ONLY` (governing conflict
  resolutions cited by the admission record).
- `01_CANONICAL_BASE/…V2.1.0/`: `REFERENCE_ONLY` preserved base (never edited).
- `03_PRE_ANALYSIS/`: `REFERENCE_ONLY` OPEN proposals (P1..P8 not adopted).
- `06_RESEARCH_REFERENCES/`, `90_ARCHIVE/`: `REFERENCE_ONLY`.
