from __future__ import annotations
from typing import Protocol
from pydantic import BaseModel, Field


class Judgement(BaseModel):
    p: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    distribution: dict[str, float] = Field(default_factory=dict)


class ScreenQuestion(BaseModel):
    id: str
    requirement_id: str
    requirement_text: str
    candidate_text: str
    span_quote: str | None = None


class Classifier(Protocol):
    kind: str

    async def decide(self, state: str, questions: dict[str, str]) -> dict[str, Judgement]: ...


class ClassifierUnavailable(RuntimeError):
    pass