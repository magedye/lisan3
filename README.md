# LISAN3 local startup

Run all backend commands from the repository root. The canonical migration tree
is the root `alembic/` directory; `backend/alembic/` is retained only as legacy
history and is not a valid runtime migration source.

## First-time setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
Set-Location frontend
npm ci
Set-Location ..
```

## Initialize and run

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

In a second PowerShell terminal:

```powershell
Set-Location frontend
$env:BACKEND_URL = "http://127.0.0.1:8000"
npm run dev
```

Open <http://127.0.0.1:3000>. Backend liveness is at `/health`; governed
readiness is at `/operations/health` and returns HTTP 503 when the database is
not at the canonical Alembic head or is missing model tables or columns.

By default both Alembic and the backend use the absolute repository-local
`lisanapp.db`. Set `LISAN_DATABASE_URL` before either command to use another
SQLite database.

## Legacy local database safety

Revision `5542b3a62e23` belongs to the retired pre-V3 migration chain. A database
at that revision cannot be upgraded through the current intentional V3 squash.
Do not delete it and do not run `alembic stamp head`. Preserve it as a backup,
then initialize a new database with the root migration command above. Any data
transfer requires a separate, explicitly governed migration decision.
