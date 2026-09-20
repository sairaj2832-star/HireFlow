from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    job: str
    objective: str
    phase: str
    candidate_state: dict[str, Any] = field(default_factory=dict)
    pending: list[str] = field(default_factory=list)
    evidence_gaps: list[str] = field(default_factory=list)
    human_reviews: list[str] = field(default_factory=list)
    audit_refs: list[str] = field(default_factory=list)


class Orchestrator:
    """Primary loop — goal→observe→reason→select→execute→update→sufficiency→done/re-plan/escalate."""

    def __init__(self, job_id: str, objective: str) -> None:
        self.state = AgentState(job=job_id, objective=objective, phase="init")
        self._steps: list[str] = []
        self._result: dict[str, Any] = {}

    def _observe(self) -> None:
        self._steps.append("observe")
        self.state.phase = "observe"
        try:
            from app.routers.jobs import _JOBS, _SCREENS
            job = _JOBS.get(self.state.job)
            screens = {k: v for k, v in _SCREENS.items() if v.get("run_id")}
            self._result = {
                "job": job,
                "screened": list(screens.keys()),
                "candidates": len(job.get("requirements", [])) if job else 0,
            }
        except Exception:
            self._result = {}

    def _reason(self) -> None:
        self._steps.append("reason")
        self.state.phase = "reason"
        if self.state.job not in self._result.get("screened", []):
            self.state.pending = ["screen"]
        else:
            self.state.pending = []

    def _select(self) -> None:
        self._steps.append("select")
        self.state.phase = "select"

    def _execute(self) -> None:
        self._steps.append("execute")
        self.state.phase = "execute"
        if "screen" in self.state.pending:
            try:
                from app.services.screening import run_screen
                result = asyncio.run(run_screen(self.state.job))
                self._result["screen_result"] = result
                self.state.evidence_gaps = [
                    c["candidate_id"] for c in result.get("candidates", [])
                    if c.get("needs_review")
                ]
            except Exception as exc:
                self._result["screen_error"] = str(exc)

    def _update(self) -> None:
        self._steps.append("update")
        self.state.phase = "update"
        if "screen_result" in self._result:
            self.state.audit_refs.append(
                f"screen:{self._result['screen_result'].get('run_id', '')}"
            )

    def _check_sufficiency(self) -> bool:
        self._steps.append("sufficiency_check")
        return "screen" not in self.state.pending and len(self._steps) > 5

    def _budget(self) -> int:
        try:
            from app.services.config_loader import load_policy
            pol = load_policy()
            return int(pol.get("loop", {}).get("max_steps", 12))
        except Exception:
            return 12

    def _done(self) -> None:
        self.state.phase = "done"

    def run(self) -> dict[str, Any]:
        budget = self._budget()
        while len(self._steps) < budget:
            self._observe()
            self._reason()
            self._select()
            self._execute()
            self._update()
            if self._check_sufficiency():
                break
        self._done()
        return {
            "job_id": self.state.job,
            "objective": self.state.objective,
            "phase": self.state.phase,
            "steps_executed": self._steps,
            "result": self._result,
            "evidence_gaps": self.state.evidence_gaps,
            "audit_refs": self.state.audit_refs,
        }
