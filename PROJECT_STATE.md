# Lisanapp Canonical Consolidation — Project State

## Repository State
- **Repository root**: `D:\APP\tafseer\lisanapp3` (dedicated Git repository for Lisanapp)
- **Branch**: `main`
- **HEAD**: `0e5f256deede286252c299aa2541ea5a8a6b0753` — baseline commit
  `chore: establish governed Lisanapp implementation baseline` (202 tracked files)
- **Remotes**: none configured (no push authorized)
- **Working Tree**: CLEAN at baseline SHA

### Git Provenance Note (2026-08-22)
The previously recorded parent-repository reference (`tafseer` repo,
branch `v7.1-execution`, HEAD `6c98d56f32eb11ab7fcb3d62ae2676019ecbeeb7`)
does **NOT** identify the Lisanapp candidate: the entire `lisanapp3/`
directory was untracked in that repository. An independent read-only
adversarial V3 review discovered this provenance defect; this dedicated
repository was initialized so candidate revisions identify only this
product. The independent V3 verdict remains **V3_NOT_CONFIRMED** until a
fresh independent review is performed against a committed candidate SHA.
Do not treat pre-baseline evidence as candidate-SHA verification.

### Pre-Baseline Evidence Continuity
All prior execution evidence (pytest 45 collected / 5 E2E journeys,
Ruff, Pyright 1.1.411 [5 errors / 62 warnings], Schemathesis v4.25.0
trace, Cosmic Ray 108 mutations / 82 killed / 26 survived) was executed
against the pre-baseline working tree whose content is captured by the
baseline SHA. It supports continuity of state but does not by itself
constitute verified-against-committed-candidate evidence; the V4 gate
must re-execute verification against this SHA.

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
- **Next Action**: Submit baseline SHA `0e5f256deede286252c299aa2541ea5a8a6b0753` for a fresh independent read-only review (or the next gate required by project policy) before any V4 execution. Known open defects from the prior independent review remain unresolved and must not be repaired silently.
