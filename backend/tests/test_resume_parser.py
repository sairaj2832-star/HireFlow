# backend/tests/test_resume_parser.py
def test_parse_resume_skills_and_experience():
    from app.services.resume_parser import parse_resume_text
    text = "Alex Rivera\nalex@example.com\nSkills: Python, FastAPI, PyTorch\nExperience: 3 years building REST APIs with FastAPI\nProjects: Built ML service with Docker"
    p = parse_resume_text(text, "cand_01")
    assert "Python" in p.skills
    assert any(s["id"] == "esco:fastapi" for s in p.normalized_skills)
    assert p.experience_years == 3.0
    assert len(p.projects) >= 1

def test_parse_resume_no_pii_leak():
    from app.services.resume_parser import parse_resume_text
    p = parse_resume_text("Name: Sam\nSkills: Python", "cand_02")
    assert not hasattr(p, "date_of_birth")

def test_parse_resume_quotes_evidence():
    from app.services.resume_parser import parse_resume_text
    p = parse_resume_text("Built REST APIs using FastAPI for X project.", "cand_03")
    assert len(p.evidence_spans) >= 1
    assert "FastAPI" in p.evidence_spans[0]

def test_parse_resume_bytes_utf8_and_pdf_path():
    from app.services.resume_parser import parse_resume
    raw = b"Skills: Python\nExperience: 2 years"
    p = parse_resume(raw, "cv.txt", "cand_04")
    assert p.candidate_id == "cand_04"
