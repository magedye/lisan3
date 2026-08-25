# Stitch Production Coverage Matrix

Status date: 2026-08-25. This matrix is descriptive evidence, not a new
authority source. Canonical product, UX, registry, and status contracts retain
precedence. The inspected asset root is:

`ui/stitch_lisanapp_governed_research_prototype -complete/stitch_lisanapp_governed_research_prototype`

Every listed screen has both `<screen-id>/code.html` and
`<screen-id>/screen.png`, except that `_17/screen.png` is a 28-byte invalid
image. The HTML remains inspectable and the screen is superseded by the valid
`res_root_01_golden_final` pair.

## Classification Inventory

Each of the 28 matched Golden pairs has exactly one classification. A
`CURRENT_BACKEND_GAP` row records the classification at inventory time; its
resolution is stated separately and does not rewrite the historical finding.

| Screen ID / name | Purpose | Golden HTML | Screenshot | Classification | Resolution / reason |
|---|---|---|---|---|---|
| `_1` — Main Operations | Attention/home concept | `_1/code.html` | `_1/screen.png` | `REFERENCE_ONLY_OR_SUPERSEDED` | Superseded by `res_home_01_golden`. |
| `_2` — Governed Ask | Ask-result concept | `_2/code.html` | `_2/screen.png` | `REFERENCE_ONLY_OR_SUPERSEDED` | Absorbed by the canonical Home Ask flow. |
| `_3` — Root Workspace Blocked | Blocked root state | `_3/code.html` | `_3/screen.png` | `REFERENCE_ONLY_OR_SUPERSEDED` | Superseded by the final Root pair and governed blocked state. |
| `_4` — Quality and Purity | Eight-dimensional purity view | `_4/code.html` | `_4/screen.png` | `CURRENT_EXECUTABLE` | Implemented on the claim traceability route. |
| `_5` — Root Workspace Blocked | Blocked root variant | `_5/code.html` | `_5/screen.png` | `REFERENCE_ONLY_OR_SUPERSEDED` | Duplicate Root-state reference. |
| `_6` — Quality and Purity | Purity variant | `_6/code.html` | `_6/screen.png` | `REFERENCE_ONLY_OR_SUPERSEDED` | Superseded by `_4`. |
| `_7` — Research Workspace | Run workspace variant | `_7/code.html` | `_7/screen.png` | `REFERENCE_ONLY_OR_SUPERSEDED` | Absorbed by `res_root_01_golden_final` and `_18`. |
| `_8` — Governance Center | Rules, proposals, impact and review | `_8/code.html` | `_8/screen.png` | `CURRENT_EXECUTABLE` | Existing governed commands plus real overview read model. |
| `_9` — Knowledge Explorer | Derived graph variant | `_9/code.html` | `_9/screen.png` | `REFERENCE_ONLY_OR_SUPERSEDED` | Superseded by `_10`. |
| `_10` — Knowledge Explorer | Derived graph and text provenance | `_10/code.html` | `_10/screen.png` | `CURRENT_EXECUTABLE` | Implemented over independently confirmed R1 contracts. |
| `_11` — Analytics Dashboard | Operational attention counts | `_11/code.html` | `_11/screen.png` | `CURRENT_BACKEND_GAP` | Resolved by `GET /attention`; no inferred metrics. |
| `_12` — Governed Ask | Ask-result variant | `_12/code.html` | `_12/screen.png` | `REFERENCE_ONLY_OR_SUPERSEDED` | Absorbed by Home. |
| `_13` — Main Operations | Home variant | `_13/code.html` | `_13/screen.png` | `REFERENCE_ONLY_OR_SUPERSEDED` | Superseded by `res_home_01_golden`. |
| `_14` — Research Run Builder | Create a governed run | `_14/code.html` | `_14/screen.png` | `CURRENT_EXECUTABLE` | Uses existing `POST /runs` with explicit user inputs. |
| `_15` — Resources and Admission | Corpus authority/lifecycle | `_15/code.html` | `_15/screen.png` | `CURRENT_BACKEND_GAP` | Resolved read-only in `GET /governance/overview`. |
| `_16` — Review Queue | Review and freshness attention | `_16/code.html` | `_16/screen.png` | `CURRENT_BACKEND_GAP` | Resolved read-only in `GET /governance/overview`. |
| `_17` — Root Workspace Blocked | Corrupt screenshot variant | `_17/code.html` | `_17/screen.png` (invalid) | `REFERENCE_ONLY_OR_SUPERSEDED` | Valid final Root assets supersede it. |
| `_18` — Research Run Detail | Run context, artifacts and Gates | `_18/code.html` | `_18/screen.png` | `CURRENT_BACKEND_GAP` | Resolved by `GET /runs/{run_id}/workspace`. |
| `audit_log` — Audit Log | Read-only audit trail and filtering | `audit_log/code.html` | `audit_log/screen.png` | `CURRENT_EXECUTABLE` | Implemented over `GET /audit`. |
| `blind_lab` — Blind Lab | Isolation preflight and observations | `blind_lab/code.html` | `blind_lab/screen.png` | `CURRENT_EXECUTABLE` | Implemented without simulation actions. |
| `hypothesis_lab` — Hypothesis Lab | Observation/hypothesis comparison | `hypothesis_lab/code.html` | `hypothesis_lab/screen.png` | `CURRENT_BACKEND_GAP` | Resolved in the governed run workspace aggregate. |
| `res_home_01_golden` — Attention Center | Canonical Home, Ask and resume | `res_home_01_golden/code.html` | `res_home_01_golden/screen.png` | `CURRENT_BACKEND_GAP` | Resolved by `GET /attention`. |
| `res_root_01_golden` — Root Workspace | Earlier Golden Root pair | `res_root_01_golden/code.html` | `res_root_01_golden/screen.png` | `REFERENCE_ONLY_OR_SUPERSEDED` | Superseded by the `_final` pair. |
| `res_root_01_golden_final` — Root Workspace | Canonical governed run workspace | `res_root_01_golden_final/code.html` | `res_root_01_golden_final/screen.png` | `CURRENT_BACKEND_GAP` | Resolved by the fail-closed workspace read model. |
| `semantic_differentiation_lab` — Semantic Differentiation | Vector discovery and governed resolution | `semantic_differentiation_lab/code.html` | `semantic_differentiation_lab/screen.png` | `BLOCKED_BY_R2_CONFIRMATION` | Requires adopted production model, vector runtime, EvidenceResolver and R3; no shell was fabricated. |
| `stale` — Non-current Claim | Stale/revalidation state | `stale/code.html` | `stale/screen.png` | `CURRENT_EXECUTABLE` | Implemented as an explicit warning plus history/provenance. |
| `steward_global_command_drawer` — Steward | Preview, authority, confirm, execute | `steward_global_command_drawer/code.html` | `steward_global_command_drawer/screen.png` | `CURRENT_EXECUTABLE` | Implemented with user-entered commands and backend validation. |
| `ui_contract_gap_register` — Contract Gap Register | Design-time inventory aid | `ui_contract_gap_register/code.html` | `ui_contract_gap_register/screen.png` | `REFERENCE_ONLY_OR_SUPERSEDED` | Replaced by this durable repository matrix; it is not a production route. |

Classification count: 8 `CURRENT_EXECUTABLE`, 7 `CURRENT_BACKEND_GAP`,
1 `BLOCKED_BY_R2_CONFIRMATION`, 0 `BLOCKED_BY_MODEL_ARTIFACT`, and 12
`REFERENCE_ONLY_OR_SUPERSEDED` (28 total).

## Production Mapping and Evidence

| Screen | Production route / reusable components | Backend dependency | Phase / model dependency | Visual status | Interaction status | Real-data status | Tests | Exact missing work / evidence |
|---|---|---|---|---|---|---|---|---|
| `_1`, `_13`, `res_home_01_golden` | `/`; `AppShell`, `PageHeader`, metric/list/Ask/Run Builder primitives | `GET /attention`, `POST /ask`, `POST /runs` | Current; none | Golden system implemented; canonical pair drives layout | Ask, resume and create-run pass | Persisted rows only; explicit fixture labels in E2E | Journeys 1, 7, 8; `test_ui_read_models.py` | No current-scope gap. Duplicate pairs remain references. |
| `_2`, `_12` | `/`; Home Ask result and four-axis status component | `POST /ask` | Current; AI states remain runtime states | Absorbed into canonical Home | Found/insufficient/error paths implemented | Backend response only | Journeys 1 and 7; status-axis tests | No separate route is warranted. |
| `_3`, `_5`, `_17`, `res_root_01_golden` | `/run/[id]`; blocked-state primitives | Workspace aggregate | Current; none | Superseded/absorbed; `_17` screenshot invalid | Blocked paths fail visibly | Real run/isolation/Gate state | Journeys 1 and 8 | No separate implementation; final pair is canonical. |
| `_4`, `_6` | `/claims/[id]`; `StatusAxes`, evidence columns, finding cards | Claim, quality, manifest, provenance, history reads | Current; no model required for existing purity evaluation | Golden quality language/system implemented | Read and details interactions pass | Persisted claim evidence; derived read-only purity result | Journey 3; Journey 8 | `_6` is reference-only. |
| `_7`, `_18`, `hypothesis_lab`, `res_root_01_golden_final` | `/run/[id]`; context strip, stage sequence, tabs, artifact/Gate/claim cards | `GET /runs/{run_id}/workspace` | Current; no model | Golden final structure implemented responsively | Tabs, navigation, blocked/released states pass | Persisted run artifacts; claims fail closed until CLEAN + Internal Lock | Journeys 1, 2, 8; read-model tests | Inventory-time backend gap is resolved. |
| `_8` | `/governance`; forms, queues, confirmation dialog | Overview + existing rule/proposal/impact/history commands | Current; none | Golden governance system implemented | Create/propose/impact/approve/history pass | Persisted rules, proposals, claims, snapshots | Journey 4 | No current-scope gap. |
| `_9`, `_10` | `/run/[id]/knowledge`; React Flow plus text provenance fallback | Existing R1 graph projection/rebuild/explorer | R1 independently confirmed; no production model | Golden explorer implemented | Rebuild/read/blocked states pass | Derived, read-only, visibly non-authoritative graph | Journey 6 | `_9` remains a duplicate reference. |
| `_11` | `/`; attention metric grid | `GET /attention` | Current; none | Golden operational dashboard language implemented | Read/retry/empty states pass | Counts are direct persisted-query results | Journeys 7 and 8; read-model tests | Inventory-time gap resolved; no speculative analytics added. |
| `_14` | `/`; Run Builder | Existing `POST /runs` | Current; none | Golden builder absorbed into Home | Validation and create/navigation pass | User supplies methodology and corpus IDs; no hardcoded demo values | Journey 1 | No separate route needed. |
| `_15` | `/governance`; corpus authority cards | `GET /governance/overview` | Current; none | Golden resource-admission semantics implemented | Read/empty/error paths pass | Six independent persisted lifecycle axes | Read-model tests; build/lint | Inventory-time gap resolved read-only. |
| `_16` | `/governance`; review queue and four-axis cards | `GET /governance/overview` | Current; none | Golden review queue implemented | Read/empty/error paths pass | Persisted independent axes | Journey 4; read-model tests | Inventory-time gap resolved. Review mutation remains on existing governed contracts only. |
| `audit_log` | `/audit`; filters, `EntityLink`, table states | `GET /audit?entity_type&entity_id` | Current; none | Golden audit layout implemented | Filter/reset/link paths pass | AuditLog rows only | Journeys 5, 7, 8 | No mutation is exposed. |
| `blind_lab` | `/run/[id]/blind`; preflight banner, observation form | Existing isolation, corpus and observation contracts | Current; none | Golden isolation system implemented | Preflight, record and contamination distinction pass | Persisted snapshot occurrences and isolation state | Journey 2 | No simulation button or forbidden bypass action remains. |
| `semantic_differentiation_lab` | No production route/component | Future governed retrieval contract | R2 confirmation + production model + EvidenceResolver + R3 required | Intentionally absent | Blocked | No eligible production data/provider | Classification review only | Exact dependency is outside this task; no fake UI or `LISAN-Quran-Embedding` access. |
| `stale` | `/claims/[id]`; warning, axes, history/provenance | Claim/history/provenance reads | Current; none | Golden non-current warning implemented | Read/history paths pass | Persisted freshness and audit events | Journey 8 | No current-scope gap. |
| `steward_global_command_drawer` | `/steward`; preview, authority panel, confirmation dialog, result/audit table | Existing Steward preview/execute/audit contracts | Current; none | Golden drawer intent rendered as responsive page workflow | Allowed and forbidden commands pass | User-entered command payloads; backend result/audit only | Journey 5 | No semantic truth or Gate authority is granted. |
| `ui_contract_gap_register` | No production route; repository matrix | None | Design-time reference | Superseded by durable Markdown evidence | Not applicable | Not application data | Inventory/parity review | This document is the maintained replacement. |

## Cross-Cutting Verification

- RTL is native at the document and shell level; responsive desktop/tablet/mobile
  layout uses logical CSS properties and a non-intercepting off-canvas menu.
- All four canonical axes use separate labels and values. Stage progression,
  quality/purity, retrieval similarity, and AI runtime state are not presented
  as epistemic authority.
- Loading, empty, error, blocked, stale, contamination, and confirmation states
  are explicit. Forms have programmatic labels and stable `id` or `name`
  attributes; tabs and dialogs use native/ARIA semantics.
- Full Playwright evidence at the implementation checkpoint: 8 passed. Focused
  production read-model/status tests: 8 passed. ESLint and the Next production
  build pass. Exact candidate-bound detached evidence is recorded in
  `LISAN3_UI_COMPLETION_CHECKPOINT.md` after candidate verification.
