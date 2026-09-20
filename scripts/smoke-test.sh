#!/bin/bash
# Post-deployment smoke test for HireFlow
# Usage: bash scripts/smoke-test.sh https://your-backend.railway.app

set -e

BACKEND_URL="${1:-http://localhost:8000}"
echo "=== HireFlow Smoke Test ==="
echo "Backend: $BACKEND_URL"
echo ""

# 1. Health
echo -n "1. Health check... "
HEALTH=$(curl -s "$BACKEND_URL/health")
echo "$HEALTH" | grep -q '"status":"ok"' && echo "PASS" || { echo "FAIL: $HEALTH"; exit 1; }

# 2. Create job
echo -n "2. Create job... "
JOB=$(curl -s -X POST "$BACKEND_URL/jobs" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","jd_text":"Python\nFastAPI\nML"}')
JOB_ID=$(echo "$JOB" | grep -o '"job_id":"[^"]*"' | cut -d'"' -f4)
[ -n "$JOB_ID" ] && echo "PASS (job_id=$JOB_ID)" || { echo "FAIL: $JOB"; exit 1; }

# 3. GET /jobs
echo -n "3. GET /jobs... "
JOBS=$(curl -s "$BACKEND_URL/jobs")
echo "$JOBS" | grep -q "$JOB_ID" && echo "PASS" || { echo "FAIL: $JOBS"; exit 1; }

# 4. Ingest candidates
echo -n "4. Ingest candidates... "
INGEST=$(curl -s -X POST "$BACKEND_URL/jobs/$JOB_ID/candidates:ingest" \
  -F "files=@/dev/stdin" <<< "Skills: Python, FastAPI
Experience: 5 years")
echo "$INGEST" | grep -q '"candidate_ids"' && echo "PASS" || { echo "FAIL: $INGEST"; exit 1; }

# 5. Screen
echo -n "5. Screen... "
SCREEN=$(curl -s -X POST "$BACKEND_URL/jobs/$JOB_ID/screen")
echo "$SCREEN" | grep -q '"run_id"' && echo "PASS" || { echo "FAIL: $SCREEN"; exit 1; }

# 6. Shortlist
echo -n "6. Shortlist... "
SHORTLIST=$(curl -s "$BACKEND_URL/jobs/$JOB_ID/shortlist")
echo "$SHORTLIST" | grep -q '"ranked"' && echo "PASS" || { echo "FAIL: $SHORTLIST"; exit 1; }

# 7. Query
echo -n "7. Query... "
QUERY=$(curl -s "$BACKEND_URL/jobs/$JOB_ID/query?filter=all")
echo "$QUERY" | grep -q '"results"' && echo "PASS" || { echo "FAIL: $QUERY"; exit 1; }

# 8. Report
echo -n "8. Report... "
REPORT=$(curl -s "$BACKEND_URL/jobs/$JOB_ID/report")
echo "$REPORT" | grep -q '"sections"' && echo "PASS" || { echo "FAIL: $REPORT"; exit 1; }

# 9. Audit
echo -n "9. Audit... "
AUDIT=$(curl -s "$BACKEND_URL/jobs/$JOB_ID/audit-pack")
echo "$AUDIT" | grep -q '"audit_events"' && echo "PASS" || { echo "FAIL: $AUDIT"; exit 1; }

echo ""
echo "=== All smoke tests PASSED ==="