# backend/app/models/profile.py
from __future__ import annotations
from typing import Any, Literal
import re
from pydantic import BaseModel, Field, field_validator
from app.services.config_loader import load_taxonomy

REQ_ID_RE = re.compile(r"^REQ-\d{2}$")

class Requirement(BaseModel):
    id: str = Field(pattern=r"^REQ-\d{2}$")
    text: str = Field(min_length=4, max_length=500)
    cls: Literal["hard", "soft"] = "soft"
    weight: float = Field(ge=0, le=1)
    gate: Literal["hard", "soft"] = "soft"
    evidence_needed: str | None = Field(default=None, max_length=300)

    @field_validator("id")
    @classmethod
    def check_id(cls, v: str) -> str:
        if not REQ_ID_RE.match(v):
            raise ValueError("id must be REQ-01..REQ-99")
        return v

class CandidateProfile(BaseModel):
    candidate_id: str
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    title: str | None = None
    summary: str | None = None
    skills: list[str] = Field(default_factory=list)
    normalized_skills: list[dict[str, Any]] = Field(default_factory=list)
    experience_years: float | None = Field(default=None, ge=0)
    experience_entries: list[dict[str, Any]] = Field(default_factory=list)
    education: list[dict[str, Any]] = Field(default_factory=list)
    projects: list[dict[str, Any]] = Field(default_factory=list)
    certifications: list[dict[str, Any]] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    seniority: str | None = None
    availability: str | None = None
    links: list[str] = Field(default_factory=list)
    raw_text_ref: str | None = None
    parse_confidence: float | None = Field(default=None, ge=0, le=1)
    extraction_method: str | None = None
    evidence_spans: list[str] = Field(default_factory=list)
    # synthetic-only: no date_of_birth, no photo, no zip-as-feature

_alias_index: dict[str, dict[str, Any]] | None = None

def _index() -> dict[str, dict[str, Any]]:
    global _alias_index
    if _alias_index is None:
        tax = load_taxonomy()
        idx: dict[str, dict[str, Any]] = {}
        for s in tax.get("skills", []):
            for key in [s["label"].lower()] + [a.lower() for a in s.get("aliases", [])]:
                idx[key] = s
        _alias_index = idx
    return _alias_index

def normalize_skills(raw_skills: list[str]) -> list[dict[str, Any]]:
    idx = _index()
    out: list[dict[str, Any]] = []
    for raw in raw_skills:
        key = raw.strip().lower()
        hit = idx.get(key)
        if hit:
            out.append({"id": hit["id"], "label": hit["label"], "raw": raw, "normalized": True})
        else:
            out.append({"id": f"custom:{key}", "label": raw.strip(), "raw": raw, "normalized": False})
    return out
