# UI Backend Contract Matrix

| UI ID | Canonical Name | Status | Route | Role | Read Model/Query | Commands | Backend Contract | Schema | Auth | Loading | Empty | Error | AI States | Implementation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `res_home_01_golden` | Ask Lisan | Golden | `/` | All | `GetAttentionCenter` | `CreateResearchRun` | `ResearchRunCreate` | `ResearchRun` | None | Yes | Yes | Yes | `AI_PROCESSING`, `AI_UNAVAILABLE` | Pending |
| `res_root_01_golden_final` | Semantic Research | Golden | `/run/[id]` | All | `GetResearchRun` | `SubmitGateReport`, `CreateClaim` | `GateReportCreate`, `SemanticClaimCreate` | `ResearchRun` | None | Yes | Yes | Yes | `ARTIFACT_GENERATED` | Pending |
| `blind_lab` | Blind Lab Isolation | Golden | `/run/[id]/blind` | All | `GetIsolationState` | `RecordObservation` | `ObservationArtifact` | `Observation` | None | Yes | Yes | Yes | `TOOL_UNAVAILABLE` | Pending |
| `steward_drawer` | Steward Command | Golden | `/steward` | All | `GetRuleRegistry` | `CreateChangeProposal` | `ChangeProposal` | `Rule` | None | Yes | Yes | Yes | `AI_OUTPUT_INVALID` | Pending |
| `audit_log` | Audit Trail | Golden | `/audit` | All | `GetAuditTrail` | None | `AuditEvent` | `Audit` | None | Yes | Yes | Yes | `EVIDENCE_RESOLUTION_PENDING` | Pending |

*Note: Roles and Auth are mocked or handled natively as domain invariants due to the trusted single-user monolith architecture. AI States represent runtime conditions, not official epistemic statuses.*
