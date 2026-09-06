# Authority Map

## Precedence Level
1. **Owner Instruction**: Latest explicit owner instruction in chat; `PROMPT/1.MD` is the durable execution request when it does not conflict with a later instruction.
2. **Repository Policy**: Root `AGENTS.md` and applicable scoped `AGENTS.md` files.
3. **Canonical Engineering and Governance References**:
   `SIMPLIFIED_AI_AUTHORITY_AND_GOVERNANCE_CONTRACT.md`,
   `docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md`,
   `docs/canonical/LISAN_TOOLING_ADOPTION_REFERENCE.md`,
   `docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`,
   `docs/canonical/ADMISSION_TANZIL.md`,
   `docs/canonical/ADMISSION_QAC.md`,
   `docs/canonical/ADMISSION_MASTER_PACKAGE_V1_0_1.md`, and
   `docs/canonical/LISAN_PURITY_AND_STRUCTURAL_EVIDENCE_CONTRACT.md` within their
   stated scopes.
   - The accepted post-V2.1 owner-directive delta of the Master Integrated
     Package v1.0.1 (`02_CURRENT_OWNER_DIRECTIVES/` INT-* directives, bound by
     `docs/canonical/ADMISSION_MASTER_PACKAGE_V1_0_1.md`) governs where it
     resolves a conflict via `MASTER_SUPERSESSION_MAP.csv`. The package's
     `03_PRE_ANALYSIS/` and proposal registries remain OPEN / non-governing.
     `docs/FOUNDATIONAL_PROFILE_DRAFT.md` is a non-gating consolidation for
     review, not an authority.
4. **Canonical UX/Product Contract**: `ui/Lisanapp Governed UX Constitution & Implementation Reference — النسخة 4.0 (Final).md` for UX and product behavior.
5. **Active Derived Semantic Runtime**: `skills/lisan-semantic-extraction/SKILL.md`, subordinate to higher authority.
6. **Accepted Registries, Schemas, and Backend/API Contracts**: Only artifacts that exist and are accepted within their defined authority.
7. **Approved Plans and Operational State**: Durable plans, then `PROJECT_STATE.md` as non-authoritative resumable context.
8. **Visual and Historical Material**: Stitch prototype exports, legacy reuse material, historical reports, and superseded `main skills/` sources are evidence or reference only.

## Separation of Authority
- Developer permission does not equal epistemic authority.
- AI may issue a traceable `Research Judgment`; that does not equal Canonical
  Project Acceptance.
- Independent verification is required only at canonicalization, not for every
  observation, hypothesis, comparison, or research judgment.
- Steward cannot grant semantic truth or canonical acceptance.
- Backend authorization enforces domain invariants, independent of UI visibility.
- Graph and Vector retrieval outputs are derived candidates; they never become canonical authority without governed Evidence resolution.

## Current semantic-governance boundary

- The current decision-bearing status model is limited to `research_state` and
  `canonical_state`. Result strength and verification are attributes used by
  the canonicalization decision, not parallel workflow axes.
- There is no research `LOCK`, `PURITY_CHECK`, freshness axis, publication axis,
  or owner decision required before a Research Judgment.
- The host resolves active source, methodology, source policy, runtime
  capabilities, and accepted root memory. Caller-supplied authority is never
  authoritative.
- `main skills/` remains historical/reference material. The only active derived
  semantic runtime is `skills/lisan-semantic-extraction/SKILL.md`.
