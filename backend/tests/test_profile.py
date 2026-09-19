# backend/tests/test_profile.py
import pytest
from pydantic import ValidationError

def test_requirement_id_format():
    from app.models.profile import Requirement
    r = Requirement(id="REQ-01", text="Python 3+ years", cls="hard", weight=0.25, gate="hard")
    assert r.id == "REQ-01"
    with pytest.raises(ValidationError):
        Requirement(id="R1", text="x", cls="hard", weight=0.25, gate="hard")

def test_requirement_weight_range():
    from app.models.profile import Requirement
    with pytest.raises(ValidationError):
        Requirement(id="REQ-02", text="x", cls="soft", weight=2.0, gate="soft")

def test_candidate_profile_23_fields_no_pii():
    from app.models.profile import CandidateProfile
    p = CandidateProfile(candidate_id="cand_01", full_name="Alex Rivera", email="alex@example.com", skills=["Python"], experience_years=3)
    assert p.candidate_id == "cand_01"
    # synthetic-only guard: DoB/photo must not exist as fields
    assert not hasattr(p, "date_of_birth")
    assert not hasattr(p, "photo")

def test_normalize_skills_alias():
    from app.models.profile import normalize_skills
    out = normalize_skills(["py", "React.js", "unknown-skill-xyz"])
    ids = [s["id"] for s in out]
    assert "esco:python" in ids
    assert "esco:react" in ids
    # unknown passes through with normalized flag false
    unk = [s for s in out if s["label"] == "unknown-skill-xyz"][0]
    assert unk["normalized"] is False
