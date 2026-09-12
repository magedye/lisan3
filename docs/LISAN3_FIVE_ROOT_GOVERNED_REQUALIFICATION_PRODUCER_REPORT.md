# Five-Root Governed Requalification — Producer Report (Stage A)

**Status:** `FIVE_ROOT_GOVERNED_REQUALIFICATION_READY_FOR_FRESH_INDEPENDENT_REVIEW`
**Date:** 2026-09-13 · **Qualification runtime SHA:** `d780476e4a3b119ae993588f20333f2ce5fe9246`
**Branch:** `five-root-governed-requalification`

This report documents DB-native governed state persisted into the authoritative runtime
(`lisanapp.db`). **The database is the authority; this file only documents it.** It contains
NO comparison with the historical Batch 07 claims (that is deferred to Stage B, after a fresh
independent semantic review). The five Batch 07 root JSON artifacts were **not read** while the
new claims were produced, and remain **byte-identical**.

## Nature and limits of these claims

These are **AI-produced, non-canonical Research Judgments** (`canonical_state = NOT_CANONICAL`)
authorized by `SIMPLIFIED_AI_AUTHORITY_AND_GOVERNANCE_CONTRACT.md` (AI MAY induce patterns and
prefer a root concept as a Research Judgment) and `skills/lisan-semantic-extraction/SKILL.md`.
They are **not** project truth, **not** verified, **not** accepted. Final authority rests with a
fresh independent review and an explicit owner canonicalization decision bound to the exact
`claim_id`/`revision_id` below.

**Honest provenance disclosures (for the fresh reviewer):**
1. The semantic induction was produced by **clean-room subagents** (2 independent analysts + 1
   adversary → aggregator with a mandatory overclaim gate), each restricted to the Quran-internal
   occurrence packet (Tanzil verse text + admitted QAC morphology) and explicitly forbidden from
   reading Batch 07, any `docs/**` semantic file, external lexica/tafsir/translation, or the web.
2. An LLM cannot perfectly exclude absorbed lexical knowledge; the governance guardrails
   (evidence-linkage, named anti-contamination diagnostics, adversarial gate, independent review,
   owner decision) exist precisely to bound that residual. Treat these claims as hypotheses to be
   independently re-derived, not as settled results.
3. **`glm` caveat:** the orchestration context that assembled these results had, in an earlier
   runtime-review task, incidental exposure to `glm`'s historical Batch 07 conclusion. The `glm`
   analysis itself was produced clean-room, but the reviewer should give `glm` extra scrutiny for
   independence.

## Governed claim identity table

| root | claim_id | rev | state | strength | scope | scope_kind | obs (exact-set) | sup/ctr | falsification | canonical |
|------|----------|-----|-------|----------|-------|------------|-----------------|---------|---------------|-----------|
| ESw ع ص و | `jud_9506cecf` | 1 | PREFERRED | STRONG | REPRESENTATIVE | LEXICALIZED_CLASS | 12/12 ✓ | 12/0 | PASSED | NOT_CANONICAL |
| dnw د ن و | `jud_6733070a` | 1 | PREFERRED | MODERATE | REPRESENTATIVE | ROOT_GENERALIZATION | 133/133 ✓ | 16/8 | PASSED | NOT_CANONICAL |
| flH ف ل ح | `jud_50b6a890` | 1 | PREFERRED | MODERATE | REPRESENTATIVE | DERIVATIONAL_FAMILY | 40/40 ✓ | 38/3 | PASSED | NOT_CANONICAL |
| fwh ف و ه | `jud_303cd726` | 1 | PREFERRED | STRONG | UNIVERSAL | LEXICALIZED_CLASS | 13/13 ✓ | 7/6 | PASSED | NOT_CANONICAL |
| glm غ ل م | `jud_d51f1e74` | 1 | PREFERRED | MODERATE | REPRESENTATIVE | LEXICALIZED_CLASS | 13/13 ✓ | 5/5 | PASSED | NOT_CANONICAL |

Produced root_concept (one line each; full content in `docs/evidence/requalification/five_root_produced_claims.json`):

- **ESw** — a rigid, elongated, hand-held rod/staff (concrete noun عَصَا / عِصِيّ).
- **dnw** — NEARNESS / PROXIMITY (spatial near/close/low/within-reach), elative projecting to lower/lesser/fewer.
- **flH** — attain the desired favorable outcome; succeed/prosper/thrive (Form-IV attainment predicate).
- **fwh** — mouth (the bodily oral aperture).
- **glm** — young male human (boy/youth): [+male] + [+young/pre-full-adult], attested as the noun ghulām.

## Overclaim gate outcome

The mandatory adversarial overclaim sweep **downgraded 4 of 5** proposals (only `fwh` retained its
initial calibration). No claim was inflated to match any prior result. `dnw`, `flH`, `glm` carry
recorded counterevidence and/or unresolved occurrences; `fwh` is asserted UNIVERSAL yet carries 6
counterevidence occurrences — a tension the fresh reviewer should specifically test. Full sweeps and
the eight required research questions per root: `docs/evidence/requalification/five_root_overclaim_sweep.json`.

## Governed runtime state (authoritative DB `lisanapp.db`)

- **ResearchRuns:** 5 (one per root), each host-bound to snapshot `snap_tanzil_1_1_ac0724796cbb`
  and methodology `LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4`.
- **Isolation:** 5 `ESTABLISHED` + `CLEAN` states via the fail-closed establishment path, each with
  an immutable attestation audit_ref (`aud_4dac0314`, `aud_d7b77063`, `aud_82b54a80`, `aud_0bed1e3c`,
  `aud_16dc6263`). No run proceeded on a mere row.
- **Observations:** 211 DB-native `ObservationArtifact`s, exact-set coverage of every confirmed
  word-level occurrence (12 + 133 + 40 + 13 + 13), each `token:<word_ref>` scoped to the snapshot.
- **Completeness:** host-derived (`sufficient_for_claim = true` for every claim), never imported.
- **SemanticClaims:** 5, all `NOT_CANONICAL`, `verification_state = NOT_REQUIRED`, revision 1.
- **VerificationRecords:** 0. **ACCEPTED:** 0.

Per-root run/isolation/observation/completeness/hashes: `docs/evidence/requalification/five_root_governed_state.json`.
Structural occurrence populations (semantics-free): `docs/evidence/requalification/five_root_structural_manifest.json`.

## Verification performed by the producer (necessary, not sufficient)

- Qualification tests `tests/test_canonical_runtime_qualification.py`: **24 passed**.
- Full non-e2e suite `pytest tests --ignore=tests/e2e`: **251 passed** (exit 0).
- Independent fail-closed negative-control harness: **32/32** (missing/wrong-root/wrong-snapshot
  tokens rejected; contamination blocks; NOT_ESTABLISHED blocks; incomplete UNIVERSAL insufficient;
  unsupported evidence rejected; stale methodology fails; non-production corpus fails; unauthorized
  actor cannot canonicalize — the producer cannot self-create owner acceptance).
- Batch 07 root JSONs blob-identical to `main@d780476`; authoritative `lisanapp.db` not committed.

## Boundaries held

No canonicalization; no VerificationRecords; no ACCEPTED transition; no edit/annotation of any Batch
07 semantic JSON; no historical comparison in this report; `BATCH_08_NOT_AUTHORIZED`.

## Next

Stage B: a **fresh** Sol xhigh independent semantic reviewer (blind to Batch 07 initially) inspects
each claim per `docs/LISAN3_FIVE_ROOT_FRESH_REVIEW_HANDOFF.md`, returns a per-claim verdict, then
(only afterward) opens Batch 07 for comparison, then prepares an owner-decision package bound to the
exact `claim_id`/`revision_id`. Owner decisions on the historical Batch 07 claims do **not** transfer.
