from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
from typing import Any
import uuid
from app.services.jd_parser import parse_jd, parse_jd_bytes
from app.services.intake import ingest_jd, ingest_resume

router = APIRouter(prefix="/jobs", tags=["jobs"])
_JOBS: dict[str, dict[str, Any]] = {}  # B1 in-memory; B2 moves to SQLite materialization


class CreateJobJson(BaseModel):
    title: str
    jd_text: str | None = None


@router.post("", status_code=201)
async def create_job(request: Request) -> dict[str, Any]:
    content_type = request.headers.get("content-type", "")
    job_id, run_id = f"job_{uuid.uuid4().hex[:8]}", f"run_{uuid.uuid4().hex[:8]}"
    
    if "multipart/form-data" in content_type:
        form = await request.form()
        jd_file = form.get("jd_file")
        _ = form.get("title", "Untitled Job")  # title accepted but not stored in B1
        jd_text = form.get("jd_text")
        
        if isinstance(jd_file, UploadFile):
            raw = await jd_file.read()
            reqs = parse_jd_bytes(raw, jd_file.filename or "jd.txt")
            ingest_jd(job_id, run_id, raw, jd_file.filename or "jd.txt", jd_file.content_type or "text/plain")
        elif jd_text:
            reqs = parse_jd(str(jd_text))
            ingest_jd(job_id, run_id, str(jd_text).encode(), "jd.txt", "text/plain")
        else:
            raise HTTPException(400, "provide jd_text or jd_file")
    else:
        # JSON body
        import json
        body = await request.body()
        try:
            data = json.loads(body)
            payload = CreateJobJson(**data)
        except Exception:
            raise HTTPException(400, "invalid JSON body")
        
        if payload.jd_text:
            reqs = parse_jd(payload.jd_text)
            ingest_jd(job_id, run_id, payload.jd_text.encode(), "jd.txt", "text/plain")
        else:
            raise HTTPException(400, "provide jd_text or jd_file")
    
    _JOBS[job_id] = {"job_id": job_id, "run_id": run_id, "requirements": [r.model_dump() for r in reqs]}
    return {"job_id": job_id, "run_id": run_id, "requirements": _JOBS[job_id]["requirements"]}


@router.get("/{job_id}")
def get_job(job_id: str) -> dict[str, Any]:
    if job_id not in _JOBS:
        raise HTTPException(404, "job not found")
    return _JOBS[job_id]


@router.patch("/{job_id}/requirements")
def patch_requirements(job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    # B1: simple overwrite, bump version; B6 adds version_diff
    if job_id not in _JOBS:
        raise HTTPException(404, "job not found")
    _JOBS[job_id]["requirements"] = payload.get("requirements", _JOBS[job_id]["requirements"])
    return _JOBS[job_id]


@router.post("/{job_id}/candidates:ingest")
def ingest_candidates(job_id: str, files: list[UploadFile] = File(...)) -> dict[str, list[str]]:
    if job_id not in _JOBS:
        raise HTTPException(404, "job not found")
    run_id = _JOBS[job_id]["run_id"]
    candidate_ids: list[str] = []
    quarantined: list[str] = []
    for f in files:
        raw = f.file.read()
        if f.content_type == "application/x-msdownload" or (f.filename or "").endswith(".exe"):
            raise HTTPException(400, f"blocked executable: {f.filename}")
        cid = f"cand_{uuid.uuid4().hex[:6]}"
        try:
            out = ingest_resume(job_id, run_id, cid, raw, f.filename or "cv.txt", f.content_type or "text/plain")
        except ValueError as e:
            if "blocked" in str(e):
                raise HTTPException(400, str(e))
            raise
        candidate_ids.append(cid)
        if out["quarantined"]:
            quarantined.append(cid)
    return {"candidate_ids": candidate_ids, "quarantined": quarantined}