import asyncio
import httpx
import pytest
from app.models.classifier import Judgement, ClassifierUnavailable
from app.services.jevs import JevClassifier, Metrics, decide_with_retry


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