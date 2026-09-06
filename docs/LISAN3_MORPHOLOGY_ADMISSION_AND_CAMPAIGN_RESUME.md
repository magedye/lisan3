# LISAN3 — Morphology Admission & Request 02 Resume Report

**source verdict**: `QUALIFIED_QURANIC_MORPHOLOGY_ADMITTED`
**campaign verdict**: `LARGE_SCALE_SEMANTIC_CAMPAIGN_EXECUTED_TO_CURRENT_QUALIFIED_LIMIT`
**branch**: `pre-analysis-foundation` · **base of this task**: `d5b24e3` · **candidate**: see final commit
**artifacts**: `docs/canonical/ADMISSION_QAC.md`, `artifacts/semantic-campaign/CALIBRATION_BATCH_01.json`, `artifacts/semantic-campaign/CAMPAIGN_STATUS.json`

Answers the owner's 18-point final-output request.

1. **Source admitted** — Quranic Arabic Corpus (QAC) Morphology v0.4, as a LOCAL, hash-bound, acquire-per-install immutable structural source (raw GPL bytes not committed; importer fail-closes on SHA drift).
2. **Exact identity/version/checksum** — `quranic-corpus-morphology-0.4.txt`, 6,309,503 bytes, SHA-256 `a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46`, © 2011 Kais Dukes. Bytes acquired from an immutable-commit-pinned mirror and verified byte-identical to the documented official artifact (Stage-A evidence).
3. **License/terms disposition** — Embedded terms read verbatim: QAC = GNU GPL (verbatim distribution permitted; no changes; source indication + link + notice retention required); embedded Tanzil 1.0.2 = CC BY-ND 3.0. To avoid an unresolved redistribution/copyleft question and not fabricate legal clearance, the raw artifact is **not redistributed via the repo**; each install acquires its own byte-identical copy. Derived annotations carry the required attribution + lineage.
4. **Canonical mapping** — Tanzil 1.1 remains the sole text/verse authority. All 6,236 QAC verse references match Tanzil exactly (0 unmatched); 112 opening-basmala offsets + 4 documented residual cases (`2:181`, `8:6`, `13:37`, `37:130`) recorded, not silently resolved. QAC `FORM` never overwrites Tanzil text.
5. **Total morphology records** — 128,219 segments (PREFIX 28,670 / STEM 77,915 / SUFFIX 21,634).
6. **Total roots discovered** — **1,642** distinct roots (`ROOT` on 49,968 segments).
7. **Eligible roots** — 1,642 (all roots with confirmed occurrences are research-eligible).
8. **Disputed/ineligible roots** — 0 disputed at admission (QAC is internally consistent: 0 malformed rows, 0 duplicate locations). Cross-source disagreement handling exists (DISPUTED/UNRESOLVED attribution status) but no second source was cross-run this session.
9. **Cross-source disagreements** — none computed (single qualified source admitted; a Birzeit/SinaLab cross-check remains available as a future STRUCTURAL_VALIDATION_SIGNAL). QAC identity is independently established by exact SHA-match to the official artifact.
10. **Root Universe artifact** — `RootUniverseService.derive` over `structural_tokens`; 1,642 roots with occurrence counts, form inventory, distribution, and priority dimensions. Deterministic and reproducible across sessions. (Runtime store; not committed as raw GPL-derived bulk data.)
11. **Tests** — `tests/test_qac_morphology.py` (parse logic on an authored fixture always; full-corpus integration when the local artifact is present: 1,642 roots, 49,968 tokens, reconciliation, reproducibility). Full suite: **184 passed** (non-e2e).
12. **Campaign resume point** — Resumed from `PHASE_1_HANDOFF.json`; `CampaignState 'calibration-batch-01'` COMPLETE. Next batch selects unprocessed roots from the 1,642-root universe.
13. **Calibration roots processed** — 8 (deterministic diverse portfolio): `ktb, slm, Hkm, Elm, Amn, kfr, SbH, byn` (spanning frequency, form-diversity, the Jabal-hypothesis root `slm`, and a rarer root).
14. **Total roots processed after resume** — 8 (calibration batch 01).
15. **Accepted/strong/moderate/unresolved** — **accepted = 0.** All 8 produced a PREFERRED internal candidate (STRONG×3, MODERATE×5) that adversarial verification reduced to **PARTIALLY_SUPPORTED (8/8)**. None reached UNIVERSAL coverage or independent verification, so none is canonical. This is the methodology correctly refusing to over-unify — honest calibration, not generated answers.
16. **Methodology findings/revisions** — 0 methodology revisions (invariants held). Findings captured: (a) representative sampling is insufficient for a universal claim — apparent 30/30 consistency (ktb) still failed specific occurrences (62:2 oral teaching, 35:29 recitation) under adversarial check; (b) form/derivation layer separation is the dominant difficulty (Amn 26 fails; SbH consistent only 12/30); (c) distinctiveness must be tested against nearest roots (kfr flagged non-distinct); (d) adversarial verification is essential — it changed every verdict.
17. **Remaining genuine blockers** — none are data blockers. Acceptance to canonical requires (i) full-corpus (all-occurrence) universal-presence testing per root, and (ii) independent HUMAN verification — neither achievable to standard in a single autonomous run. Expansion across 1,642 roots is an ongoing batched effort (Request 02 §12–§13).
18. **Final candidate SHA** — recorded at the campaign-artifacts commit on `pre-analysis-foundation` (see git log).

## Integrity note
The campaign was run for real on real, qualified data (QAC v0.4 + Tanzil 1.1), with each root's induction grounded only in its actual Quranic occurrences (not model memory), and every judgment independently attacked by an adversarial verifier. The honest outcome — 0 accepted, 8 partially-supported, with concrete counter-occurrences and findings — is the methodology working as designed: it is conservative, falsification-driven, and refuses acceptance without universal coverage and human verification.
