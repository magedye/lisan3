# UI Backend Contract Matrix

| UI ID | Canonical Name | Status | Route | Role | Read Model/Query | Commands | Backend Contract | Schema | Auth | Loading | Empty | Error | AI States | Implementation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `res_home_01_golden` | Ask Lisan | Golden | `/` | All | `GetAttentionCenter` | `CreateResearchRun` | `ResearchRunCreate` | `ResearchRun` | None | Yes | Yes | Yes | `AI_PROCESSING`, `AI_UNAVAILABLE` | Pending |
| `res_root_01_golden_final` | Semantic Research | Golden | `/run/[id]` | All | `GetResearchRun` | `SubmitGateReport`, `CreateClaim` | `GateReportCreate`, `SemanticClaimCreate` | `ResearchRun` | None | Yes | Yes | Yes | `ARTIFACT_GENERATED` | Pending |
| `blind_lab` | Blind Lab Isolation | Golden | `/run/[id]/blind` | All | `GetIsolationState` | `RecordObservation` | `ObservationArtifact` | `Observation` | None | Yes | Yes | Yes | `TOOL_UNAVAILABLE` | Pending |
| `steward_drawer` | Steward Command | Golden | `/steward` | All | `GetRuleRegistry` | `CreateChangeProposal` | `ChangeProposal` | `Rule` | None | Yes | Yes | Yes | `AI_OUTPUT_INVALID` | Pending |
| `audit_log` | Audit Trail | Golden | `/audit` | All | `GetAuditTrail` | None | `AuditEvent` | `Audit` | None | Yes | Yes | Yes | `EVIDENCE_RESOLUTION_PENDING` | Pending |

*Note: Roles and Auth are mocked or handled natively as domain invariants due to the trusted single-user monolith architecture. AI States represent runtime conditions, not official epistemic statuses.*

## Planned Hybrid Retrieval Mappings

The following mappings are planned only. They do not claim any R1, R2, or R3
implementation exists.

| Golden capability | Phase | Planned backend/read-model scope | Authority boundary |
|---|---|---|---|
| Knowledge Explorer | `R1 — PLANNED / ACTIVATION_ALLOWED_POST_V3` | Graph projection; `KnowledgeNode` / `KnowledgeEdge`; NetworkX analysis; provenance; React Flow visualization | Graph output is derived and read-only. |
| Semantic Differentiation Lab | `R2/R3 — PLANNED` | Vector discovery; embedding-space identity; `RetrievalCandidate`; `EvidenceResolver` | Candidates require governed Evidence resolution. |
| Purity Detector | `R2/R3 — OPTIONAL_ASSISTANCE_PLANNED` | Exact-source comparison and vector candidate similarity | Vector output is candidate evidence only. |
| Dependency / Provenance Views | `R1/R3 — PLANNED` | Governed graph projection; graph paths; source-layer provenance | Canonical dependency records remain authoritative. |
| Ask Lisan / AI Research Runtime | `R3 — PLANNED` | Exact Retrieval; Vector Candidate Discovery; Graph Candidate Retrieval; `EvidenceResolver` | Retrieval does not grant semantic truth, Gate success, or publication. |
