# LISAN3 — Window 03 / Batch 05 Closure

**verdict**: `LARGE_SCALE_ROOT_RESEARCH_CONTINUED_AUTONOMOUSLY`
**base candidate**: `c2b8434` (Window 02 V2 checkpoint, PASSED)
**date**: 2026-09-10

Window 03 opened with Batch 05: **40 new roots** researched end-to-end through the
existing full-occurrence, exact-set, word_ref-level coverage pipeline. Window 02's
48 roots were **not** reprocessed (except one shared-artifact restoration forced by
a filename-collision defect — see below; its research content is unchanged).
Nothing was canonicalized.

## Batch 05 selection (deterministic, diversity-preserving)
Selected via `tools/campaign.py select` across all five occurrence tiers
(3,878 confirmed occurrences; 100 shards @50):

| Tier | Roots |
|---|---|
| xl (>200) | rbb 980, qwm 660, Aty 549 |
| l (50–200) | bny 184, xrj 182, SlH 180, sbl 176, tbE 172, Awl 170 |
| m (15–50) | krm, Ehd, Sdr, zyn, SrT, nsy, w*r, HfZ, bdl, dbr |
| s (4–15) | E$w, ETw, Hrv, Sff, Swm, fqr, lwm, rjm, rsw, vwy |
| xs (≤3) | Aff, Afq, Ajj, Anf, Ass, Azf, Dgv, DjE, Ebs, Erw, Ery |

Diversity spans occurrence frequency (3→980), form/derivational range, construction
variety (e.g. qawm "people" vs qāma "stand"; rabb "Lord" vs the -āniyy/-iyy
nisba band), semantic-neighbour pressure, and structural difficulty.

## Pipeline executed (each stage persists per root)
1. `prep` full-coverage packets (RootDescriptiveProfile + every confirmed occurrence).
2. **Discovery + adversarial verify** workflow (80 agents: 40 blind-internal-discovery
   → 40 adversarial refuters, pipelined; xhigh effort on rbb/qwm/Aty with chunked
   reads of the >1,800-line packets). 0 errors; every root fully accounted
   (occurrences_checked == occurrences_total for all 40).
3. `prep-coverage` → 100 shards with the frozen candidate embedded.
4. **Coverage-mapping** workflow (100 shard mappers + per-root resistant
   reconciliation). Every word_ref mapped; **0 exact-set defects** (researched set
   == confirmed StructuralToken set for all 40 roots).
5. `persist-coverage` with deterministic exact-set validation → durable per-root
   artifacts + ledger + CampaignState.

## Results (recomputed from durable artifacts)

| Metric | Value |
|---|---|
| Total Root Universe | 1,642 |
| Processed (cumulative) | **88** (48 + 40) |
| Research-complete (exact-set COMPLETE) | **88 / 88** |
| `PENDING_COVERAGE_EVIDENCE` | **0** |
| Remaining queue | 1,554 |
| Universal-presence-holds (cumulative) | 45 |
| Canonicalization-pending | 88 (nothing canonicalized) |

**Batch 05 strength**: STRONG 20 · MODERATE 6 · WEAK 13 · UNRESOLVED 1
(universal presence: 26/40). Cumulative: STRONG 34 · MODERATE 10 · WEAK 34 · UNRESOLVED 10.

- **STRONG + universal (20)**: Aty, xrj, sbl, tbE, w*r, HfZ, bdl, zyn, SrT, Swm, Sff,
  lwm, vwy, E$w, Aff, Afq, Ass, Azf, DjE, Ery.
- **MODERATE + universal (6)**: Ajj, Dgv, Ebs, Hrv, nsy, rsw.
- **WEAK (13)** — adversarial verdict `PARTIALLY_SUPPORTED` (over-breadth / a genuine
  hard sub-sense) blocks universal, per the documented kwn precedent: rbb (the
  -āniyy/-iyy nisba band), qwm (qawm "people" vs "stand-upright"), bny, SlH, Awl,
  Sdr, dbr, krm, Ehd, ETw, fqr, rjm, Erw.
- **UNRESOLVED (1)**: Anf — nose (5:45) vs. the temporal adverb آنِفًا "just now"
  (47:16); the internal discoverer could not reconcile 47:16:16:1 without forcing.

ROOT_SEMANTIC_UNITY held NON-NEGOTIABLE throughout: no majority/percentage was used;
unity was tested against each root's hardest occurrences; unresolved occurrences block
universal presence rather than being absorbed.

## Methodology revisions (between-batch; reproducible; regression-covered)
Two reproducible integrity defects were discovered and fixed with focused tests;
non-negotiable principles preserved.

1. **Cross-lens root unity** (`finalize_root_disposition`). Universal presence was
   computed only from coverage + adversarial verdict, ignoring the discovery lens.
   Root **Anf** surfaced the contradiction: `research_state=UNRESOLVED` yet
   `universal_presence_holds=True` / `independent_verification=PASSED`. Fix: an
   UNRESOLVED discovery result, and any occurrence the discoverer flagged
   (`presence.inconsistent_refs`), now block universal presence and surface in
   `unreconciled_occurrences`. Only Anf was affected (all other 87 roots clean).
   Regression: `test_17`, `test_18`.

2. **Case-insensitive filename collision** (`safe_name`). Buckwalter uses letter
   case to distinguish letters (S=ص vs s=س, D=ض vs d=د, T=ط vs t=ت, Z=ظ vs z=ز,
   H=ح vs h=ه). On Windows' case-insensitive filesystem, Batch 05's **Swm** (ص و م)
   overwrote Window 02's **swm** (س و م) artifact. The QAC universe has **137** such
   case-fold pairs — a latent data-loss defect at scale. Fix: `safe_name` now escapes
   the five homograph uppercase letters with the existing reversible hex scheme
   (`S`→`_53_`), yielding 0 collisions universe-wide. The 24 affected processed
   artifacts were migrated to collision-safe filenames (research content unchanged);
   the overwritten `swm` artifact was restored byte-identical from `c2b8434`.
   Regression: `test_19`.

Methodology revision id unchanged (`LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4`):
these are storage-integrity and disposition-consistency fixes, not a change to the
research method or its non-negotiable principles.

## V2-style checkpoint proofs
1. Focused regression suite `tests/test_campaign_coverage.py` (19) +
   `tests/test_qac_morphology.py` (5): **24 PASSED**.
2. Exact equality confirmed StructuralToken word_refs == researched word_refs for
   **every** research-complete root (88/88), recomputed independently.
3. 88 ledger roots == 88 durable artifact files; **0** case-insensitive filename
   collisions; **0** content/filename mismatches; **0** stale files.
4. **0** contradictions (no root is universal-present while UNRESOLVED or carrying a
   discoverer-flagged occurrence).
5. Research ≠ canonicalization: all 88 `canonical_authorization = PENDING`.

## Blockers
None. Canonicalization remains independent and PENDING (not a research blocker).

## Durable state / resume
- Ledger: `artifacts/semantic-campaign/CAMPAIGN_RESEARCH_LEDGER.json` (88 roots).
- Per-root artifacts: `artifacts/semantic-campaign/roots/*.json` (88; collision-safe
  filenames via `safe_name`).
- Resume: `artifacts/semantic-campaign/RESUME.md`. Next action: `select --n 40` →
  prep → discovery/verify workflow → prep-coverage → coverage-mapping workflow →
  persist-coverage for Batch 06, continuing Window 03 toward the full 1,642 universe.
