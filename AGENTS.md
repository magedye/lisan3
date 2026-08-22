# Lisanapp Agent Policy

This file is intentionally small, durable, and always applicable.

Detailed product requirements, Quranic methodology, workflows, tooling policy,
schemas, registries, acceptance criteria, and volatile implementation state
belong in their canonical repository artifacts, scoped skills, or PROJECT_STATE.

## Mission

Deliver the currently authorized Lisanapp outcome correctly, incrementally,
efficiently, and with claim-appropriate evidence.

Preserve unrelated user work.

Never claim more completion than the available evidence proves.

## Source Precedence

Apply sources in this order unless a later explicit owner decision changes it:

1. Latest explicit owner instruction.
2. Repository and applicable scoped AGENTS policy.
3. Canonical Lisan product, methodology, and governance requirements.
4. Accepted ADRs and public contracts.
5. Official registries and schemas within their defined authority.
6. Canonical UX/product contracts.
7. Approved plans and scoped tasks.
8. Current implementation and tests.
9. PROJECT_STATE and other state summaries.
10. Assumptions.

Derived skills, AI output, fixtures, reports, prototype UI, legacy material,
and model memory never override higher authority.

## Canonical References

Use the canonical repository artifacts rather than duplicating their contents.

Primary entry point:
- `docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md`

Tool adoption:
- `docs/canonical/LISAN_TOOLING_ADOPTION_REFERENCE.md`

Semantic runtime:
- `skills/lisan-semantic-extraction/SKILL.md`

Execution request:
- `PROMPT/1.MD`

## Execution Discipline

Before acting:

1. Resolve the current bounded goal.
2. Read the applicable canonical source.
3. Read PROJECT_STATE when resuming.
4. Verify PROJECT_STATE against Git/runtime evidence.
5. Correct stale state before continuing.

Do not reopen settled architecture/product decisions unless:
- a newer owner instruction changes them;
- canonical sources conflict;
- or implementation evidence proves a real blocker.

Avoid unrelated refactoring and speculative infrastructure.

## Claim / Evidence Discipline

Use these states precisely:

- IMPLEMENTED
- TESTED
- VERIFIED_FOR_PROFILE
- TECHNICALLY_RELEASE_READY
- INDEPENDENTLY_REVIEWED
- RELEASE_ACCEPTED

Never collapse them.

Remember:

- installed ≠ configured
- configured ≠ executed
- executed ≠ passed
- passed ≠ verified outside tested scope
- green tests ≠ release readiness
- fixture/mock/fake-provider evidence ≠ production evidence

Before declaring a scope complete, map:

`requirement → implementation → executed evidence → verdict`

Any mandatory FAIL, PARTIAL, or NOT_VERIFIED prevents COMPLETE.

## Authority / Registry Discipline

Never invent official statuses, gates, lifecycle states, or authority.

Resolve them from the applicable canonical registry or contract.

A value appearing in code, tests, fixtures, UI, reports, legacy documents,
or AI output is not canonical merely because it exists.

## Critical Domain Invariants

Preserve canonical Lisan invariants, including:

- analysis stages remain separate from official status axes;
- Epistemic, Review, Freshness, and Publication remain independent;
- failed critical Gates cannot be bypassed;
- Steward cannot establish semantic truth or force Gate success;
- AI output is proposal/analysis, not canonical evidence by itself;
- Blind Lab isolation is enforced beyond UI visibility;
- fixture or unverified-source results cannot enter canonical knowledge.

Canonical artifacts define the exact rules.

## Verification

Follow the repository verification skill and V0–V4 cadence.

Use focused checks during implementation and broader gates only when justified.

For critical invariants, test negative paths and actively attempt to disprove
the current completion claim before reporting success.

Classify failures before modifying code, tests, or requirements.

## Failure Classes

Use:

- PRODUCT_DEFECT
- TEST_DEFECT
- ENVIRONMENT_DEFECT
- STALE_CONTEXT
- EXTERNAL_DEPENDENCY
- EXPECTED_OPTIONAL_STATE
- AUTHORITY_CONFLICT

Never weaken canonical requirements merely to make verification green.

## Tooling

Follow `docs/canonical/LISAN_TOOLING_ADOPTION_REFERENCE.md`.

Do not add dependencies or infrastructure without a demonstrated requirement
and satisfied adoption trigger.

Experimental tools do not become runtime dependencies or authority automatically.

## Context Persistence

PROJECT_STATE is resumable state, never authoritative truth.

Update it after meaningful checkpoints with:
- branch / HEAD / working tree;
- current scope;
- decisions;
- changed files;
- executed evidence;
- blockers;
- exact next action.

Persist state before context compaction, handoff, or stopping.

## Commits

Prefer coherent, reviewable commits.

Do not mix unrelated cleanup with scoped work.
Do not rewrite reviewed history without explicit justification.
Do not push remotely without owner authorization.

## Agent / Review Separation

Use one execution agent by default.

Use subagents only for partitionable exploration, noisy analysis,
or genuinely independent review.

The implementation agent must not self-grant:
- INDEPENDENTLY_REVIEWED
- RELEASE_ACCEPTED

Independent acceptance uses a fresh read-only context against the candidate
revision and canonical acceptance criteria.