# HireFlow — AI Candidate Screening & Interview Intelligence (MVP)

> B0 Foundation: repo scaffolding, FastAPI+Pydantic v2 backend shell,
> Vite+React+Tailwind frontend shell, SQLite WAL+JSON+FTS5 + JSONL ledger,
> artifacts dir, server-only secrets, 5 config files. `make verify` gates B0.

## Source of truth (read before coding)

1. `MASTER.md` — living source of truth (frozen §§38/39/40/58/59/63/64)
2. `HireFlow_Architecture_Design_Report.md` — normative §§1-23
3. `hireflow_research.md` — evidence base only, cite by §
4. `AGENTS.md` — repo rules for coding agents
5. `docs/superpowers/plans/2026-09-20-B0-Foundation.md` — B0 build plan

`MASTER.md` wins on conflicts (Report §2.1).

## Quickstart (B0)

```bash
# backend (from backend/)
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # win32
pip install -r requirements.txt
python -m app.db.migrate
uvicorn app.main:app --reload --port 8000   # :8000, /health, /docs

# frontend (from frontend/)
npm install
npm run dev                    # :5173, proxies /api -> :8000
```

## Verify (B0 gate, required before claiming done)

```bash
powershell -ExecutionPolicy Bypass -File scripts/verify.ps1
# ruff + mypy + pytest (backend) + npm lint/build (frontend) + WAL check
```

## Layout

- `backend/app/` — FastAPI app, models, routers, services, db, orchestrator stub
- `backend/migrations/` — SQLite DDL (`001_ledger.sql`)
- `backend/artifacts/` — gitignored runtime: `hireflow.db`, `journal.jsonl`
- `backend/artifacts/seed/` — committed offline demo bundle
- `configs/` — `evidence_taxonomy.yaml`, `consent.yaml` (synthetic-only=true)
- `frontend/src/` — pages, `components/EvidenceBox.tsx`, `lib/api.ts`
