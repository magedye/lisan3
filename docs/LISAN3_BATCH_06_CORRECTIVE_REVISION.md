# Batch 06 Corrective Revision

**Revision:** `BATCH_06_CORRECTIVE_REVISION_2026_09_11`
**Starting candidate:** `5c95def0012d4cb938973e37aecfce83b5aeb3d5`
**Branch:** `semantic-campaign-batch06`
**Scope:** the frozen Batch 06 population only (40 roots / 3,098 occurrences)

## Purpose and boundary

This is an owner-authorized corrective revision responding only to the blocking
findings in the fresh read-only semantic-results review. It preserves that
review as historical evidence; it does not claim a new independent review,
canonicalization, merge, push, release, purity campaign, or Batch 07 start.

The evidence policy remains `QURAN_INTERNAL_ONLY`. No dictionary, tafsir,
translation, web source, embedding, or inherited lexical assumption was used
as Quranic primary evidence. The source bindings remain the admitted Tanzil
snapshot `snap_tanzil_1_1_ac0724796cbb`, QAC SHA-256
`a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46`, and
semantic runtime SHA-256
`01784170cac4e715c1477cb6a04a2c34b21c4bdb91705aa1eb6b2a896efcedbd`.

## Corrected judgments

| Root | Final classification | Corrective boundary |
|---|---|---|
| `kvr` | `PRODUCTIVE_ABUNDANCE_CLASSES_WITH_OPAQUE_KAWTHAR_SEAM` | `108:1:3:2` is RESISTANT; no universal abundance claim includes it. |
| `mvl` | `QUALIFIED_DERIVATIONAL_FAMILY_PARTITION` | Comparison/equivalence, parable, representation, exemplary, `al-muthla`, `al-mathulat`, and Form V remain partitioned; `19:17:8:2` is `VALID_WITH_QUALIFICATION` locally only. |
| `qlb` | `HEART_AND_TURNING_CLASSES_UNRESOLVED_AT_ROOT_LEVEL` | Heart and turning classes are not forced into an orienting-core explanation. |
| `swA` | `EXPOSED_PRIVATE_PARTS_AND_ADVERSE_CLASSES_UNRESOLVED_AT_ROOT_LEVEL` | The seven exact exposed-private-parts records are partitioned from adverse/badness; contextual shame is not a root bridge. |
| `fSl` | `PRODUCTIVE_BOUNDARY_CLASSES_WITH_FAMILY_CLAN_SEAM` | `70:13:1:2` remains RESISTANT. |
| `wlj` | `ENTRY_CLASSES_WITH_INVALID_SOCIAL_INSIDER_RECONCILIATION` | `9:16:20:1` is restored to RESISTANT; its historical reconciliation remains visible with `INVALID_INSUFFICIENT_QURAN_INTERNAL_BRIDGE`. |
| `Sgr` | `MAGNITUDE_AGE_AND_ABASEMENT_CLASSES_UNRESOLVED_AT_ROOT_LEVEL` | Magnitude/age and abasement have no asserted generic-scale bridge. |
| `Ezr` | `REINFORCEMENT_HONOR_HELP_BOUNDARY_UNRESOLVED` | The three occurrences do not distinguish reinforcement, honor, and help uniquely. |
| `Hfw` | `SOLICITUDE_CLAIMED_KNOWLEDGE_AND_EXHAUSTIVE_DEMAND_UNRESOLVED` | No generic close-attention bridge is asserted. |
| `Sbg` | `DIVINE_SIBGHA_AND_CULINARY_SIBGH_UNRESOLVED_AT_ROOT_LEVEL` | Divine sibgha and culinary sibgh remain unbridged; no dye, coloring, or imbuing presupposition is imported. |

The twelve formerly confirmed STRONG roots remain semantically unchanged. The
post-correction strength distribution is **12 STRONG / 8 MODERATE / 9 WEAK /
11 UNRESOLVED**. The 3,098 persisted records remain present, while final
RESISTANT occurrences rise from 562 to 565 because of the three explicitly
restored or newly retained seams (`kvr`, `fSl`, `wlj`).

## Persisted root-judgment contract

Every Batch 06 artifact now contains the exact root-artifact fields:
`contract_type`, `claim_scope`, `claim_scope_kind`, `layer_attribution`,
`root_evidence_refs`, `root_counterevidence_refs`, `hard_cases`,
`rejection_condition`, `falsification_status`, `reopen_conditions`, and
`purity_status`.

`claim_scope` retains its canonical evidentiary values (`UNIVERSAL`,
`REPRESENTATIVE`, `LOCAL`). `claim_scope_kind` separately records whether the
persisted conclusion is a root generalization, derivational family,
lexicalized class, occurrence-level result, or unresolved/class-only result.
This is not an alias: it prevents evidence-coverage extent from being confused
with the semantic kind of a claim.

All direct evidence, counterevidence, and hard-case references resolve to a
persisted `occurrence_dispositions.word_ref`. Every artifact keeps
`purity_status = NOT_EVALUATED`; no purity conclusion is implied.

## Provenance retained

The correction preserves every occurrence record and its original identity,
source metadata, preliminary disposition/note, verifier objection, final
disposition, reconciliation rationale, and reconciliation lineage.

- `mvl` retains the historic preliminary RESISTANT -> final CONSISTENT
  reconciliation for `19:17:8:2`, augmented only with the current local
  outcome `VALID_WITH_QUALIFICATION`.
- `wlj` retains the historic preliminary RESISTANT -> final CONSISTENT attempt
  in lineage, while the current occurrence disposition and final disposition
  are both RESISTANT and the corrective outcome is
  `INVALID_INSUFFICIENT_QURAN_INTERNAL_BRIDGE`.

## Verification record

- V0: frozen branch/starting SHA, corpus bindings, 40-root manifest, and owner
  files were established before the correction.
- V1: every corrected target has a contract, reference, hard-case, and lineage
  check; the replay test protects preliminary/reconciliation provenance.
- V2: the corrected manifest still totals 40 roots and 3,098 exact-set
  occurrences. No Batch 05 corrective artifact is in the Batch 06 root set.
- V3: all 40 root artifacts have zero missing root-judgment fields and zero
  unresolved root-reference links; case-fold-safe filenames and ledger links
  remain required checks.

The corrective runner is
`python -m tools.campaign apply-batch06-corrective --repo-root .`; it only
uses the frozen manifest and
`artifacts/semantic-campaign/BATCH_06_CORRECTIVE_JUDGMENTS.json`.

## Remaining gaps and handoff

The semantic gaps are intentional and explicit: the ten corrected roots above
require a fresh independent Quran-internal review before any synthesis or
canonical step. No universal claim may be restored unless the exact listed
bridge is demonstrated and the persisted judgment is revised under authority.

**Handoff state:** `BATCH_06_CORRECTIVE_REVISION_READY_FOR_FRESH_REVIEW`.
The next action is a fresh, independent, read-only review of the exact
corrective commit after it is created. Do not merge, push, start Batch 07, or
canonicalize under this revision.
