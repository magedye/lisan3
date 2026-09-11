# Batch 06 Representation Remediation

**Revision:** `BATCH_06_REPRESENTATION_REMEDIATION_2026_09_11`
**Starting candidate:** `5b131676837c674e92723ccc6df02e1fb2fdc676`
**Branch:** `semantic-campaign-batch06`
**Scope:** representation-only correction of persisted judgment controls for the
frozen Batch 06 set (40 roots / 3,098 occurrences).

## Boundary

This remediation does not rerun semantic research or change a root conclusion,
classification, claim scope, occurrence disposition, resistance, adversarial
record, falsification result, evidence reference, or lineage. It replaces only
the three remaining judgment-control representations:

1. positional `hard_cases` on 19 no-counterevidence artifacts;
2. the common rejection-condition invalidation template across all 40 roots;
3. the two common reopen-condition templates across all 40 roots.

The durable authored control source is
`artifacts/semantic-campaign/BATCH_06_REPRESENTATION_REMEDIATION.json`. It
binds every root to its persisted `claim_scope`, `claim_scope_kind`, semantic
boundary, class partition, adversarial record, resistant seam, or structural
limitation. It is not a new semantic run and introduces no external evidence.

## Corrected controls

The former `_root_cluster_evidence_refs` fallback selected the first encountered
occurrence in each class. That behavior is unavailable now: generic
judgment-control generation fails closed and the new replay accepts explicit,
root-authored controls only.

Seventeen of the 19 formerly positional roots now have one specific persisted
hard case with a role and an evidence basis. These include a natural-effect
dispatch (`rsl` 105:3:1:2), territorial inheritance (`ArD` 7:137:7:2),
combat-without-completed-death (`qtl` 2:216:3:2), figurative crop emergence
(`zrE` 48:29:32:2), cosmic refusal (`Aby` 33:72:8:2), and the private-purpose
boundary (`Hwj` 12:68:16:1).

`Eyr` and `Hdq` have `hard_cases: []` with the explicit
`NO_GENUINE_HARD_CASE` representation. Their persisted limitation is a
packet-wide single-form/single-family ceiling, not an individual adversarial
occurrence. Neither root has persisted counterevidence that this representation
would conceal.

Every root now has an individually authored rejection condition answering what
Quran-internal fact invalidates its exact universal, qualified, or unresolved
claim. Every root also has two evidence-bound reopen conditions. The controls
refer to the actual relevant boundary—for example an opaque lexical seam,
derivational partition, resistant occurrence, morphology assignment, or
contextual extension—not merely another named cluster.

## Frozen-state and contract proof

The replay requires `HEAD = 5b131676837c674e92723ccc6df02e1fb2fdc676`, then
snapshots and rechecks all frozen contract, claim, evidence, falsification,
adversarial, occurrence, resistance, lineage, purity, and internal-discovery
fields before writing. The replay completed with:

- canonical contract errors: `0`;
- frozen payload drift: `[]`;
- roots / occurrence identities: `40 / 3,098`;
- strength distribution: `12 STRONG / 8 MODERATE / 9 WEAK / 11 UNRESOLVED`;
- final resistant occurrences: `565`;
- falsification statuses preserved: `17 PASSED / 11 NOT_REQUIRED / 12 NOT_RUN`.

The prior Batch 05 artifacts remain out of scope; no Batch 07 artifact or
research run is introduced.

## Regression controls and verification

`validate_batch06_root_judgment_contract` now requires an explicit
`hard_case_representation`, rejects positional roles, requires evidence bases
for evidence-derived cases, prevents a no-hard-case record from hiding
counterevidence, binds universal and unresolved rejection logic to their scope,
and requires two non-empty reopen controls.

Focused verification:

- `python -m tools.campaign apply-batch06-representation-remediation --repo-root .`
  completed with zero canonical errors and zero frozen payload drift.
- `python -m pytest tests/test_campaign_coverage.py -q` passed 42 tests.
- `python -m ruff check tools/campaign.py tests/test_campaign_coverage.py`
  passed.
- `python -m pytest tests/test_campaign_coverage.py tests/test_qac_morphology.py -q`
  passed 48 tests.

The tests compare all 40 controls after removing root identifiers: the
rejection and reopen sets remain 40 distinct epistemic controls, not merely
identifier substitution. They also compare every current artifact with the
starting candidate using the complete representation-frozen snapshot.

The final consistency sweep independently found zero canonical-contract errors,
zero frozen-payload drift, zero remaining legacy rejection/reopen template
matches, 40 normalized rejection controls, 40 normalized reopen-control sets,
and all five Batch 05 corrective artifacts unchanged from the starting
candidate.

## Handoff

`BATCH_06_REPRESENTATION_REMEDIATION_READY_FOR_FRESH_REVIEW` means only that
this implementation-side correction is ready for a new independent, read-only
review. It does not establish `INDEPENDENTLY_REVIEWED`, canonicalization,
merge, push, release, acceptance, or authority to start Batch 07.
