# LISAN3 — Large-Scale Root Research: Execution Window Report

**verdict**: `LARGE_SCALE_ROOT_RESEARCH_CONTINUED_AUTONOMOUSLY`
(the qualified Root Universe is NOT yet processed to its technical limit — the
execution window terminated on an external runtime blocker, per owner correction §16)
**branch**: `pre-analysis-foundation` · **candidate SHA**: `42c2e2a`
**date**: 2026-09-08

This window implemented the owner's integrity correction (deterministic exact-set,
word_ref-level coverage) and continued the campaign until the runtime window ended.

## 1. Total Root Universe
**1,642** roots (49,968 confirmed root-bearing occurrences; QAC v0.4 over Tanzil 1.1).

## 2. Prior processed count
8 (calibration batch 01 — representative-sample era, since superseded by full coverage).

## 3. Newly processed this window
48 roots received a durable research artifact (batches 02+03+04).

## 4. Total processed
**48 / 1,642** roots have a durable research judgment. **1,594 remaining.**

## 5. Result strength (ledger; provisional strengths marked where coverage pending)
STRONG 9 · MODERATE 4 · WEAK 30 · UNRESOLVED 5.
Only the 8 exact-set-validated roots (batch 02) carry *final* strengths; the other
40 strengths are provisional pending coverage/verification (see §6).

## 6. Exact-set research-complete count
**8** roots passed deterministic word_ref-level exact-set coverage validation
(batch 02): ktb, slm, Hkm, Elm, Amn, kfr, SbH, byn.
- Universal presence holds (research MODERATE, verification PASSED): **ktb (319/319), Hkm (210/210)**.
- Preferred but not universal (a confirmed occurrence resists → WEAK): Amn (879/879, 1 resistant), kfr (525/525, 1 resistant), byn (523/523).
- UNRESOLVED: slm (140/140), Elm (854/854, 76 resistant), SbH (45/45, 21 resistant).
The other **40** roots (batch 03: 16; batch 04: 24) are `PENDING_COVERAGE_EVIDENCE`.

## 7. Canonicalization-pending count
**48** — every processed root is `canonical_authorization: PENDING`. No canonical
authorization was produced or fabricated (research ≠ canonical is preserved).

## 8. Genuine blockers
- **Runtime/session limit (external)** — mid-window the model session limit was
  reached ("resets 12:10pm Asia/Aden"), failing 20 batch-02, 29 batch-03, and all
  24 batch-04 verification agents. This is a terminating execution window, not a
  methodological defect. It is fully recoverable after reset via the resume command.
- No systemic methodological blocker. No data blocker (morphology admitted).

## 9. Methodology revisions
0 (invariants held). The correction added coverage *evidence*, not a new authority axis.

## 10. Regression tests
8 new exact-set coverage tests (`tests/test_campaign_coverage.py`), all green:
exact-once packet, missing blocks COMPLETE, duplicate cannot substitute, resistant
blocks universal presence, research/canon independence, resume preserves exact
sets, idempotent persist, reprocessing preserves lineage. Prior suites remain green.

## 11. External hypotheses tested
0 this window (the calibration/expansion focused on blind internal discovery +
coverage). The unified external-hypothesis register is built and ready; Jabal-style
tests run after a root's internal result is frozen.

## 12. Cross-root findings
- **Exact-set coverage is materially stricter than model-claimed coverage.** Amn
  reported 879/879 "consistent" in discovery+adversarial verify, yet word_ref-level
  mapping surfaced 1 resistant occurrence → Amn correctly dropped STRONG→WEAK. This
  validates the owner's core correction.
- Higher-frequency abstract roots (Elm "know" 854, SbH 45) resist single-unifier
  closure (76 / 21 resistant); concrete-anchored roots (ktb, Hkm) reach universal
  presence. A recurring pattern: metaphor/decree clusters are the hardest cases.
- `Hrr` surfaced as a probable genuine dual-origin root (heat vs. manumission) —
  correctly REFUTED rather than force-unified.

## 13. Exact remaining queue count
**1,594** roots unprocessed + 40 processed-but-`PENDING_COVERAGE_EVIDENCE` needing
coverage/verification completion (batch 03 coverage, batch 04 verification+coverage).

## 14. Candidate SHA
`42c2e2a` (branch `pre-analysis-foundation`). Prior lineage: 974d2d6 (runner+batch02),
d53584f (coverage integrity), 42c2e2a (batch02 exact-set + batches 03/04 state).

## 15. Deterministic resume command
No conversation history required. See `artifacts/semantic-campaign/RESUME.md`.
Summary:
```
# 0. ensure the local QAC artifact is present (acquire-per-install, sha a1d12923...)
python tools/campaign.py bootstrap
# 1. finish interrupted coverage/verification (batches 03, 04)
#    (re-run the coverage / discovery workflows for PENDING roots, then persist-coverage)
# 2. continue expansion
python tools/campaign.py select --n 40   # next diverse batch
#    prep -> discovery workflow -> persist -> prep-coverage -> coverage workflow -> persist-coverage
python tools/campaign.py status          # research vs canonicalization progress
```

## Durable state (all committed or reproducible)
- Ledger: `artifacts/semantic-campaign/CAMPAIGN_RESEARCH_LEDGER.json` (48 roots).
- Per-root artifacts (exact-set validated): `artifacts/semantic-campaign/roots/*.json` (8).
- `CampaignState` row `root-research-campaign` (runtime DB; rebuildable via bootstrap).
- Runner: `tools/campaign.py`; coverage service: `backend/domain/services/research_coverage.py`.
