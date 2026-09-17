# LISAN 3 Recovery Runbook

## Scope
This document covers DB integrity and operational recovery procedures for the Lisan 3 platform.

## Corrupted State
1. If the closure validator (`tools/validate_closure.py`) fails, the orchestrator MUST NOT close the campaign.
2. The orchestrator will mark the campaign as `BLOCKED`.
3. To recover, run `alembic upgrade head` to ensure schema integrity.
4. If a partial transaction locked the DB, the orchestrator's idempotency allows safe restart (`CampaignStateService.resume()`).
5. Never force push to fix semantic claims. Issue a new ClaimRevision with `correction_reason` and run it through a fresh `IndependentReview`.
