"""Goal analysis (FR-02) and task decomposition (FR-03) -- TRD section 22
"Agent Action Contract": the LLM is asked to return structured JSON, never
free-form instructions, and its output is validated before anything
downstream trusts it. This is the seam described in the seminar's most
important design decision: the LLM PROPOSES a structured action; it never
executes anything directly.
"""
from __future__ import annotations

import json
import re

from agent.state import SubTask, RiskLevel
from llm.base import LLMProvider

RISKY_KEYWORDS = ["send", "announce", "notify", "message", "email", "delete", "pay", "purchase", "publish"]

DECOMPOSE_PROMPT_TEMPLATE = """You are the planning component of an Agentic AI system. Decompose the
user's goal into an ordered list of subtasks. Return ONLY a JSON array, no prose, where each item has
exactly these fields: task_id, description, tool, arguments, expected_outcome, risk (one of LOW/MEDIUM/HIGH).
Only use tools from this list: {tool_names}

GOAL:
{goal}

Return the JSON array now.
"""


def analyze_goal(goal: str) -> dict:
    """FR-02: extract objective, constraints, and flag potentially risky
    intents from the raw goal text. Deliberately simple pattern matching --
    this is a cheap pre-check, not a replacement for the risk gate that
    every tool call still passes through regardless of this analysis."""
    lowered = goal.lower()
    flagged = [kw for kw in RISKY_KEYWORDS if kw in lowered]
    return {
        "objective": goal.strip(),
        "constraints": [],
        "potentially_risky": flagged,
    }


def _parse_json_tasks(raw_text: str) -> list[dict]:
    text = raw_text.strip()
    # tolerate a model wrapping the array in markdown fences
    fence_match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1)
    else:
        bracket_match = re.search(r"(\[.*\])", text, re.DOTALL)
        if bracket_match:
            text = bracket_match.group(1)
    return json.loads(text)


def decompose(goal: str, llm: LLMProvider, tool_names: list[str]) -> list[SubTask]:
    prompt = DECOMPOSE_PROMPT_TEMPLATE.format(tool_names=", ".join(tool_names), goal=goal)
    raw = llm.generate(prompt)

    try:
        raw_tasks = _parse_json_tasks(raw)
    except (json.JSONDecodeError, AttributeError):
        # Robustness fallback (FR-03 must not crash the loop on a malformed
        # LLM response): degrade to a single generic task rather than fail.
        raw_tasks = [{
            "task_id": "T01",
            "description": f"Address the goal: {goal}",
            "tool": "search_knowledge",
            "arguments": {"query": goal[:200]},
            "expected_outcome": "Relevant information retrieved",
            "risk": "LOW",
        }]

    subtasks = []
    for rt in raw_tasks:
        tool = rt.get("tool")
        if tool not in tool_names:
            continue  # SR-06: never accept a tool name outside the allowlist
        risk_str = str(rt.get("risk", "LOW")).upper()
        risk = RiskLevel(risk_str) if risk_str in RiskLevel.__members__ else RiskLevel.LOW
        subtasks.append(SubTask(
            task_id=rt.get("task_id", f"T{len(subtasks)+1:02d}"),
            description=rt.get("description", ""),
            tool=tool,
            arguments=rt.get("arguments", {}) or {},
            expected_outcome=rt.get("expected_outcome"),
            risk=risk,
        ))
    return subtasks
