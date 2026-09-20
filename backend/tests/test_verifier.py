from app.models.policy import load_policy_typed
from app.services.verifier import VERIFY_FAIL, anomaly_flag, verify_quote


def test_verbatim_quote_passes():
    r = verify_quote("built REST APIs using Python",
                     "EXPERIENCE\nbuilt REST APIs using Python\n2020-2024", 0.85)
    assert r["pass"] is True
    assert r["ratio"] >= 0.85


def test_mismatched_quote_fails_and_logs_type():
    r = verify_quote("I invented tensorflow at Google",
                     "EXPERIENCE\nbuilt CRUD apps in PHP", 0.85)
    assert r["pass"] is False
    assert r["ratio"] < 0.85
    assert VERIFY_FAIL == "VERIFICATION_FAILED"


def test_boundary_exact_threshold():
    src = "Skillful in OpenTelemetry tracing."
    near = verify_quote("Skillful in OpenTelemetry tracing", src, 0.85)
    assert near["pass"] is True


def test_empty_source_fails():
    r = verify_quote("anything", "", 0.85)
    assert r["pass"] is False


def test_anomaly_zero_spans_but_supported():
    pol = load_policy_typed()
    assert anomaly_flag(0, "SUPPORTED", pol) == "zero_skill_outranks_expert"
    assert anomaly_flag(2, "SUPPORTED", pol) is None
    assert anomaly_flag(0, "NOT_SUPPORTED", pol) is None