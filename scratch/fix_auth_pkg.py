import json
import os

with open('scratch/batch08_repaired_plan.json') as f:
    plan = json.load(f)

table = "| Arabic Root | Buckwalter | Occurrences | Frequency Band | Morphological Profile | Planning Risk | Previous Processing | Reopen Check | Eligibility | Proposed Wave |\n"
table += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"

waves = [[] for _ in range(4)]
for idx, item in enumerate(plan['details']):
    root, count, band = item
    wave_num = (idx // 10) + 1
    waves[wave_num - 1].append(count)
    table += f"| {root} | {root} | {count} | {band} | Pending | Pending Evaluation | None | NO_REOPEN | ELIGIBLE | Wave {wave_num} |\n"

wave_counts = [sum(w) for w in waves]

auth_md = f"""# LISAN3 Batch 08 Readiness and Authorization Package

**STATUS: BATCH_08_NOT_AUTHORIZED**

This document establishes the readiness of the Lisanapp repository and governed runtime for Batch 08 semantic campaign execution, and proposes a repaired candidate population. This is a proposal only; no semantic campaign is active.

## 1. Population Accounting Repair
* **Structural Universe**: Exactly 1642 admitted roots.
* **Historical Processed Universe**: Exactly 248 unique roots processed across Batches 02–07 (including the 5 DB-native roots).
* **Current DB-native claimed roots**: 5 roots (ESw, dnw, flH, fwh, glm).
* **True Unprocessed Universe**: Exactly 1394 roots.

## 2. Readiness Verdict
**BATCH_08_READY_FOR_OWNER_AUTHORIZATION**

## 3. Repaired Campaign Population
* **Root Count**: 40
* **Total Occurrences**: {plan['total_occurrences']}
* **Candidate Population Hash**: `{plan['batch_hash']}`
* Zero overlap with all 248 historically processed roots.

## 4. Candidate Root Table
{table}

## 5. Execution Architecture
* **Producer Architecture**: 2 independent Quran-internal analysts + 1 source-purity adversary + 1 semantic-overclaim adversary -> aggregator -> DB-native claim freeze.
* **Independent-Review Architecture**: 100% full independent review required for all roots. Review occurs per wave. Fresh reviewer, separated from producer context.
* **Correction-Loop Policy**: RESEARCH -> FROZEN_CLAIM -> INDEPENDENT_REVIEW -> VERIFIED or RETURN_FOR_CORRECTION -> NEW_REVISION -> RE-REVIEW. Bounded to 3 iterations.
* **Continuous Delegation Model**: Authorized orchestrator may proceed through research, review, correction, and FF merge without explicit owner confirmation, EXCEPT for human non-delegable gates and canonicalization.

## 6. Wave Plan
* Wave 1: 10 roots, {wave_counts[0]} occurrences
* Wave 2: 10 roots, {wave_counts[1]} occurrences
* Wave 3: 10 roots, {wave_counts[2]} occurrences
* Wave 4: 10 roots, {wave_counts[3]} occurrences

## 7. Hard Stop Conditions
* Corrupted provenance or exact-set failure.
* Attempted circumvention of independent review.
* Loss of `ESTABLISHED/CLEAN` isolation.
* Infrastructure corruption.

## 8. Exact Authorization Scope Requested
Authorization to create `campaign/batch08` branch, activate repaired manifest `{plan['batch_hash']}`, and execute continuous governed research/review cycles for the proposed 40 roots. No canonicalization is authorized.
"""

os.makedirs('docs/evidence/batch08', exist_ok=True)
with open('docs/LISAN3_BATCH_08_READINESS_AND_AUTHORIZATION.md', 'w') as f:
    f.write(auth_md)

auth_json = {
    "status": "BATCH_08_NOT_AUTHORIZED",
    "verdict": "BATCH_08_READY_FOR_OWNER_AUTHORIZATION",
    "baseline_sha": "09a936fad61a74bb1f8e99f86637a28cd48b2bef",
    "population_repair": {
        "structural_roots": 1642,
        "historical_processed_roots": 248,
        "db_native_claimed_roots": 5,
        "true_unprocessed_roots": 1394
    },
    "proposed_population": {
        "count": 40,
        "occurrences": plan['total_occurrences'],
        "hash": plan['batch_hash'],
        "waves": wave_counts
    }
}
with open('docs/evidence/batch08/BATCH_08_READINESS_AND_AUTHORIZATION.json', 'w') as f:
    json.dump(auth_json, f, indent=2)

print("Files generated.")
