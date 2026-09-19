$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot | Split-Path -Parent

function Invoke-Step($label, $workdir, $cmd) {
  Write-Host "=== $label ==="
  Push-Location $workdir
  try {
    Invoke-Expression $cmd
    if ($LASTEXITCODE -ne 0) { exit 1 }
  } finally {
    Pop-Location
  }
}

$BackendVenv = Join-Path $Root "backend\.venv\Scripts"
$Py = if (Test-Path (Join-Path $BackendVenv "python.exe")) { Join-Path $BackendVenv "python.exe" } else { "python" }
$Ruff = if (Test-Path (Join-Path $BackendVenv "ruff.exe")) { Join-Path $BackendVenv "ruff.exe" } else { "ruff" }
$Mypy = if (Test-Path (Join-Path $BackendVenv "mypy.exe")) { Join-Path $BackendVenv "mypy.exe" } else { "mypy" }

Write-Host "=== backend: migrate (idempotent) ==="
Push-Location (Join-Path $Root "backend")
try {
  & $Py -m app.db.migrate; if ($LASTEXITCODE -ne 0) { exit 1 }
} finally {
  Pop-Location
}

Invoke-Step "backend: ruff" (Join-Path $Root "backend") "& `"$Ruff`" check app/ tests/"
Invoke-Step "backend: mypy" (Join-Path $Root "backend") "& `"$Mypy`" app/"
Invoke-Step "backend: pytest" (Join-Path $Root "backend") "& `"$Py`" -m pytest -q"
Invoke-Step "frontend: lint" (Join-Path $Root "frontend") "npm run lint"
Invoke-Step "frontend: build" (Join-Path $Root "frontend") "npm run build"

Write-Host "=== verify: WAL check ==="
Push-Location (Join-Path $Root "backend")
try {
  & $Py -c "import sqlite3; con=sqlite3.connect('artifacts/hireflow.db'); m=con.execute('PRAGMA journal_mode').fetchone()[0]; con.close(); print('journal_mode=' + m); assert m.lower()=='wal'"
  if ($LASTEXITCODE -ne 0) { exit 1 }
} finally {
  Pop-Location
}

Write-Host "verify OK"
