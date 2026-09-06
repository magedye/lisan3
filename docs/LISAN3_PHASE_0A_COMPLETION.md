# LISAN3 — Phase 0A Completion & Handoff

> **SUPERSEDED BY OWNER REQUEST 01** (see `docs/LISAN3_REQUEST_01_COMPLETION.md`).
> This record describes the initial conservative Phase 0A slice. Request 01 later
> evolved the descriptive model to **four** knowledge levels (DIRECT / QUALIFIED /
> DISPUTED / UNRESOLVED) and **persisted** it, adding tables `structural_tokens`,
> `external_hypothesis_records`, `campaign_states` (migration `b3d6e2f8c150`).
> Where this document says "no table / no migration / deliberately not built", read
> that as true of Phase 0A only; the persisted stores and the unified external
> register are now built and owner-authorized. Root-unity enforcement was also
> hardened (counterexample occurrences can no longer satisfy universal coverage).


**verdict**: `MASTER_ADMITTED_AND_PRE_ANALYSIS_FOUNDATION_QUALIFIED`
**explicitly NOT**: `READY_FOR_LARGE_SCALE_ROOT_ANALYSIS`
**date**: 2026-09-06 · **base SHA**: `34d4b01cd3ddbfe6424823aa6ef46c696ecfd3d3` ·
**branch**: `main` (no commit/push/tag/merge performed)

Persisted per owner directive: this record is the durable current-task state that
precedes owner Request 01. Mode executed: Inspect → Map → Reuse → Minimal
Implement → Verify.

## 1. Verdict
Qualified. The Master Integrated Package v1.0.1 is conservatively admitted
(hash-bound, no duplication); the accepted post-V2.1 owner directives that must
precede analysis are realized reuse-first; and a deterministic descriptive-
knowledge foundation now exists. Large-scale root analysis is NOT authorized.

## 2. Base / candidate identity
Worked directly on `main` at `34d4b01…`; clean tracked tree at start. No new
branch/worktree (in-place, additive). HEAD unchanged.

## 3. Package / material admitted or mapped
`Quran_Lisan_Master_Integrated_Package_v1.0.1.zip`
SHA-256 `4f88c3556e32ce0c5697db6acfaf711c7d03e05179863964fe57c8cae021268b`,
admitted **by hash, not bytes** via `docs/canonical/ADMISSION_MASTER_PACKAGE_V1_0_1.md`.
`02_CURRENT_OWNER_DIRECTIVES/` = governing delta; V2.1 base preserved; `03_PRE_ANALYSIS/`
+ proposal registries = OPEN/non-governing; `MASTER_SUPERSESSION_MAP.csv` (SUP-004/005/006/009)
cited for conflict resolution.

## 4. Items reused unchanged (no duplication)
`CorpusSnapshot`/`CorpusOccurrence`, `QACAdapter`/`alignment`, `derive_completeness`
(exact universal coverage), `CanonicalizationPolicy`, `BlindLabIsolationService` +
`IsolationState`, `MethodologyRevision` immutability, `ChangeProposal`/`RuleRevision`/
`GovernanceRule`/`AuditLog` (governed capture), `AIContextBuilder`, `Hypothesis`.
Package registries admitted as archive (INT-BOOT-001 realized by existing models).

## 5. Newly implemented gaps (minimal, additive)
1. **Root Descriptive Profile** — `backend/domain/services/corpus/descriptive_profile.py`:
   deterministic, meaning-free read-model (root→forms→counts, refs, surah
   distribution, singletons, disagreements), tagging each datum with one of three
   knowledge levels. No table, no migration, no LLM. (V3 / INT-PRE-OWN-001)
2. **Root-unity canonicalization guard** — `backend/domain/services/canonicalization.py`:
   a UNIVERSAL `ROOT_CONCEPT` with any non-empty `unresolved_cases` cannot be
   ACCEPTED. (V4 / INT-OWN-ROOT-002)
3. **Hypothesis origin marker** — additive `Hypothesis.origin`
   (`INDEPENDENT_INTERNAL_DERIVATION` default | `EXTERNAL_CANDIDATE`) + migration
   `a2f5c1d7b940` + schema/endpoint wiring. (V6 / INT-EXT §9)

## 6. Descriptive knowledge capability
Deterministic and reproducible: identical tokens → byte-identical profile
(`as_dict()` equality). Counts computed in pure Python; provenance read from the
snapshot. Three levels enforced: DIRECT_TEXTUAL_FACT (refs, surah distribution) vs
QUALIFIED_STRUCTURAL_ANNOTATION (root/form attribution + attribution-dependent
counts) vs DISPUTED_OR_UNRESOLVED_STRUCTURAL_ANNOTATION (unconfirmed attributions).

## 7. Root Descriptive Profile evidence
`tests/test_phase0a_pre_analysis_foundation.py::test_1/2/3` — non-model-generated
facts, reproducible counts (`total_confirmed_occurrences==4`, forms
`{FORM_II_VERB:2, FORM_IV_VERB:1, NOUN:1}`), and preserved structural uncertainty
(disputed token excluded from confirmed count, surfaced in disagreements).

## 8. Structural-data reliability handling
Root/form attribution never presented as a textual fact; disagreements preserved,
not hidden; QAC remains `SOURCE_ROLE_PENDING` (unchanged).

## 9. Root-semantic-unity enforcement
Existing exact-set coverage forbids any majority shortcut (`supported==eligible`);
new guard blocks acceptance while a confirmed occurrence is unexplained. Proven by
`test_4` (blocked) and `test_5` (2-of-3 majority → 422; contract exposes no
threshold/percent/majority field).

## 10. Terminology delta
Reused package `05_TERMINOLOGY_CLARITY_DELTA.md` for new human-facing text; **no**
technical ID/schema rename. Recorded in the admission map and FP-9. `origin` uses
plain enumerated values, not «دلالة».

## 11. External-hypothesis support
`Hypothesis.origin` marks external candidates (e.g. Jabal) so they cannot
masquerade as blind internal discovery; external origin has no confidence field
and no canonical transition. Existing methodology immutability + source-read
blocking keep external claims out of authority. Proven by `test_6/7`. The unified
external register + claim_type taxonomy were **deliberately not built** (OPEN
non-owner proposals).

## 12. Isolation mechanism used
Lightest sufficient: reused `BlindLabIsolationService`/`IsolationState` + added the
one `Hypothesis.origin` marker. Full permanent dual-lane lifecycle (SUP-008)
deliberately avoided.

## 13. FOUNDATIONAL_PROFILE_DRAFT
`docs/FOUNDATIONAL_PROFILE_DRAFT.md` — 10 accepted-only premises (FP-1..FP-10),
5 fields each, `DRAFT / NON_GATING`, with an explicit OPEN appendix. No five-layer
taxonomy; no OPEN item promoted.

## 14. Tests and exact results
`pytest tests --ignore=tests/e2e` → **166 passed** (incl. 9 new). New file covers
all 10 mandatory properties (test 10 = the full green suite). Migration validated
on a throwaway DB: full upgrade chain, single head `a2f5c1d7b940`, `origin` present,
downgrade/upgrade round-trip clean. Ruff clean on all changed files.

## 15. Mandatory-test mapping
1 `test_1` · 2 `test_2` · 3 `test_3` · 4 `test_4` · 5 `test_5` · 6 `test_6` ·
7 `test_7` · 8 `test_8` · 9 `test_9` · 10 full suite (166 passed).

## 16. Complexity added
One additive column + migration (`Hypothesis.origin`); one deterministic service
(no persistence); one ~9-line canonicalization guard; five docs. No new gate,
status axis, registry, or authority store.

## 17. Complexity deliberately avoided
Persisted `StructuralToken`/Root-Profile authority store (GQ-PRE-003 OPEN);
`EXTERNAL_HYPOTHESIS_REGISTER` + `claim_type` taxonomy; full dual-lane lifecycle
(SUP-008); P1..P8 formalization (SUP-007); wide V2.1 terminology rename; any
mass schema/ID rename; corpus/UI/vector/auth changes.

## 18. Files changed
Modified: `.gitignore`, `AUTHORITY_MAP.md`, `REUSE_CANDIDATE_REGISTER.md`,
`backend/domain/models.py`, `backend/domain/schemas.py`,
`backend/domain/services/canonicalization.py`, `backend/main.py`.
Added: `backend/domain/services/corpus/descriptive_profile.py`,
`alembic/versions/a2f5c1d7b940_add_hypothesis_origin.py`,
`tests/test_phase0a_pre_analysis_foundation.py`,
`docs/canonical/ADMISSION_MASTER_PACKAGE_V1_0_1.md`,
`docs/FOUNDATIONAL_PROFILE_DRAFT.md`, `docs/LISAN3_PHASE_0A_COMPLETION.md`.

## 19. Unrelated files confirmed untouched
No other tracked file changed (`git diff --stat` = 7 files). Untracked owner
packages/kits preserved. No corpus identity, UI, auth, vector, or broad schema
change. No commit/push/tag/merge.

## 20. Blockers before calibration
None hard. Before a real batch, the owner should decide GQ-PRE-003 (whether to
persist a StructuralToken store to make profiles reusable across runs at scale)
and whether QAC morphology is promoted beyond `SOURCE_ROLE_PENDING`.

## 21. Owner decisions genuinely required
(a) GQ-PRE-003 persisted descriptive store vs on-demand service; (b) SUP-007
P1..P8 formalization; (c) SUP-008 dual-lane scope; (d) unified external register +
claim_type taxonomy; (e) calibration batch size + mandatory robustness tests;
(f) full-vs-human-facing terminology review.
