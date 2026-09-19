# backend/app/services/cleanse.py
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Literal

Verdict = Literal["clean", "suspect", "blocked"]

EXECUTABLE_MIMES = {"application/x-msdownload", "application/x-executable", "application/x-sh"}
INSTRUCTION_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"rank\s+me\s+first",
    r"select\s+jonas\s+becker",  # Report §19.2 hidden-prompt archetype
    r"system\s*:\s*you\s+are",
]
PHANTOM_INK_THRESHOLD = 0.015  # <1.5% ink — stub: rendered/extracted length ratio proxy
RENDERED_DELTA_THRESHOLD = 0.5  # if extracted is >50% longer than raw, suspect

@dataclass(frozen=True)
class CleansingResult:
    verdict: Verdict
    phantom_flag: bool
    ink_ratio: float | None
    rendered_vs_extracted_delta: float | None
    signals: list[str]
    clean_text_ref: str  # never a mutated copy — points at input

def cleanse_upload(filename: str, mime: str, raw_bytes: bytes, extracted_text: str) -> CleansingResult:
    signals: list[str] = []
    phantom = False
    ink_ratio: float | None = None
    delta: float | None = None
    clean_text_ref = extracted_text  # reference, not mutation

    # executable mime → blocked before any parsing
    if mime.lower() in EXECUTABLE_MIMES or filename.lower().endswith((".exe", ".bat", ".sh")):
        return CleansingResult("blocked", False, None, None, ["executable"], clean_text_ref)

    text_lower = extracted_text.lower()
    for pat in INSTRUCTION_PATTERNS:
        if re.search(pat, text_lower):
            signals.append(f"instruction:{pat}")

    # rendered-vs-extracted delta (proxy for hidden text / white-on-white)
    raw_len = max(1, len(raw_bytes.decode(errors="ignore")))
    ext_len = max(1, len(extracted_text))
    delta = abs(ext_len - raw_len) / max(raw_len, ext_len)
    if delta > RENDERED_DELTA_THRESHOLD:
        signals.append(f"rendered_vs_extracted_delta:{delta:.2f}")
        phantom = True

    # ink ratio stub: if extracted is huge vs raw, flag phantom (<1.5% ink proxy)
    ink_ratio = min(1.0, raw_len / ext_len) if ext_len else 1.0
    if ink_ratio < PHANTOM_INK_THRESHOLD:
        phantom = True
        signals.append(f"phantom_ink:{ink_ratio:.4f}")

    if any("executable" in s for s in signals):
        verdict: Verdict = "blocked"
    elif signals:
        verdict = "suspect"
    else:
        verdict = "clean"
    # instruction always at least suspect, never clean
    if any("instruction" in s for s in signals) and verdict == "clean":
        verdict = "suspect"
    return CleansingResult(verdict, phantom, ink_ratio, delta, signals, clean_text_ref)
