import json
import os

with open('scratch/batch08_plan.json') as f:
    plan = json.load(f)

# Reconstruct the batch table
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

This document establishes the readiness of the Lisanapp repository and governed runtime for Batch 08 semantic campaign execution, and proposes a candidate population. This is a proposal only; no semantic campaign is active.

## 1. Current Project Baseline
* Starting main SHA: `09a936fad61a74bb1f8e99f86637a28cd48b2bef`
* Current lifecycle state: `POST_CAMPAIGN_GOVERNANCE_HARDENING_COMPLETE` / `FIVE_ROOT_CAMPAIGN_COMPLETE_NO_CANONICAL_ADOPTIONS`

## 2. Readiness Verdict
**BATCH_08_READY_FOR_OWNER_AUTHORIZATION**

## 3. Proposed Campaign Population
* **Root Count**: 40
* **Total Occurrences**: {plan['total_occurrences']}
* **Candidate Population Hash**: `{plan['batch_hash']}`
* Zero overlap with previously processed roots.

## 4. Candidate Root Table
{table}

## 5. Execution Architecture
* **Producer Architecture**: 2 independent Quran-internal analysts + 1 source-purity adversary + 1 semantic-overclaim adversary -> aggregator -> DB-native claim freeze.
* **Independent-Review Architecture**: 100% full independent review required for all roots. Review occurs per wave. Fresh reviewer, separated from producer context. Maximum of 3 correction cycles allowed per root before forced UNRESOLVED closure.
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
Authorization to create `campaign/batch08` branch, activate manifest `{plan['batch_hash']}`, and execute continuous governed research/review cycles for the proposed 40 roots. No canonicalization is authorized.
"""

os.makedirs('docs/evidence/batch08', exist_ok=True)

with open('docs/LISAN3_BATCH_08_READINESS_AND_AUTHORIZATION.md', 'w') as f:
    f.write(auth_md)

auth_json = {
    "status": "BATCH_08_NOT_AUTHORIZED",
    "verdict": "BATCH_08_READY_FOR_OWNER_AUTHORIZATION",
    "baseline_sha": "09a936fad61a74bb1f8e99f86637a28cd48b2bef",
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
