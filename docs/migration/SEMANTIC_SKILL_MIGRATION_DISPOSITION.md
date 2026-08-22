# Semantic Skill Migration Disposition

## Overview
This document records the reconciliation between the **Revised Semantic Runtime Skill** (`SKILL_LISAN_QURANIC_SEMANTIC_EXTRACTION_REVISED.md`) and the **Executive Protocol** (`Lisan Quranic Semantic Extraction — Executive Protocol.md`). 

As dictated by the Canonical Implementation Reference and `PROMPT/1.MD`, the **Revised Skill** is the baseline canonical derived runtime skill. The Executive Protocol is evaluated as a source candidate to migrate non-conflicting material.

## Dispositions

| Area / Feature | Disposition | Rationale |
|---|---|---|
| **Authority Preflight & Limitations** | `KEEP_REVISED` | The Revised Skill explicitly prevents the skill from self-granting authority or fabricating statuses. The Executive Protocol implies some autonomous locking. The Revised approach is strictly safer for a governed system. |
| **Layer Separation (Root + Form + Syntax)** | `KEEP_REVISED` | Both documents share the exact same equation. The Revised Skill's phrasing is maintained. |
| **Coverage Metrics (7 dimensions)** | `KEEP_REVISED` | Both documents share the exact same 7 dimensions of coverage. |
| **Differentiation Axes (14 axes)** | `KEEP_REVISED` | Both documents share the exact same 14 axes. |
| **Falsification & Rejection Condition** | `MERGE_WITH_CLARIFICATION` | Both require `REJECTION_CONDITION`. The Revised Skill's YAML structure for falsification is more precise and will be maintained. |
| **Prohibited Patterns (PM-01 to PM-18)** | `MIGRATE_FROM_EXECUTIVE` | The Executive Protocol provides a very concise and actionable table of prohibited patterns (e.g., Dictionary-First, Contextual Leakage). This will be migrated into the canonical skill. |
| **Presentation Schema (YAML Template)** | `MIGRATE_FROM_EXECUTIVE` | Section 11 of the Executive Protocol defines a clear, uniform YAML output schema (`TARGET`, `CONTRACT_TYPE`, `OFFICIAL_STATUS`, `COVERAGE_PROFILE`, etc.). This structure is migrated as the required output format. |
| **Lock Gate Criteria (Table)** | `DEFER_TO_REGISTRY` | The Executive Protocol hardcodes lock gate criteria (Scope Stability, Coverage, etc.). According to the new architecture, gate definitions must be resolved dynamically from the Registry, so this section is removed from the static skill and deferred to the backend registry logic. |
| **Official Statuses** | `DEFER_TO_REGISTRY` | Both documents list statuses (UNKNOWN, LOCK_BLOCKED). The Revised Skill explicitly notes these must come from `official_statuses_ref`. This delegation is maintained. |

## Conclusion
The new Canonical Skill (`skills/lisan-semantic-extraction/SKILL.md`) will be the Revised Skill, appended with the Presentation Schema and Prohibited Patterns from the Executive Protocol. The original two files in `main skills/` are now marked `SUPERSEDED/MIGRATED`.
