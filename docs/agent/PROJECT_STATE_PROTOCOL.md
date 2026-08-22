# PROJECT_STATE Protocol

## Purpose

`PROJECT_STATE.md` stores the resumable operational position of the project.

It is not authoritative product truth.

## Required Fields

Record:

- branch;
- HEAD;
- working tree status;
- current bounded goal;
- completed work packages/slices;
- current evidence-supported statuses;
- relevant canonical revisions;
- changed files;
- migrations;
- executed verification evidence;
- configured-but-not-executed tooling;
- real blockers;
- unresolved authority questions;
- exact next action.

## Resume Procedure

Before relying on PROJECT_STATE:

1. read applicable AGENTS policy;
2. inspect branch and HEAD;
3. inspect working tree;
4. inspect applicable canonical artifacts;
5. inspect relevant migration/contract state;
6. inspect verification evidence;
7. reconcile differences;
8. correct stale PROJECT_STATE.

## Evidence Language

Never write:

`verified`

when the evidence is merely:

- implemented,
- configured,
- mocked,
- planned,
- or inferred.

Use explicit qualifiers such as:

- TESTED_WITH_FIXTURES
- TESTED_WITH_FAKE_PROVIDER
- CONFIGURED_NOT_EXECUTED
- ARTIFACT_VERIFICATION_PENDING

when applicable.

## Handoff

Before compaction, session end, or agent handoff:

- persist current evidence;
- persist blockers;
- persist the exact next command/action;
- never rely on conversation memory as the only resume mechanism.
