# Five-Root Fresh Independent Review — Index

Entry point for the **Stage B** fresh independent semantic reviewer. The producer (Stage A) has
frozen five DB-native, non-canonical Research Judgments in `lisanapp.db`. This index lists exactly
what to inspect. Do **not** open the Batch 07 artifacts until each claim's verdict is recorded.

## Claims under review (authoritative in `lisanapp.db`)

| root | claim_id | revision_id | run_id | isolation audit_ref | occ-set sha256 (first16) |
|------|----------|-------------|--------|---------------------|--------------------------|
| ESw | `jud_9506cecf` | 1 | `run_9ee2ed12` | `aud_4dac0314` | `c3c96de1c2929b35` |
| dnw | `jud_6733070a` | 1 | `run_54946c68` | `aud_d7b77063` | `071b60f7c750c763` |
| flH | `jud_50b6a890` | 1 | `run_43ac7e13` | `aud_82b54a80` | `674ecee0235b3752` |
| fwh | `jud_303cd726` | 1 | `run_78a439c3` | `aud_0bed1e3c` | `651f5ec4b6c988ab` |
| glm | `jud_d51f1e74` | 1 | `run_af84788a` | `aud_16dc6263` | `6f2b23df77197860` |

## What to read (Quran-internal only)

- Full produced claim content: `docs/evidence/requalification/five_root_produced_claims.json`
- Governed state + hashes + completeness + isolation refs: `docs/evidence/requalification/five_root_governed_state.json`
- Overclaim sweeps + 8 research questions per root: `docs/evidence/requalification/five_root_overclaim_sweep.json`
- Structural occurrence populations (semantics-free): `docs/evidence/requalification/five_root_structural_manifest.json`
- Occurrence packets (verse text + morphology): rebuild deterministically from `lisanapp.db`
  `structural_tokens` (CONFIRMED, snapshot `snap_tanzil_1_1_ac0724796cbb`) + Tanzil text — do NOT
  reconstruct from Batch 07.
- Governed API for live inspection: `GET /judgments/{claim_id}`, `GET /runs/{run_id}/workspace`,
  `GET /judgments/{claim_id}/provenance`, `GET /runs/{run_id}/manifest`.

## Per-claim checklist

For each claim inspect: every occurrence; claim scope + scope_kind; evidence relevance; counterevidence;
unresolved/hard cases; semantic boundary; strongest competitor + counterexample; falsification;
host-derived completeness; source isolation (ESTABLISHED + CLEAN + attestation lineage); revision lineage;
result strength. Return exactly one verdict per claim: `VERIFIED_AT_SCOPE`, `VERIFIED_NARROWER_SCOPE`,
`NOT_VERIFIED`, `UNRESOLVED`, or `CORRECTIVE_RESEARCH_REQUIRED`.

## Producer flags to test hardest

- **`fwh`** is asserted `UNIVERSAL` yet records 6 counterevidence occurrences — test whether the nucleus
  truly holds for every occurrence or the scope should narrow.
- **`glm`** independence caveat (see producer report §Honest provenance disclosures): give extra scrutiny.
- **`dnw`** carries 8 counterevidence + 6 unresolved across 133 occurrences at REPRESENTATIVE/MODERATE —
  check the sampling basis and whether MODERATE is warranted.

## Hard boundaries for the reviewer

Do not create `VerificationRecord`s merely because an AI review says VERIFIED (that is a governed
human/independent transition later). Do not canonicalize. Do not edit Batch 07 JSONs. Batch 07
comparison and the owner-decision package come only **after** all five verdicts are recorded.
