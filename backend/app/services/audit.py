from __future__ import annotations
from pathlib import Path
from typing import Any, Union
from app.db.ledger_store import LedgerStore


def build_audit_pack(job_id: str, db_path: Union[Path, None] = None,
                     journal_path: Union[Path, None] = None) -> dict[str, Any]:
    store = LedgerStore(db_path=db_path, journal_path=journal_path)
    events = [e for e in store.get_events() if e.get("job_id") == job_id]
    audit_events: list[dict[str, Any]] = []
    for e in events:
        audit_events.append({
            "event": e.get("type", "UNKNOWN"),
            "timestamp": e.get("event_hash", ""),
            "detail": str({k: v for k, v in e.items()
                           if k not in ("event_hash", "prev_hash", "canonical_json")}),
        })
    return {
        "job_id": job_id,
        "audit_events": audit_events,
        "count": len(audit_events),
    }
