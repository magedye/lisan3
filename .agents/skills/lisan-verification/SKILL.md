# Skill — Lisan Verification

## Goal

Determine what the evidence actually proves.

Do not preserve a previous completion claim merely because it exists in
PROJECT_STATE, task.md, a report, or prior model output.

## V0 — Preflight

Use when starting/resuming where needed.

Verify:
- authority;
- Git/runtime state;
- environment;
- dependencies;
- relevant baseline evidence.

## V1 — Inner Loop

Use focused tests/static checks that can quickly disprove the current change.

Do not run the entire suite mechanically after each edit.

## V2 — Checkpoint

After a cohesive boundary change verify applicable:
- integration behavior;
- migrations;
- contract compatibility;
- persistence;
- affected generated artifacts;
- frontend/backend integration.

## V3 — Phase Gate

Re-read canonical phase acceptance first.

Build an evidence matrix.

Verify all applicable categories:
- affected subsystem suite;
- schemas and registries;
- migrations;
- API contracts;
- static checks;
- canonical documentation consistency;
- critical journeys;
- adopted verification tooling.

A green pytest suite alone is not V3 evidence.

## V4 — Release Gate

Run against the actual candidate revision.

Verify project-defined release requirements, including as applicable:
- candidate identity;
- clean/specified worktree;
- migrations from zero;
- full tests;
- contracts;
- frontend production build;
- browser E2E;
- Corpus integrity;
- AI live/fake distinction;
- focused security/integrity checks;
- dependency audits;
- reproducibility evidence.

Do not self-grant independent acceptance.

## Evidence Rules

Always distinguish:

`installed → configured → executed → passed → supports claim`

Never skip a step in reporting.

Examples:

- Promptfoo config exists → CONFIGURED_NOT_EXECUTED.
- Cosmic Ray baseline passes → BASELINE_PASSED_MUTATION_RUN_PENDING.
- Fake provider test passes → TESTED_WITH_FAKE_PROVIDER.
- frontend builds → BUILD_VERIFIED, not E2E_VERIFIED.
- fixture Corpus passes → TESTED_WITH_FIXTURES, not canonical Corpus verified.

## Adversarial Checks

For critical invariants, test failure and bypass paths.

Try to find a counterexample before accepting the claim.

## Gate Verdict

If a mandatory gate item lacks evidence:

return BLOCKED/PARTIAL as defined by the project.

Do not weaken the gate to match the current implementation.
