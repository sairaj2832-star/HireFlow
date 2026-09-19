# backend/tests/test_orchestrator_stub.py
def test_orchestrator_signature():
    from app.orchestrator.loop import Orchestrator

    o = Orchestrator(job_id="j1", objective="screen")
    assert hasattr(o, "run")
    try:
        o.run()
        raise AssertionError("run() should raise NotImplementedError in B0")
    except NotImplementedError as e:
        assert "B4" in str(e)


def test_purge_has_ttl():
    from app.services.purge import RETENTION_DAYS

    assert RETENTION_DAYS == 365
