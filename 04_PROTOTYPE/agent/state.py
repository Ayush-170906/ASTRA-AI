"""Shared agent state: the single source of truth the controller, UI, and
tests all read/write. No database — an in-memory dataclass is sufficient
for this prototype's scope (TRD section 16)."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import time
from typing import Any, Optional


class AgentStatus(str, Enum):
    IDLE = "IDLE"
    PLANNING = "PLANNING"
    RETRIEVING = "RETRIEVING"
    SELECTING_TOOL = "SELECTING_TOOL"
    RISK_CHECK = "RISK_CHECK"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    EXECUTING = "EXECUTING"
    OBSERVING = "OBSERVING"
    VERIFYING = "VERIFYING"
    REPLANNING = "REPLANNING"
    COMPLETED = "COMPLETED"
    ESCALATED = "ESCALATED"
    TERMINATED = "TERMINATED"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass
class TraceEvent:
    """One row of the execution trace shown in the UI (TRD section 17)."""
    step: int
    stage: str
    description: str
    tool: Optional[str] = None
    risk: Optional[str] = None
    status: str = "OK"
    result: Optional[str] = None
    timestamp: float = field(default_factory=time)

    def to_dict(self) -> dict:
        return {
            "step": self.step,
            "stage": self.stage,
            "description": self.description,
            "tool": self.tool,
            "risk": self.risk,
            "status": self.status,
            "result": self.result,
            "timestamp": self.timestamp,
        }


@dataclass
class SubTask:
    task_id: str
    description: str
    tool: Optional[str] = None
    arguments: dict = field(default_factory=dict)
    expected_outcome: Optional[str] = None
    risk: Optional[RiskLevel] = None
    done: bool = False


@dataclass
class AgentState:
    goal: str = ""
    constraints: list[str] = field(default_factory=list)
    tasks: list[SubTask] = field(default_factory=list)
    current_task_index: int = 0

    retrieved_context: list[str] = field(default_factory=list)
    selected_tool: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    approval_status: Optional[str] = None  # None | "PENDING" | "APPROVED" | "DENIED"

    tool_result: Any = None
    observation: Any = None
    verification_result: Optional[bool] = None

    retry_count: int = 0
    max_retries: int = 2

    status: AgentStatus = AgentStatus.IDLE
    execution_trace: list[TraceEvent] = field(default_factory=list)
    final_result: Optional[dict] = None

    # Demo-only controls (not part of the core architecture): let the
    # presenter deliberately trigger the retry/escalation path on a
    # specific task during a live demo, since the built-in tools are
    # deterministic and would otherwise always pass verification. Every
    # forced failure is logged with an explicit "Demo-forced" reason so it
    # is never mistaken for a real defect (see verification/verifier.py).
    demo_force_fail_task_desc_contains: Optional[str] = None
    demo_force_fail_remaining: int = 0

    def log(self, stage: str, description: str, tool: str = None,
            risk: str = None, status: str = "OK", result: str = None) -> TraceEvent:
        event = TraceEvent(
            step=len(self.execution_trace) + 1,
            stage=stage,
            description=description,
            tool=tool,
            risk=risk,
            status=status,
            result=result,
        )
        self.execution_trace.append(event)
        return event

    @property
    def current_task(self) -> Optional[SubTask]:
        if 0 <= self.current_task_index < len(self.tasks):
            return self.tasks[self.current_task_index]
        return None

    def reset(self):
        """Reset to a fresh IDLE state, keeping max_retries configuration."""
        max_retries = self.max_retries
        self.__init__()
        self.max_retries = max_retries
