$ErrorActionPreference = "Continue"
$head_sha = git rev-parse --short HEAD
Write-Output "--- Starting V4 Verification for SHA $head_sha ---"

Write-Output "`n=== PIP CHECK ==="
.venv\Scripts\pip check

Write-Output "`n=== RUFF ==="
.venv\Scripts\ruff check .

Write-Output "`n=== PYRIGHT ==="
npx pyright

Write-Output "`n=== ALEMBIC MIGRATION VERIFICATION ==="
$env:DATABASE_URL = "sqlite:///lisan-v4-test.db"
.venv\Scripts\alembic upgrade head
.venv\Scripts\alembic downgrade base
.venv\Scripts\alembic upgrade head

Write-Output "`n=== NPM AUDIT (FRONTEND) ==="
Push-Location frontend
npm audit
Pop-Location

Write-Output "`n=== ESLINT (FRONTEND) ==="
Push-Location frontend
npm run lint
Pop-Location

Write-Output "`n=== FRONTEND BUILD ==="
Push-Location frontend
npm run build
Pop-Location

Write-Output "`n=== OPENAPI SYNC ==="
.venv\Scripts\python generate_openapi.py
git diff frontend/src/api/openapi.ts

Write-Output "`n=== PYTEST (FULL SUITE, HYPOTHESIS, PLAYWRIGHT, SCHEMATHESIS) ==="
.venv\Scripts\pytest -v

Write-Output "`n--- V4 Verification Complete ---"
