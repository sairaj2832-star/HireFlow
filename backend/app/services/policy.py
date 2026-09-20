from __future__ import annotations
from typing import Any
from app.models.policy import Policy
from app.models.profile import Requirement


def grade_of(p: float, pol: Policy) -> str:
    if p >= pol.thresholds["SUPPORTED"]:
        return "SUPPORTED"
    if p >= pol.thresholds["NEEDS_VALIDATION"]:
        return "NEEDS_VALIDATION"
    return "NOT_SUPPORTED"


def verdict_of(req: Requirement, j: dict[str, float], pol: Policy) -> dict[str, Any]:
    p = round(min(max(float(j["p"]), 0.0), 1.0), 3)
    conf = round(min(max(float(j.get("confidence", 0.5)), 0.0), 1.0), 3)
    focus = pol.brakes.needs_review_band[0] < p < pol.brakes.needs_review_band[1]
    low_conf_high_weight = (
        req.weight >= pol.brakes.high_weight_threshold
        and conf < pol.brakes.suspect_conf_threshold
    )
    return {
        "requirement_id": req.id,
        "p": p,
        "confidence": conf,
        "grade": grade_of(p, pol),
        "needs_review": bool(focus or low_conf_high_weight),
    }


def compose(judgements: dict[str, dict[str, float]],
            requirements: list[Requirement], pol: Policy) -> dict[str, Any]:
    if not requirements:
        return {"composite": 0.0, "tier": "NOT_SUPPORTED", "needs_review": False, "per_req": []}
    per_req: list[dict[str, Any]] = []
    for r in requirements:
        j = judgements.get(r.id)
        if j is None:
            j = {"p": 0.0, "confidence": 0.0}
        per_req.append(verdict_of(r, j, pol))
    total_w = sum(r.weight for r in requirements) or 1.0
    comp = sum(v["p"] * w for v, w in zip(per_req, (r.weight for r in requirements))) / total_w
    comp = min(comp, pol.caps.get("cap", 1.0))
    return {
        "composite": round(comp, 3),
        "tier": grade_of(comp, pol),
        "needs_review": any(v["needs_review"] for v in per_req),
        "per_req": per_req,
    }