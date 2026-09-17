# LISAN 3 Platform Operations and Recovery

## Campaign Lifecycle
1. Authorized payload and population is placed in `docs/evidence/campaign-manifests/`.
2. Operator uses CLI or `/runs` API to enqueue the population.
3. Orchestrator executes root-by-root, verifying eligibility.
4. Validation via `tools/validate_closure.py` ensures DB matches campaign metrics exactly.

## Database Recovery
If a transaction fails or the orchestrator crashes:
1. `backend.infrastructure.database` uses robust SQLAlchemy session transactions.
2. Uncommitted transactions are automatically rolled back.
3. Restarting the orchestrator will `resume()` from the `CampaignState` table, discovering the exact next uncompleted root.
4. If the local `.db` is corrupted, operator restores from standard SQLite backup and runs `alembic upgrade head`.

## Tooling Hygiene
All `scratch/` scripts used for historical manual ORM simulation are permanently deprecated for production use. They exist purely as historical artifacts and testing boundaries.
