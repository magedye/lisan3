# LISAN 3 Review and Revision Lifecycle

## Core Principles
A `SemanticClaim` is a snapshot of research. Once submitted, it cannot be silently mutated. Corrections require an explicit new revision.

## Lifecycle
1. **Creation**: Claim is created at `revision_id = 1`.
2. **Independent Review**: A reviewer accesses the claim in a read-only state. They evaluate evidence and submit an `IndependentReview`.
3. **Rejection & Correction**: If rejected, the Orchestrator transitions the claim to `CORRECTION_REQUIRED`. The researcher submits a correction, incrementing `revision_id = 2`.
4. **Fresh Review**: The new revision undergoes a brand-new `IndependentReview`.
5. **Verification**: If approved, a `VerificationRecord` is bound to that exact `revision_id`.
6. **Canonicalization**: The system canonicalizes ONLY if the verified `revision_id` matches the current `revision_id`.

## UI Reflection
The API must always expose `revision_number` and the entire list of `IndependentReviews` for full transparency.
