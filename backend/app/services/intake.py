# backend/app/services/intake.py
from __future__ import annotations
import hashlib
import uuid
from pathlib import Path
from typing import Any, Union
from app.services.cleanse import cleanse_upload
from app.services.jd_parser import parse_jd_bytes
from app.services.resume_parser import parse_resume
from app.db.ledger_store import LedgerStore

def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sid(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def ingest_jd(job_id: str, run_id: str, raw: bytes, filename: str, mime: str,
              db_path: Union[Path, None]=None, journal_path: Union[Path, None]=None) -> dict[str, Any]:
    store = LedgerStore(db_path=db_path, journal_path=journal_path)
    extracted = raw.decode(errors="ignore")
    if filename.lower().endswith(".pdf"):
        try:
            import fitz
            with fitz.open(stream=raw, filetype="pdf") as doc:
                extracted = "\n".join(p.get_text() for p in doc) or extracted
        except Exception:
            pass
    cr = cleanse_upload(filename, mime, raw, extracted)
    if cr.verdict == "blocked":
        raise ValueError("blocked: executable or policy violation")
    source_id, artifact_id = _sid("src"), _sid("art")
    store.append({"type":"SOURCE_INGESTED","id":source_id,"run_id":run_id,"job_id":job_id,"kind":"jd","filename":filename,"sha256":_sha(raw),"verdict":cr.verdict})
    store.append({"type":"ARTIFACT_CLEANSED","id":artifact_id,"source_id":source_id,"run_id":run_id,"parser":"pymupdf","cleanse":{"phantom_flag":cr.phantom_flag,"verdict":cr.verdict,"signals":list(cr.signals)}})
    reqs = parse_jd_bytes(raw, filename)
    span_ids: list[str] = []
    for r in reqs:
        sid = _sid("span")
        store.append({"type":"REQUIREMENT_DEFINED","id":r.id,"job_id":job_id,"text":r.text,"weight":r.weight,"gate":r.gate})
        store.append({"type":"EVIDENCE_SPAN_MAPPED","id":sid,"artifact_id":artifact_id,"quote":r.text,"loc":{"page":1,"line_start":1,"line_end":1,"char_start":0,"char_end":len(r.text)}})
        span_ids.append(sid)
    return {"source_id":source_id,"artifact_id":artifact_id,"verdict":cr.verdict,"quarantined":cr.verdict!="clean","span_ids":span_ids,"event_hashes":[store.get_events()[-1]["event_hash"]]}

def ingest_resume(job_id: str, run_id: str, candidate_id: str, raw: bytes, filename: str, mime: str,
                  db_path: Union[Path, None]=None, journal_path: Union[Path, None]=None) -> dict[str, Any]:
    store = LedgerStore(db_path=db_path, journal_path=journal_path)
    extracted = raw.decode(errors="ignore")
    if filename.lower().endswith(".pdf"):
        try:
            import fitz
            with fitz.open(stream=raw, filetype="pdf") as doc:
                extracted = "\n".join(p.get_text() for p in doc) or extracted
        except Exception:
            pass
    uploads = Path(__file__).resolve().parents[2] / "artifacts" / "uploads"
    uploads.mkdir(parents=True, exist_ok=True)
    (uploads / f"{candidate_id}.txt").write_text(extracted, encoding="utf-8", errors="ignore")
    cr = cleanse_upload(filename, mime, raw, extracted)
    if cr.verdict == "blocked":
        raise ValueError("blocked: executable or policy violation")
    source_id, artifact_id = _sid("src"), _sid("art")
    store.append({"type":"SOURCE_INGESTED","id":source_id,"run_id":run_id,"job_id":job_id,"kind":"resume","candidate_id":candidate_id,"filename":filename,"sha256":_sha(raw),"verdict":cr.verdict})
    store.append({"type":"ARTIFACT_CLEANSED","id":artifact_id,"source_id":source_id,"run_id":run_id,"parser":"pymupdf","cleanse":{"phantom_flag":cr.phantom_flag,"verdict":cr.verdict,"signals":list(cr.signals)}})
    profile = parse_resume(raw, filename, candidate_id)
    span_ids: list[str] = []
    for q in profile.evidence_spans:
        sid = _sid("span")
        store.append({"type":"EVIDENCE_SPAN_MAPPED","id":sid,"artifact_id":artifact_id,"candidate_id":candidate_id,"quote":q,"loc":{"page":1,"line_start":1,"line_end":1,"char_start":0,"char_end":len(q)}})
        span_ids.append(sid)
    quarantined = cr.verdict != "clean"
    return {"source_id":source_id,"artifact_id":artifact_id,"verdict":cr.verdict,"quarantined":quarantined,"span_ids":span_ids,"candidate_id":candidate_id}
