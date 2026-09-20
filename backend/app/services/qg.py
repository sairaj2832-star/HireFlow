from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Union

from app.db.ledger_store import LedgerStore
from app.models.policy import load_policy_typed
from app.services.policy import grade_of


PathLike = Union[Path, None]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _requirement_id(value: Any) -> str | None:
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        for key in ("id", "requirement_id", "req_id"):
            if value.get(key) is not None:
                return str(value[key])
    for key in ("id", "requirement_id", "req_id"):
        if hasattr(value, key):
            item = getattr(value, key)
            if item is not None:
                return str(item)
    return None


def _requirement_text(value: Any, requirement_id: str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        for key in ("text", "requirement_text", "description"):
            if value.get(key) is not None:
                return str(value[key])
        return requirement_id
    for key in ("text", "requirement_text", "description"):
        if hasattr(value, key):
            item = getattr(value, key)
            if item is not None:
                return str(item)
    return requirement_id


def _normalize_requirements(requirements: Any) -> list[dict[str, str]]:
    values: Iterable[Any]
    if isinstance(requirements, Mapping):
        if "requirements" in requirements:
            nested = requirements.get("requirements")
            values = nested if isinstance(nested, Iterable) and not isinstance(nested, (str, bytes, Mapping)) else []
        else:
            values = []
            for key, value in requirements.items():
                if isinstance(value, Mapping):
                    item = dict(value)
                    item.setdefault("id", str(key))
                    values = [*values, item]
                elif isinstance(value, str):
                    values = [*values, {"id": str(key), "text": value}]
    elif isinstance(requirements, Iterable) and not isinstance(requirements, (str, bytes, Mapping)):
        values = requirements
    else:
        values = []

    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for value in values:
        requirement_id = _requirement_id(value)
        if not requirement_id:
            continue
        if requirement_id in seen:
            continue
        seen.add(requirement_id)
        out.append({
            "requirement_id": requirement_id,
            "text": _requirement_text(value, requirement_id),
        })
    return out


def _normalize_gaps(evidence_gaps: Any) -> dict[str, list[str]]:
    if evidence_gaps is None:
        return {}
    values: Any = evidence_gaps
    if isinstance(values, Mapping) and "gaps" in values:
        values = values.get("gaps")
    if isinstance(values, Mapping):
        pairs: list[tuple[str | None, Any]] = []
        for key, value in values.items():
            if key in {"candidate_id", "job_id", "run_id"}:
                continue
            pairs.append((str(key), value))
    elif isinstance(values, Iterable) and not isinstance(values, (str, bytes, Mapping)):
        pairs = []
        for value in values:
            if isinstance(value, Mapping):
                requirement_id = _requirement_id(value)
                pairs.append((requirement_id, value))
            elif isinstance(value, str):
                pairs.append((value, value))
            else:
                pairs.append((None, value))
    else:
        pairs = [(None, values)]

    out: dict[str, list[str]] = {}
    for requirement_id, value in pairs:
        if requirement_id is None:
            if isinstance(value, Mapping):
                requirement_id = _requirement_id(value)
            elif isinstance(value, str):
                requirement_id = value
        if not requirement_id:
            continue
        if isinstance(value, Mapping):
            gap_text = value.get("gap_text") or value.get("text") or value.get("reason")
            gap = str(gap_text) if gap_text is not None else ""
        else:
            gap = str(value)
        out.setdefault(requirement_id, [])
        if gap:
            out[requirement_id].append(gap)
    return out


def _last(events: list[dict[str, Any]], predicate: Any) -> dict[str, Any] | None:
    found = None
    for event in events:
        if predicate(event):
            found = event
    return found


def _candidate_job_id(
    candidate_id: str,
    events: list[dict[str, Any]],
    requirements: list[dict[str, str]],
) -> str | None:
    policy = _last(
        events,
        lambda event: event.get("type") == "POLICY_STATE_SET"
        and event.get("candidate_id") == candidate_id,
    )
    if policy and policy.get("job_id"):
        return str(policy["job_id"])
    judgment = _last(
        events,
        lambda event: event.get("type") == "JUDGMENT_RECORDED"
        and event.get("candidate_id") == candidate_id,
    )
    if judgment and judgment.get("job_id"):
        return str(judgment["job_id"])
    for event in events:
        if event.get("type") == "REQUIREMENT_DEFINED" and event.get("id") in {
            item["requirement_id"] for item in requirements
        }:
            return str(event["job_id"]) if event.get("job_id") else None
    return None


def _requirement_texts_from_ledger(
    job_id: str | None,
    events: list[dict[str, Any]],
) -> dict[str, str]:
    out: dict[str, str] = {}
    for event in events:
        if event.get("type") != "REQUIREMENT_DEFINED":
            continue
        if job_id and event.get("job_id") not in (None, job_id):
            continue
        requirement_id = _requirement_id(event)
        if requirement_id:
            out[requirement_id] = _requirement_text(event, requirement_id)
    return out


def _policy_per_requirement(policy_event: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not policy_event:
        return {}
    per_req = policy_event.get("per_req") or policy_event.get("requirements") or []
    if isinstance(per_req, Mapping):
        per_req = [
            {**(value if isinstance(value, Mapping) else {}), "requirement_id": key}
            for key, value in per_req.items()
        ]
    out: dict[str, dict[str, Any]] = {}
    if isinstance(per_req, Iterable) and not isinstance(per_req, (str, bytes, Mapping)):
        for item in per_req:
            if not isinstance(item, Mapping):
                continue
            requirement_id = _requirement_id(item)
            if requirement_id:
                out[requirement_id] = dict(item)
    return out


def _verification_by_requirement(
    candidate_id: str,
    events: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for event in events:
        if event.get("candidate_id") != candidate_id:
            continue
        if event.get("type") not in {"VERIFICATION_PASSED", "VERIFICATION_FAILED"}:
            continue
        requirement_id = _requirement_id(event)
        if requirement_id:
            out[requirement_id] = event
    return out


def _spans_by_requirement(
    candidate_id: str,
    events: list[dict[str, Any]],
    requirement_text: Mapping[str, str],
) -> dict[str, list[dict[str, Any]]]:
    out = {requirement_id: [] for requirement_id in requirement_text}
    for event in events:
        if event.get("type") != "EVIDENCE_SPAN_MAPPED" or event.get("candidate_id") != candidate_id:
            continue
        requirement_id = _requirement_id(event)
        if requirement_id and requirement_id in out:
            out[requirement_id].append(event)
            continue
        quote = str(event.get("quote", "")).casefold()
        for item_id, text in requirement_text.items():
            if text.casefold() in quote:
                out[item_id].append(event)
                break
    return out


def _is_gap(
    requirement_id: str,
    judgments: Mapping[str, dict[str, Any]],
    policy_per_req: Mapping[str, dict[str, Any]],
    verifications: Mapping[str, dict[str, Any]],
    spans: Mapping[str, list[dict[str, Any]]],
    policy_event: dict[str, Any] | None,
) -> bool:
    judgment = judgments.get(requirement_id)
    explicit_grade = None
    if judgment:
        explicit_grade = judgment.get("grade") or judgment.get("status") or judgment.get("verdict")
    policy_item = policy_per_req.get(requirement_id)
    if explicit_grade is None and policy_item:
        explicit_grade = policy_item.get("grade") or policy_item.get("status") or policy_item.get("verdict")
    if explicit_grade is not None:
        if str(explicit_grade).upper() in {"NOT_SUPPORTED", "NEEDS_VALIDATION"}:
            return True
    elif judgment:
        try:
            if grade_of(float(judgment.get("p", 0.0)), load_policy_typed()) in {
                "NOT_SUPPORTED",
                "NEEDS_VALIDATION",
            }:
                return True
        except (TypeError, ValueError):
            return True

    verification = verifications.get(requirement_id)
    if verification and verification.get("type") == "VERIFICATION_FAILED":
        return True
    if not spans.get(requirement_id):
        aggregate_absent = policy_event.get("absent_spans", 0) if policy_event else 0
        if aggregate_absent:
            return True
    return False


def generate_questions(
    candidate_id: str,
    requirements: Any,
    evidence_gaps: Any,
    db_path: PathLike = None,
    journal_path: PathLike = None,
) -> list[dict[str, str]]:
    """Generate deterministic, evidence-gap interview questions."""
    store = LedgerStore(db_path=db_path, journal_path=journal_path)
    events = store.get_events()
    candidate_events = [
        event for event in events
        if event.get("candidate_id") == candidate_id
    ]
    if not candidate_events:
        raise ValueError(f"candidate not found: {candidate_id}")

    policy_event = _last(
        events,
        lambda event: event.get("type") == "POLICY_STATE_SET"
        and event.get("candidate_id") == candidate_id,
    )
    judgments: dict[str, dict[str, Any]] = {}
    for event in events:
        if event.get("type") != "JUDGMENT_RECORDED" or event.get("candidate_id") != candidate_id:
            continue
        requirement_id = _requirement_id(event)
        if requirement_id:
            judgments[requirement_id] = event
    if not policy_event and not judgments:
        raise ValueError(f"candidate not screened: {candidate_id}")

    normalized_requirements = _normalize_requirements(requirements)
    job_id = _candidate_job_id(candidate_id, events, normalized_requirements)
    ledger_requirements = _requirement_texts_from_ledger(job_id, events)
    requirement_map: dict[str, str] = {}
    for item in normalized_requirements:
        requirement_map[item["requirement_id"]] = item["text"]
    for requirement_id, text in ledger_requirements.items():
        requirement_map.setdefault(requirement_id, text)
    if not requirement_map:
        requirement_map = {
            requirement_id: requirement_id for requirement_id in judgments
        }

    ordered_ids = [item["requirement_id"] for item in normalized_requirements]
    ordered_ids.extend(
        requirement_id for requirement_id in requirement_map
        if requirement_id not in ordered_ids
    )
    gaps = _normalize_gaps(evidence_gaps)
    policy_per_req = _policy_per_requirement(policy_event)
    verifications = _verification_by_requirement(candidate_id, events)
    spans = _spans_by_requirement(candidate_id, events, requirement_map)

    gap_requirements: list[str] = []
    for requirement_id in ordered_ids:
        if requirement_id in gaps and gaps[requirement_id]:
            gap_requirements.append(requirement_id)
        elif _is_gap(
            requirement_id,
            judgments,
            policy_per_req,
            verifications,
            spans,
            policy_event,
        ):
            gap_requirements.append(requirement_id)

    questions: list[dict[str, str]] = []
    requirement_count = 0
    for requirement_id in gap_requirements:
        if requirement_count >= 3 or len(questions) >= 6:
            break
        requirement_count += 1
        requirement_text = requirement_map.get(requirement_id, requirement_id)
        entries = gaps.get(requirement_id) or [""]
        for index, _gap in enumerate(entries[:2]):
            if len(questions) >= 6:
                break
            suffix = "" if index == 0 else f":{index + 1}"
            questions.append({
                "question_id": f"{candidate_id}:{requirement_id}{suffix}",
                "requirement_id": requirement_id,
                "gap_text": f"No verified evidence for {requirement_text}",
                "question": (
                    f"Walk me through your experience with {requirement_text}. "
                    "What did you build, how was it deployed, what were the scale requirements?"
                ),
            })

    if questions:
        run_id = str(policy_event.get("run_id", "question_generation")) if policy_event else "question_generation"
        store.append({
            "type": "QUESTION_GENERATED",
            "id": f"qgen_{uuid.uuid4().hex[:12]}",
            "candidate_id": candidate_id,
            "job_id": job_id,
            "run_id": run_id,
            "timestamp": _utc_now(),
            "questions": questions,
        })
    return questions
