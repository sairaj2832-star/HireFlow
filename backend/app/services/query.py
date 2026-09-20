from __future__ import annotations
from pathlib import Path
from typing import Any, Union
from app.db.ledger_store import LedgerStore


def nl_query(job_id: str, filter_field: str, value: str,
             db_path: Union[Path, None] = None,
             journal_path: Union[Path, None] = None) -> dict[str, Any]:
    store = LedgerStore(db_path=db_path, journal_path=journal_path)
    events = [e for e in store.get_events() if e.get("job_id") == job_id]
    results: list[dict[str, Any]] = []
    for e in events:
        if e.get("type") != "POLICY_STATE_SET":
            continue
        cid = e.get("candidate_id")
        if not cid:
            continue
        if filter_field == "tier" and str(e.get("tier", "")) == value:
            results.append({
                "candidate_id": cid,
                "score": float(e.get("composite", 0.0)),
                "tier": e.get("tier", ""),
            })
        elif filter_field == "grade" and e.get("grade") == value:
            results.append({
                "candidate_id": cid,
                "score": float(e.get("composite", 0.0)),
                "tier": e.get("tier", ""),
            })
        elif filter_field == "candidate_id" and cid == value:
            results.append({
                "candidate_id": cid,
                "score": float(e.get("composite", 0.0)),
                "tier": e.get("tier", ""),
            })
    results.sort(key=lambda r: r["score"], reverse=True)
    return {"job_id": job_id, "results": results}
