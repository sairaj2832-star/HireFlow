# backend/tests/test_benchmark.py
from app.scripts.benchmark_screening import generate_synthetic_cvs, run_offline_benchmark


def test_generates_40_deterministic_cvs():
    a = generate_synthetic_cvs(40, seed=42)
    b = generate_synthetic_cvs(40, seed=42)
    assert len(a) == 40
    assert all(p[1] for p in a)
    assert a == b


def test_offline_benchmark_writes_metrics(tmp_path):
    res = run_offline_benchmark(tmp_path / "out.json")
    assert res["n_candidates"] == 40
    assert 0.0 <= res["needs_review_rate"] <= 1.0
    assert 0.0 <= res["verified_rate"] <= 1.0
    assert res["latency_p50_ms"] >= 0.0
    assert res["cost_usd"] is None  # vendor claims stay UNVERIFIED
    assert "accuracy" not in res
    assert (tmp_path / "out.json").exists()