# backend/app/services/resume_parser.py
from __future__ import annotations
import re
from typing import Any
from app.models.profile import CandidateProfile, normalize_skills

SKILL_LINE_RE = re.compile(r"skills\s*:\s*(.+)", re.I)
EXP_YEARS_RE = re.compile(r"(\d+(?:\.\d+)?)\s*years?", re.I)
EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PROJECT_RE = re.compile(r"projects?\s*:\s*(.+)", re.I)

def _extract_text(raw: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        try:
            import fitz
            doc = fitz.open(stream=raw, filetype="pdf")
            return "\n".join(p.get_text() for p in doc) or raw.decode(errors="ignore")
        except Exception:
            pass
    return raw.decode(errors="ignore")

def parse_resume_text(text: str, candidate_id: str) -> CandidateProfile:
    skills: list[str] = []
    m = SKILL_LINE_RE.search(text)
    if m:
        skills = [s.strip() for s in re.split(r"[,;|]", m.group(1)) if s.strip()]
    else:
        # fallback: scan for known skill tokens in full text
        for tok in ["Python", "FastAPI", "PyTorch", "React", "Docker", "SQL"]:
            if re.search(rf"\b{re.escape(tok)}\b", text, re.I):
                skills.append(tok)
    years: float | None = None
    ym = EXP_YEARS_RE.search(text)
    if ym:
        years = float(ym.group(1))
    email = EMAIL_RE.search(text)
    projects: list[dict[str, Any]] = []
    pm = PROJECT_RE.search(text)
    if pm:
        projects.append({"name": pm.group(1).strip()[:200], "description": pm.group(1).strip()})
    # evidence spans: sentence-level quotes containing a skill
    sentences = re.split(r"(?<=[\.\n])\s+", text)
    spans = [s.strip() for s in sentences if any(k.lower() in s.lower() for k in skills)][:6]
    spans = [s for s in spans if 8 <= len(s) <= 600]
    return CandidateProfile(
        candidate_id=candidate_id,
        email=email.group(0) if email else None,
        skills=skills,
        normalized_skills=normalize_skills(skills),
        experience_years=years,
        projects=projects,
        raw_text_ref=text[:4000],
        parse_confidence=0.78 if skills else 0.35,
        extraction_method="regex+alias",
        evidence_spans=spans,
    )

def parse_resume(raw: bytes, filename: str, candidate_id: str) -> CandidateProfile:
    return parse_resume_text(_extract_text(raw, filename), candidate_id)
