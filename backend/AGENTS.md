# Lisanapp Backend Policy

This file supplements the root `AGENTS.md` for work under `backend/`.

## Architecture

Preserve the trusted local single-user modular-monolith architecture.

Current baseline:
- Python
- FastAPI
- Pydantic v2
- SQLAlchemy 2
- Alembic
- SQLite
- Pydantic AI where adopted by canonical tooling policy

Do not introduce microservices, distributed queues, authentication systems,
or remote infrastructure without an approved requirement.

## Layer Boundaries

Keep HTTP routes thin.

Canonical mutations should follow the established application/domain boundary:

`HTTP → application command/service → domain validation → persistence → audit`

Do not place semantic authority or lifecycle rules directly in route handlers
when they belong to domain/application policy.

Queries/read models must not mutate canonical knowledge.

## Domain Integrity

Do not trust state supplied by the client merely because it passed Pydantic.

Enforce semantic and governance invariants in domain/application logic.

Official states and Gate definitions must resolve from canonical contracts
or registries rather than duplicated literals.

Analysis stage is not an epistemic state.

Keep Epistemic, Review, Freshness, and Publication independent.

## AI

AI is a governed exploratory runtime.

Model output must pass:
`structured output → schema validation → domain validation → evidence resolution`

AI must not:
- invent canonical Evidence;
- assign official states directly;
- grant Gate PASS;
- grant Internal Lock;
- publish;
- bypass Blind Lab isolation.

Fake/test provider results remain test evidence only.

## Corpus

Canonical Quranic evidence must come through admitted Corpus artifacts.

Do not use model memory as canonical Quran evidence.

Test fixtures must remain distinguishable from production Corpus artifacts.

Rejected auxiliary semantic fields must not enter Blind Lab evidence.

## Persistence

Durable research state must survive process/chat loss.

Use Alembic for durable schema changes.

Do not silently replace migration history.
Pre-release migration squashing requires an explicit documented decision.

## Backend Verification

For affected work use the smallest appropriate combination of:
- pytest
- Hypothesis
- Ruff
- Pyright
- migration-from-zero checks
- OpenAPI generation
- Schemathesis when its adoption trigger applies
- focused mutation testing when required

A configured tool is not execution evidence.
