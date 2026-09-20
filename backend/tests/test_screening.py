# backend/tests/test_screening.py
import asyncio
import pytest
from app.services.screening import run_screen
from app.services.intake import ingest_jd, ingest_resume


def _seed(tmp_path):
    kwargs = {"db_path": tmp_path / "t.db", "journal_path": tmp_path / "j.jsonl"}
    job_id, run_id = "job_test", "run_test"
    ingest_jd(job_id, run_id, b"Python, FastAPI, ML", "jd.txt", "text/plain", **kwargs)
    ingest_resume(job_id, run_id, "cand_ok",
                  b"Skills: Python, FastAPI, ML\nExperience: 4 years building REST APIs",
                  "cv.txt", "text/plain", **kwargs)
    for cid in ("cand_missing", "cand_low"):
        ingest_resume(job_id, run_id, cid,
                      b"Skills: Java\nExperience: 10 years", "cv.txt", "text/plain", **kwargs)
    return job_id, kwargs


def test_run_screen_appends_events_and_rates(tmp_path):
    from app.db.ledger_store import LedgerStore
    job_id, kwargs = _seed(tmp_path)
    res = asyncio.run(run_screen(job_id, **kwargs))
    assert res["run_id"].startswith("run_")
    assert res["job_id"] == job_id
    assert 0.0 <= res["needs_review_rate"] <= 1.0
    assert 0.0 <= res["verified_rate"] <= 1.0
    store = LedgerStore(**kwargs)
    kinds = [e["type"] for e in store.get_events()]
    assert "JUDGMENT_RECORDED" in kinds
    assert "POLICY_STATE_SET" in kinds
    assert "VERIFICATION_PASSED" in kinds or "VERIFICATION_FAILED" in kinds


def test_run_screen_shapes(tmp_path):
    job_id, kwargs = _seed(tmp_path)
    res = asyncio.run(run_screen(job_id, **kwargs))
    cand = next(c for c in res["candidates"] if c["candidate_id"] == "cand_ok")
    assert cand["tier"] in ("SUPPORTED", "NEEDS_VALIDATION", "NOT_SUPPORTED")
    assert cand["per_req"] and all(v["grade"] in ("SUPPORTED", "NEEDS_VALIDATION", "NOT_SUPPORTED")
                                   for v in cand["per_req"])
    assert cand["policy_hash"]
    assert res["policy_hash"] == cand["policy_hash"]
    assert "cohorts" in res


def test_run_screen_unknown_job_raises(tmp_path):
    with pytest.raises(ValueError):
        asyncio.run(run_screen("job_none", db_path=tmp_path / "t.db",
                               journal_path=tmp_path / "j.jsonl"))


def test_run_screen_verification_is_per_requirement(tmp_path):
    from app.db.ledger_store import LedgerStore
    kwargs = {"db_path": tmp_path / "t.db", "journal_path": tmp_path / "j.jsonl"}
    ingest_jd("job_pr", "run_pr", b"- Python\n- FastAPI", "jd.txt", "text/plain", **kwargs)
    ingest_resume("job_pr", "run_pr", "cand_pr",
                  b"Skills: Python\nExperience: 3 years", "cv.txt", "text/plain", **kwargs)
    res = asyncio.run(run_screen("job_pr", **kwargs))
    store = LedgerStore(**kwargs)
    events = [e for e in store.get_events()
              if e.get("candidate_id") == "cand_pr"
              and e.get("type") in ("VERIFICATION_PASSED", "VERIFICATION_FAILED")]
    by_req = {e["requirement_id"]: e for e in events}
    assert set(by_req) == {"REQ-01", "REQ-02"}
    assert by_req["REQ-01"]["type"] == "VERIFICATION_PASSED"
    assert by_req["REQ-02"]["type"] == "VERIFICATION_FAILED"
    assert by_req["REQ-02"]["method"] == "absent_span"
    assert by_req["REQ-02"]["ratio"] is None
    assert by_req["REQ-01"]["ratio"] != by_req["REQ-02"]["ratio"]
    cand = next(c for c in res["candidates"] if c["candidate_id"] == "cand_pr")
    assert cand["verified_spans"] == 1
    assert cand["failed_spans"] == 0
    assert cand["absent_spans"] == 1