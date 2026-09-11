# Batch 06 Final Contract Remediation

**Revision:** `BATCH_06_FINAL_CONTRACT_REMEDIATION_2026_09_11`
**Starting candidate:** `8ef76292978c61c9283648d5f578d928e39e7320`
**Branch:** `semantic-campaign-batch06`
**Scope:** representation-only correction of the frozen Batch 06 set (40 roots / 3,098 occurrences)

## Boundary and disposition

This checkpoint corrects the two independent-review blockers without rerunning
semantic research. It replaces the inactive aliases `root_evidence_refs` and
`root_counterevidence_refs` with the active runtime fields
`supporting_evidence_refs` and `counterevidence_refs`; the aliases are now
rejected by the Batch 06 validator.

The remediation also replaces generic review controls with root-specific,
resolvable records. Supporting evidence binds every persisted `CONSISTENT`
occurrence for its root. Counterevidence binds every persisted resistant,
adversarial-failure, or retained reconciliation reference. Each hard case,
rejection condition, and reopen condition names the particular root, its
material classes, and its recorded boundary.

No root conclusion, occurrence identity/disposition, resistant occurrence,
lineage record, classification, strength, or outcome was changed. The ten
authorized adversarial records (`kvr`, `mvl`, `qlb`, `swA`, `fSl`, `wlj`,
`Sgr`, `Ezr`, `Hfw`, `Sbg`) now serialize their already-persisted qualified or
unresolved boundaries accurately. A partial or non-distinctive adversarial
record is `NOT_RUN`, never inferred as `PASSED`.

## Canonical controls

The active runtime contract is
`LISAN3_SEMANTIC_RUNTIME_V3_2026_09_06`, as defined by the canonical
implementation reference and semantic-extraction methodology. All 40 artifacts
now carry the canonical evidence fields, a structured `falsification_evidence`
record, and the eight named purity diagnostics. Each unsupported diagnostic is
explicitly `NOT_EVALUATED`, has no fabricated evidence, and is not a blocker.

The replay snapshots and compares these frozen fields before any write:
`research_state`, `result_strength`, `universal_presence_holds`,
`candidate_root_contribution`, `occurrence_dispositions`,
`resistant_occurrences`, and `resistant_deep_analysis` (including the discovery
object, which contains the persisted root conclusion and classifications).

## Verification record

- Canonical active-field errors: **80 before / 0 after** (two missing active
  fields across 40 artifacts).
- Frozen population: **40 roots / 3,098 occurrence identities**.
- Strength distribution: **12 STRONG / 8 MODERATE / 9 WEAK / 11 UNRESOLVED**.
- Final resistant occurrences: **565**; the prior Batch 05 corrective artifacts
  remain outside this change.
- The focused campaign suite passes **38 tests**; it includes canonical field,
  claim-specific control, target adversarial, and frozen-payload checks.

The replay command is:

```powershell
.venv\Scripts\python.exe -m tools.campaign apply-batch06-final-contract --repo-root .
```

It fails closed unless `HEAD` is exactly the starting candidate, the ten-target
set is exact, all 40 artifacts validate, and the frozen payload comparison is
unchanged.

## Handoff

`BATCH_06_FINAL_CONTRACT_REMEDIATION_READY_FOR_FRESH_REVIEW` means only that
this implementation-side remediation is ready for a new independent,
read-only review. It does not establish `INDEPENDENTLY_REVIEWED`,
canonicalization, merge, push, release, acceptance, or authority to begin
Batch 07.
