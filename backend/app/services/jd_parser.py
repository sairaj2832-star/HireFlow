# backend/app/services/jd_parser.py
from __future__ import annotations
import os
import re
from typing import Literal
from app.models.profile import Requirement

BULLET_RE = re.compile(r"^[\-\*\u2022]\s*(.+)$", re.M)
HARD_HINTS = {"must have", "required", "requirement", "minimum"}
SOFT_HINTS = {"nice to have", "preferred", "plus", "bonus"}

def _split_bullets(jd_text: str) -> list[str]:
    lines = [line.strip() for line in jd_text.splitlines() if line.strip()]
    bullets: list[str] = []
    no_bullet_markers_yet = True
    for line in lines:
        m = BULLET_RE.match(line)
        if m:
            bullets.append(m.group(1).strip())
            no_bullet_markers_yet = False
        elif no_bullet_markers_yet and len(line) > 12:
            # plain (non-bullet) long line is also a requirement in plain JD (only while no bullet markers seen)
            bullets.append(line)
    # fallback: split on commas/semicolons if no bullets found
    if not bullets:
        parts = re.split(r"[;,]\s*", jd_text)
        bullets = [p.strip() for p in parts if len(p.strip()) > 6][:8]
    # atomicity: break overly long bullets on 'and'/'with'
    atomic: list[str] = []
    for b in bullets:
        if len(b) > 100 and " and " in b.lower():
            for part in re.split(r"\s+and\s+", b, flags=re.I):
                if part.strip():
                    atomic.append(part.strip()[:110])
        else:
            atomic.append(b[:150])
    return [a for a in atomic if len(a) >= 6][:12]

def _gate_for(text: str, jd_lower: str) -> Literal["hard", "soft"]:
    t = text.lower()
    # jd-wide HARD_HINTS prefix first (first line only, before bullets)
    first_line = jd_lower.splitlines()[0].strip() if jd_lower.splitlines() else ""
    if any(h in first_line for h in HARD_HINTS):
        return "hard"
    # per-req "must"
    if "must" in t:
        return "hard"
    # per-req HARD_HINTS
    if any(h in t for h in HARD_HINTS):
        return "hard"
    # per-req SOFT_HINTS
    if any(h in t for h in SOFT_HINTS):
        return "soft"
    return "soft"

def parse_jd(jd_text: str, job_id: str | None = None) -> list[Requirement]:
    # LLM seam: if GEMINI_API_KEY set, attempt structured call; on any error fall back
    if os.getenv("GEMINI_API_KEY"):
        try:
            from app.services.jd_llm import llm_parse_jd  # not present in B1 → ImportError → fallback
            llm_reqs: list[Requirement] = llm_parse_jd(jd_text)
            if llm_reqs:
                return llm_reqs
        except Exception:
            pass
    bullets = _split_bullets(jd_text)
    reqs: list[Requirement] = []
    for i, b in enumerate(bullets, start=1):
        gate = _gate_for(b, jd_text)
        # weight: hard 0.25, soft 0.12, normalized later by policy
        weight = 0.25 if gate == "hard" else 0.12
        reqs.append(Requirement(id=f"REQ-{i:02d}", text=b, cls=gate, weight=weight, gate=gate))
    # ensure weights sum to ~1.0 (normalize)
    total = sum(r.weight for r in reqs) or 1.0
    for r in reqs:
        r.weight = round(r.weight / total, 3)
    return reqs

def parse_jd_bytes(raw: bytes, filename: str) -> list[Requirement]:
    text = raw.decode("utf-8", errors="ignore")
    # PyMuPDF seam: if pymupdf available and PDF, try extraction
    if filename.lower().endswith(".pdf"):
        try:
            import fitz
            doc = fitz.open(stream=raw, filetype="pdf")
            text = "\n".join(page.get_text() for page in doc) or text
        except Exception:
            pass
    return parse_jd(text)
