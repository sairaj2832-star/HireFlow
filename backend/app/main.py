import sqlite3
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import jobs

app = FastAPI(title="HireFlow", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router)


def _wal_mode() -> str:
    db = Path(__file__).resolve().parents[2] / "artifacts" / "hireflow.db"
    if not db.exists():
        return "unknown"
    try:
        con = sqlite3.connect(str(db))
        try:
            row = con.execute("PRAGMA journal_mode;").fetchone()
            return str(row[0]) if row else "unknown"
        finally:
            con.close()
    except Exception:
        return "unknown"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": app.version, "wal_mode": _wal_mode()}


@app.get("/")
def root() -> dict[str, str]:
    return {"name": "HireFlow", "docs": "/docs"}