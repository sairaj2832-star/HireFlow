# backend/app/services/screening.py
from __future__ import annotations
import uuid
from pathlib import Path
from typing import Any, Union

from app.db.ledger_store import LedgerStore
from app.models.policy import load_policy_typed
from app.models.profile import Requirement
from app.services import policy as policy_svc
from app.services.config_loader import policy_hash
from app.services.grouping import build_cohorts
from app.services.jevs import decide_with_retry, make_classifier
from app.services.verifier import (VERIFY_FAIL, VERIFY_PASS, anomaly_flag, verify_quote)

_UPLOADS = Path(__file__).resolve().parents[2] / "artifacts" / "uploads"


def _sid(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def candidate_source_text(candidate_id: str, db_path: Union[Path, None] = None,
                          journal_path: Union[Path, None] = None) -> str:
    f = _UPLOADS / f"{candidate_id}.txt"
    if f.exists():
        return f.read_text(encoding="utf-8", errors="ignore")
    store = LedgerStore(db_path=db_path, journal_path=journal_path)
    quotes = [e["quote"] for e in store.get_events()
              if e.get("type") == "EVIDENCE_SPAN_MAPPED" and e.get("candidate_id") == candidate_id]
    return "\n".join(quotes)


def _requirements(job_id: str, db_path: Union[Path, None]) -> list[Requirement]:
    store = LedgerStore(db_path=db_path)
    out: list[Requirement] = []
    for e in store.get_events():
        if e.get("type") == "REQUIREMENT_DEFINED" and e.get("job_id") == job_id:
            out.append(Requirement(id=e["id"], text=e["text"],
                                   cls=e.get("cls", "soft"),
                                   weight=float(e.get("weight", 0.3)),
                                   gate=e.get("gate", "soft"),
                                   evidence_needed=e.get("evidence_needed")))
    return out


def _candidates(job_id: str, db_path: Union[Path, None]) -> list[tuple[str, str]]:
    store = LedgerStore(db_path=db_path)
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for e in store.get_events():
        cid = e.get("candidate_id")
        if e.get("type") == "SOURCE_INGESTED" and e.get("kind") == "resume" \
                and e.get("job_id") == job_id and cid and cid not in seen:
            seen.add(cid)
            out.append((cid, candidate_source_text(cid, db_path)))
    return out


async def run_screen(job_id: str, db_path: Union[Path, None] = None,
                     journal_path: Union[Path, None] = None) -> dict[str, Any]:
    store = LedgerStore(db_path=db_path, journal_path=journal_path)
    reqs = _requirements(job_id, db_path)
    if not reqs:
        raise ValueError(f"unknown job or no requirements: {job_id}")
    pol = load_policy_typed()
    phash = policy_hash()
    candidates = _candidates(job_id, db_path)
    classifier = make_classifier()
    run_id = f"run_{uuid.uuid4().hex[:8]}"

    screen_candidates: list[dict[str, Any]] = []
    total_checked = 0
    total_verified = 0

    events = store.get_events()  # hoisted once
    spans_by_candidate: dict[str, list[str]] = {}
    for e in events:
        cid = e.get("candidate_id")
        if e.get("type") == "EVIDENCE_SPAN_MAPPED" and cid:
            spans_by_candidate.setdefault(cid, []).append(e.get("quote", ""))

    for cid, text in candidates:
        questions = {f"{cid}:{r.id}": r.text for r in reqs}
        judgements: dict[str, Any] = {}
        try:
            judgements = await decide_with_retry(classifier, text, questions,
                                                 retries=pol.loop.retries)
        except Exception:  # noqa: BLE001 — never abort screening on provider failure
            judgements = {qid: None for qid in questions}

        per_req_judgements: dict[str, dict[str, float]] = {}
        for r in reqs:
            j: Any = judgements.get(f"{cid}:{r.id}")
            if j is None:
                p_val, conf_val = 0.0, 0.0
            else:
                p_val, conf_val = j.p, j.confidence
            per_req_judgements[r.id] = {"p": p_val, "confidence": conf_val}
            store.append({
                "type": "JUDGMENT_RECORDED", "id": _sid("j"), "run_id": run_id,
                "job_id": job_id, "candidate_id": cid, "requirement_id": r.id,
                "p": p_val, "confidence": conf_val,
                "judge": {"kind": classifier.kind,
                          "model": getattr(classifier, "model", None)},
                "policy_hash": phash,
            })

        composed = policy_svc.compose(per_req_judgements, reqs, pol)
        req_texts = {r.id: r.text for r in reqs}
        candidate_spans = spans_by_candidate.get(cid) or []
        verified_spans = 0
        failed_spans = 0
        absent_spans = 0
        for v in composed["per_req"]:
            total_checked += 1
            # per-requirement verification (human ruling): the requirement's OWN spans
            # are the candidate quotes that mention its text; a requirement with no such
            # span is MISSING evidence, never a fabricated "REQ-xx" fidelity comparison.
            own = [q for q in candidate_spans
                   if (req_texts.get(v["requirement_id"]) or "").lower() in q.lower()]
            if not own:
                absent_spans += 1
                store.append({"type": VERIFY_FAIL, "id": _sid("v"), "run_id": run_id,
                              "candidate_id": cid, "requirement_id": v["requirement_id"],
                              "method": "absent_span", "ratio": None, "policy_hash": phash})
                continue
            vr = verify_quote(own[0], text, pol.brakes.fuzzy_ratio)
            if vr["pass"]:
                verified_spans += 1
                total_verified += 1
                store.append({"type": VERIFY_PASS, "id": _sid("v"), "run_id": run_id,
                              "candidate_id": cid, "requirement_id": v["requirement_id"],
                              "method": "fuzzy", "ratio": vr["ratio"], "policy_hash": phash})
            else:
                failed_spans += 1
                store.append({"type": VERIFY_FAIL, "id": _sid("v"), "run_id": run_id,
                              "candidate_id": cid, "requirement_id": v["requirement_id"],
                              "method": "fuzzy", "ratio": vr["ratio"], "policy_hash": phash})
        anomaly = anomaly_flag(verified_spans, composed["tier"], pol)
        store.append({
            "type": "POLICY_STATE_SET", "id": _sid("ps"), "run_id": run_id,
            "job_id": job_id, "candidate_id": cid, "composite": composed["composite"],
            "tier": composed["tier"], "needs_review": composed["needs_review"],
            "verified_spans": verified_spans, "failed_spans": failed_spans,
            "absent_spans": absent_spans, "anomaly": anomaly, "policy_hash": phash,
        })
        screen_candidates.append({
            "candidate_id": cid, "tier": composed["tier"], "composite": composed["composite"],
            "needs_review": composed["needs_review"], "per_req": composed["per_req"],
            "verified_spans": verified_spans, "failed_spans": failed_spans,
            "absent_spans": absent_spans, "anomaly": anomaly, "policy_hash": phash,
        })

    cohorts = build_cohorts(screen_candidates, job_id, pol.version)
    n = len(screen_candidates) or 1
    return {
        "run_id": run_id, "job_id": job_id, "policy_hash": phash,
        "policy_version": pol.version, "classifier_kind": classifier.kind,
        "needs_review_rate": round(sum(1 for c in screen_candidates if c["needs_review"]) / n, 3),
        "verified_rate": round(total_verified / (total_checked or 1), 3),
        "candidates": screen_candidates, "cohorts": cohorts,
    }