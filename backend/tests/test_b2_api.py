# backend/tests/test_b2_api.py
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def _offline_classifier(monkeypatch):
    # Never hit the network: force the seeded offline fallback regardless of .env keys.
    from app.config import settings
    monkeypatch.setattr(settings, "typesafe_api_key", None)
    monkeypatch.setattr(settings, "gemini_api_key", None)
    monkeypatch.setattr(settings, "openrouter_api_key", None)


def _make_env():
    from app.main import app
    c = TestClient(app)
    job = c.post("/jobs", json={"title": "BE", "jd_text": "Python\nFastAPI\nML"}).json()
    job_id = job["job_id"]
    c.post(f"/jobs/{job_id}/candidates:ingest",
           files=[("files", ("c1.txt", b"Skills: Python, FastAPI, ML\nExperience: 4y", "text/plain")),
                  ("files", ("c2.txt", b"Skills: Java\nExperience: 10y", "text/plain"))])
    return c, job_id


def test_screen_endpoint_returns_run_id():
    c, job_id = _make_env()
    r = c.post(f"/jobs/{job_id}/screen")
    assert r.status_code == 201, r.text
    assert r.json()["run_id"].startswith("run_")


def test_shortlist_sorted_cohorts_and_typed():
    c, job_id = _make_env()
    c.post(f"/jobs/{job_id}/screen")
    j = c.get(f"/jobs/{job_id}/shortlist").json()
    assert j["job_id"] == job_id
    assert len(j["ranked"]) == 2
    comps = [c["composite"] for c in j["ranked"]]
    assert comps == sorted(comps, reverse=True)
    assert all("tier" in c and "per_req" in c for c in j["ranked"])
    assert "needs_review_rate" in j
    assert "cohorts" in j


def test_shortlist_before_screen_404():
    c, job_id = _make_env()
    assert c.get(f"/jobs/{job_id}/shortlist").status_code == 404


def test_evidence_boxes():
    c, job_id = _make_env()
    c.post(f"/jobs/{job_id}/screen")
    cand_id = c.get(f"/jobs/{job_id}/shortlist").json()["ranked"][0]["candidate_id"]
    r = c.get(f"/candidates/{cand_id}/evidence")
    assert r.status_code == 200
    j = r.json()
    assert j["boxes"]
    box = j["boxes"][0]
    assert "req" in box and "span" in box and "judgment" in box
    assert set(box["span"]) >= {"quote", "page", "line"}
    assert "conf" in box


def test_evidence_404_when_not_screened():
    c, job_id = _make_env()
    cand = c.post(f"/jobs/{job_id}/candidates:ingest",
                  files=[("files", ("z.txt", b"x", "text/plain"))]).json()
    assert c.get(f"/candidates/{cand['candidate_ids'][0]}/evidence").status_code == 404