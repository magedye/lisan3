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
