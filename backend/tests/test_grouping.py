# backend/tests/test_grouping.py
from app.services.grouping import build_cohorts


def _cand(cid, grades, confs):
    return {"candidate_id": cid,
            "per_req": [{"requirement_id": f"REQ-{i+1:02d}", "grade": g, "confidence": c,
                         "p": 0.8 if g == "SUPPORTED" else 0.3, "needs_review": False}
                        for i, (g, c) in enumerate(zip(grades, confs))],
            "tier": "SUPPORTED"}


def test_build_cohorts_group_strong_shared_missing():
    results = [
        _cand("c1", ["SUPPORTED", "SUPPORTED", "NOT_SUPPORTED"], [0.9, 0.8, 0.9]),
        _cand("c2", ["SUPPORTED", "SUPPORTED", "NOT_SUPPORTED"], [0.85, 0.9, 0.9]),
        _cand("c3", ["SUPPORTED", "SUPPORTED", "NOT_SUPPORTED"], [0.8, 0.85, 0.7]),
        _cand("c4", ["NOT_SUPPORTED", "SUPPORTED", "SUPPORTED"], [0.9, 0.8, 0.85]),
    ]
    cohorts = build_cohorts(results, job_id="job_x", policy_version="0.1.0-b0")
    labels = [c["predicate"]["label"] for c in cohorts]
    assert any("REQ-01" in l and "REQ-02" in l for l in labels)
    big = [c for c in cohorts if c["predicate"]["label"] ==
           "strong_on:REQ-01,REQ-02_missing:REQ-03"]
    assert len(big) == 1
    assert big[0]["centroid_stats"]["n"] == 3
    assert set(big[0]["member_ids"]) == {"c1", "c2", "c3"}
    assert big[0]["action"]["approval"] == "explicit-before-send"
    assert big[0]["policy_version"] == "0.1.0-b0"


def test_small_group_left_ungrouped():
    results = [
        _cand("c1", ["SUPPORTED", "NOT_SUPPORTED"], [0.9, 0.9]),
        _cand("c2", ["SUPPORTED", "NOT_SUPPORTED"], [0.8, 0.9]),
    ]
    cohorts = build_cohorts(results, job_id="job_x", policy_version="v", min_members=3)
    assert cohorts == []