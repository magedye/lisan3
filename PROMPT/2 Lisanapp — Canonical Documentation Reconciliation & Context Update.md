# Lisanapp — Canonical Documentation Reconciliation & Context Update

## Goal

Work directly in:

`D:\APP\tafseer\lisanapp3`

The owner has already saved the new canonical architecture contract at:

`docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`

Treat that document as:

`CANONICAL — APPROVED / EXECUTION_GATED`

Your task is **documentation/context reconciliation only**.

Do not implement R1/R2/R3 product code yet.

Historical context: this procedure was drafted while V3 remediation was
active. V3 is now `V3_INDEPENDENTLY_CONFIRMED` for the reviewed candidate
`6bb6505484dd649d092032a36d456f9f7fba5da1`.

Do not add Graph/Vector infrastructure yet.

---

# 1. Verify the new canonical document

Read:

`docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`

Verify:

- file exists;
- status/version are present;
- execution gate is `V3_INDEPENDENTLY_CONFIRMED`;
- execution order is `R1 → R2 → R3`;
- Graph/Vector layers are explicitly derived/non-authoritative.

Do not rewrite the document unless there is an actual contradiction with a higher-authority source.

If a contradiction exists, record it as an authority issue rather than silently editing the contract.

---

# 2. Update the Canonical Platform Reference

Edit:

`docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md`

Add one concise canonical reference to:

`LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`

Use wording equivalent to:

> Hybrid retrieval, Knowledge Graph, Vector Discovery, EvidenceResolver, and their integration with the AI Runtime are governed by `LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`.

Do not copy the architecture or R1/R2/R3 roadmap into the platform reference.

Prevent duplicate normative content.

---

# 3. Reconcile the Tooling Adoption Reference

Edit:

`docs/canonical/LISAN_TOOLING_ADOPTION_REFERENCE.md`

Reconcile relevant tool decisions with the new canonical architecture.

At minimum ensure these statuses are consistent:

- NetworkX → `ADOPT_NEXT_AFTER_V3`
- React Flow / `@xyflow/react` → `ADOPT_NEXT_AFTER_V3`
- sqlite-vec → `APPROVED_FOR_EVALUATION`
- Qdrant Embedded/Local → `CONDITIONAL_LATER`
- Qdrant Server → `DO_NOT_ADOPT_NOW`
- Neo4j → `DO_NOT_ADOPT_NOW`
- Embedding model → `TO_BE_SELECTED_BY_BENCHMARK`
- RDFLib → `APPROVED_FOR_EVALUATION`
- RDF/OWL → `CONDITIONAL_LATER`
- Protégé → `LAB_ONLY`
- Haystack/LlamaIndex → `CONDITIONAL_LATER` for external-source retrieval only
- LangChain → `DO_NOT_ADOPT_NOW`
- Prolog → `DO_NOT_ADOPT_NOW`

Do not duplicate the full Hybrid Retrieval architecture into the tooling reference.

The tooling document should define adoption policy/status, not product architecture.

If an existing status conflicts with the new canonical architecture, reconcile it and record the change.

---

# 4. Update UI ↔ Backend Contract Matrix

Edit:

`docs/canonical/UI_BACKEND_CONTRACT_MATRIX.md`

Add/reconcile the affected Golden UX capabilities.

At minimum map:

## Knowledge Explorer

Future backend:

- Graph projection read model
- KnowledgeNode / KnowledgeEdge
- NetworkX analysis
- provenance
- React Flow visualization

Phase:

`R1 — PLANNED_POST_V3`

## Semantic Differentiation Lab

Future backend:

- Vector candidate discovery
- embedding-space identity
- Candidate Neighbor result
- EvidenceResolver

Phase:

`R2/R3 — PLANNED_POST_V3`

## Purity Detector

Future optional assistance:

- Exact source comparison
- Vector candidate similarity for Heritage Bias / contamination detection

Authority note:

Vector results are candidate findings only.

Phase:

`R2/R3 — PLANNED_POST_V3`

## Dependency / Provenance views

Future backend:

- governed graph projection
- graph paths
- source-layer provenance

Phase:

`R1/R3 — PLANNED_POST_V3`

## Ask Lisan / AI Research Runtime

Future integration:

- Exact Retrieval
- Vector Candidate Discovery
- Graph Candidate Retrieval
- EvidenceResolver

Phase:

`R3 — PLANNED_POST_V3`

Do not mark any R1/R2/R3 capability as implemented.

Preserve current backend mappings separately.

---

# 5. Reconcile Domain Documentation

If this file exists:

`docs/canonical/LISAN_DOMAIN_MODEL.md`

update it minimally.

Add only references/concepts needed to acknowledge future derived objects such as:

- `KnowledgeNode`
- `KnowledgeEdge`
- `SemanticEmbedding`
- `RetrievalCandidate`
- `EvidenceResolver`

Mark them clearly as:

`PLANNED / DERIVED / POST-V3`

Do not define production schemas prematurely.

Do not copy full field definitions from the Hybrid Retrieval contract unless an existing domain document requires a brief conceptual mapping.

If the file does not exist, do not create it solely for this task unless another canonical document explicitly requires it.

---

# 6. Update Root AGENTS.md

Edit the root:

`AGENTS.md`

Keep it small.

Under the canonical references section, add only:

`docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`

Do not copy Graph/Vector rules into `AGENTS.md`.

The purpose is JIT discovery of the canonical contract.

---

# 7. Update Scoped AGENTS Files

If these exist:

- `backend/AGENTS.md`
- `frontend/AGENTS.md`

add one concise scoped instruction.

## Backend

Use wording equivalent to:

> For Graph, Vector, Knowledge Explorer, EvidenceResolver, retrieval, or hybrid-search changes, read and follow `docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`.

## Frontend

Use wording equivalent to:

> For Knowledge Explorer, Semantic Differentiation candidate discovery, graph visualization, or retrieval-provenance UI changes, read and follow `docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`.

Do not duplicate its architecture.

If scoped AGENTS files do not exist, do not create them solely for one reference unless this matches the repository's established agent-policy structure.

---

# 8. Create the Repo-Scoped Hybrid Retrieval Skill

If `.agents/skills/` is part of the current repository convention, create:

`.agents/skills/lisan-hybrid-retrieval/SKILL.md`

Keep this skill procedural and compact.

It must NOT duplicate the architecture contract.

Use this behavior:

```text
Trigger:
Use for implementation or verification involving Knowledge Graph,
Vector Discovery, embeddings, EvidenceResolver, Knowledge Explorer,
or Hybrid Retrieval.

Procedure:
1. Read applicable AGENTS policy.
2. Read LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md.
3. Verify activation gate:
   V3_INDEPENDENTLY_CONFIRMED.
4. If gate is not satisfied:
   do not implement R1/R2/R3;
   report execution gated.
5. Resolve current phase:
   R1, R2, or R3.
6. Build acceptance-to-evidence map for that phase.
7. Implement only the active phase.
8. Run focused V1/V2 verification.
9. Perform adversarial self-review.
10. Update PROJECT_STATE.

Rules:
- Vector/Graph results are derived candidates, never authority.
- Exact canonical evidence governs conflicts.
- Preserve Blind Lab isolation.
- Do not add Graph/Vector servers without canonical approval.
```

If repository skills are unsupported or not currently used, skip creation and document that AGENTS + canonical references remain sufficient.

---

# 9. Update PROJECT_STATE.md

Reconcile:

`PROJECT_STATE.md`

with the new architectural decision.

Add a concise state entry equivalent to:

```text
Hybrid Retrieval Architecture:
CANONICAL_APPROVED

Canonical Reference:
docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md

Activation Gate:
V3_INDEPENDENTLY_CONFIRMED — SATISFIED

Execution Order:
R1 → R2 → R3

Current Retrieval Phase:
R1_NOT_STARTED
```

Do not imply that Graph or Vector functionality is implemented.

Preserve the candidate-bound provenance of the independent V3 confirmation.
Historical `V3_NOT_CONFIRMED / V4_ENTRY_BLOCKED` findings remain review
evidence; they are not current project state.

Remember:

`PROJECT_STATE.md` is resumable state, not authority.

---

# 10. Update Current Implementation Plan

Inspect the current durable implementation plan/task artifacts inside the repository.

Do not rely on IDE brain/scratch artifacts as the sole plan.

Reconcile the active plan so it clearly separates:

## Current Track

`Post-V3 Hybrid Retrieval documentation reconciliation`

This owner-selected reconciliation precedes R1 to remove authority ambiguity;
it is not a substitute for, or a blocker imposed by, the satisfied V3 gate.

## Next Implementation Track

`R1 Knowledge Graph Foundation — activation allowed, not started`

```text
R1 Knowledge Graph Foundation
→ R2 Vector Discovery
→ R3 Hybrid Retrieval
```

R1 requires a separately authorized bounded work package. R2 and R3 remain
ordered after verified predecessor phases. Do not let future architecture
expand the documentation-only scope.

---

# 11. Reconcile PROMPT/1.MD by Reference Only

Inspect:

`PROMPT/1.MD`

Do not rewrite the large implementation request.

If necessary, add one concise addendum/reference noting that future Graph/Vector/Hybrid Retrieval work is governed by:

`docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`

and is execution-gated until:

`V3_INDEPENDENTLY_CONFIRMED`.

Do not duplicate R1/R2/R3 content into `PROMPT/1.MD`.

If no update is required because canonical precedence already resolves this cleanly, leave `PROMPT/1.MD` unchanged and report why.

---

# 12. Documentation Drift Audit

Search relevant canonical and agent-policy files for competing statements about:

- Neo4j
- Qdrant
- sqlite-vec
- NetworkX
- React Flow
- RDF/OWL
- Vector authority
- Graph authority
- Stitch authority
- R1/R2/R3 timing

Classify conflicts:

- `DUPLICATE_NONCONFLICTING`
- `STALE`
- `CONFLICTING`
- `HISTORICAL_ONLY`

Correct only normative stale/conflicting material.

Do not rewrite historical reports or evidence artifacts.

---

# 13. Stitch Reconciliation

Ensure documentation consistently states:

- UX Constitution is authoritative for UX/product behavior.
- Golden Stitch prototype is design/interaction reference.
- Stitch mock data is not backend/domain truth.
- Material design changes may be prototyped in Stitch.
- ordinary implementation fixes/data binding/accessibility fixes do not require a mandatory Stitch round trip.
- Knowledge Explorer and Semantic Differentiation Golden views remain the UX targets for future R1/R2 integration.

Do not reopen or regenerate the Stitch prototype.

---

# 14. Tool Adoption Enforcement

Ensure no current plan tells the implementation agent to install:

- sqlite-vec
- NetworkX
- React Flow for this new architecture
- RDFLib
- Qdrant

during pre-R1 preparation.

Their statuses must remain gated according to the canonical tooling/architecture references.

Do not uninstall tools already legitimately used elsewhere.

---

# 15. Verify Reference Integrity

After edits, verify:

- every relative canonical link resolves;
- no duplicate canonical architecture exists;
- root AGENTS remains compact;
- scoped AGENTS do not duplicate architecture;
- PROJECT_STATE accurately says implementation is not started;
- implementation plan records V3 confirmation and R1 as not started;
- no R1/R2/R3 implementation code was added.

Run appropriate text/link/reference checks if available.

No product test suite is required unless a documentation edit affects generated/runtime behavior.

---

# 16. Context Persistence

Before finishing:

verify Git state.

Update `PROJECT_STATE.md` with:

- files changed;
- canonical architecture reference;
- V3 current status;
- future R1/R2/R3 gate;
- exact next action.

Do not claim this documentation reconciliation implements any R1/R2/R3 capability.

---

# 17. Commit Discipline

If the repository policy permits commits in the current implementation thread, create one coherent documentation/governance commit such as:

`docs: reconcile post-V3 hybrid retrieval authority`

Do not mix product-code changes into this commit.

Do not push remotely.

If current policy/task does not authorize committing, leave changes staged/unstaged as appropriate and report exact Git state.

---

# Stop Condition

Stop when:

1. the Hybrid Retrieval contract is referenced by the canonical platform documentation;
2. tooling statuses are reconciled;
3. UI/backend matrix reflects future R1/R2/R3 mappings;
4. applicable AGENTS policies reference the contract;
5. optional repo skill is installed if repository conventions support it;
6. PROJECT_STATE records the approved architecture and `R1_NOT_STARTED` state;
7. active implementation guidance records V3 confirmation and the separately authorized R1 boundary;
8. normative documentation drift has been reconciled;
9. no R1/R2/R3 implementation has started.

Do not implement Graph/Vector functionality.

---

# Return only

## Canonical Reference
- verified path
- status/version

## Updated Documents
- file
- exact purpose of update

## AGENTS / Skills
- references added
- skill created/skipped and reason

## Tooling Reconciliation
- changed statuses
- remaining conflicts, if any

## UI / Backend Matrix
- R1/R2/R3 planned mappings

## PROJECT_STATE
- current V3 status
- Hybrid Retrieval gate
- exact next action

## Plan
- current post-V3 documentation reconciliation track
- next separately authorized R1 track

## Drift Audit
- stale/conflicting statements corrected
- historical items intentionally preserved

## Git
- branch
- HEAD
- working tree
- commit if created

## Verdict

`CANONICAL_RECONCILIATION_COMPLETE`

or

`RECONCILIATION_GAPS_REMAIN`
