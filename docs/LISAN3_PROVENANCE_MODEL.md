# LISAN 3 Provenance Model

## Concept
Every representation of knowledge in Lisan 3 must be traceable back to its origin snapshot and the exact human/system actor that attested to it.

## Graph Structure
1. **Corpus Snapshot**: Immutable version of the Arabic/Buckwalter structural text.
2. **StructuralToken**: An attribution of a word in the snapshot to a root.
3. **ResearchRun**: The bounding context in which a researcher studied a root.
4. **IsolationState**: Cryptographic-like proof that the researcher operated cleanly, without external/synthetic leakage.
5. **ObservationArtifact**: Documented contexts where the root appeared in the snapshot.
6. **SemanticClaim**: The resulting research hypothesis or conclusion.
7. **ClaimRevision**: Immutably versions corrections.
8. **IndependentReview**: Third-party evaluation of the claim against the snapshot.
9. **VerificationRecord**: Output of a successful independent review.
10. **Canonicalization Evaluation**: The system's rules engine determining if the verified claim aligns with Lisan Platform goals.
11. **AuditLog**: Immutable trace of the canonicalization.

## UI Requirements
Any claim marked `ACCEPTED` must expose an API or direct link for `ProvenanceService.get_run_provenance` so that users can verify its authenticity.
