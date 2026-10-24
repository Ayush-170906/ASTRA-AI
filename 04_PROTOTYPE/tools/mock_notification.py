"""The prototype's one deliberately HIGH-risk tool (seminar demo scenario,
TRD section 6/11). This NEVER contacts a real mail/SMS service -- it only
appends to an in-memory list, so it is safe to approve during a live demo.
Explicit non-goal: no real external communication anywhere in this codebase.
"""
from tools.registry import Tool, ToolResult
from agent.state import RiskLevel

_SENT_LOG: list[dict] = []  # in-memory only; never persisted, never a real send


def _mock_send_announcement(message: str, recipients: str = "all registered participants") -> ToolResult:
    record = {"recipients": recipients, "message": message}
    _SENT_LOG.append(record)
    return ToolResult(
        success=True,
        result=record,
        message=f"[MOCK] Announcement recorded for delivery to {recipients} (no real message was sent).",
    )


def get_sent_log() -> list[dict]:
    return list(_SENT_LOG)


mock_send_announcement_tool = Tool(
    name="mock_send_announcement",
    description="Mock-send an announcement to all registered participants (simulated, no real delivery).",
    risk_level=RiskLevel.HIGH,
    run=_mock_send_announcement,
    approval_reason="External communication affects third parties (event policy: announcements require coordinator approval).",
)
