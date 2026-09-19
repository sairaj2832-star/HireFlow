# backend/tests/test_health.py
from fastapi.testclient import TestClient


def test_health_returns_ok():
    from app.main import app

    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    j = r.json()
    assert j["status"] == "ok"
    assert "version" in j
    # wal_mode asserted in test_migrate after migration runs


def test_health_has_no_secrets_leak():
    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)
    r = client.get("/health")
    assert "TYPESAFE_API_KEY" not in r.text
    assert "GEMINI_API_KEY" not in r.text
