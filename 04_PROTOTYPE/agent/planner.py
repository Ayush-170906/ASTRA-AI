"""Ordering and replanning (FR-04, TRD section 4 "Planner"). For this
prototype's scope, decompose() already returns subtasks in a sensible
execution order, so the planner's job is mostly bookkeeping: track the
current task, and handle what "replan" means on a verification failure.
"""
from __future__ import annotations

from agent.state import AgentState


class Planner:
    def __init__(self, state: AgentState):
        self.state = state

    def has_next(self) -> bool:
        return self.state.current_task is not None

    def advance(self) -> None:
        self.state.current_task_index += 1
        self.state.retry_count = 0

    def replan(self) -> None:
        """Called on a verification failure while retries remain. For this
        prototype's deterministic tools there is nothing to change about
        *how* the task is done, so replanning here means: retry the same
        task, same arguments, incrementing retry_count. A provider with a
        real LLM could instead ask it to propose revised arguments; the
        seam is this method, not the controller loop."""
        self.state.retry_count += 1
