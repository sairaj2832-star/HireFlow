# backend/tests/test_configs.py
def test_policy_thresholds():
    from app.services.config_loader import load_policy

    p = load_policy()
    assert p["thresholds"]["SUPPORTED"] == 0.75
    assert p["thresholds"]["NEEDS_VALIDATION"] == 0.45
    assert "weights" in p and "caps" in p


def test_policy_thresholds_ordered():
    from app.services.config_loader import load_policy

    p = load_policy()
    assert p["thresholds"]["SUPPORTED"] > p["thresholds"]["NEEDS_VALIDATION"]


def test_taxonomy_has_200_entries_or_stub():
    from app.services.config_loader import load_taxonomy

    t = load_taxonomy()
    assert len(t["skills"]) >= 20  # B0 stub 20, B1 expands to 200
    assert all("id" in s and "label" in s for s in t["skills"])


def test_registry_has_15_capabilities():
    from app.services.config_loader import load_registry

    r = load_registry()
    assert len(r["capabilities"]) == 15
    assert all("risk" in c and "latency_ms" in c for c in r["capabilities"])


def test_consent_synthetic_only():
    from app.services.config_loader import load_consent

    c = load_consent()
    assert c["synthetic-only"] is True


def test_evidence_taxonomy_values():
    from app.services.config_loader import load_evidence_taxonomy

    e = load_evidence_taxonomy()
    assert "DIRECT" in e["grades"]
    assert "UNANSWERED" in e["uncertainty"]
