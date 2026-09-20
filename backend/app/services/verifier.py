from __future__ import annotations

from typing import Any

from rapidfuzz import fuzz

from app.models.policy import Policy

VERIFY_PASS = "VERIFICATION_PASSED"
VERIFY_FAIL = "VERIFICATION_FAILED"


def verify_quote(quote: str, source_text: str, threshold: float = 0.85) -> dict[str, Any]:
    if not source_text or not quote:
        return {"method": "fuzzy", "ratio": 0.0, "pass": False}
    ratio = fuzz.partial_ratio(quote.lower(), source_text.lower()) / 100.0
    return {"method": "fuzzy", "ratio": round(ratio, 3), "pass": ratio >= threshold}


def anomaly_flag(verified_spans: int, candidate_tier: str, pol: Policy) -> str | None:
    if verified_spans == 0 and candidate_tier == "SUPPORTED":
        return "zero_skill_outranks_expert"
    return None