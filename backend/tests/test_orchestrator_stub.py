# backend/tests/test_orchestrator_stub.py
def test_orchestrator_runs():
    from app.orchestrator.loop import Orchestrator

    o = Orchestrator(job_id="j1", objective="screen")
    assert hasattr(o, "run")
    result = o.run()
    assert result["job_id"] == "j1"
    assert "steps_executed" in result
    assert len(result["steps_executed"]) > 0


def test_orchestrator_state_machine():
    from app.orchestrator.loop import Orchestrator

    o = Orchestrator(job_id="j2", objective="screen")
    o._observe()
    assert o.state.phase == "observe"
    o._reason()
    assert o.state.phase == "reason"
    o._select()
    assert o.state.phase == "select"
    o._execute()
    assert o.state.phase == "execute"
    o._update()
    assert o.state.phase == "update"


def test_purge_has_ttl():
    from app.services.purge import RETENTION_DAYS

    assert RETENTION_DAYS == 365
