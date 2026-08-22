# Lisanapp Canonical Consolidation — Project State

## Repository State
- **Branch**: `v7.1-execution`
- **HEAD**: `6c98d56f32eb11ab7fcb3d62ae2676019ecbeeb7` Disable line-ending conversion repo-wide to preserve package checksums
- **Remotes**: `origin git@github.com:magedye/tafser.git`
- **Working Tree**: Many untracked and deleted files (mostly in `../V7` parent context). Active directory contains new consolidation files.

## Active Authorities
- UX Constitution v4.0 (for frontend reference)
- Canonical Implementation Reference (to be generated)
- Semantic Extraction Revised Skill

## Current Progress
- **Environment Discovery**: `py.exe` successfully discovered and used to construct a project-local `.venv`. Python blocker is **RESOLVED**.
- **WP-00**: Complete
- **WP-01**: Complete (Legacy classification verified, skills reconciled)
- **WP-02**: Complete (Backend `.venv` configured, OpenAPI generated successfully, SQLite persisted, migrations executed)
- **WP-03**: Complete (Frontend built successfully, typed API clients generated)
- **WP-04 Slice A**: Complete (Ask Lisan & Research Run boundary implemented and verified)
- **WP-04 Slice G**: Complete (Knowledge Explorer, Audit Logs, Provenance, Reproduction Manifests, Quality Dimension Schemas)
- **V3 Phase Gate**: `V3_PARTIAL` (Missing canonical Corpus evidence [TESTED_WITH_FIXTURES], AI tested with fake provider only [TESTED_WITH_FAKE_PROVIDER], E2E stubs only [CONFIGURED_NOT_EXECUTED]).
- **Corpus Admission**: `CORPUS_ARTIFACT_VERIFICATION_PENDING`
- **WP-04 Slice B**: Complete (Blind Lab isolation boundary, corpus, and structural observation implemented, Hardened)
- **WP-04 Slice C**: Complete (Semantic Analysis, Hypothesis, Neighbor differentiation, Falsification, and Gate evaluation implemented)
- **AI Runtime Integration**: COMPLETE
  - The AI-First Governed Runtime has been integrated via **Pydantic AI**.
  - `AIExecutionRecord` table established for full provenance.
  - `ModelProvider` protocol upgraded to Pydantic AI `Agent`.
  - Fake vs Live Verification Status: **TESTED_WITH_FAKE_PROVIDER** (using Pydantic AI `TestModel`).
  - `AIContextBuilder` enforces Blind Lab Isolation, strictly limiting context available to the AI.
  - `SemanticSkillLoader` implemented to resolve and snapshot canonical skill (`skills/lisan-semantic-extraction/SKILL.md`).
- **Tooling & Governance Checkpoint**:
  - **Tooling Reference**: `docs/canonical/LISAN_TOOLING_ADOPTION_REFERENCE.md` (Linked from canonical).
  - **Pydantic AI**: ADOPTED (Replaced custom ModelProvider/FakeModelProvider).
  - **Hypothesis**: ADOPTED (Added `test_properties.py` for invariant testing).
  - **Promptfoo**: ADOPTED (Baseline created in `tools/governance-lab/ai-evals/`).
  - **Ruff / Pyright**: ADOPTED (Installed and available for V1 checks).
  - **Tanzil Admission**: Recommended `ADMIT_AS_CANONICAL_TEXT`.
  - **QAC Admission**: Recommended `ADMIT_AS_AUXILIARY_STRUCTURAL_SOURCE`.
- **Corpus Production Adapter**: IMPLEMENTED and TESTED_WITH_FIXTURES
  - Tanzil: `SOURCE_ROLE_APPROVED`, `ARTIFACT_VERIFICATION_PENDING`, `CANONICAL_ACTIVATION_PENDING` (Tests use fixtures until explicit artifact hashing).
  - QAC: `SOURCE_ROLE_APPROVED`, `ARTIFACT_VERIFICATION_PENDING`, `CANONICAL_ACTIVATION_PENDING` (Tests use fixtures).
  - QAC morphological data strictly isolated (Semantic fields like ONTOLOGY and SEM quarantined).
  - Cross-source alignment logic implemented.
  - `CorpusSnapshot` persisted model introduced.
  - Verification: `CORPUS_ADAPTER_VERIFIED_FOR_ADMITTED_SOURCES` (tested against deterministic local stubs).
- **WP-04 Slice D (Review & Publication)**: COMPLETE
  - Replaced official_status with 4 axes: Epistemic, Review, Freshness, Publication on `SemanticClaim`.
  - Added `ReviewDecision` tracking and endpoints.
  - Publication strictly governed by Epistemic State, Review State, and Validated Corpus Snapshot.
- **Next Action**: Proceed with WP-04 Slices E/F/G (Governance, Steward, Knowledge).
