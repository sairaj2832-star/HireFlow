# CONTEXT REPORT — HireFlow Repository State (2026-09-20)

---

## PROJECT_STATE

**Repository:** HireFlow — AI Candidate Screening & Interview Intelligence (MVP)
**Current branch:** `b1-intake` (also `master` exists; no active work on master)
**Working tree:** 4 modified files + ~12 untracked files (see below)
**Recent relevant commits:** 20 commits, all on `b1-intake`. Most recent: `76e1439 feat(b2): 40-CV offline benchmark logs needs-review rate + latency`. Branch is firmly at **B2 screening complete** stage.

### Uncommitted changes (likely from a previous agent working on B3/B5/B6 scaffolding):
- `backend/tests/test_grouping.py` — whitespace fix (`l` → `label` variable name)
- `frontend/src/App.tsx` — added NavLink nav bar + 7 screen routes (Intake done, others Placeholder)
- `frontend/src/components/EvidenceBox.tsx` — upgraded to styled box with grade prop (B3)
- `frontend/src/lib/api.ts` — added ~160 lines: getShortlist, getCandidate, getEvidence, generateQuestions, addInterviewNote, getReport, getQuery, getAuditPack (B2/B3/B5/B6 stubs)
- **Untracked:** `frontend/src/pages/{CandidateDetail,Evidence,Interview,Query,Report,Shortlist}Page.tsx` (7 pages, IntakePage committed), `backend/artifacts/benchmark/results.json`, `backend/tests/test_b2_gate.py`, `dataset/`, `frontend/.eslintrc.cjs`

### Generated/runtime files (gitignored, do NOT touch):
`backend/artifacts/hireflow.db*`, `backend/artifacts/journal.jsonl`, `backend/artifacts/uploads/`, `.venv/`, `node_modules/`, `backend/.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`

---

## B0→B7 IMPLEMENTATION MAP

### B0: Foundation — IMPLEMENTED (committed)
- **What's real:** FastAPI app with `/health`, SQLite WAL+FTS5 migration (`001_ledger.sql`), 8 Pydantic ledger schemas (SourceRecord, Artifact, EvidenceSpan, Claim, Assessment, ReportAnswer, RunVersion, ApproverLog) per ADR-001, `LedgerStore` (JSONL journal + materialized SQLite, hash chain `sha256(canonical+prev_hash)`, mutex-serialized append, `supersede()`), 5 YAML configs (policy.yaml, taxonomy_slice.yaml 20 skills stub, registry.yaml 13 capabilities, evidence_taxonomy.yaml, consent.yaml synthetic-only=true), server-only Settings (TYPESAFE/GEMINI/OPENROUTER keys never to client), frontend shell (Vite+React+Tailwind, `/api` proxy, EvidenceBox stub), `scripts/verify.ps1`, `Makefile`, `.gitignore`
- **Missing:** Nothing — B0 is fully committed and green
- **Risk:** FTS5 `tokenize='unicode61 "remove_diacritics 2"'` was rejected by SQLite 3.43.1; currently plain `unicode61` (deferred to B6)
- **Key files:** `backend/app/main.py`, `backend/app/models/ledger.py`, `backend/app/db/migrate.py`, `backend/app/db/ledger_store.py`, `backend/policy.yaml`, `backend/registry.yaml`, `backend/taxonomy_slice.yaml`, `configs/*`, `frontend/src/App.tsx` (committed version), `frontend/src/components/EvidenceBox.tsx` (committed version)

### B1: Intake — IMPLEMENTED (committed)
- **What's real:** `cleanse.py` (BRAKE1: executable MIME block, instruction-pattern regex, rendered-vs-extracted delta, phantom ink proxy; never edits bytes), `jd_parser.py` (deterministic REQ-01..N with hard/soft gates/weights, LLM seam, PyMuPDF fallback), `resume_parser.py` (23-field CandidateProfile, ESCO alias normalize_skills, evidence spans, no PII), `intake.py` (cleanse→parse→ledger append, quarantine on suspect/blocked, uploads persistence), `routers/jobs.py` (4 B1 endpoints: POST /jobs, GET /jobs/{id}, PATCH /jobs/{id}/requirements, POST /jobs/{id}/candidates:ingest with multipart + quarantine), `IntakePage.tsx` (JD upload, candidate upload, quarantine banner, loading/error states)
- **Tests:** test_cleanse (5), test_profile (4), test_jd_parser (4), test_resume_parser (4), test_intake (4), test_jobs_api (4 — committed separately), test_b1_gate (3), test_repo_hygiene (2), test_configs — all passing
- **Missing:** In-memory `_JOBS` store instead of SQLite (B2 plan), `POST /candidates/{id}` endpoint not yet in router, no versioned requirements
- **Risk:** `routers/jobs.py` now has B2 endpoints mixed with B1 (screen/shortlist added in B2 commit); intake router must not break

### B2: Screening — IMPLEMENTED (committed)
- **What's real:** `models/policy.py` (typed Policy with Brakes/Loop, `load_policy_typed()`), `models/classifier.py` (Judgement, ScreenQuestion, Classifier Protocol, ClassifierUnavailable), `services/policy.py` (compose() — the ONLY scorer: grade_of, verdict_of, weighted composite+caps+tiers+needs_review), `services/jevs.py` (JevClassifier via api.typesafe.ai, LLMStructuredFallback with seeded bundle, make_classifier() feature flag, Metrics with p50/p95, decide_with_retry), `services/verifier.py` (BRAKE2: verify_quote fuzzy≥0.85 via rapidfuzz, anomaly_flag zero_skill_outranks_expert), `services/screening.py` (run_screen: classify→verify→compose→ledger append JUDGMENT_RECORDED/VERIFICATION_PASSED|FAILED/POLICY_STATE_SET→cohorts), `services/grouping.py` (build_cohorts: evidence-shaped cohorts with predicate/centroid_stats/action), `routers/jobs.py` (POST /jobs/{id}/screen, GET /jobs/{id}/shortlist), `routers/candidates.py` (GET /candidates/{id}, GET /candidates/{id}/evidence — B2 stub with placeholder boxes), `app/scripts/benchmark_screening.py` (40 synthetic CVs offline, logs needs-review rate/latency, no accuracy), `tests/test_b2_gate.py` (4 tests)
- **Tests:** test_policy (2), test_policy_compose (4), test_classifier_models (4), test_jevs (10), test_verifier (5), test_screening (4), test_grouping (2), test_b2_api (6), test_b2_gate (4), test_benchmark (2), test_ledger_store (5 incl concurrent), test_migrate (4), test_ledger_models (7), test_health (2), test_verify_gate (2), plus B0/B1 tests
- **Missing:** `routers/candidates.py` evidence boxes use hardcoded `{"quote": "verified quote", "page": 1, "line": 1}` placeholder (B3 to wire real loc), no async B2 endpoints wired in frontend, no real retriever/qg/renderer
- **Risk:** `test_jevs.py::test_make_classifier_feature_flag` does plain assignment `settings.typesafe_api_key = False` which works but is non-standard; conftest autouse fixture nulls keys for all other tests

### B3: Evidence — PARTIALLY IMPLEMENTED (uncommitted scaffolding)
- **What's real:** Ledger schemas exist (EvidenceSpan with quote/loc/conf/verified, Claim, Assessment with grade/uncertainty/p/confidence/claim_ids/policy_hash/judge, ReportAnswer with version/version_diff, ApproverLog with time_on_evidence_s); EvidenceBox component upgraded; api.ts has getEvidence types and functions; EvidencePage created
- **Placeholder/stub:** `routers/candidates.py` evidence boxes return hardcoded `{"quote": "verified quote", "page": 1, "line": 1}` — NOT real candidate spans; no Claim/Assessment persistence endpoints; no audit trail endpoints; EvidencePage renders boxes but data comes from B2 placeholder
- **Missing:** EvidenceSpan→ledger persistence for evidence mapping (only B1 maps REQ-as-spans, not resume evidence), Claim/Assessment ledger writes (BRAKE2 writes them but no API to read), EvidencePage boxes not connected to real ledger data, audit pack endpoint
- **Risk:** B3 depends on B2 screening output; cannot make real progress until run_screen persists per-requirement evidence spans to ledger with real quotes/loc

### B4: Agent (STUB — NotImplementedError)
- **What's real:** `orchestrator/loop.py` has AgentState dataclass (job, objective, phase, candidate_state, pending, evidence_gaps, human_reviews, audit_refs) and Orchestrator class with `run()` raising `NotImplementedError("B4: implement loop over registry.yaml with 12-step budget and 3 BRAKES")`
- **Missing:** Entire custom loop (~150 lines), CapabilityRegistry dispatch, state machine, goal→observe→reason→select→execute→update→sufficiency→done/re-plan/escalate, BRAKE1/2/3 wiring
- **No tests** for orchestrator loop (only test_orchestrator_stub.py exists — verifies the stub raises)
- **Risk:** B4 is the biggest single-block gap; it's the orchestration backbone that B5/B6/B7 depend on; but B3/B5/B6 could work via direct REST calls without the agent loop for demo purposes

### B5: Interview — STUB (frontend placeholders, no backend)
- **What's real:** InterviewPage.tsx exists (gap-conditioned QG UI, notes box), api.ts has generateQuestions/addInterviewNote types, frontend tests expect Question/InterviewNoteResponse types
- **Missing:** `services/qg.py` (gap-conditioned question generation — does not exist), `routers/candidates.py` POST /candidates/{id}/questions (not implemented — returns 404), POST /candidates/{id}/interview-notes (not implemented), re-eval diff v1→v2 logic, follow-up gate (Jev Noul 0.35-0.65 → LLM depth)
- **Risk:** B5 is thin if scoped to: intake candidate text → seeded LLM questions → notes → ledger append → screening recompose (no full QG engine needed for demo)

### B6: Query+Report — STUB (frontend placeholders, no backend)
- **What's real:** ReportPage.tsx, QueryPage.tsx exist; api.ts has getReport/getQuery/getAuditPack types; frontend has filter UI (tier/verified)
- **Missing:** `services/retriever.py` (FTS5+FAISS hybrid — does not exist), `services/renderer.py` (cited report renderer — does not exist), `services/qg.py`, GET /jobs/{id}/query (not implemented), GET /jobs/{id}/report (not implemented), GET /jobs/{id}/audit-pack (not implemented), NLQ with citations/refuse-if-unverified
- **Risk:** Same as B5 — can be reduced to: ledger-native NLQ (FTS5 query over evidence_spans_fts → cited answers), report from screening results (deterministic template), audit from ledger events export

### B7: Polish/Deploy — STUB
- **What's real:** 8 frontend pages exist (7 created + Intake), App.tsx has nav with all 7 routes (Intake, Shortlist, Candidates, Evidence, Interview, Report, Query + 4 placeholders for jd/audit/policy/approvals)
- **Missing:** error/loading states on most pages, deploy setup, smoke tests, concurrency/failure tests, audit view (placeholder), policy editor (placeholder), approval queue (placeholder), purge job wiring
- **Risk:** B7 is frontend polish + deploy config — can be incremental

---

## CURRENT_VERIFICATION

| Check | Status | Notes |
|---|---|---|
| **Tests** | **98 passed** | `PYTHONPATH="." ; .venv/Scripts/pytest -q` from backend/ — 23 test files, 0 failed, 0 errors |
| **Lint (ruff)** | **Clean** | `ruff check app/ tests/` — no issues |
| **Typecheck (mypy)** | **Clean** | `mypy app/` — "Success: no issues found in 30 source files" |
| **Frontend lint** | **FAILING** | 2 errors: InterviewPage.tsx:3 unused `InterviewNoteResponse`, QueryPage.tsx:10 unused `useEffect` |
| **Frontend build** | **FAILING** | tsc fails on same 2 unused-var errors (tsconfig strict with noUnusedLocals) |
| **WAL check** | **PASS** | `journal_mode=wal` confirmed on real DB |
| **Integration** | **GREEN** | B2 API tests pass end-to-end via TestClient (test_b2_api: 6 tests, test_b2_gate: 4 tests) |
| **Smoke test** | **GREEN** | verify.ps1 logic: migrate→ruff→mypy→pytest→WAL check |

**Note:** Tests require `PYTHONPATH="."` from backend/ — verify.ps1 apparently handles this via its working directory context but direct pytest invocation does not.

---

## END_TO_END_FLOW

### Working path (B0→B2 fully functional):
```
POST /jobs (JSON or multipart) → parse_jd_bytes → REQ-01..N → ingest_jd → ledger SOURCE_INGESTED+ARTIFACT_CLEANSED+REQUIREMENT_DEFINED+EVIDENCE_SPAN_MAPPED
→ POST /jobs/{id}/candidates:ingest → cleanse_upload (BRAKE1) → parse_resume → CandidateProfile → ledger events + uploads/{cand}.txt
→ POST /jobs/{id}/screen → run_screen → make_classifier (seeded fallback) → per-req Jev judgments → verify_quote (BRAKE2) → compose() → ledger: JUDGMENT_RECORDED/VERIFICATION_PASSED|FAILED/POLICY_STATE_SET → build_cohorts
→ GET /jobs/{id}/shortlist → ranked candidates (tier/composite/needs_review/cohorts)
→ GET /candidates/{id} → screenings summary
→ GET /candidates/{id}/evidence → B2 placeholder boxes (hardcoded quote/page/line)
```

### First broken point:
**B3 Evidence persistence** — `routers/candidates.py:get_evidence` returns hardcoded `{"quote": "verified quote", "page": 1, "line": 1}` instead of real EvidenceSpan data from the ledger. The EvidenceBox component expects `span: {quote, page, line}` and `judgment: {p, confidence, grade}` but the API doesn't serve real evidence.

### Downstream dependencies after the break:
- B3: Evidence boxes need real EvidenceSpan/Claim/Assessment ledger reads
- B4: Orchestrator loop is entirely unimplemented (NotImplementedError)
- B5: POST /candidates/{id}/questions and POST /candidates/{id}/interview-notes return 404 (no routes)
- B6: GET /jobs/{id}/query, GET /jobs/{id}/report, GET /jobs/{id}/audit-pack return 404 (no routes)
- B7: Pages have no real data to display past B2 shortlist/evidence placeholder

---

## DATA_CONTRACTS

### Critical schemas (ledger.py — ADR-001, 8 Pydantic models):
1. **SourceRecord** — id, run_id, kind[jd/resume/transcript/notes], filename, mime, sha256(64), bytes, consent_tier[L0/L1], retention_until, created_at
2. **Artifact** — id, source_id, run_id, parser[mineru/pymupdf/tesseract_ocr], parser_version, clean_text_ref, cleanse{phantom_flag, ink_ratio, rendered_vs_extracted_delta, verdict}, event_hash
3. **EvidenceSpan** — id, artifact_id, candidate_id, quote(8-600), loc{page,line_start,line_end,char_start,char_end}, granularity, confidence[0-1], verified{method,ratio,pass}, supersedes_id
4. **Claim** — id, candidate_id, text(≤280), span_ids(min 1), polarity[asserts/denies], extractor, supersedes_id
5. **Assessment** — id, candidate_id, requirement_id, grade[supporting/neutral/conflicting/missing], uncertainty[none/unanswered/conflicting/unverifiable/stale], p[0-1], confidence[0-1], claim_ids, policy_hash, judge, supersedes_id
6. **ReportAnswer** — id, kind[summary/evaluation_report/nl_answer/question_set], candidate_ids, assessment_ids(min 1), body_md, version(≥1), prev_version_id, version_diff
7. **RunVersion** — run_id, code_sha, policy_hash, policy_version, models
8. **ApproverLog** — id, run_id, actor, action[approve/override/reject/request_revalidation/final_hire_decision], target_ids, rationale, time_on_evidence_s

### Critical APIs (existing vs needed):
**Existing (working):** POST /jobs, GET /jobs/{id}, PATCH /jobs/{id}/requirements, POST /jobs/{id}/candidates:ingest, GET /jobs/{id}/shortlist, GET /candidates/{id}, GET /candidates/{id}/evidence, POST /jobs/{id}/screen
**Needed but returning 404:** POST /candidates/{id}/questions, POST /candidates/{id}/interview-notes, GET /jobs/{id}/query, GET /jobs/{id}/report, GET /jobs/{id}/audit-pack, GET/POST /approvals, PATCH /jobs/{id}/requirements versioning

### Critical invariants:
- `event_hash = sha256(canonical_json + prev_hash)` — chains linearly, mutex-protected
- Ledger is append-only — UPDATE/DELETE rejected by DB triggers
- `compose()` is the ONLY scorer — LLM never emits final score/tier/gate
- `grade_of`: p≥0.75 SUPPORTED, p≥0.45 NEEDS_VALIDATION, else NOT_SUPPORTED
- `needs_review` flag: p in [0.35, 0.65] OR (high-weight req AND conf<0.5)
- Brakes: fuzzy ≥0.85 else drop; anomaly: zero verified + SUPPORTED tier → flag
- Synthetic-only: no date_of_birth/photo in CandidateProfile; `consent.yaml: synthetic-only=true`
- Secrets (TYPESAFE/GEMINI/OPENROUTER keys) never to client
- All mutation endpoints return audit_ref (B2/B3+ requirement)

---

## BRAKES_AND_LEDGER

### BRAKE1 (cleanse):
- **Where:** `services/cleanse.py`, called by `intake.py` before any parsing
- **What it verifies:** executable MIME block, instruction patterns (ignore previous instructions, rank me first, etc.), rendered-vs-extracted delta (>50%), phantom ink ratio (<1.5% proxy)
- **Consumes:** filename, mime, raw_bytes, extracted_text
- **Outputs:** CleansingResult{verdict: clean/suspect/blocked, phantom_flag, signals, clean_text_ref}
- **Downstream:** intake.py raises ValueError("blocked") on blocked verdict; API returns 400; UI shows quarantine banner

### BRAKE2 (verifier):
- **Where:** `services/verifier.py`, called by `screening.py` per-requirement after screening
- **What it verifies:** fuzzy quote-vs-source ratio ≥0.85 (rapidfuzz), anomaly flag (zero_skill_outranks_expert)
- **Consumes:** quote, source_text, threshold (from policy.yaml), verified_spans count, candidate tier, Policy
- **Outputs:** verify_quote{method, ratio, pass}, anomaly_flag(string|null)
- **Downstream:** screening.js appends VERIFICATION_PASSED/VERIFICATION_FAILED events; failed spans → candidate's failed_spans count

### BRAKE3 (approval):
- **NOT IMPLEMENTED** — no code exists yet; only referenced in plans and architecture docs
- **Planned:** UI + HUMAN_DECISION events; explicit gates for rank/shortlist/question/report/message/shortlist/policy edit; note summary → audited pre-approve; retrieval/views → read-only
- **Downstream:** BLOCKS report rendering and human decision flows

### Evidence ledger:
- Dual-write: JSONL journal (`artifacts/journal.jsonl`) + SQLite (`artifacts/hireflow.db`)
- Hash chain via `event_hash`/`prev_hash` columns; mutex `_LEDGER_LOCK` serializes concurrent appends
- FTS5 virtual table `evidence_spans_fts` over evidence quotes
- Append-only triggers on all 6 main tables
- `supersede()` method for corrections (appends new version, sets supersedes_id)

### Audit:
- Audit events logged as ledger events (JUDGMENT_RECORDED, VERIFICATION_PASSED/FAILED, POLICY_STATE_SET, SOURCE_INGESTED, ARTIFACT_CLEANSED, etc.)
- No dedicated audit endpoint yet (B6)
- `ApproverLog` model exists but no API writes it yet

---

## PARALLELIZATION

### Agent A → B3/B4:
- **Ownership:** `backend/app/services/screening.py` (minor), `backend/app/routers/candidates.py` (major rewrite for real evidence), `backend/app/orchestrator/loop.py` (full implementation), `backend/app/services/policy.py` (minor, already done)
- **New files:** `services/qg.py` (B5), `services/retriever.py` (B6), `services/renderer.py` (B6), `services/evidence.py` (B3), new migration DDL
- **Conflict risk:** HIGH on `routers/candidates.py` (Agent A needs real evidence boxes, Agent B may need questions endpoint in same file), `backend/app/services/intake.py` (Agent A may add evidence persistence)

### Agent B → B5/B6:
- **Ownership:** `backend/app/routers/candidates.py` (questions/interview-notes endpoints), new router endpoints for query/report/audit-pack, `frontend/src/pages/InterviewPage.tsx`, `frontend/src/pages/QueryPage.tsx`, `frontend/src/pages/ReportPage.tsx`
- **New files:** `services/retriever.py`, `services/renderer.py` (B6), frontend report/query logic
- **Conflict risk:** MEDIUM — same `routers/candidates.py` as Agent A; can be split by function (Agent A: GET evidence boxes, Agent B: POST questions + POST notes)

### Agent C → B7:
- **Ownership:** All `frontend/src/pages/*.tsx` (polish), `frontend/src/lib/api.ts` (add real type guards), deploy config, smoke test scripts
- **Conflict risk:** LOW — frontend only, unless Agent A/B also modify pages

### Conflict-prone files:
1. **`backend/app/routers/candidates.py`** — HIGH: Agents A+B both need to add endpoints here
2. **`backend/app/services/intake.py`** — MEDIUM: Agent A needs evidence span persistence
3. **`frontend/src/App.tsx`** — MEDIUM: routing changes by B7 while B3/B5/B6 add page components
4. **`frontend/src/lib/api.ts`** — MEDIUM: type additions from all agents
5. **`backend/policy.yaml`** — LOW: already frozen, may need threshold tuning from benchmark
6. **`backend/app/db/ledger_store.py`** — LOW: append-only, mutex already in place; schema additions via migration only
7. **`backend/tests/`** — MEDIUM: parallel test additions; coordinate naming and conftest fixture changes

---

## 5_HOUR_SCOPE

### Must have (for working E2E demo):
1. Fix B3 evidence boxes — wire `GET /candidates/{id}/evidence` to real EvidenceSpan data from ledger (not hardcoded)
2. Implement `POST /candidates/{id}/questions` — even seeded/gap-conditioned questions from intake text
3. Implement `POST /candidates/{id}/interview-notes` — ledger append + recompose diff
4. Implement `GET /jobs/{id}/query` — FTS5-based cited NLQ (thin slice)
5. Implement `GET /jobs/{id}/report` — deterministic report from screening results (no LLM needed for MVP)
6. Implement `GET /jobs/{id}/audit-pack` — export ledger events as JSON
7. Fix frontend lint/build errors (2 unused vars)
8. Fix `POST /jobs/{id}/screen` to persist full results in `_SCREENS` (currently stores partial — shortlist needs candidate data not just run_id)

### Should have (if time permits):
1. BRAKE3 approval queue UI stub with human decision events
2. BIAS probe logging (decoupled, already stubbed)
3. Purge job (TTL 12mo, already stubbed in `purge.py`)
4. Benchmark dashboard showing needs-review rate from `benchmark/results.json`
5. Error/loading states on all frontend pages
6. Audit view page (placeholder exists)

### Safe to defer:
1. Custom orchestrator loop (B4) — demo works via REST calls without it
2. Full QG engine (Jev gate → LLM depth) — seeded questions suffice for demo
3. ReportLab/WeasyPrint PDF export — JSON report sufficient for MVP demo
4. FAISS embeddings / cross-encoder rerank — FTS5-only retrieval sufficient
5. Live interview transcription — paste notes mode (already documented as MVP)
6. Multi-agent framework — custom loop deferred
7. Policy editor page
8. JD view page (placeholder)
9. Approval queue page (placeholder)

### B5 reduction:
- **Thin vertical slice:** intake candidate text → deterministic question generation (keyword-triggered from gaps) → POST /candidates/{id}/questions → notes POST → screening recompose (re-run run_screen)
- **Drop:** full QG engine with Jev gate + LLM depth judge + follow-up gating
- **Demo path:** candidate has evidence gap (no FastAPI span) → system generates "Walk through your FastAPI experience?" question → user submits note → re-screen shows updated state

### B6 reduction:
- **Thin vertical slice:** GET /jobs/{id}/query → FTS5 query over evidence_spans_fts → cited answers reusing B2 evidence box format; GET /jobs/{id}/report → template from screening results (Python, not LLM); GET /jobs/{id}/audit-pack → JSON export of ledger events
- **Drop:** hybrid retriever (FAISS/cross-encoder), NL planner, LLM citation forcing, PDF export
- **Demo path:** "Show Python candidates" → FTS5 search → return candidates with Python evidence spans cited → audit pack shows the ledger trail

---

## CRITICAL RISKS

1. **B4 orchestrator not implemented** — the "agentic" demo differentiator is missing. Workaround: drive via REST UI (manual step-by-step) for demo; the loop is described but `run()` raises NotImplementedError.
2. **Frontend build is broken** — 2 lint errors block `npm run build`; must fix before B7 deploy gate.
3. **Tests require PYTHONPATH="."** — `verify.ps1` must handle this correctly (it does via context, but direct `pytest` fails). If verify.ps1 doesn't set PYTHONPATH, all 34 tests that import `app.*` will fail.
4. **B3 evidence is hardcoded** — GET /candidates/{id}/evidence returns placeholder boxes, making the evidence UI non-functional. This is the first break in the E2E flow after B2.
5. **POST /jobs/{id}/screen stores partial data** — `_SCREENS[job_id]` only stores run_id/needs_review_rate/etc. but the shortlist endpoint reads `candidates` and `cohorts` from it. The screen endpoint does append these to `_SCREENS[job_id]` but if the screen fails or is re-run, data may be stale.
6. **`routers/candidates.py` is a conflict hotspot** — both B3 (evidence) and B5 (questions/notes) need to add endpoints to this router.
7. **Uncommitted B3/B5/B6 scaffolding** — 4 modified files + 7 untracked page files represent uncommitted agent work. These need to be reviewed and either committed or discarded before new work.
8. **Seeding/DB state** — `backend/artifacts/hireflow.db` and `journal.jsonl` are gitignored and may contain stale state from previous test runs. The B1 gate test reads from the default LedgerStore which uses the real db.
9. **`dataset/` directory** — 616KB CSV + 4817 JSONL resumes present but not integrated into the codebase (B1 uses synthetic inline CVs per B2 plan).
10. **`.env` committed warning** — `backend/.env` contains what appear to be real API keys (TYPESAFE_API_KEY, GEMINI_API_KEY, OPENROUTER_API_KEY). While `.env` is in `.gitignore`, check if it was ever committed or exists on disk with real credentials.

---

## FINAL_READINESS

**YES** — sufficient repository context to execute the next implementation instruction. The codebase is at B2 (screening fully implemented and tested), B3-B7 are stubs/placeholders with clear interfaces defined in the B1/B2 implementation plans. The 5-hour scope is well-defined: B3 evidence wiring + B5/B6 thin vertical slices + frontend fixes + BRAKE3 skeleton. Key risks (B4 absence, broken lint, hardcoded evidence) are understood and have documented workarounds for demo purposes.
