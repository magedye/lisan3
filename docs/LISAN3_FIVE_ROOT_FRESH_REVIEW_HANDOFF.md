# Fresh Independent Semantic Review — Exact Handoff Prompt (Stage B)

Run the block below in a **fresh Sol xhigh context** that has performed neither the production nor the
runtime review. Do not collapse producer and reviewer into one context.

---

You are a fresh, independent semantic reviewer for the Lisan governed runtime at
`D:\APP\tafseer\lisanapp3`. Expected `main`/branch HEAD context: producer branch
`five-root-governed-requalification` off `main@d780476e4a3b119ae993588f20333f2ce5fe9246`.

## Mission

Independently review five DB-native, non-canonical Research Judgments (Quran-internal ROOT_CONCEPT
claims) that a producer froze in the authoritative runtime `lisanapp.db`. Roots: ع ص و (ESw),
د ن و (dnw), ف ل ح (flH), ف و ه (fwh), غ ل م (glm).

## Critical independence rule

Until you have recorded your verdict for a given root, DO NOT read that root's Batch 07 artifact
(`artifacts/semantic-campaign/roots/{E_53_w,dnw,fl_48_,fwh,glm}.json`), any Batch 07 report section,
its historical independent verdict, or the historical owner `VERIFY_AT_SCOPE` decisions. Do NOT use
external lexica / dictionaries / tafsir / translation / web / model-prior glosses as semantic
authority. Evidence = the Quranic occurrences only.

## Inputs (read these; they are Quran-internal or governance state)

- `docs/LISAN3_FIVE_ROOT_FRESH_REVIEW_INDEX.md` (claim IDs, evidence pointers, producer flags)
- `docs/evidence/requalification/five_root_produced_claims.json` (full produced claim content)
- `docs/evidence/requalification/five_root_governed_state.json` (runs, isolation, completeness, hashes)
- `docs/evidence/requalification/five_root_overclaim_sweep.json` (sweeps + 8 research questions)
- Occurrence evidence: rebuild each packet from `lisanapp.db` `structural_tokens` (CONFIRMED,
  snapshot `snap_tanzil_1_1_ac0724796cbb`) joined to Tanzil verse text — NOT from Batch 07.
- Live inspection: `GET /judgments/{claim_id}`, `GET /runs/{run_id}/workspace`,
  `GET /judgments/{claim_id}/provenance`, `GET /runs/{run_id}/manifest`.

## For each claim, independently re-derive and check

Every occurrence; claim scope + scope_kind; evidence relevance; counterevidence; hard/unresolved
cases; semantic boundary; strongest competitor + counterexample; falsification; host-derived
completeness; source isolation (ESTABLISHED + CLEAN + attestation lineage: input_manifest,
attesting_actor, attested_at, audit_ref); revision lineage; result strength. Re-run the eight
required research questions yourself; do not defer to the producer's answers.

Give special scrutiny to: `fwh` (asserted UNIVERSAL with 6 recorded counterevidence occurrences);
`glm` (producer orchestrator had incidental prior exposure to the historical conclusion — verify
independence from first principles); `dnw` (133 occurrences, REPRESENTATIVE/MODERATE, sampling basis).

## Verdict per claim (exactly one)

`VERIFIED_AT_SCOPE` · `VERIFIED_NARROWER_SCOPE` · `NOT_VERIFIED` · `UNRESOLVED` ·
`CORRECTIVE_RESEARCH_REQUIRED`. Bind each verdict to the exact `claim_id` and `revision_id`.

## Hard limits

- Do NOT create `VerificationRecord`s, even for a VERIFIED verdict (that governed transition is a
  later human/independent step). Do NOT canonicalize. Do NOT set `canonical_state = ACCEPTED`.
- Do NOT edit or annotate any Batch 07 JSON.
- Do NOT start Batch 08 (`BATCH_08_NOT_AUTHORIZED`).

## Only after all five verdicts are recorded — Phase 12/13

Then, and only then, open the Batch 07 claims and classify each root's old-vs-new relationship as
one of: `INDEPENDENT_CONVERGENCE`, `PARTIAL_CONVERGENCE`, `MATERIAL_DIVERGENCE`, `NEW_CLAIM_NARROWER`,
`NEW_CLAIM_BROADER`, `HISTORICAL_CLAIM_NOT_REPRODUCED`. Do NOT change the new claim to maximize
historical agreement. Finally, prepare an owner-decision package per root (root, claim_id,
revision_id, exact new claim, scope, evidence, counterevidence, falsification, your verdict, Batch 07
comparison) and STOP. The owner decides on the exact new revision; historical `VERIFY_AT_SCOPE`
decisions do NOT transfer. Canonicalization, if any, occurs only through `CanonicalizationPolicy`.
