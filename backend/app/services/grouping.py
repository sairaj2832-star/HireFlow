# backend/app/services/grouping.py
from __future__ import annotations
from typing import Any


def _grade_profile(candidate: dict[str, Any]) -> dict[str, Any]:
    strong = [v["requirement_id"] for v in candidate["per_req"] if v["grade"] == "SUPPORTED"]
    missing = [v["requirement_id"] for v in candidate["per_req"]
               if v["grade"] in ("NEEDS_VALIDATION", "NOT_SUPPORTED")]
    label = f"strong_on:{','.join(strong)}_missing:{','.join(missing)}"
    return {"strong_on": strong, "missing": missing, "label": label}


def build_cohorts(results: list[dict[str, Any]], job_id: str, policy_version: str,
                  min_members: int = 3) -> list[dict[str, Any]]:
    buckets: dict[str, dict[str, Any]] = {}
    for c in results:
        profile = _grade_profile(c)
        buckets.setdefault(profile["label"], {"profile": profile, "members": []})
        buckets[profile["label"]]["members"].append(c)

    cohorts: list[dict[str, Any]] = []
    for label, item in buckets.items():
        members = item["members"]
        if len(members) < min_members:
            continue
        n = len(members)
        confs = [v["confidence"] for m in members for v in m["per_req"]]
        meanc = round(sum(confs) / len(confs), 3) if confs else 0.0
        nr = sum(1 for m in members if m.get("needs_review")) / n
        contradiction_count = sum(
            1 for m in members for v in m["per_req"] if v["grade"] == "CONTRADICTED")
        contrad_rate = contradiction_count / (n * len(members[0]["per_req"])) if members[0]["per_req"] else 0.0
        cohorts.append({
            "cohort_id": f"cohort_{abs(hash(label)) % (10**8)}",
            "job_id": job_id,
            "predicate": item["profile"],
            "member_ids": [m["candidate_id"] for m in members],
            "centroid_stats": {"n": n, "mean_conf": meanc,
                               "needs_validation_rate": round(nr, 3),
                               "contradiction_rate": round(contrad_rate, 3)},
            "action": {"type": "batch_followup_pack", "question_pack_id": None,
                       "approval": "explicit-before-send"},
            "policy_version": policy_version,
        })
    return cohorts