import asyncio
import httpx
import pytest
from app.config import settings as app_settings
from app.models.classifier import Judgement, ClassifierUnavailable
from app.services.jevs import JevClassifier, LLMStructuredFallback, METRICS, Metrics, decide_with_retry, make_classifier, seeded_judgement


def _mk(handler, key: str = "test-secret") -> JevClassifier:
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return JevClassifier(api_key=key, timeout_s=5.0, client_override=client)


def test_jev_success_parses_judgements():
    def handler(request: httpx.Request) -> httpx.Response:
        body = request.read().decode()
        assert "Bearer test-secret" in request.headers["authorization"]
        assert '"questions"' in body
        return httpx.Response(200, json={"judgements": {
            "q1": {"p": 0.9, "confidence": 0.8, "distribution": {"supporting": 0.9, "neutral": 0.1}},
            "q2": {"p": 0.4, "confidence": 0.6, "distribution": {"supporting": 0.4, "neutral": 0.6}},
        }})

    jc = _mk(handler)
    out = asyncio.run(jc.decide("state text", {"q1": "Python?", "q2": "FastAPI?"}))
    assert out["q1"].p == 0.9
    assert out["q1"].distribution["supporting"] == 0.9
    assert out["q2"].p == 0.4


def test_jev_500_raises_classifier_unavailable():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="boom")

    with pytest.raises(ClassifierUnavailable):
        asyncio.run(_mk(handler).decide("s", {"q1": "Python?"}))


def test_jev_timeout_raises_classifier_unavailable():
    async def slow(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("simulated network timeout")

    client = httpx.AsyncClient(transport=httpx.MockTransport(slow))
    jc = JevClassifier(api_key="k", timeout_s=0.05, client_override=client)
    with pytest.raises(ClassifierUnavailable):
        asyncio.run(jc.decide("s", {"q1": "Python?"}))


def test_metrics_p50_p95():
    m = Metrics()
    for ms in [10, 20, 30, 40, 100]:
        m.add({"kind": "jev", "latency_ms": ms, "cost": None, "questions": 2})
    p50, p95 = m.latency_p50_p95()
    assert p50 == 30.0
    assert p95 == 100.0
    assert m.summary()["total_questions"] == 10


def test_jev_invalid_shape_raises_classifier_unavailable():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"judgements": {"q1": {"p": None, "confidence": 0.5, "distribution": {}}}})

    with pytest.raises(ClassifierUnavailable):
        asyncio.run(_mk(handler).decide("s", {"q1": "Python?"}))


def test_decide_with_retry_recovers_after_one_failure():
    calls = {"n": 0}

    class Flaky:
        kind = "flaky"
        async def decide(self, state, questions):
            calls["n"] += 1
            if calls["n"] == 1:
                raise ClassifierUnavailable("first")
            return {"q1": Judgement(p=0.7, confidence=0.8, distribution={})}

    out = asyncio.run(decide_with_retry(Flaky(), "s", {"q1": "Python?"}, retries=1))
    assert out["q1"].p == 0.7
    assert calls["n"] == 2


def test_fallback_without_key_returns_seeded(monkeypatch):
    monkeypatch.setattr(app_settings, "gemini_api_key", None)
    monkeypatch.setattr(app_settings, "openrouter_api_key", None)
    fb = LLMStructuredFallback(api_key=False, model="test")
    out = asyncio.run(fb.decide("candidate profile", {"q1": "Python?", "q2": "FastAPI?"}))
    assert set(out) == {"q1", "q2"}
    for j in out.values():
        assert isinstance(j, Judgement)
        assert 0.0 <= j.p <= 1.0
        assert 0.0 <= j.confidence <= 1.0


def test_fallback_openai_compatible_http_parses():
    def handler(request: httpx.Request) -> httpx.Response:
        body = request.read().decode()
        assert "temperature" in body
        assert '"type":"json_object"' in body.replace(" ", "")
        return httpx.Response(200, json={"choices": [{"message": {"content": (
            '{"judgements": {"q1": {"p": 0.8, "confidence": 0.7, '
            '"distribution": {"supporting": 0.8, "neutral": 0.2}}}}'
        )}}]})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    fb = LLMStructuredFallback(api_key="k", model="m", base_url="https://x/v1",
                               client_override=client)
    out = asyncio.run(fb.decide("s", {"q1": "Python?"}))
    assert out["q1"].p == 0.8


def test_fallback_provider_error_falls_back_to_seeded():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(502, text="bad gateway")

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    fb = LLMStructuredFallback(api_key="k", model="m", base_url="https://x/v1",
                               client_override=client)
    out = asyncio.run(fb.decide("s", {"q1": "Python?"}))
    assert 0.0 <= out["q1"].p <= 1.0


def test_fallback_invalid_json_from_provider_falls_back_to_seeded():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"choices": [{"message": {"content": "{not json"}}]})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    fb = LLMStructuredFallback(api_key="k", model="m", base_url="https://x/v1",
                               client_override=client)
    out = asyncio.run(fb.decide("s", {"q1": "Python?"}))
    assert 0.0 <= out["q1"].p <= 1.0
    assert any(r.get("kind") == "llm" and r.get("error") for r in METRICS._rows)


def test_seeded_judgement_is_deterministic_and_metadata_based():
    a = seeded_judgement("cand_x", "Must have Python", ["python", "fastapi"], 0.9)
    b = seeded_judgement("cand_x", "Must have Python", ["python", "fastapi"], 0.9)
    assert a.p == b.p
    assert a.confidence == b.confidence
    assert 0.0 <= a.p <= 1.0
    assert a.confidence <= 0.8  # seeded confidence capped, marked non-authoritative


def test_make_classifier_feature_flag():
    settings = __import__("app.config", fromlist=["settings"]).settings
    settings.typesafe_api_key = False  # type: ignore[assignment]
    from app.services.jevs import JevClassifier
    assert isinstance(make_classifier(), LLMStructuredFallback)
    settings.typesafe_api_key = "test-key"
    assert isinstance(make_classifier(), JevClassifier)
    settings.typesafe_api_key = None