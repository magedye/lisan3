# Lisanapp Canonical Implementation Reference

Authority revision: `LISAN3_CANONICAL_IMPLEMENTATION_V3_2026_09_06`

The current AI authority and semantic-governance boundary is owned by
[`SIMPLIFIED_AI_AUTHORITY_AND_GOVERNANCE_CONTRACT.md`](../../SIMPLIFIED_AI_AUTHORITY_AND_GOVERNANCE_CONTRACT.md).
Tool adoption and hybrid retrieval remain governed by their existing canonical
references and are not changed by this revision.

## Product and architecture

Lisanapp is a modular-monolith Quranic semantic research application:

- backend: Python, FastAPI, SQLAlchemy, Pydantic v2, SQLite;
- frontend: Next.js, TypeScript, Tailwind CSS, RTL logical properties;
- boundary: REST/OpenAPI with generated TypeScript contracts;
- identity: trusted local single-user runtime with server-owned domain actions.

The UI cannot write canonical knowledge directly. Canonical mutation passes
through server-side validation, policy, persistence, and audit.

## Authority

The latest owner instruction and `AUTHORITY_MAP.md` govern precedence. The
active semantic runtime is `skills/lisan-semantic-extraction/SKILL.md` as a
derived instruction artifact; it cannot redefine source or project authority.
Historical `main skills/` files are reference only.

## Minimal semantic status model

Workflow checkpoints do not grant authority. A persisted semantic result has:

- `research_state`: `PREFERRED`, `UNRESOLVED`, or `REJECTED`;
- `canonical_state`: `NOT_CANONICAL`, `ACCEPTED`, or `REOPEN_REQUIRED`;
- `result_strength`: `WEAK`, `MODERATE`, `STRONG`, or `UNRESOLVED`;
- `verification_state`: `NOT_REQUIRED`, `NOT_VERIFIED`, or `VERIFIED`;
- `falsification_status`: `NOT_REQUIRED`, `NOT_RUN`, `PASSED`, or `FAILED`.

Only the first two are decision-bearing status axes. Strength, verification,
falsification, and host-derived completeness are explicit qualification facts.
There is no semantic-research lock, Purity gate, freshness axis, publication
axis, or review axis.

## Research and canonical authority

AI is a primary research actor and may persist a `Research Judgment` after
deterministic validation. It may not set `canonical_state=ACCEPTED`.

Canonicalization is one explicit server-owned transition. It requires a strong
preferred current-revision result, sufficient claim-sensitive coverage,
resolvable evidence and counterevidence treatment, passed falsification,
independent verification, current source/method bindings, clean source
isolation, and explicit trusted-local authorization. Failure returns exact
reasons and changes no canonical state.

A material new evidence record or affected governing revision changes an
accepted result to `REOPEN_REQUIRED`; it is then excluded from accepted-memory
retrieval until verified and accepted again. No silent mutation is permitted.

## Provenance and evidence

Every important result traces through:

`Research Judgment -> evidence/counterevidence -> run -> corpus snapshot -> methodology revision`

AI executions additionally record provider/model, skill revision, real tool
availability, input/output artifact references, status, and error. Hidden
chain-of-thought is never stored. Simulated tools or model memory are not
evidence.

Metadata is retained only when used for lineage, reproduction, authorization,
or a current decision.

## Source and methodology authority

- The canonical Quran snapshot controls text and verse identity. Research-run
  admission accepts only authority-verified, production-active snapshots.
- The active methodology source is immutable per registered revision and bound
  to the exact `skills/lisan-semantic-extraction/SKILL.md` SHA-256.
- The host selects the current eligible source and methodology. Optional caller
  hints are validated but never grant authority.
- Internal Quranic induction receives only admitted Quran data and same-run
  artifacts. External semantic sources and prior answers are excluded by
  context/tool permissions, not merely by prompt wording.
- Accepted project knowledge may be retrieved for answering or later
  comparison, but never counts as primary Quranic evidence.

Tanzil and QAC admission/activation boundaries remain owned by
`docs/canonical/ADMISSION_TANZIL.md` and `docs/canonical/ADMISSION_QAC.md`.
This revision does not admit, activate, or redesign either corpus layer.

## Coverage, falsification, and semantic layers

The host derives coverage from persisted corpus/observation evidence. A claim
over all occurrences requires complete indexed coverage. Deep analysis may be
a justified representative sample when the declared claim scope permits it;
local claims require the exact local occurrence. AI cannot self-certify counts.

Preferred important conclusions require a structured rejection condition and
a passed falsification attempt. Observations and exploratory hypotheses do not.

Semantic analysis preserves this attribution order:

`root -> derivation/inflection -> lexeme -> form -> construction -> local form/roles -> context/discourse -> local meaning -> final statement`

The UI may abbreviate layers that do not affect the answer, but the persisted
judgment records the material layer attribution.

## Diagnostics

The eight historical Purity dimensions remain diagnostics. Unsupported
diagnostics are `NOT_EVALUATED`, not fake passes and not generic research
blockers. A finding becomes hard only when it proves a current hard-boundary
violation such as actual prohibited-source exposure, unresolved asserted
evidence, circular primary support, or unsupported generalization. The detailed
boundary is in `LISAN_PURITY_AND_STRUCTURAL_EVIDENCE_CONTRACT.md`.

## Change control and migrations

Governing revisions are append-oriented; affected accepted results are reopened
with audit evidence. Schema changes use incremental reversible Alembic
migrations. Existing migration files are not rewritten.

## Claim and release discipline

Keep implementation, tests, profile verification, technical release readiness,
independent review, and release acceptance distinct. The implementing agent
cannot self-grant independent review or release acceptance.
