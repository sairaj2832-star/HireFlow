from __future__ import annotations
import hashlib
import json
import random
import threading
import time
from pathlib import Path
from typing import Any

import httpx

from pydantic import ValidationError

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
            return {qid: Judgement(**j) for qid, j in data.items()}
        except (ValueError, KeyError, ValidationError, TypeError, AttributeError) as exc:
            raise ClassifierUnavailable("jev unparseable response") from exc


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


SEED_BUNDLE = Path(__file__).resolve().parents[2] / "artifacts" / "seed" / "fallback_bundle.json"


def _load_seed() -> dict[str, Any]:
    if SEED_BUNDLE.exists():
        data = json.loads(SEED_BUNDLE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    return {"subjective": 0.5, "confidence": 0.55}


def seeded_judgement(question_id: str, requirement_text: str,
                     candidate_keywords: list[str], parse_confidence: float) -> Judgement:
    """OUR CHOICE deterministic offline fallback — meters needs-review rate, never claims accuracy."""
    seed = _load_seed()
    digest = int(hashlib.sha256(f"{question_id}:{requirement_text}".encode()).hexdigest(), 16)
    rng = random.Random(digest % (2**32))
    base = seed.get("subjective", 0.5)
    kw = [k for k in candidate_keywords if k and k in requirement_text.lower()]
    boost = 0.15 * min(len(kw), 2)
    p = min(1.0, max(0.0, base + boost + rng.choice([-0.05, 0.0, 0.05])))
    conf = min(seed.get("confidence", 0.55), 0.8)
    return Judgement(p=round(p, 3), confidence=round(conf, 3),
                     distribution={"supporting": round(p, 3), "neutral": round(1 - p, 3)})


class LLMStructuredFallback:
    """LLM structured-output classifier (OpenAI-compatible). Identical {p,confidence,distribution}.

    Seeded bundle when unconfigured/offline — demo never blocks (MASTER §58, Report §17).
    LiteLLM gateway can slot in behind this seam (model<>policy contract unchanged).
    """

    kind = "llm"

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini",
                 base_url: str = "https://api.openai.com/v1",
                 client_override: httpx.AsyncClient | None = None) -> None:
        self.api_key = api_key or settings.gemini_api_key or settings.openrouter_api_key
        if settings.openrouter_api_key:
            self.base_url = "https://openrouter.ai/api/v1"
        else:
            self.base_url = base_url
        self.model = model
        self._client = client_override

    async def decide(self, state: str, questions: dict[str, str]) -> dict[str, Judgement]:
        if not self.api_key:
            return self._seeded(state, questions)
        t0 = time.perf_counter()
        try:
            client = self._client
            own = False
            if client is None:
                client = httpx.AsyncClient()
                own = True
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "temperature": 0,
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {"role": "system",
                         "content": "You map a candidate profile to job requirements. Return ONLY "
                                    "JSON {judgements:{<id>:{p:0..1,confidence:0..1,"
                                    "distribution:{supporting:..,neutral:..}}}}. "
                                    "p is P(requirement supported by candidate evidence)."},
                        {"role": "user",
                         "content": f"CANDIDATE:\n{state}\n\nREQUIREMENTS:\n"
                                    + "\n".join(f"{qid}: {text}" for qid, text in questions.items())},
                    ],
                },
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10.0,
            )
            if own:
                await client.aclose()
            METRICS.add({"kind": self.kind, "latency_ms": (time.perf_counter() - t0) * 1000,
                         "cost": None, "questions": len(questions)})
            if resp.status_code != 200:
                return self._seeded(state, questions)
            data = resp.json()["choices"][0]["message"]["content"]
            parsed = json.loads(data).get("judgements", {})
            out: dict[str, Judgement] = {}
            for qid, j in parsed.items():
                if qid in questions and set(j) >= {"p", "confidence"}:
                    try:
                        out[qid] = Judgement(**j)
                    except Exception:  # noqa: BLE001 — skip malformed item, keep the rest
                        continue
            if out:
                return out
            return self._seeded(state, questions)
        except Exception as exc:  # noqa: BLE001 — MUST fall back, never block demo
            METRICS.add({"kind": self.kind, "latency_ms": (time.perf_counter() - t0) * 1000,
                         "cost": None, "questions": len(questions), "error": str(exc)})
            return self._seeded(state, questions)

    def _seeded(self, state: str, questions: dict[str, str]) -> dict[str, Judgement]:
        keywords = [tok.strip(".,:;()[]{}\"'") for tok in state.lower().split()]
        return {qid: seeded_judgement(qid, text, [k for k in keywords if len(k) > 2], 0.5)
                for qid, text in questions.items()}


def make_classifier() -> Classifier:
    """Feature flag (MASTER §58): Jev primary iff TYPESAFE_API_KEY, else LLM fallback."""
    if settings.typesafe_api_key:
        return JevClassifier()
    return LLMStructuredFallback()