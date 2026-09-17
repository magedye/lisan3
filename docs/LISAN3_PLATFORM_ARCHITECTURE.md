# LISAN 3 Platform Architecture

## Overview
LISAN 3 is governed by a strict, immutable domain-driven design, organized by explicit states and hard boundary layers. No operation can bypass the `backend.domain.services` lifecycle.

## Layer Boundaries
1. **Infrastructure**: Database connections, migrations (`alembic/`), raw ORM interactions (`backend/infrastructure/database.py`).
2. **Domain Models**: Immutable entity schemas defined in `backend/domain/models.py`. Models cannot perform state transitions themselves.
3. **Application Services**: The absolute authority. Located in `backend/domain/services/`. Only these services may mutate governed state.
4. **API / Routing**: Defined in `backend/main.py`. The API translates HTTP requests to service calls. It does not contain business logic.
5. **Campaign Tooling & CLI**: Scripts (`tools/`) and external workflows orchestrate work via API or direct service invocation, but NEVER via direct ORM mapping.
6. **Frontend**: The user interface reads from the API and displays canonical vs. research state correctly.

## Core Services
- **Campaign Orchestrator** (`campaign_state.py`): Explicit state machine handling PLANNED, AUTHORIZED, RUN_CREATED, ISOLATION_ESTABLISHED, etc.
- **Run Admission** (`run_admission.py`): Validates eligibility of a root for campaign inclusion.
- **Isolation** (`isolation.py`): Establishes Blind Lab isolation, records snapshots, locks scopes.
- **Research Judgment** (`research_judgment.py`): Receives AI/human research results, enforces evidence rules.
- **Canonicalization** (`canonicalization.py`): Promotes a VERIFIED claim to canonical knowledge via strict evaluations.
- **Knowledge Graph** (`knowledge_graph.py`): Traces structural origins, derivation paths, and dependency graphs.
- **Methodology Authority** (`methodology_authority.py`): Enforces the governing semantic/Quranic methodology for any research run.

## UX / Frontend
- Strict separation between Arabic root identity and structural Buckwalter forms.
- Distinction between `ACCEPTED` (Canonical), `UNRESOLVED`, and `PENDING` research claims.
- Operator console for campaign administration and review.

## Observability & Audit
- `AuditLog`: Immutable history of all governed entity mutations.
- `tools/validate_closure.py`: Enforces campaign completion integrity before state freeze.
