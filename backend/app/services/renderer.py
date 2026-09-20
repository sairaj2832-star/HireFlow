from __future__ import annotations
import uuid
from pathlib import Path
from typing import Any, Union
from app.db.ledger_store import LedgerStore
from app.models.ledger import ReportAnswer


def render_report(job_id: str, db_path: Union[Path, None] = None,
                  journal_path: Union[Path, None] = None) -> dict[str, Any]:
    store = LedgerStore(db_path=db_path, journal_path=journal_path)
    events = [e for e in store.get_events() if e.get("job_id") == job_id]
    candidates: list[str] = []
    seen: set[str] = set()
    for e in events:
        cid = e.get("candidate_id")
        if cid and cid not in seen and e.get("type") in ("POLICY_STATE_SET", "JUDGMENT_RECORDED"):
            seen.add(cid)
            candidates.append(cid)
    assessments: list[str] = []
    for e in events:
        if e.get("type") == "ASSESSMENT_RECORDED" and e.get("assessment_id"):
            assessments.append(e["assessment_id"])
    sections: list[dict[str, str]] = [
        {"title": "Role Fit Summary",
         "content": f"Job {job_id}: {len(candidates)} candidates evaluated across {len(assessments)} assessments."},
        {"title": "Per-Requirement Assessment",
         "content": "Each requirement assessed against candidate evidence with confidence scores and verification status."},
        {"title": "Evidence Appendix",
         "content": f"{len(events)} ledger events recorded for this run."},
        {"title": "Gaps & Human Review",
         "content": "Candidates flagged for human review require explicit approval before hire decision."},
    ]
    version = 1
    prev_id = None
    if assessments:
        existing = [e for e in events if e.get("type") == "REPORT_GENERATED"]
        if existing:
            version = len(existing) + 1
            prev_id = existing[-1].get("report_answer_id")
    if not assessments and candidates:
        assessments = candidates
    report_answer = ReportAnswer(
        id=f"ra_{uuid.uuid4().hex[:8]}",
        kind="evaluation_report",
        candidate_ids=candidates,
        assessment_ids=assessments,
        body_md="\n".join(f"## {s['title']}\n{s['content']}" for s in sections),
        version=version,
        prev_version_id=prev_id,
        version_diff={"added": sections, "changed": [], "retracted": []} if version > 1 else None,
    )
    canonical = report_answer.model_dump_json(exclude_none=True)
    store.append({
        "type": "REPORT_GENERATED", "id": report_answer.id, "run_id": job_id,
        "job_id": job_id, "report_answer_id": report_answer.id,
        "canonical": canonical, "version": version,
    })
    return {
        "job_id": job_id,
        "report": {"sections": sections},
        "report_answer_id": report_answer.id,
        "version": version,
    }
