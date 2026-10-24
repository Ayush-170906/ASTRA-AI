"""Human-approval gate (TRD sections 12-13). Streamlit reruns the whole
script on every interaction, so this cannot be a blocking `input()` call --
instead the controller is a resumable state machine: this module tells it
whether to PROCEED, WAIT (pause and render the approval UI), or the human
has DENIED (terminate safely). `state.approval_status` is the only piece of
state carried across Streamlit reruns for this decision.
"""
from enum import Enum

from agent.state import AgentState, RiskLevel
from safety.risk import requires_approval


class GateDecision(str, Enum):
    PROCEED = "PROCEED"
    WAIT = "WAIT"
    DENIED = "DENIED"


def gate(state: AgentState) -> GateDecision:
    """The one and only checkpoint a task must pass before execution.
    There is no other code path in this prototype that invokes a tool
    without going through this function first (see controller.py)."""
    if not requires_approval(state.risk_level):
        return GateDecision.PROCEED

    if state.approval_status == "APPROVED":
        return GateDecision.PROCEED
    if state.approval_status == "DENIED":
        return GateDecision.DENIED
    return GateDecision.WAIT
