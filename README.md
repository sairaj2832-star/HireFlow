# HireFlow — AI Candidate Screening & Interview Intelligence

> **Release v1.0.0** — Hackathon-ready deployment. Single-instance FastAPI + Vite/React + SQLite with judged ledger loop.

## Product Overview

HireFlow screens candidates using a **Judged Ledger Loop** — every assessment is traced back to real evidence from the resume, persisted immutably in a hash-chained ledger, and verified through multiple BRAKE gates.

**Key features:**
- JD → structured requirements (REQ-01..N)
- Resume → 23-field profile with evidence spans
- BRAKE1: Content cleansing (hidden prompt detection, phantom ink)
- Policy-based screening with deterministic compose() scorer
- BRAKE2: Fuzzy evidence verification (≥0.85 threshold)
- Gap-conditioned question generation
- Cited reports with audit trail
- Deterministic seeded fallback (never blocks on network)

## Architecture

```
Frontend (Vite/React)     Backend (FastAPI)         SQLite WAL
   Tailwind CSS            Pydantic v2               JSONL Ledger
      |                         |                        |
      +-- /api/* ------------> :8000 -------------------> hireflow.db
                                   |
                          +--------+--------+
                          |                 |
                     Classifier        Verifier
                     (Jev/LLM)        (fuzzy ≥0.85)
```

**Stack:**
- Frontend: Vite + React + Tailwind CSS
- Backend: FastAPI + Pydantic v2 + Python 3.11
- Database: SQLite WAL + JSONL journal + FTS5
- LLM: Gemini-flash via LiteLLM + OpenRouter fallback (or seeded deterministic fallback)

## Quickstart

### Backend (local)
```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # win32
pip install -r requirements.txt
python -m app.db.migrate
uvicorn app.main:app --reload --port 8000
```

### Frontend (local)
```bash
cd frontend
npm install
npm run dev
# Opens http://localhost:5173, proxies /api to :8000
```

## Environment Variables

### Backend (`.env`)
```
TYPESAFE_API_KEY=          # Optional: Jev classifier primary
GEMINI_API_KEY=            # Optional: Google Gemini LLM fallback
OPENROUTER_API_KEY=        # Optional: OpenRouter LLM fallback
APP_ENV=production         # Optional: Environment flag
```

**Without API keys:** The system uses a deterministic seeded fallback. The demo never blocks on network issues.

### Frontend
```
VITE_API_BASE_URL=http://localhost:8000  # Local dev
VITE_API_BASE_URL=https://your-backend.railway.app  # Production
```

**Never expose** `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, or `TYPESAFE_API_KEY` to the frontend.

## Verification

### Pre-deployment
```bash
powershell -ExecutionPolicy Bypass -File scripts/verify.ps1
```

### Post-deployment
```bash
bash scripts/smoke-test.sh https://your-backend.railway.app
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Backend → Railway
```bash
railway new
railway deploy
```

### Frontend → Vercel
```bash
cd frontend
vercel --prod
```

## Demo

See [DEMO_RUNBOOK.md](DEMO_RUNBOOK.md) for the complete demo flow, demo data, and troubleshooting guide.

## Layout

```
backend/
  app/                   # FastAPI application
    main.py              # App entry point
    routers/             # API routers (jobs, candidates)
    services/            # Business logic (intake, screening, qg, etc.)
    orchestrator/        # Agent loop
    db/                  # Migration + ledger store
    models/              # Pydantic schemas
  migrations/            # SQLite DDL
  artifacts/             # Runtime data (gitignored)
  artifacts/seed/        # Offline demo bundle (tracked)
  policy.yaml            # Thresholds/weights/caps
  registry.yaml          # Capability registry
  taxonomy_slice.yaml    # ESCO skill taxonomy
frontend/
  src/
    pages/               # 8 screens (Dashboard, Intake, Shortlist, etc.)
    components/          # EvidenceBox, etc.
    lib/api.ts           # API client
configs/
  evidence_taxonomy.yaml # Evidence state taxonomy
  consent.yaml           # Synthetic-only declaration
scripts/
  verify.ps1             # B0 verification gate
  smoke-test.sh          # Post-deployment smoke test
```

## Known Limitations

- **SQLite:** Single-instance only. Not suitable for horizontal scaling.
- **Seeded Fallback:** Without API keys, classification uses deterministic seeded fallback (not ML).
- **No PDF Export:** Reports are JSON only.
- **No BRAKE3:** Human approval queue not implemented.
- **No FAISS:** FTS5 is used for retrieval (not FAISS/cross-encoder).
- **Single Region:** Deployed to a single Railway region.

## Source of Truth

1. `docs/MASTER.md` — Living source of truth
2. `docs/HireFlow_Architecture_Design_Report.md` — Architecture specification
3. `docs/hireflow_research.md` — Research evidence base
4. `AGENTS.md` — Repo rules for coding agents

## License

Proprietary — Hackathon project.