# backend/tests/test_jd_parser.py
def test_parse_jd_numbered_reqs():
    from app.services.jd_parser import parse_jd
    jd = "We need:\n- Python 3+ years building REST APIs\n- FastAPI production experience\n- ML with PyTorch"
    reqs = parse_jd(jd)
    assert len(reqs) >= 3
    assert reqs[0].id == "REQ-01"
    assert all(r.weight > 0 for r in reqs)

def test_parse_jd_weight_gate_hard_soft():
    from app.services.jd_parser import parse_jd
    jd = "Requirements:\nMust have: Python\nNice to have: Tailwind"
    reqs = parse_jd(jd)
    # first is hard gate, second soft (heuristic)
    assert reqs[0].gate == "hard"
    assert any(r.gate == "soft" for r in reqs)

def test_parse_jd_atomicity_each_req_short():
    from app.services.jd_parser import parse_jd
    reqs = parse_jd("Python and FastAPI and ML and Docker and K8s and AWS and React and SQL")
    # each bullet must be atomic — no mega-req with 8 skills in one text
    for r in reqs:
        assert len(r.text) < 120

def test_parse_jd_bytes_pdf_fallback():
    from app.services.jd_parser import parse_jd_bytes
    raw = b"Job Description\n- Python\n- FastAPI"
    reqs = parse_jd_bytes(raw, "jd.txt")
    assert len(reqs) >= 2
