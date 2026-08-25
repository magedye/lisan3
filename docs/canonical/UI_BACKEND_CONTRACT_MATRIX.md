# UI Backend Contract Matrix

This matrix records the production UI-to-contract binding. It does not create
new authority, statuses, commands, or phase permission. Golden Stitch assets
govern visual intent only; canonical product, UX, registry, and backend
contracts govern behavior and meaning.

| UI capability | Production route | Read model / query | Commands | Loading / empty / error | Authority boundary | Implementation evidence |
|---|---|---|---|---|---|---|
| Attention Center, governed Ask and Run Builder | `/` | `GET /attention`; `POST /ask` response | `POST /runs` | Yes / Yes / Yes | Attention is persisted operational state; Ask does not establish truth; methodology and corpus IDs are explicit user inputs. | Implemented and tested in Playwright Journeys 1, 7 and 8 plus `test_ui_read_models.py`. |
| Research Run / Root Workspace / Hypothesis view | `/run/[id]` | `GET /runs/{run_id}/workspace` | Existing Gate and claim contracts are not broadened by the aggregate | Yes / Yes / Yes | Stage is separate from four status axes. Claims fail closed unless isolation is `CLEAN` and the existing current Internal Lock Gate check passes. | Implemented and tested in Journeys 1, 2 and 8. |
| Blind Lab | `/run/[id]/blind` | Existing run, isolation and corpus-occurrence reads | Existing isolation preflight and observation recording | Yes / Yes / Yes | Prior contamination is distinct from a forbidden access attempt; the UI has no simulation/bypass action. | Implemented and tested in Journey 2. |
| Knowledge Explorer | `/run/[id]/knowledge` | Existing R1 graph read/rebuild contracts | Derived projection rebuild only | Yes / Yes / Yes | Graph is derived, read-only and non-authoritative; text provenance is available alongside React Flow. | Implemented and tested in Journey 6. |
| Claim traceability, stale state and purity | `/claims/[id]` | `GET /claims/{claim_id}` plus existing provenance, quality, reproduction-manifest and history reads | None on this route | Yes / Yes / Yes | Epistemic, Review, Freshness and Publication stay independent. Evidence and counterevidence remain balanced. Purity is eight-dimensional and is not truth/confidence. Quality GET is read-only. | Implemented and tested in Journeys 3 and 8 plus status-axis tests. |
| Governance, resource admission and review queue | `/governance` | `GET /governance/overview`; existing rule history and impact reads | Existing rule/proposal/impact/approval commands with confirmation | Yes / Yes / Yes | Corpus lifecycle axes and claim axes remain independent; confirmation does not bypass backend validation. | Implemented and tested in Journey 4 and read-model tests. |
| Steward Command Center | `/steward` | Existing preview/result/audit reads | Existing Steward execute contract with explicit confirmation | Yes / Yes / Yes | Steward cannot establish semantic truth, force Gate success, or bypass immutable constraints. No hardcoded production demo command is offered. | Implemented and tested for allowed and forbidden paths in Journey 5. |
| Audit Trail | `/audit` | `GET /audit` with `entity_type` and `entity_id` filters | None | Yes / Yes / Yes | Read-only AuditLog projection; filters do not create or reinterpret events. | Implemented and tested in Journeys 5, 7 and 8. |

Roles/authentication remain within the canonical trusted single-user monolith
boundary. AI runtime states are operational conditions and are never official
epistemic statuses.

## Golden Asset Classification

The exact 28-pair inventory, classifications, supersession decisions,
production mapping, model dependencies, visual/interaction/data state, and
test evidence are maintained in
`docs/STITCH_PRODUCTION_COVERAGE_MATRIX.md`.

## Hybrid Retrieval Boundary

| Golden capability | Phase | Backend/read-model status | Authority boundary |
|---|---|---|---|
| Knowledge Explorer | `R1_INDEPENDENTLY_CONFIRMED` only for candidate `a0d10d7fd5ff8845d3071b7e68f1500f92fd9563` | Implemented over the existing graph projection | Graph output is derived and read-only; candidate relations are visibly non-established. |
| Semantic Differentiation Lab | `BLOCKED_BY_R2_CONFIRMATION` | No production route. Production model, vector population, EvidenceResolver and R3 are absent. | No placeholder/fake screen may imply availability. |
| Purity view | Current model-independent evaluation only | Existing eight-dimensional evaluation is exposed read-only. Optional future retrieval assistance is not implemented. | Similarity, if later authorized, remains candidate evidence and not confidence/truth. |
| Dependency / provenance views | Current R1/claim contracts | Implemented through graph text fallback and claim provenance/history | Canonical dependency records remain authoritative. |
| Ask Lisan / AI research runtime | Existing `/ask` contract only | Existing found/insufficient/runtime-state behavior is exposed. Hybrid retrieval is not implemented. | AI output does not grant semantic truth, Gate success, review, freshness, or publication. |
