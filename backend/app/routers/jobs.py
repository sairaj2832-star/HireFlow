"""B0 stub — B1 wires real job/candidate routes (14 REST, Report §13.2)."""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/jobs/{job_id}")
def get_job(job_id: str) -> dict[str, str]:
    raise HTTPException(status_code=501, detail=f"B1: job {job_id} routes not implemented")
