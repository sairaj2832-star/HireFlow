# backend/tests/test_policy.py
import pytest
from pydantic import ValidationError
from app.models.policy import Policy, load_policy_typed


def test_loads_live_policy_yaml():
    pol = load_policy_typed()
    assert pol.thresholds["SUPPORTED"] == 0.75
    assert pol.thresholds["NEEDS_VALIDATION"] == 0.45
    assert pol.brakes.needs_review_band == [0.35, 0.65]
    assert pol.brakes.fuzzy_ratio == 0.85
    assert pol.loop.max_steps >= 1


def test_rejects_bad_threshold():
    with pytest.raises(ValidationError):
        Policy(version="x", thresholds={"SUPPORTED": 1.5, "NEEDS_VALIDATION": 0.45},
               weights={}, caps={"cap": 1.0},
               brakes={"needs_review_band": [0.35, 0.65], "suspect_conf_threshold": 0.5,
                       "high_weight_threshold": 0.5, "fuzzy_ratio": 0.85},
               loop={"max_steps": 12, "retries": 1})