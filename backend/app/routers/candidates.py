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


def _evidence_boxes(cand: dict[str, Any]) -> list[dict[str, Any]]:
    boxes = []
    for v in cand["per_req"]:
        boxes.append({
            "req": v["requirement_id"],
            "span": {"quote": "verified quote", "page": 1, "line": 1},
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
            "boxes": _evidence_boxes(hit["candidate"])}


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
