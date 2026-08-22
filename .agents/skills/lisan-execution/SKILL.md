# Skill — Lisan Execution

## Trigger

Use for implementation, bug fixing, refactoring, migration, or continuation
of an existing Lisan work package.

## Procedure

### 1. Resume

Resolve:
- root/scoped AGENTS policy;
- canonical requirement;
- current branch and HEAD;
- working tree;
- PROJECT_STATE;
- relevant evidence.

Verify PROJECT_STATE before trusting it.

### 2. Bound the Goal

State the smallest cohesive current goal.

Do not reopen unrelated requirements or architecture.

### 3. Build Acceptance Map

Before implementation map:

`requirement → expected implementation boundary → required evidence`

Do not use task.md as product authority.

### 4. Implement Minimally

Reuse existing contracts and patterns.

Do not add infrastructure for hypothetical future requirements.

Preserve unrelated user work.

### 5. V1 Inner Loop

Run the smallest checks capable of disproving the current change.

### 6. Failure Classification

When verification fails, classify it before modifying implementation or tests.

### 7. V2 Checkpoint

After the cohesive boundary works, run relevant:
- integration tests;
- migrations;
- contracts;
- generated artifacts;
- affected frontend/backend checks.

### 8. Pre-Delivery Reconciliation

Re-read the authoritative acceptance source after implementation.

Map:

`requirement → implementation → executed evidence → verdict`

Do not close from task.md alone.

### 9. Adversarial Self-Review

Before reporting COMPLETE, attempt to disprove it.

Ask:
- What mandatory requirement did I not prove?
- What path could bypass the invariant?
- Did any mock/fixture/fake-provider become production evidence?
- Did I use a value from code instead of resolving authority?
- Did I configure rather than execute a tool?
- Did I prove runtime behavior or only code/schema generation?

Fix discovered defects and rerun focused evidence.

### 10. Persist

Update PROJECT_STATE with verified evidence and exact next action.

## Completion Rule

If a mandatory acceptance item is:
- FAIL,
- PARTIAL,
- or NOT_VERIFIED,

the containing scope is not COMPLETE.
