# backend/tests/test_migrate.py
import sqlite3
import tempfile
from pathlib import Path

SHA = "a" * 64


def test_migration_creates_tables_and_wal():
    from app.db.migrate import migrate

    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "hireflow.db"
        migrate(db_path=db)
        con = sqlite3.connect(str(db))
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        names = {r[0] for r in cur.fetchall()}
        assert "source_records" in names
        assert "artifacts" in names
        assert "evidence_spans" in names
        assert "claims" in names
        assert "assessments" in names
        assert "report_answers" in names
        assert "run_versions" in names
        assert "approver_logs" in names
        cur.execute("PRAGMA journal_mode;")
        assert cur.fetchone()[0].lower() == "wal"
        con.close()


def test_fts5_exists():
    from app.db.migrate import migrate

    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "hireflow.db"
        migrate(db_path=db)
        con = sqlite3.connect(str(db))
        cur = con.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='evidence_spans_fts'"
        )
        assert cur.fetchone() is not None
        con.close()


def test_trigger_rejects_update():
    from app.db.migrate import migrate

    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "hireflow.db"
        migrate(db_path=db)
        con = sqlite3.connect(str(db))
        try:
            con.execute(
                "INSERT INTO source_records (id, run_id, kind, filename, mime, sha256, bytes,"
                " consent_tier, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
                ("s1", "r1", "resume", "cv.pdf", "application/pdf", SHA, 1,
                 "L0_application", "2026-09-20T00:00:00Z"),
            )
            con.commit()
            try:
                con.execute("UPDATE source_records SET filename='hacked.pdf' WHERE id='s1'")
                con.commit()
                raise AssertionError("UPDATE should be rejected by trigger")
            except sqlite3.Error as e:
                # RAISE(ABORT, ...) surfaces as IntegrityError
                assert "append-only" in str(e).lower()
        finally:
            con.close()


def test_trigger_rejects_delete():
    from app.db.migrate import migrate

    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "hireflow.db"
        migrate(db_path=db)
        con = sqlite3.connect(str(db))
        try:
            con.execute(
                "INSERT INTO source_records (id, run_id, kind, filename, mime, sha256, bytes,"
                " consent_tier, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
                ("s2", "r1", "resume", "cv.pdf", "application/pdf", SHA, 1,
                 "L0_application", "2026-09-20T00:00:00Z"),
            )
            con.commit()
            try:
                con.execute("DELETE FROM source_records WHERE id='s2'")
                raise AssertionError("DELETE should be rejected by trigger")
            except sqlite3.Error:
                pass
        finally:
            con.close()
