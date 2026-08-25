# UI Backend Contract Matrix

| UI ID | Canonical Name | Status | Route | Role | Read Model/Query | Commands | Backend Contract | Schema | Auth | Loading | Empty | Error | AI States | Implementation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `res_home_01_golden` | Ask Lisan | Golden | `/` | All | `AskLisan`; `GetAttentionCenter` unavailable | `CreateResearchRun` | `AskLisanRequest` / `AskLisanResponse`; `ResearchRunCreate` | `SemanticClaimResponse`; `ResearchRunResponse` | None | Yes | Yes | Yes | `AI_PROCESSING`, `AI_UNAVAILABLE` | Implemented and tested for the Arabic RTL shell plus real Ask/Create Run flow; the Attention Center read model and full Golden/Stitch completion are not claimed. |
| `res_root_01_golden_final` | Semantic Research | Golden | `/run/[id]` | All | `GetResearchRun` | `SubmitGateReport`, `CreateClaim` | `GateReportCreate`, `SemanticClaimCreate` | `ResearchRun` | None | Yes | Yes | Yes | `ARTIFACT_GENERATED` | Pending |
| `blind_lab` | Blind Lab Isolation | Golden | `/run/[id]/blind` | All | `GetIsolationState` | `RecordObservation` | `ObservationArtifact` | `Observation` | None | Yes | Yes | Yes | `TOOL_UNAVAILABLE` | Pending |
| `steward_drawer` | Steward Command | Golden | `/steward` | All | `GetRuleRegistry` | `CreateChangeProposal` | `ChangeProposal` | `Rule` | None | Yes | Yes | Yes | `AI_OUTPUT_INVALID` | Pending |
| `audit_log` | Audit Trail | Golden | `/audit` | All | `ListAuditLogs` (`GET /audit`) | None | `AuditLogResponse[]` | `AuditLog` | None | Yes | Yes | Yes | `EVIDENCE_RESOLUTION_PENDING` | Implemented and tested as a read-only list with loading, empty, and error states; full Golden/Stitch completion is not claimed. |

*Note: Roles and Auth are mocked or handled natively as domain invariants due to the trusted single-user monolith architecture. AI States represent runtime conditions, not official epistemic statuses.*

## Planned Hybrid Retrieval Mappings

The mappings below retain their phase-specific status. Knowledge Explorer R1
is independently confirmed only for candidate
`a0d10d7fd5ff8845d3071b7e68f1500f92fd9563`. Entries marked `R1/R3`, `R2/R3`,
or otherwise planned do not claim completion beyond the explicitly evidenced
phase and candidate.

| Golden capability | Phase | Planned backend/read-model scope | Authority boundary |
|---|---|---|---|
| Knowledge Explorer | `R1_INDEPENDENTLY_CONFIRMED` for `a0d10d7fd5ff8845d3071b7e68f1500f92fd9563` | Graph projection; `KnowledgeNode` / `KnowledgeEdge`; NetworkX analysis; provenance; React Flow visualization | Graph output is derived and read-only; candidate relations are visibly non-established. |
| Semantic Differentiation Lab | `R2/R3 — PLANNED` | Vector discovery; embedding-space identity; `RetrievalCandidate`; `EvidenceResolver` | Candidates require governed Evidence resolution. |
| Purity Detector | `R2/R3 — OPTIONAL_ASSISTANCE_PLANNED` | Exact-source comparison and vector candidate similarity | Vector output is candidate evidence only. |
| Dependency / Provenance Views | `R1/R3 — PLANNED` | Governed graph projection; graph paths; source-layer provenance | Canonical dependency records remain authoritative. |
| Ask Lisan / AI Research Runtime | `R3 — PLANNED` | Exact Retrieval; Vector Candidate Discovery; Graph Candidate Retrieval; `EvidenceResolver` | Retrieval does not grant semantic truth, Gate success, or publication. |
