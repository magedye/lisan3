# LISAN 3 Campaign Orchestrator

## Goal
The orchestrator is a strict state machine that derives its state entirely from authoritative DB entities. It prevents skipped transitions and ensures idempotency.

## States
A root in a campaign moves through these derived states:

- **PLANNED**: Exists in campaign queue.
- **AUTHORIZED**: Campaign is authorized, root is eligible.
- **RUN_CREATED**: `ResearchRun` exists.
- **ISOLATION_ESTABLISHED**: `IsolationState` is ESTABLISHED and CLEAN.
- **OBSERVATIONS_COMPLETE**: `ObservationArtifact` covers all eligible occurrences.
- **RESEARCH_IN_PROGRESS**: `ResearchRun` stage is RESEARCH, `AIExecutionRecord` or manual input ongoing.
- **CLAIM_FROZEN**: `SemanticClaim` exists and is finalized.
- **INDEPENDENT_REVIEW_PENDING**: Claim requires independent verification.
- **CORRECTION_REQUIRED**: Review rejected, new revision required.
- **VERIFIED**: `VerificationRecord` exists with `INDEPENDENT` type and `VERIFIED` decision.
- **CANONICALIZATION_ELIGIBLE**: VERIFIED, but not yet canonicalized.
- **CANONICALIZED**: `AuditLog` records `CANONICALIZE` action, canonical_state is ACCEPTED.
- **UNRESOLVED**: Claim is WEAK or unresolved.
- **CLOSED**: Final terminal state.
- **BLOCKED**: Contamination or unauthorized action blocked progress.

## Derivation Logic
The orchestrator calculates the state on-the-fly by querying the repository bounds, ensuring that no stale reports dictate reality.
