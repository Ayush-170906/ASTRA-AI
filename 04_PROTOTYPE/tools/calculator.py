"""Deterministic, safe arithmetic tools -- LOW risk (TRD section 11)."""
from tools.registry import Tool, ToolResult
from agent.state import RiskLevel


def _calculate_capacity(registered: int, capacity: int) -> ToolResult:
    if registered < 0 or capacity < 0:
        return ToolResult(False, None, "registered/capacity must be non-negative")
    remaining = capacity - registered
    return ToolResult(
        success=True,
        result=remaining,
        message=f"{remaining} additional registrations available (capacity {capacity}, registered {registered})",
    )


calculate_capacity_tool = Tool(
    name="calculate_capacity",
    description="Compute remaining registration capacity = capacity - registered.",
    risk_level=RiskLevel.LOW,
    run=_calculate_capacity,
)
