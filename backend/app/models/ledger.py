"""Ledger schemas — Report §5 ADR-001. Append-only; correction = supersedes_id."""

from __future__ import annotations

import hashlib
from typing import Any, Literal

from pydantic import BaseModel, Field


def hash_event(prev_hash: str | None, canonical_json: str) -> str:
    """event_hash = sha256((prev_hash or '') + canonical_json)."""
    payload = (prev_hash or "") + canonical_json
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class SourceRecord(BaseModel):
    id: str
    run_id: str
    kind: Literal["jd", "resume", "transcript", "notes"]
    filename: str
    mime: str
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    bytes: int = Field(ge=0)
    consent_tier: Literal["L0_application", "L1_pool"]
    retention_until: str | None = None
    created_at: str  # ISO datetime, validated loosely in B0


class Artifact(BaseModel):
    id: str
    source_id: str
    run_id: str
    parser: Literal["mineru", "pymupdf", "tesseract_ocr"]
    parser_version: str | None = None
    clean_text_ref: str
    cleanse: dict[str, Any]  # {phantom_flag, ink_ratio, rendered_vs_extracted_delta, verdict}
    event_hash: str | None = None


class EvidenceSpan(BaseModel):
    id: str
    artifact_id: str
    candidate_id: str
    quote: str = Field(min_length=8, max_length=600)
    loc: dict[str, Any]  # {page, line_start, line_end, char_start, char_end}
    granularity: Literal["sentence", "paragraph"] | None = None
    confidence: float = Field(ge=0, le=1)
    verified: dict[str, Any]  # {method, ratio, pass}
    supersedes_id: str | None = None


class Claim(BaseModel):
    id: str
    candidate_id: str
    text: str = Field(max_length=280)
    span_ids: list[str] = Field(min_length=1)
    polarity: Literal["asserts", "denies"] | None = None
    extractor: str | None = None
    supersedes_id: str | None = None


class Assessment(BaseModel):
    id: str
    candidate_id: str
    requirement_id: str
    grade: Literal["supporting", "neutral", "conflicting", "missing"]
    uncertainty: Literal["none", "unanswered", "conflicting", "unverifiable", "stale"] | None = None
    p: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    claim_ids: list[str]
    policy_hash: str
    judge: dict[str, Any]
    supersedes_id: str | None = None


class ReportAnswer(BaseModel):
    id: str
    kind: Literal["summary", "evaluation_report", "nl_answer", "question_set"]
    candidate_ids: list[str]
    assessment_ids: list[str] = Field(min_length=1)
    body_md: str
    version: int = Field(ge=1)
    prev_version_id: str | None = None
    version_diff: dict[str, Any] | None = None


class RunVersion(BaseModel):
    run_id: str
    code_sha: str
    policy_hash: str
    policy_version: str | None = None
    models: dict[str, Any]


class ApproverLog(BaseModel):
    id: str
    run_id: str
    actor: str
    action: Literal["approve", "override", "reject", "request_revalidation", "final_hire_decision"]
    target_ids: list[str]
    rationale: str | None = None
    time_on_evidence_s: int | None = Field(default=None, ge=0)
