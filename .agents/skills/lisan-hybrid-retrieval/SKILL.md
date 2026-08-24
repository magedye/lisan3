# Skill — Lisan Hybrid Retrieval

## Trigger

Use for implementation or verification involving Knowledge Graph, Vector
Discovery, embeddings, EvidenceResolver, Knowledge Explorer, or Hybrid
Retrieval.

## Procedure

1. Read applicable root and scoped `AGENTS.md` policy.
2. Read `docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`.
3. Verify the current phase and its prerequisite evidence. The V3 prerequisite
   is satisfied only for reviewed candidate `6bb6505484dd649d092032a36d456f9f7fba5da1`.
4. Enforce the order `R1 → R2 → R3`; R1 requires a separately authorized
   bounded work package, R2 requires verified R1, and R3 requires verified R1
   and R2.
5. Build an acceptance-to-evidence map for the active phase.
6. Implement or verify only that active phase.
7. Preserve Blind Lab isolation and source-layer provenance.
8. Treat Graph and Vector outputs as derived candidates, never canonical
   authority; exact canonical Evidence resolves conflicts.
9. Do not add Graph or Vector servers without explicit canonical approval.
10. Run focused verification, perform adversarial self-review, and update
    `PROJECT_STATE.md` with evidence-supported state.
