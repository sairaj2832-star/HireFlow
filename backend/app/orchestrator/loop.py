"""B0 stub — B4 implements single custom loop ~150 lines over CapabilityRegistry."""

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
    """Primary loop — B4 fills in goal→observe→reason→select→execute→update→sufficiency→done/re-plan/escalate."""

    def __init__(self, job_id: str, objective: str) -> None:
        self.state = AgentState(job=job_id, objective=objective, phase="init")

    def run(self) -> None:
        raise NotImplementedError(
            "B4: implement loop over registry.yaml with 12-step budget and 3 BRAKES"
        )
