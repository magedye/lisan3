# LISAN3 Stabilization Checkpoint

Status: `IMPLEMENTED` and `TESTED` for implementation candidate
`b95894365e03e49c4a47ad4f489549b55fc34730`.

This checkpoint preserves the completed model-independent R2 work. It does not
select or execute an embedding model, activate production vector population,
start R3 or V4, establish independent review, or grant release acceptance.

## Initial repository state

- Root: `D:\APP\tafseer\lisanapp3`
- Branch: `main`, tracking `origin/main`, initially ahead by 18 commits
- Initial HEAD: `1b1c0dbef1860112e8b1b757144457fe356598a0`
- Initial worktree: only owner files `check_db2.py` and `debug_proxy.py` were
  untracked; both remained untouched and uncommitted.

## Database root cause and classification

- The backend configured `sqlite:///./lisanapp.db`, so its target depended on
  the process working directory. Root Alembic also used a relative URL.
- The active runtime file was
  `D:\APP\tafseer\lisanapp3\lisanapp.db`, with 8 application tables and
  `alembic_version=5542b3a62e23`.
- Revision `5542b3a62e23` belongs to the retained `backend/alembic/` legacy
  chain. Its history reaches the governed baseline
  `0e5f256deede286252c299aa2541ea5a8a6b0753`; it is not an ancestor in the
  canonical root Alembic graph.
- The canonical root graph is the intentional V3 squash and forward chain:
  `80330541af56 -> f4c0a1b2c3d4 -> b7e4c1d9a5f2 -> c9e2a7f4b6d1`.
- Therefore the old local DB is `STALE_CONTEXT`, not evidence of a missing
  repository migration. Separately, the cwd-relative URL, no-op startup hook,
  and unconditional healthy readiness response were a `PRODUCT_DEFECT` because
  they concealed that stale state while `/audit` failed with HTTP 500.
- No database was deleted and `alembic stamp` was never used. The legacy DB was
  moved intact to
  `local-state-backups/lisanapp.pre-v3-5542b3a62e23.20260825.db`.

## Frontend and Stitch reconciliation

Production App Router inventory after reconciliation:

- `/`
- `/audit`
- `/governance`
- `/steward`
- `/run/[id]`
- `/run/[id]/blind`
- `/run/[id]/knowledge`
- `/claims/[id]`

The Stitch source inventory is retained under
`ui/stitch_lisanapp_governed_research_prototype -complete/`:

- 28 page-reference pairs (`code.html` plus `screen.png`): anonymous `_1`
  through `_18`, plus `audit_log`, `blind_lab`, `hypothesis_lab`,
  `res_home_01_golden`, `res_root_01_golden`, `res_root_01_golden_final`,
  `semantic_differentiation_lab`, `stale`, `steward_global_command_drawer`, and
  `ui_contract_gap_register`.
- One design directory, `lisanapp_governed_research_system/DESIGN.md`.
- Four root references: reconciled Golden design, design-system handover, UX
  Constitution implementation reference, and gap-closure prompt.

No production Stitch component or copied Stitch asset existed in current Git or
its reachable history. The original `/` scaffold was the minimal Ask Lisan page
from baseline commit `0e5f256...`; it was not a recently deleted Golden page.
The production public assets were only the five default Next SVG files.

The minimal reconciliation adds a reusable Arabic RTL Golden shell, turns `/`
into the truthful Attention Center while preserving the real Ask/Create Run
flow, and adds `/audit` against the existing read-only backend contract. It does
not copy remote fonts/images, invent dashboard counts, or reproduce prototype
fixture data. Where no Attention Center read contract exists, the UI says so.

## Runtime and artifact cleanup

- Replaced the cwd-relative backend default with the absolute repository-local
  SQLite path; `LISAN_DATABASE_URL` remains an explicit SQLite override.
- Root Alembic normalizes only its default URL, preserving programmatic URLs for
  isolated tests.
- `/operations/health` now compares the active revision, model tables, and model
  columns to canonical Alembic heads and returns HTTP 503 with
  `BLOCKED_SCHEMA` on mismatch. `/health` remains liveness.
- Removed the no-op table-creation startup hook and documented reproducible
  PowerShell initialization/startup in the root README.
- Stopped only the verified project Uvicorn/Next processes on ports 8000, 8765,
  and 3000. The old ignored `e2e_test.db` was preserved at
  `local-state-backups/e2e_test.legacy-d7e1917cbc59.20260825.db`.
- A fresh local `alembic upgrade head` created `lisanapp.db` at
  `c9e2a7f4b6d1`; inspection reports `CURRENT`, no missing tables, and no missing
  columns.
- Existing ignored dependency/build caches (`.venv`, `node_modules`, `.next`,
  pytest/Ruff/Hypothesis caches) were audited and left reusable; they are not
  source artifacts or runtime blockers. The temporary verification worktree
  and its generated dependencies/database/build were removed after verification.

## Regression coverage

- `tests/test_runtime_database.py` proves the default DB path is repository
  absolute, a fresh migrated DB matches the current models, and legacy
  `5542b3a62e23` is reported without mutation.
- Slice G health coverage now requires a current database schema.
- Journey 7 verifies the Golden navigation and Attention Center, then reads a
  real persisted audit event through `/audit`.
- Existing frontend `any` lint failures were replaced mechanically with
  generated OpenAPI types or narrow local response shapes; behavior was not
  redesigned.

## Clean-checkout verification

Detached worktree candidate:
`b95894365e03e49c4a47ad4f489549b55fc34730`.

- Fresh `npm ci`: 480 packages installed from lockfile; 0 vulnerabilities.
- Fresh DB: all four canonical migrations applied; head `c9e2a7f4b6d1`;
  revision/table/column status `CURRENT`; Alembic drift test reported no new
  upgrade operations.
- Full pytest: 134 passed, including all seven Playwright journeys.
- Ruff: passed.
- Pyright: 0 errors and 145 existing non-blocking SQLAlchemy-style warnings.
- `pip check`: no broken requirements.
- ESLint: passed.
- Next production build: passed and emitted all eight production routes.
- `npm audit --omit=dev`: 0 vulnerabilities.
- Live clean-worktree backend: `/health`, `/operations/health`, and `/audit`
  returned HTTP 200; readiness reported the exact clean-worktree DB as
  `CURRENT`.
- Live production Next server: all eight routes returned HTTP 200. Chromium
  verified the Golden home and audit headings, captured a 1440x1000 screenshot,
  and reported zero console errors.
- Final verification worktree Git status was clean before removal.

## Remaining status boundary

No unexplained local runtime blocker remains for a fresh SQLite initialization,
backend startup, production frontend startup, or current production routes.
The 145 Pyright warnings and SQLAlchemy `datetime.utcnow()` deprecation warnings
remain non-blocking pre-existing quality debt. This checkpoint is not an
independent review and does not change the R2/R3/V4/model boundary.
