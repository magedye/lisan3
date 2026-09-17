# Review Plan: New Lisan Project Reuse & Lessons Kit

## Scope

Create an evidence-based, non-authoritative design handoff for a future independent Quran Lisan project. All authored output remains in `NEW_LISAN_PROJECT_REUSE_KIT/`; no Lisan3 behavior, authority, state, contracts, schemas, tests, UI, or existing documentation will be changed.

## Evidence strata

1. Current policy and authority map.
2. Canonical methodology, corpus, purity, retrieval, and tooling contracts.
3. Active implementation: domain models, services, adapters, AI runtime, retrieval, Blind Lab, and ResearchRun.
4. Test and evaluation evidence, especially negative paths.
5. Active state/handoff and concrete execution evidence.
6. Historical and legacy reuse material, explicitly labeled non-authoritative.
7. Agent recommendations, explicitly separated from repository evidence.

## Ordered review tasks

### Task 1: Freeze the review baseline

Acceptance criteria:

- Exact HEAD, branch, and initial porcelain status are recorded.
- Pre-existing owner files are identified and left untouched.
- Final preservation can be compared with the initial state.

Verification: compare final `git status --porcelain=v2 --untracked-files=all` with the initial baseline, allowing only this kit as a new path.

### Task 2: Build the source and authority map

Acceptance criteria:

- Canonical, active-derived, implementation, test, historical, and state sources are distinguished.
- Major required source areas from the owner request are represented.
- Superseded material is never treated as current authority.

Verification: inventory coverage audit against the owner-request list.

### Task 3: Extract semantic-method and evidence candidates

Acceptance criteria:

- Root concept, semantic layering, evidence/source separation, counterevidence, falsification, and confidence lessons are traced to sources.
- Safety/evidence necessities are separated from Lisan3 governance choices.
- Each significant candidate has exactly one required classification.

Verification: matrix schema and classification consistency check.

### Task 4: Extract runtime, retrieval, data, Skill, Agent, and Tool candidates

Acceptance criteria:

- Deterministic Tool responsibilities are separated from model judgment.
- Skills, Agents, and architecture candidates are assessed rather than automatically adopted.
- Gem/Opal overlap and triggers for an independent engine are explicit.

Verification: cross-check candidates against implementation and tests.

### Task 5: Author the complete kit incrementally

Acceptance criteria:

- All required numbered artifacts and the `materials/` folder exist.
- Every candidate Skill has the requested compact specification fields.
- Evidence and agent inference are visibly labeled.

Verification: required-path and required-section checks after each document group.

### Task 6: Adversarial verification

Acceptance criteria:

- Internal Markdown links resolve.
- Major evidence strata were considered.
- Recommendations are traceable.
- No artifact was imported merely because Lisan3 already contains it.
- No path outside the kit was created or modified by this task.

Verification: automated link/classification/path checks plus manual adversarial review.

## Risks and controls

| Risk | Control |
|---|---|
| Treating current Lisan3 governance as new-project authority | Classify governance separately and state that all new-project choices remain owner decisions. |
| Overclaiming observed lessons | Label statements as repository evidence, historical evidence, or agent inference. |
| Missing relevant implementation behavior | Cross-read contracts, services, schemas, and tests; perform a second missed-material search. |
| Copying too much legacy material | Curate only small high-value derivatives with provenance headers. |
| Altering owner work | Use additive files only under the kit and compare final Git state to baseline. |

## Commit policy

No commit, push, PR, tag, release, or acceptance action is authorized.
