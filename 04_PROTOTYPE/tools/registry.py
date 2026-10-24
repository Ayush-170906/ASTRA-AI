"""Tool interface and allowlist registry (TRD sections 10, SR-06). The
registry is the only allowlisted set of actions the agent may ever invoke --
there is no path in this codebase from LLM output straight to code
execution. An LLM can only ever *name* a tool already in this registry;
naming an unregistered tool is a lookup failure, not an execution."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from agent.state import RiskLevel


@dataclass
class ToolResult:
    success: bool
    result: Any = None
    message: str = ""


@dataclass
class Tool:
    name: str
    description: str
    risk_level: RiskLevel
    run: Callable[..., ToolResult]
    approval_reason: str = ""

    def execute(self, **arguments) -> ToolResult:
        try:
            return self.run(**arguments)
        except Exception as exc:  # tool failures are data, not crashes
            return ToolResult(success=False, result=None, message=f"Tool error: {exc}")


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def names(self) -> list[str]:
        return list(self._tools.keys())

    def describe_all(self) -> list[dict]:
        return [
            {"name": t.name, "description": t.description, "risk": t.risk_level.value}
            for t in self._tools.values()
        ]
