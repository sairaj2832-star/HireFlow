from __future__ import annotations
import threading
import time
from typing import Any
import httpx

from app.config import settings
from app.models.classifier import Judgement, Classifier, ClassifierUnavailable


class Metrics:
    """Thread-safe latency + cost log per classifier call (AGENTS.md §64 #7)."""

    def __init__(self) -> None:
        self._rows: list[dict[str, Any]] = []
        self._lock = threading.Lock()

    def add(self, row: dict[str, Any]) -> None:
        with self._lock:
            self._rows.append(row)

    def latency_p50_p95(self) -> tuple[float, float]:
        with self._lock:
            vals = sorted(r["latency_ms"] for r in self._rows)
        if not vals:
            return 0.0, 0.0
        n = len(vals)
        p50 = vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2
        p95 = vals[min(n - 1, int(0.95 * n) if n > 1 else 0)]
        return float(p50), float(p95)

    def summary(self) -> dict[str, Any]:
        p50, p95 = self.latency_p50_p95()
        return {
            "calls": len(self._rows),
            "latency_p50_ms": p50,
            "latency_p95_ms": p95,
            "total_questions": sum(r.get("questions", 0) for r in self._rows),
            "total_cost": sum(r.get("cost") or 0.0 for r in self._rows),
        }


METRICS = Metrics()


class JevClassifier:
    """Jev (TypeSafe systemone) primary classifier. Feature-flagged by TYPESAFE_API_KEY."""

    kind = "jev"
    endpoint = "https://api.typesafe.ai/v1/systemone"

    def __init__(self, api_key: str | None = None, timeout_s: float = 10.0,
                 client_override: httpx.AsyncClient | None = None) -> None:
        self.api_key = api_key or settings.typesafe_api_key
        self.timeout_s = timeout_s
        self._client = client_override
        self.model = "jev/systemone"

    async def _post(self, payload: dict[str, Any]) -> httpx.Response:
        client = self._client
        own = False
        if client is None:
            client = httpx.AsyncClient(timeout=self.timeout_s)
            own = True
        try:
            return await client.post(
                self.endpoint,
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.timeout_s,
            )
        finally:
            if own:
                await client.aclose()

    async def decide(self, state: str, questions: dict[str, str]) -> dict[str, Judgement]:
        if not self.api_key:
            raise ClassifierUnavailable("typesafe_api_key not configured")
        t0 = time.perf_counter()
        try:
            resp = await self._post({
                "state": state,
                "questions": [{"id": qid, "text": text} for qid, text in questions.items()],
            })
        except (httpx.TimeoutException, httpx.HTTPError) as exc:
            METRICS.add({"kind": self.kind, "latency_ms": (time.perf_counter() - t0) * 1000,
                         "cost": None, "questions": len(questions)})
            raise ClassifierUnavailable(str(exc)) from exc
        METRICS.add({"kind": self.kind, "latency_ms": (time.perf_counter() - t0) * 1000,
                     "cost": None, "questions": len(questions)})
        if resp.status_code != 200:
            raise ClassifierUnavailable(f"jev http {resp.status_code}")
        try:
            data = resp.json()["judgements"]
        except (ValueError, KeyError) as exc:
            raise ClassifierUnavailable("jev unparseable response") from exc
        return {qid: Judgement(**j) for qid, j in data.items()}


async def decide_with_retry(classifier: Classifier, state: str, questions: dict[str, str],
                            retries: int = 1) -> dict[str, Judgement]:
    last: Exception | None = None
    for _ in range(retries + 1):
        try:
            return await classifier.decide(state, questions)
        except ClassifierUnavailable as exc:
            last = exc
            continue
    assert last is not None
    raise last