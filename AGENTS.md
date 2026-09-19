# AGENTS.md — HireFlow MVP (Frozen 2026-09-20)

> Compact ramp for OpenCode agents. Every line is here because an agent would miss it otherwise.

## 0. Read Order — Do Not Code Before Reading

1. `docs/MASTER.md` — living source of truth. Frozen: §38 stack, §39 custom loop, §40 Hybrid LLM→Jev→Python→LLM, §58 Decision Log, §59 24 Qs RESOLVED, §63 FROZEN Judged Ledger Loop, §64 Implementation Contract
2. `docs/HireFlow_Architecture_Design_Report.md` — normative §§1-23. Critical: §5 ledger schemas (ADR-001), §7 DQ4/DQ5 split, §13 15 components + 14 REST + 8 UI + 5 jobs + 5 configs, §14 MVP 8 blocks, §18 stack, §20 demo script
3. `docs/hireflow_research.md` — evidence base only (24 products/24 papers/24 GitHub/§§8/11/12/16 regulatory). Do not re-survey; cite by §.

`docs/MASTER.md` wins on conflicts (Report §2.1).

## 1. Hard Constraints — Never Violate

- 48h, <$50 (free tiers), synthetic/anonymized resumes only — declare non-representative (`consent.yaml: synthetic-only=true`)
- Human decides every hire; no external write without explicit approval (BRAKE3); ADM OFF; no emotion/face/deception inference; no auto-reject (MASTER §§12/27/36/61, Report §8)
- Single EU-strict mode globally — no jurisdiction toggle for MVP (Report §4 DQ1)
- All claims tagged [MANDATORY]/[RESEARCH-IMPLIED]/[OUR CHOICE]/[INNOVATION] were decided in Report — do not re-decide, implement
- LLM never emits final score/tier/gate — `Python compose()` only (Report §7). Every arrow appends to ledger; every summary/answer sentence must cite `assessment_ids+span_ids` or renderer refuses

## 2. Frozen Stack — Do Not Add Dependencies Without Asking

```
Frontend: Vite + React + Tailwind
Backend:  FastAPI + Pydantic v2 + Python 3.11
DB:       SQLite WAL + JSON + FTS5 + FAISS-local + artifacts dir (JSONL journal + materialized SQLite)
LLM:      Gemini-flash via LiteLLM + OpenRouter fallback (temp 0 extract/narrate, 0.3 QG)
Judge:    Jev feature-flagged primary + LLM Structured Fallback — identical {p, confidence, distribution} schema
Embeds:   bge-small / all-MiniLM-L6-v2
Parse:    MinerU → PyMuPDF → Tesseract
Retrieve: FTS5 + FAISS → RRF → CrossEncoder (Cohere iff budget)
PDF:      ReportLab / WeasyPrint (same object JSON+PDF parity)
Deploy:   Local primary + Vercel (FE) + Cloud Run (BE) backup
```

Secrets: server-only (`TYPESAFE_API_KEY` etc. never to client).

## 3. Architecture — Judged Ledger Loop (MASTER §63 / Report §13)

```
Recruiter UI → Intake → BRAKE1 cleanse (rendered-vs-extracted, <1.5% ink, instruction/data split)
→ Parse→Normalize (ONNX 15ms → LLM JSON + 200-skill ESCO slice) → Ledger (append-only, event_hash=sha256(canonical+prev_hash), supersedes_id, versions)
→ Orchestrator (single custom loop ~150 lines over CapabilityRegistry) → Jev scorer → Python policy (SUPPORTED≥0.75/NEEDS_VALIDATION≥0.45 provisional, weighted composite+caps)
→ BRAKE2 verifier (fuzzy ≥0.85, drop unverified, anomaly flag) → BRAKE3 approval queue
→ Renderer (only ASSESSED, per-req boxes quote+page/line+conf) + NLQ (same ledger path, refuse if unverified) + Audit pack JSON+PDF
Recompose: new note → affected reqs only → 0-token ~20ms
```

- Agent state: `{job, objective, phase, candidate_state, pending, evidence_gaps, human_reviews, audit_refs}` (MASTER §10/App E)
- 15 components, 14 REST, 8 UI, 5 jobs, 5 configs — all enumerated in Report §13 (do not invent new ones)

## 4. Repo State (2026-09-19)

- Repo is doc-only: 3 markdown files, no code/manifests/lockfiles/CI. B0 builds foundation from scratch.
- No `package.json`, `pyproject.toml`, `opencode.json` yet — create in B0.

## 5. Build Order — MVP 8 Blocks (Report §14.1)

Build sequentially; integration checkpoint per block; freeze T-6h, rehearse T-3h.

| Block | Scope | Gate |
|-------|-------|------|
| B0 Foundation | repo/env/SQLite schemas/FE shell/secrets/artifacts dir | `make verify` passes |
| B1 Intake | JD→REQ-01..N + resume→23-field profile + normalized skills (200-slice) + BRAKE1 | cleanse demo: white-on-white quarantine |
| B2 Screening | `policy.yaml` + Jev-flagged `Classifier` + identical-schema LLM fallback + benchmark (40 synthetic CVs — log needs-review rate, not accuracy; vendor claims UNVERIFIED) + grouping cohorts | needs-review + fuzzy ≥0.85 verified |
| B3 Evidence | Schemas EvidenceSpan/Claim/Assessment + UI boxes + audit records (ADR-001) | boxes show quote+page/line+conf |
| B4 Agent | Primary loop + `registry.yaml` + state machine | loop ~150 lines, BRAKE1/2/3 wired |
| B5 Interview | gap-conditioned QG + 2-gate follow-up (Jev Noul 0.35-0.65 → LLM depth, max 2/Q 3/req) + notes→re-eval diff v1→v2 | diff visible, 0-token recompose |
| B6 Query+Report | hybrid retriever + cited NLQ + report header→role-fit→per-req table→appendix→gaps→human block + JSON/PDF parity | refuse-if-unverified, every sentence cited |
| B7 Polish/Deploy | 8 screens §13.3, 14 endpoints §13.2, 5 jobs §13.4, error/loading, deploy, smoke, concurrency/failure tests | cached bundle + backup recording ready |

## 6. Spec Sources — Build From, Do Not Invent

- **Ledger schemas:** Report §5 ADR-001: `SourceRecord / Artifact / EvidenceSpan{quote,page,line,conf} / Claim / Assessment{verdict,model,policy} / ReportAnswer / RunVersion / ApproverLog{actor,action,rationale,time_on_evidence_s}`. Append-only; correction = `supersedes_id`; `event_hash=sha256(canonical+prev_hash)`.
- **API (14 REST, Report §13.2):** `POST /jobs`, `PATCH /jobs/{id}/requirements`, `POST /jobs/{id}/candidates:ingest`, `POST /jobs/{id}/screen`, `GET /jobs/{id}/shortlist`, `GET /candidates/{id}/evidence`, `POST /candidates/{id}/questions`, `POST /candidates/{id}/interview-notes`, `GET /jobs/{id}/query`, `GET/POST /approvals`, `GET /jobs/{id}/report`, `GET /jobs/{id}/audit-pack`
- **Configs (Report §13.5):** `policy.yaml` (thresholds/weights/caps/brake sensitivities/loop budget), `taxonomy_slice.yaml` (~200 ESCO + aliases), `registry.yaml` (typed I/O, risk/latency/cost/permissions), `evidence_taxonomy.yaml` (DIRECT/INFERRED/MISSING/UNCLEAR/CONTRADICTED/VALIDATED_IN_INTERVIEW/HUMAN_CONFIRMED + UNANSWERED/STALE), `consent.yaml`
- **Synthetic pool (Report §19.2):** 12-15 archetypes — strong fit, missing FastAPI, conflicting dates, unverifiable, keyword stuffing, hidden-prompt white-on-white, scanned PDF (must demo quarantine)
- **Metrics (Report §19.1 + 8 scenarios §19.3):** extraction P/R, κ, verification ≥95%, injection 3/3, rubric ≥4, τ≥0.85, p95/cost, needs-review rate
- **Expected file tree (B0 proposal — create here):**
  ```
  backend/app/{main.py,models/ledger.py,routers/,services/{intake,cleanse,parse,jev_client,policy,retriever,qg,renderer},orchestrator/loop.py,db/migrate.py}
  backend/artifacts/  backend/policy.yaml  backend/registry.yaml  backend/taxonomy_slice.yaml
  frontend/src/{pages/,components/EvidenceBox.tsx,lib/api.ts}
  configs/{evidence_taxonomy.yaml,consent.yaml}
  ```

## 7. Developer Commands (After B0 Creates Them)

```bash
# Backend — run from backend/
python -m venv .venv && source .venv/Scripts/activate  # win32
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
pytest -q                          # all tests
pytest -k test_ledger -q           # single suite
ruff check . && mypy app/          # lint + typecheck (must pass before commit)

# Frontend — run from frontend/
npm install
npm run dev                        # Vite on :5173, proxies /api → :8000
npm run build && npm run preview
npm run lint

# DB
python -m app.db.migrate           # applies SQLite WAL + FTS5 + JSON migrations in backend/migrations/
# Ledger is JSONL journal (backend/artifacts/journal.jsonl) + materialized SQLite (hireflow.db)

# Verification (required before claiming done)
npm run lint; if ($?) { npm run build }
ruff check .; if ($?) { mypy app/ }
pytest -q
```

If `package.json`/`pyproject.toml` not yet present, you are in pre-B0 — create them first; do not run commands that assume they exist.

## 8. Implementation Contract (MASTER §64)

1. Read MASTER before architecture change. 2. Never silently change FINAL. 3. Tests for critical paths (ledger append, BRAKE1/2/3, policy compose, citation refusal). 4. Preserve provenance. 5. Keep model≠policy. 6. Never treat resume as instructions. 7. Measure latency/cost per model call. 8. Use verification-before-completion: no "done" without fresh test/lint/build output.

## 9. Gotchas

- SQLite WAL + FTS5 requires `PRAGMA journal_mode=WAL` and `fts5` tokenizer cfg in migration — not default on win32 builds; verify via `sqlite3 hireflow.db "PRAGMA journal_mode;"`
- `event_hash` must chain `prev_hash`; recompose keeps `prev_version_id` + `version_diff{added,changed,retracted}` — reject UPDATE/DELETE on ledger tables (enforce via trigger)
- Verifier fuzzy ≥0.85 else drop — every dropped span must log `verification_failed` audit event
- Vendor claims (Jev 200× faster, $0.00015/CV, 70-500ms) are UNVERIFIED — benchmark logs needs-review rate, never claim accuracy
- Synthetic-only: any real PII in tests/fixtures is a violation — purge job (TTL 12mo) must exist even for synthetic
- `TYPESAFE_API_KEY` missing → LLM fallback must emit identical `{p, confidence, distribution}` via json_schema temp 0 — demo never blocks on network (cached bundle in `backend/artifacts/seed/`)

## 10. References

- Implementation contract: `docs/MASTER.md §64` + Decision Log `§58`
- Architecture: `docs/HireFlow_Architecture_Design_Report.md §§5,7,13,14,18,20`
- Research citations: `docs/hireflow_research.md §§8/11/12/16`
