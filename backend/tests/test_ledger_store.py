# backend/tests/test_ledger_store.py
import json
import tempfile
from pathlib import Path


def test_append_and_read():
    from app.db.ledger_store import LedgerStore

    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "hireflow.db"
        journal = Path(tmp) / "journal.jsonl"
        store = LedgerStore(db_path=db, journal_path=journal)
        h1 = store.append({"type": "SOURCE_INGESTED", "id": "src1", "run_id": "r1"})
        h2 = store.append({"type": "EVIDENCE_SPAN_MAPPED", "id": "ev1"})
        assert len(h1) == 64 and h2 != h1
        events = store.get_events()
        assert len(events) == 2
        assert events[0]["event_hash"] == h1


def test_jsonl_and_sqlite_parity():
    from app.db.ledger_store import LedgerStore

    with tempfile.TemporaryDirectory() as tmp:
        store = LedgerStore(db_path=Path(tmp) / "hireflow.db", journal_path=Path(tmp) / "j.jsonl")
        store.append({"type": "CLAIM", "id": "cl1"})
        lines = Path(store.journal_path).read_text().strip().splitlines()
        assert len(lines) == 1
        j = json.loads(lines[0])
        assert j["type"] == "CLAIM"
        assert "event_hash" in j


def test_supersede_sets_supersedes_id():
    from app.db.ledger_store import LedgerStore

    with tempfile.TemporaryDirectory() as tmp:
        store = LedgerStore(db_path=Path(tmp) / "hireflow.db", journal_path=Path(tmp) / "j.jsonl")
        store.append({"type": "ASSESSMENT", "id": "a1", "candidate_id": "c1"})
        store.supersede(
            "a1", {"type": "ASSESSMENT", "id": "a2", "candidate_id": "c1", "supersedes_id": "a1"}
        )
        evts = store.get_events()
        assert any(e.get("supersedes_id") == "a1" for e in evts)


def test_prev_hash_chain():
    from app.db.ledger_store import LedgerStore

    with tempfile.TemporaryDirectory() as tmp:
        store = LedgerStore(db_path=Path(tmp) / "hireflow.db", journal_path=Path(tmp) / "j.jsonl")
        h1 = store.append({"type": "X", "id": "1"})
        store.append({"type": "X", "id": "2"})
        evts = store.get_events()
        assert evts[1]["prev_hash"] == h1


def test_concurrent_appends_keep_chain_linear(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    import threading

    from app.db.ledger_store import LedgerStore

    store = LedgerStore(db_path=tmp_path / "t.db", journal_path=tmp_path / "j.jsonl")

    n = 16
    start = threading.Event()

    def one(i: int) -> str:
        start.wait()
        return store.append({"type": "TEST_PARALLEL", "i": i})

    with ThreadPoolExecutor(max_workers=n) as ex:
        futures = [ex.submit(one, i) for i in range(n)]
        start.set()
        hashes = [f.result() for f in futures]

    reopened = LedgerStore(db_path=tmp_path / "t.db", journal_path=tmp_path / "j.jsonl")
    evts = [e for e in reopened.get_events() if e["type"] == "TEST_PARALLEL"]
    assert len(evts) == n
    assert evts[0]["prev_hash"] is None
    for i in range(1, n):
        assert evts[i]["prev_hash"] == evts[i - 1]["event_hash"]
    assert len({e["event_hash"] for e in evts}) == n
    assert all(h for h in hashes)
