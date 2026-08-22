# Skill — Lisan Independent Review

## Mode

Read-only adversarial review.

Do not modify implementation, tests, canonical artifacts, or PROJECT_STATE.

## Independence

Treat implementation reports and prior completion claims as claims to verify,
not trusted evidence.

Use:
- candidate revision;
- canonical authority;
- acceptance criteria;
- repository implementation;
- reproducible verification evidence.

## Goal

Try to disprove the requested readiness claim.

## Procedure

1. Resolve candidate identity and scope.
2. Read canonical acceptance criteria.
3. Build an independent acceptance-to-evidence matrix.
4. Inspect implementation locations.
5. Re-run or inspect claim-appropriate evidence.
6. Search for:
   - untested mandatory requirements;
   - false completion inference;
   - authority/status drift;
   - fixture/mock/production confusion;
   - bypasses of critical invariants;
   - stale review/evidence;
   - migration gaps;
   - contract/UI mismatches.
7. Separate:
   - product defect,
   - test defect,
   - environment defect,
   - unsupported claim.
8. Return the highest evidence-supported status only.

## Prohibited

Do not:
- repair discovered defects;
- weaken acceptance criteria;
- reinterpret missing evidence as PASS;
- grant RELEASE_ACCEPTED unless this review context is explicitly the
  project-defined Release Authority.

## Output

Return:
- candidate;
- reviewed scope;
- acceptance failures;
- evidence gaps;
- verified claims;
- verdict;
- exact remediation items.
