# LISAN3 — Window 02 Closure & V2 Checkpoint

**verdict**: `WINDOW_02_EVIDENCE_COMPLETE` (V2 checkpoint PASSED)
**candidate SHA**: see closure commit on `pre-analysis-foundation`
**date**: 2026-09-10

Window 02 is closed: all 48 processed roots have a **terminal, deterministic,
exact-set coverage evidence state**. No new roots were started. Nothing was
canonicalized.

## What was finished (interrupted-work closure)
The session-limit blocker that interrupted Window 02 reset; the two interrupted
workflows were **resumed** (cached agent outputs replayed; only failures re-ran):
- **Batch-03 coverage** (16 roots): completed; all exact-set validated.
- **Batch-04 verification** (24 roots): completed; then batch-04 coverage mapping.
- **Batch-04 coverage** (24 roots): 22 passed exact-set immediately; the validator
  correctly REFUSED 2 — `Dll` (2 confirmed word_refs never emitted) and `kwn`
  (agent mis-segmented `26:112:5:1` as `26:112:5:2`). These were closed with a
  **targeted gap mapping** for the exact missing occurrences (real dispositions,
  not fabricated) and the spurious `26:112:5:2` dropped; both then passed.

This is the correction working as designed: model-claimed coverage is never trusted;
only word_ref-level exact-set equality upgrades a root to COMPLETE.

## Recomputed counts (from durable artifacts, not prose)
Independently re-validated from `artifacts/semantic-campaign/roots/*.json` against
the confirmed StructuralToken store:

| Metric | Value |
|---|---|
| Total Root Universe | 1,642 |
| Processed (Window 02 cumulative) | **48** |
| Research-complete (exact-set COMPLETE) | **48 / 48** |
| `PENDING_COVERAGE_EVIDENCE` remaining | **0** |
| Proven exact-set (no dup, no verse_ref substitution) | **48 / 48** |
| Universal-presence-holds (research judgments) | 19 |
| Canonicalization-pending | 48 (nothing canonicalized) |
| Remaining queue | 1,594 |

Result strength (research level): STRONG 14 · MODERATE 4 · WEAK 21 · UNRESOLVED 9.
STRONG examples (universal, verification PASSED, canon PENDING): ktb, Hkm, qwl, Dll,
smE, TEm, bdA, mTr, Hsn, Tyb, fsd, nfE, Eql, Hrj.

## V2 checkpoint proofs
1. **Focused regression suite** `tests/test_campaign_coverage.py`: 8/8 PASSED
   (exact-once packet; missing blocks COMPLETE; duplicate cannot substitute;
   resistant blocks universal; research/canon independence; resume preserves exact
   sets; idempotent persist; reprocessing preserves lineage). `test_qac_morphology`:
   5/5. Total 13 PASSED.
2. **Exact equality** confirmed StructuralToken word_refs == researched word_refs
   for **every** research-complete root (48/48), recomputed independently from the
   durable per-root artifacts.
3. **No duplicate substitution** and **no verse_ref substitution**: verified per
   root (every researched ref is a 4-field word_ref; set size == list size).
4. **One unreconciled confirmed occurrence blocks universal presence** (unchanged):
   e.g. byE, swE, $kw retain a resistant occurrence → not universal; kwn's
   PARTIALLY_SUPPORTED adversarial verdict blocks universal despite full coverage.
5. **Research ≠ canonicalization**: all 48 `canonical_authorization = PENDING`;
   strong research results (e.g. qwl STRONG, universal, verification PASSED) remain
   non-canonical.

## Durable state
- Ledger: `artifacts/semantic-campaign/CAMPAIGN_RESEARCH_LEDGER.json` (48 roots,
  lineage preserved through the coverage requalification).
- Per-root artifacts: `artifacts/semantic-campaign/roots/*.json` (48; each carries
  candidate, discovery judgment, adversarial verdict, `coverage_validation`
  (exact-set), full `occurrence_dispositions`, resistant deep-analysis, methodology
  + corpus + morphology-source revisions, research fields).
- `CampaignState` row `root-research-campaign` (runtime DB; rebuild via `bootstrap`).
- Resume: `artifacts/semantic-campaign/RESUME.md`.

## Blockers
None. The prior session-limit blocker is cleared. No methodological or data blocker.

## Stop condition (honored)
Stopped immediately after Window 02 closure + V2 checkpoint evidence persisted. No
new roots started. Next action (a future window): `python tools/campaign.py select`
→ prep → discovery → persist → prep-coverage → coverage → persist-coverage for
batch 05, continuing toward the full 1,642-root universe.
