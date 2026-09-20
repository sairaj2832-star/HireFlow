from app.models.policy import load_policy_typed
from app.models.profile import Requirement
from app.services.policy import compose, grade_of


def req(n: int, weight: float = 0.3) -> Requirement:
    return Requirement(id=f"REQ-{n:02d}", text=f"req {n}",
                       cls="soft", weight=weight, gate="soft", evidence_needed=None)


def test_grade_boundaries():
    pol = load_policy_typed()
    assert grade_of(0.80, pol) == "SUPPORTED"
    assert grade_of(0.75, pol) == "SUPPORTED"
    assert grade_of(0.50, pol) == "NEEDS_VALIDATION"
    assert grade_of(0.45, pol) == "NEEDS_VALIDATION"
    assert grade_of(0.30, pol) == "NOT_SUPPORTED"


def test_composite_weighted_and_capped():
    pol = load_policy_typed()
    reqs = [req(1, 0.7), req(2, 0.3)]
    j = {"REQ-01": {"p": 1.0, "confidence": 0.9}, "REQ-02": {"p": 0.0, "confidence": 0.9}}
    out = compose(j, reqs, pol)
    assert out["composite"] == 0.7  # (1.0*0.7 + 0.0*0.3) / 1.0
    assert out["tier"] == "NEEDS_VALIDATION"
    assert out["needs_review"] is False


def test_needs_review_flag_in_band():
    pol = load_policy_typed()
    reqs = [req(1, 1.0)]
    j = {"REQ-01": {"p": 0.5, "confidence": 0.9}}
    out = compose(j, reqs, pol)
    assert out["needs_review"] is True
    assert out["per_req"][0]["grade"] == "NEEDS_VALIDATION"


def test_low_conf_high_weight_flags_review():
    pol = load_policy_typed()
    reqs = [req(1, 0.9), req(2, 0.1)]
    j = {"REQ-01": {"p": 0.8, "confidence": 0.2}, "REQ-02": {"p": 0.8, "confidence": 0.9}}
    out = compose(j, reqs, pol)
    assert out["needs_review"] is True