from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Union

from app.db.ledger_store import LedgerStore


PathLike = Union[Path, None]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _candidate_exists(store: LedgerStore, candidate_id: str) -> bool:
    return any(
        event.get("candidate_id") == candidate_id
        and event.get("type") in {
            "SOURCE_INGESTED",
            "JUDGMENT_RECORDED",
            "POLICY_STATE_SET",
            "INTERVIEW_NOTE",
        }
        for event in store.get_events()
    )


def add_interview_note(
    candidate_id: str,
    note_text: str,
    run_id: str,
    db_path: PathLike = None,
) -> dict[str, Any]:
    """Append an immutable interview note to the candidate ledger."""
    if not candidate_id:
        raise ValueError("candidate_id is required")
    if not note_text or not note_text.strip():
        raise ValueError("note_text is required")
    if not run_id:
        raise ValueError("run_id is required")

    store = LedgerStore(db_path=db_path)
    if not _candidate_exists(store, candidate_id):
        raise ValueError(f"candidate not found: {candidate_id}")

    note_id = f"note_{uuid.uuid4().hex[:12]}"
    timestamp = _utc_now()
    store.append({
        "type": "INTERVIEW_NOTE",
        "id": note_id,
        "note_id": note_id,
        "candidate_id": candidate_id,
        "note_text": note_text,
        "run_id": run_id,
        "timestamp": timestamp,
    })
    return {
        "note_id": note_id,
        "candidate_id": candidate_id,
        "note_text": note_text,
        "run_id": run_id,
        "timestamp": timestamp,
    }


def get_interview_notes(
    candidate_id: str,
    db_path: PathLike = None,
) -> list[dict[str, Any]]:
    """Return interview notes in ledger order for one candidate."""
    store = LedgerStore(db_path=db_path)
    if not _candidate_exists(store, candidate_id):
        raise ValueError(f"candidate not found: {candidate_id}")

    notes: list[dict[str, Any]] = []
    for event in store.get_events():
        if event.get("type") != "INTERVIEW_NOTE" or event.get("candidate_id") != candidate_id:
            continue
        notes.append({
            "note_id": event.get("note_id") or event.get("id"),
            "candidate_id": candidate_id,
            "note_text": event.get("note_text", ""),
            "run_id": event.get("run_id", ""),
            "timestamp": event.get("timestamp", ""),
        })
    return notes
