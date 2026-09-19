# backend/tests/test_ledger_models.py
import pytest
from pydantic import ValidationError


def test_source_record_valid():
    from app.models.ledger import SourceRecord

    r = SourceRecord(
        id="src_1",
        run_id="run_1",
        kind="resume",
        filename="cv.pdf",
        mime="application/pdf",
        sha256="a" * 64,
        bytes=1234,
        consent_tier="L0_application",
        created_at="2026-09-20T00:00:00Z",
    )
    assert r.kind == "resume"


def test_source_record_rejects_invalid_kind():
    from app.models.ledger import SourceRecord

    with pytest.raises(ValidationError):
        SourceRecord(
            id="x",
            run_id="r",
            kind="linkedin",
            filename="x",
            mime="x",
            sha256="a" * 64,
            bytes=1,
            consent_tier="L0_application",
            created_at="2026-09-20T00:00:00Z",
        )


def test_evidence_span_quote_length():
    from app.models.ledger import EvidenceSpan

    with pytest.raises(ValidationError):
        EvidenceSpan(
            id="ev1",
            artifact_id="art1",
            candidate_id="cand1",
            quote="short",
            loc={"page": 1, "line_start": 1, "line_end": 1, "char_start": 0, "char_end": 5},
            confidence=0.9,
            verified={"method": "verbatim", "ratio": 1.0, "pass": True},
        )


def test_assessment_grade_enum():
    from app.models.ledger import Assessment

    with pytest.raises(ValidationError):
        Assessment(
            id="a1",
            candidate_id="c1",
            requirement_id="REQ-01",
            grade="bad",
            p=0.5,
            confidence=0.5,
            claim_ids=["cl1"],
            policy_hash="h",
            judge={"model": "jev", "p": 0.5},
        )


def test_event_hash_chains():
    from app.models.ledger import hash_event

    h1 = hash_event(None, '{"id":"e1"}')
    h2 = hash_event(h1, '{"id":"e2"}')
    assert len(h1) == 64 and len(h2) == 64
    assert h1 != h2


def test_report_answer_requires_assessment_ids():
    from app.models.ledger import ReportAnswer

    with pytest.raises(ValidationError):
        ReportAnswer(
            id="r1", kind="summary", candidate_ids=["c1"], assessment_ids=[], body_md="hello", version=1
        )


def test_approver_log_time_on_evidence():
    from app.models.ledger import ApproverLog

    a = ApproverLog(
        id="ap1",
        run_id="run1",
        actor="recruiter@example.com",
        action="approve",
        target_ids=["a1"],
        rationale="looks good",
        time_on_evidence_s=42,
    )
    assert a.time_on_evidence_s == 42
