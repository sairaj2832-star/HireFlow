# HireFlow — Demo Runbook

## Pre-demo Checklist

- [ ] Backend deployed and healthy (`GET /health` returns 200)
- [ ] Frontend deployed and accessible
- [ ] Demo data prepared (see below)
- [ ] Browser tested at the deployed frontend URL
- [ ] Network access confirmed (or seeded fallback verified)

## Demo Data

### Job Description
```
Python
FastAPI
ML
Docker
```

### Candidate 1 (Strong — Tier A)
```
Skills: Python, FastAPI, ML, Docker
Experience: 5 years building scalable REST APIs
```

### Candidate 2 (Weak — Tier C)
```
Skills: Java
Experience: 2 years
```

### Candidate 3 (Evidence Gap — Tier B)
```
Skills: Python
Experience: 3 years
```

**Expected Results:**
- Candidate 1: SUPPORTED, composite ~0.75
- Candidate 2: NOT_SUPPORTED, composite ~0.45
- Candidate 3: NEEDS_VALIDATION, composite ~0.55

## Demo Flow (8 minutes)

### 1. Introduction (30 seconds)
"Hi, this is HireFlow — an AI candidate screening system that uses a judged ledger loop to trace every assessment back to real evidence."

### 2. Intake (1 minute)
1. Open the deployed frontend
2. Paste the JD
3. Click "Create Job & Parse Requirements"
4. Show requirements list (REQ-01: Python, etc.)
5. Upload the 3 candidate files
6. Click "Ingest Candidates"

### 3. Shortlist (1 minute)
1. Navigate to the Shortlist page
2. Show the ranked candidates with tier badges
3. Point out: "Candidate 1 is SUPPORTED, Candidate 3 has a gap, Candidate 2 is NOT_SUPPORTED"
4. Show the needs_review_rate and cohort groups

### 4. Evidence (1 minute)
1. Click on Candidate 1 (strong)
2. Show the Evidence page
3. Point out: "This quote comes from the actual resume — 'Skills: Python, FastAPI, ML, Docker' — persisted in the ledger with page/line coordinates"
4. Show the judgment: p=0.75, grade=SUPPORTED, state=VERIFIED

### 5. Interview (1 minute)
1. Click on Candidate 3 (gap)
2. Go to Interview page
3. Click "Generate Questions"
4. Show: "Walk me through your experience with Python..." — a gap-conditioned question
5. Type a note and save

### 6. Report (1 minute)
1. Navigate to the Report page
2. Show 4 sections: Role Fit, Per-Requirement, Evidence Appendix, Gaps & Human Review
3. Point out: "Every section is assembled from actual ledger data"

### 7. Query (30 seconds)
1. Navigate to the Query page
2. Filter by tier=SUPPORTED
3. Show Candidate 1 appears
4. Filter by all — show all candidates

### 8. Audit (30 seconds)
1. Navigate to the Audit page
2. Show the audit timeline
3. Point out: "Every action is immutably recorded — SOURCE_INGESTED, JUDGMENT_RECORDED, POLICY_STATE_SET, etc."

## Fallback Behaviors

| Scenario | Fallback |
|----------|----------|
| No API keys configured | Seeded deterministic fallback (never blocks) |
| Network unavailable | Seeded fallback activates automatically |
| Database corruption | Migration re-runs on startup |
| Browser console errors | Check CORS settings and API base URL |

## Troubleshooting

### "GET /jobs 405"
Backend doesn't have the list endpoint. Check backend version.

### "Query all returns 0"
Ensure candidates have been screened before querying.

### "Evidence shows 'verified quote'"
This is the fallback string — real quotes should show actual resume text.

### "CORS error"
Check that the frontend API base URL matches the backend origin.

## Demo Script (Conversational)

"Welcome to HireFlow. In the next 8 minutes, I'll show you how we screen candidates with traceable evidence.

[Create job] — We start with a job description for a Backend Engineer role. The system parses it into structured requirements.

[Ingest] — We upload three resumes. BRAKE1 immediately flags any suspicious content — like hidden prompts or executable files.

[Shortlist] — The system screens all candidates. Candidate 1 is a strong match — SUPPORTED. Candidate 3 has a gap — NEEDS_VALIDATION. Candidate 2 doesn't match — NOT_SUPPORTED.

[Evidence] — For each candidate, we can trace every assessment back to the actual resume text. This quote — 'Skills: Python, FastAPI, ML, Docker' — is persisted in the ledger with page and line coordinates.

[Interview] — For the candidate with a gap, the system generates a targeted question: 'Walk me through your experience with Python?' The interviewer can save notes, and the system re-evaluates.

[Report] — The final report is assembled from actual ledger data — not a static template. Every section cites real evidence.

[Query] — You can query the results by tier, grade, or candidate ID.

[Audit] — Every action is immutably recorded in a hash-chained ledger. You can audit the entire decision trail.

This is HireFlow — AI screening with judged evidence."