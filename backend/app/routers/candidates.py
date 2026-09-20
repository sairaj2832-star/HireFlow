# backend/app/routers/candidates.py
from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/candidates", tags=["candidates"])

_Latest = tuple[str, str, dict[str, Any], dict[str, Any]]


def _latest_screen(candidate_id: str) -> dict[str, Any] | None:
    from app.routers.jobs import _SCREENS
    best: _Latest | None = None
    for job_id, scr in _SCREENS.items():
        m = {c["candidate_id"]: c for c in scr.get("candidates", [])}
        if candidate_id in m:
            if best is None or scr.get("run_id", "") > best[0]:
                best = (scr.get("run_id", ""), job_id, scr, m[candidate_id])
    if best is None:
        return None
    run_id, job_id, scr, cand = best
    return {"run_id": run_id, "job_id": job_id, "candidate": cand}


def _ledger_spans(candidate_id: str) -> list[dict[str, Any]]:
    from app.db.ledger_store import LedgerStore
    store = LedgerStore()
    return [e for e in store.get_events()
            if e.get("type") == "EVIDENCE_SPAN_MAPPED"
            and e.get("candidate_id") == candidate_id]


def _requirement_texts(job_id: str) -> dict[str, str]:
    from app.db.ledger_store import LedgerStore
    store = LedgerStore()
    out: dict[str, str] = {}
    for e in store.get_events():
        if e.get("type") == "REQUIREMENT_DEFINED" and e.get("job_id") == job_id:
            rid = e.get("id")
            if rid:
                out[rid] = e.get("text", "")
    return out


def _evidence_boxes(cand: dict[str, Any], job_id: str) -> list[dict[str, Any]]:
    spans = _ledger_spans(cand["candidate_id"] if "candidate_id" in cand else "")
    req_texts = _requirement_texts(job_id)
    boxes: list[dict[str, Any]] = []
    for v in cand["per_req"]:
        rid = v["requirement_id"]
        matched = ""
        page = 1
        line = 1
        for s in spans:
            if s.get("quote"):
                if (req_texts.get(rid, "") and req_texts[rid].lower() in s["quote"].lower()) \
                        or (rid in s.get("quote", "")):
                    matched = s["quote"]
                    loc = s.get("loc", {})
                    page = loc.get("page", 1) or 1
                    line = loc.get("line_start", 1) or 1
                    break
        if not matched:
            matched = spans[0]["quote"] if spans else "verified quote"
            loc = spans[0].get("loc", {}) if spans else {}
            page = loc.get("page", 1) or 1
            line = loc.get("line_start", 1) or 1
        boxes.append({
            "req": rid,
            "span": {"quote": matched[:600], "page": page, "line": line},
            "judgment": {"p": v["p"], "confidence": v["confidence"], "grade": v["grade"]},
            "state": "VERIFIED" if v.get("needs_review") is False else "NEEDS_REVIEW",
            "conf": v["confidence"],
        })
    return boxes


@router.get("/{candidate_id}")
def get_candidate(candidate_id: str) -> dict[str, Any]:
    hit = _latest_screen(candidate_id)
    if hit is None:
        raise HTTPException(404, "candidate not found")
    c = hit["candidate"]
    return {"candidate_id": candidate_id,
            "screenings": [{"job_id": hit["job_id"], "run_id": hit["run_id"],
                            "tier": c["tier"], "composite": c["composite"],
                            "needs_review": c["needs_review"]}]}


@router.get("/{candidate_id}/evidence")
def get_evidence(candidate_id: str) -> dict[str, Any]:
    hit = _latest_screen(candidate_id)
    if hit is None:
        raise HTTPException(404, "candidate not screened")
    return {"candidate_id": candidate_id, "run_id": hit["run_id"],
            "boxes": _evidence_boxes(hit["candidate"], hit["job_id"])}


@router.get("/{candidate_id}/questions")
def get_questions(candidate_id: str) -> dict[str, Any]:
    hit = _latest_screen(candidate_id)
    if hit is None:
        raise HTTPException(404, "candidate not found")
    from app.db.ledger_store import LedgerStore
    store = LedgerStore()
    questions: list[dict[str, str]] = []
    for e in store.get_events():
        if e.get("type") == "QUESTION_GENERATED" and e.get("candidate_id") == candidate_id:
            for q in e.get("questions", []):
                questions.append({
                    "question_id": q.get("question_id", ""),
                    "requirement_id": q.get("requirement_id", ""),
                    "gap_text": q.get("gap_text", ""),
                    "question": q.get("question", ""),
                })
    return {"candidate_id": candidate_id, "questions": questions}


@router.post("/{candidate_id}/questions")
def post_questions(candidate_id: str) -> dict[str, Any]:
    hit = _latest_screen(candidate_id)
    if hit is None:
        raise HTTPException(404, "candidate not found or not screened")
    from app.routers.jobs import _JOBS
    from app.services.qg import generate_questions
    requirements = _JOBS.get(hit["job_id"], {}).get("requirements", [])
    try:
        questions = generate_questions(candidate_id, requirements, [])
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    return {"candidate_id": candidate_id, "questions": questions}


class InterviewNoteRequest(BaseModel):
    note: str = Field(min_length=1)


@router.post("/{candidate_id}/interview-notes")
def post_interview_notes(candidate_id: str, payload: InterviewNoteRequest) -> dict[str, str]:
    hit = _latest_screen(candidate_id)
    if hit is None:
        raise HTTPException(404, "candidate not found")
    run_id = hit.get("run_id") or "interview_note"
    from app.services.interview import add_interview_note
    try:
        result = add_interview_note(candidate_id, payload.note, run_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    return {"note_id": result["note_id"], "status": "recorded"}
