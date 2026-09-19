"""Idempotent SQLite migration runner — WAL + FTS5 + append-only triggers."""

from pathlib import Path
from typing import Union
import sqlite3

MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "migrations"
DEFAULT_DB = Path(__file__).resolve().parents[2] / "artifacts" / "hireflow.db"


def migrate(db_path: Union[Path, None] = None) -> Path:
    db_path = Path(db_path) if db_path else DEFAULT_DB
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db_path))
    try:
        con.execute("PRAGMA journal_mode=WAL;")
        con.execute("PRAGMA foreign_keys=ON;")
        sql = (MIGRATIONS_DIR / "001_ledger.sql").read_text(encoding="utf-8")
        con.executescript(sql)
        con.commit()
        # Verify WAL actually set (win32 builds may silently fall back).
        cur = con.execute("PRAGMA journal_mode;")
        mode = cur.fetchone()[0]
        if mode.lower() != "wal":
            raise RuntimeError(f"WAL not enabled, got {mode}")
    finally:
        con.close()
    return db_path


if __name__ == "__main__":
    print(migrate())
