# LISAN3 Batch 06 — Wave 1 Semantic Checkpoint

Date: 2026-09-11

Branch: `semantic-campaign-batch06`

Starting main checkpoint: `6f895bf0754190a423512b7478ced5bf7bd4a266`

Population authority: `artifacts/semantic-campaign/BATCH_06_MANIFEST.json`

## Verdict

`WAVE_1_COMPLETE_WITH_EXACT_COVERAGE_AND_PRESERVED_RESISTANCE`

This is Quran-internal research evidence, not canonical knowledge, publication,
owner acceptance, or independent review. The five Batch 05 corrective roots
`Anf`, `Erw`, `rbb`, `ETw`, and `fqr` are outside this batch and unchanged.

## Executed scope and provenance

- Frozen population: 20 roots / 1,780 confirmed occurrences.
- Quran text authority: admitted Tanzil verse text in snapshot
  `snap_tanzil_1_1_ac0724796cbb`.
- Structural authority: hash-bound QAC Morphology v0.4, extraction
  `qac-0.4-import-v1`.
- Methodology: `LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4` and the
  repository cumulative-run protocol.
- Occurrence identity: exact `word_ref`; no verse-level substitution.
- Surface policy: QAC Buckwalter segment surface is preserved as structural
  evidence. `surface_form_arabic` remains
  `NOT_AVAILABLE_CANONICALLY` because no reviewed segment-level orthographic
  alignment profile exists; no Arabic token surface was guessed.
- Coverage expansion: every semantic class is explicitly selected and
  count-pinned. There is no default or majority label.

## Root outcomes

| Root Arabic | Buckwalter | Occ. | Outcome | Universal | Resistant | Candidate nucleus / boundary |
|---|---:|---:|---|---|---:|---|
| ش ي ا | `$yA` | 519 | UNRESOLVED | no | 519 | Thing/entity and willing are clear families; no distinctive internal bridge. |
| ا ر ض | `ArD` | 461 | MODERATE | yes | 0 | Terrestrial ground or earth-domain; scale is contextual. |
| م ث ل | `mvl` | 169 | MODERATE | yes | 0 | Correspondence through comparable configuration; Form V seam reconciled. |
| ق ل ب | `qlb` | 168 | MODERATE | yes | 0 | Reorientation of face/state; heart as the inner orienting center. |
| س و ا | `swA` | 167 | MODERATE | yes | 0 | Adverse or worsening quality; not restricted to moral evil. |
| ي س ر | `ysr` | 44 | WEAK | no | 3 | Low obstruction/readiness; maysir's proposed easy-gain bridge is unproven. |
| ف ص ل | `fSl` | 43 | MODERATE | yes | 0 | Boundary-making that separates, details, or decisively settles. |
| ج و ب | `jwb` | 43 | WEAK | no | 1 | Directed answering response; 89:9 rock-hewing remains outside it. |
| ت ر ك | `trk` | 43 | STRONG | yes | 0 | Cessation of retention/accompaniment: leave, spare, or leave behind. |
| ص د د | `Sdd` | 42 | WEAK | no | 1 | Obstruction/turning away; the 14:16 sadid fluid remains resistant. |
| و ل ج | `wlj` | 14 | MODERATE | yes | 0 | Passage into an interior; walija inner-circle seam reconciled. |
| ش ه و | `$hw` | 13 | STRONG | yes | 0 | Appetite drawing the self toward a desired object or experience. |
| ض ي ق | `Dyq` | 13 | STRONG | yes | 0 | Reduced room or capacity, physical, circumstantial, or inward. |
| ح ل ف | `Hlf` | 13 | STRONG | yes | 0 | Binding an assertion by an invoked oath; truth value is contextual. |
| ص غ ر | `Sgr` | 13 | MODERATE | yes | 0 | Lowness on a scale of magnitude or standing. |
| ع ز ر | `Ezr` | 3 | MODERATE | yes | 0 | Active reinforcement/upholding of a messenger; sparse single-form evidence. |
| ح د ق | `Hdq` | 3 | MODERATE | yes | 0 | Observed cultivated garden-space; deeper distinctiveness not inferred. |
| ح ل ق | `Hlq` | 3 | UNRESOLVED | no | 3 | Shaving and throat are clear; a circular-boundary bridge is not internal evidence. |
| ح و ج | `Hwj` | 3 | MODERATE | yes | 0 | Felt requirement or sought purpose addressing a practical/inward lack. |
| ص ب غ | `Sbg` | 3 | WEAK | no | 1 | Imbuing/characterizing treatment; culinary sibgh at 23:20 remains resistant. |

Distribution: **4 STRONG / 10 MODERATE / 4 WEAK / 2 UNRESOLVED**.

## Contested and reconciliation provenance

There are 528 final RESISTANT occurrences. The large count is not a completion
failure: 519 belong to `$yA`, where both full families remain deliberately
unified only at the root ID, not by a claimed semantic core. Other final seams
are `ysr` (3), `jwb` (1), `Sdd` (1), `Hlq` (3), and `Sbg` (1).

Two occurrences changed from preliminary RESISTANT to final CONSISTENT after
focused analysis, without overwriting their original state:

- `mvl` `19:17:8:2`: Form V plus the explicit human-form complement supports
  embodied correspondence.
- `wlj` `9:16:20:1`: the participant construction identifies privileged
  admission to an inner circle, a bounded extension of entry.

Each final record retains preliminary disposition, preliminary note, final
disposition, reconciliation rationale, and `deep_analysis = true`.

## Provisional cross-root relations

- `qlb` reorientation and `Dyq` constriction can co-occur in inward-state
  descriptions, but orientation and available capacity remain distinct.
- `Sgr` supplies scalar lowness, while `Dyq` supplies lack of room; neither is
  reduced to generic weakness.
- `wlj` profiles passage into an interior, whereas `jwb` profiles response to an
  address. Their boundary-crossing imagery is not a shared root nucleus.
- `$hw` appetitive pull differs from `Hwj` need/purpose: desire may exist without
  a lack-linked requirement, and need may be practical rather than appetitive.

These are research candidates only; no cross-root canonical relation is created.

## Verification evidence

- Manifest/live population: exact 20 roots / 1,780 occurrences for Wave 1.
- Persistent artifacts: 20/20 present with four-part identity and expected safe
  filename.
- Exact-set coverage: 1,780/1,780, with zero missing, unexpected, or duplicate
  `word_ref` values.
- Evidence contract: zero persisted occurrence records missing identity,
  `verse_ref`, QAC surface/morphology, candidate interpretation, canonical
  verse support, or final disposition.
- Ledger: 108 total roots; all 108 coverage-complete; 1,534 remain.
- Focused campaign tests and Ruff are required immediately before the Wave 1
  commit; their exact result is recorded in `PROJECT_STATE.md` at checkpoint.

## Limitations and boundaries

Purity dimensions are `NOT_EVALUATED` in this wave: no qualified comparison
corpora were invoked, and research purity is not a gate or lock. The campaign
does not authorize canonicalization, publication, external lexical evidence,
Batch 05 correction, Hybrid Retrieval, push, merge, tag, release, or branch
deletion.
