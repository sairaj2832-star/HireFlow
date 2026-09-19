"""Dual-write ledger store — JSONL journal + materialized SQLite (Report §5 ADR-001)."""

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any, Union

from app.db.migrate import DEFAULT_DB, migrate

DEFAULT_JOURNAL = Path(__file__).resolve().parents[2] / "artifacts" / "journal.jsonl"


def _hash(prev: Union[str, None], canonical: str) -> str:
    return hashlib.sha256(((prev or "") + canonical).encode()).hexdigest()


class LedgerStore:
    """Append-only event log. Every arrow in the Judged Ledger Loop appends here."""

    def __init__(
        self, db_path: Union[Path, None] = None, journal_path: Union[Path, None] = None
    ) -> None:
        self.db_path = Path(db_path) if db_path else DEFAULT_DB
        self.journal_path = Path(journal_path) if journal_path else DEFAULT_JOURNAL
        migrate(self.db_path)
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.journal_path.exists():
            self.journal_path.write_text("", encoding="utf-8")

    def _last_hash(self, con: sqlite3.Connection) -> Union[str, None]:
        cur = con.execute("SELECT event_hash FROM ledger_events ORDER BY seq DESC LIMIT 1")
        row = cur.fetchone()
        return str(row[0]) if row else None

    def append(self, payload: dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        con = sqlite3.connect(str(self.db_path))
        try:
            prev = self._last_hash(con)
            h = _hash(prev, canonical)
            enriched = {**payload, "event_hash": h, "prev_hash": prev}
            line = json.dumps(enriched, sort_keys=True, separators=(",", ":"))
            con.execute(
                "INSERT INTO ledger_events (event_hash, prev_hash, canonical_json)"
                " VALUES (?,?,?)",
                (h, prev, line),
            )
            con.commit()
            with open(self.journal_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            return h
        finally:
            con.close()

    def supersede(self, old_id: str, new_payload: dict[str, Any]) -> str:
        assert new_payload.get("supersedes_id") == old_id
        return self.append(new_payload)

    def get_events(self, limit: Union[int, None] = None) -> list[dict[str, Any]]:
        con = sqlite3.connect(str(self.db_path))
        try:
            q = "SELECT canonical_json FROM ledger_events ORDER BY seq ASC"
            if limit:
                q += f" LIMIT {limit}"
            rows = con.execute(q).fetchall()
            return [json.loads(r[0]) for r in rows]
        finally:
            con.close()
