from fastapi.testclient import TestClient
from app.main import app


def test_integration_smoke():
    c = TestClient(app)

    print('Step 1: Create job')
    r = c.post('/jobs', json={'title': 'Backend Dev', 'jd_text': 'Python\nFastAPI\nML\nDocker'})
    assert r.status_code == 201, r.text
    job = r.json()
    job_id = job['job_id']
    print(f'  job_id={job_id}, reqs={len(job["requirements"])}')

    print('Step 2: Ingest candidates')
    r = c.post(f'/jobs/{job_id}/candidates:ingest',
               files=[('files', ('a.txt', b'Skills: Python, FastAPI\nExperience: 4 years building REST APIs', 'text/plain')),
                      ('files', ('b.txt', b'Skills: Java\nExperience: 10 years', 'text/plain'))])
    assert r.status_code == 200, r.text
    ingest = r.json()
    print(f'  candidates={ingest["candidate_ids"]}, quarantined={ingest["quarantined"]}')

    print('Step 3: Screen')
    r = c.post(f'/jobs/{job_id}/screen')
    assert r.status_code == 201, r.text
    run_id = r.json()['run_id']
    print(f'  run_id={run_id}')

    print('Step 4: Shortlist')
    r = c.get(f'/jobs/{job_id}/shortlist')
    assert r.status_code == 200, r.text
    shortlist = r.json()
    print(f'  ranked={len(shortlist["ranked"])} candidates, cohorts={len(shortlist["cohorts"])}')

    print('Step 5: Evidence')
    cand_id = shortlist['ranked'][0]['candidate_id']
    r = c.get(f'/candidates/{cand_id}/evidence')
    assert r.status_code == 200, r.text
    evidence = r.json()
    print(f'  boxes={len(evidence["boxes"])}')
    assert 'req' in evidence['boxes'][0]
    assert 'span' in evidence['boxes'][0]
    assert 'judgment' in evidence['boxes'][0]

    print('Step 6: Questions (B5)')
    r = c.post(f'/candidates/{cand_id}/questions')
    assert r.status_code == 200, r.text
    q = r.json()
    print(f'  questions={len(q["questions"])}')

    print('Step 7: Interview notes (B5)')
    r = c.post(f'/candidates/{cand_id}/interview-notes', json={'note': 'Strong on Python'})
    assert r.status_code == 200, r.text
    note = r.json()
    print(f'  note_id={note["note_id"]}, status={note["status"]}')

    print('Step 8: Report (B6)')
    r = c.get(f'/jobs/{job_id}/report')
    assert r.status_code == 200, r.text
    report = r.json()
    print(f'  sections={len(report["report"]["sections"])}')

    print('Step 9: Query (B6)')
    r = c.get(f'/jobs/{job_id}/query?filter=tier&value=SUPPORTED')
    assert r.status_code == 200, r.text
    query = r.json()
    print(f'  results={len(query["results"])}')

    print('Step 10: Audit pack (B3)')
    r = c.get(f'/jobs/{job_id}/audit-pack')
    assert r.status_code == 200, r.text
    audit = r.json()
    print(f'  audit events={audit["count"]}')

    print()
    print('=== ALL 10 INTEGRATION STEPS PASSED ===')
