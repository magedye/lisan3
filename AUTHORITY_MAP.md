# Authority Map

## Precedence Level
1. **Owner Instruction**: Latest explicit owner instruction in chat; `PROMPT/1.MD` is the durable execution request when it does not conflict with a later instruction.
2. **Repository Policy**: Root `AGENTS.md` and applicable scoped `AGENTS.md` files.
3. **Canonical Engineering and Governance References**: `docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md`, `docs/canonical/LISAN_TOOLING_ADOPTION_REFERENCE.md`, and `docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md` within their stated scopes.
4. **Canonical UX/Product Contract**: `ui/Lisanapp Governed UX Constitution & Implementation Reference — النسخة 4.0 (Final).md` for UX and product behavior.
5. **Active Derived Semantic Runtime**: `skills/lisan-semantic-extraction/SKILL.md`, subordinate to higher authority.
6. **Accepted Registries, Schemas, and Backend/API Contracts**: Only artifacts that exist and are accepted within their defined authority.
7. **Approved Plans and Operational State**: Durable plans, then `PROJECT_STATE.md` as non-authoritative resumable context.
8. **Visual and Historical Material**: Stitch prototype exports, legacy reuse material, historical reports, and superseded `main skills/` sources are evidence or reference only.

## Separation of Authority
- Developer permission does not equal epistemic authority.
- Review approval does not equal publication automatically.
- Steward cannot grant semantic lock.
- Backend authorization enforces domain invariants, independent of UI visibility.
- Graph and Vector retrieval outputs are derived candidates; they never become canonical authority without governed Evidence resolution.
