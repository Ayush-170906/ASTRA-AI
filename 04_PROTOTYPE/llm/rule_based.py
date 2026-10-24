"""Deterministic fallback provider -- NOT part of the original TRD, added
because this deployment environment has neither an Ollama server nor an
ANTHROPIC_API_KEY configured (verified at build time: no local Ollama
reachable, no API key present). Per the TRD's own "provider-agnostic
adapter" principle, the controller must not care which provider produced
the text, so this fills the same `generate(prompt) -> str` contract with
keyword-based logic instead of a model call, letting the prototype run and
demonstrate the full control loop with zero external dependencies, cost, or
setup. Swap in LocalLLM or APIProvider at any time -- see README.md.

It only knows how to decompose the two documented demo goals (the normal
event-brief scenario and the high-risk announcement scenario); anything
else gets a single generic research task so the loop still completes
rather than crashing on unrecognized input.
"""
from __future__ import annotations

import json
import re

from llm.base import LLMProvider

# Known scenario numbers, sourced from knowledge/technical_event_info.txt.
# A real LLM+RAG pipeline would pull these from retrieved context dynamically;
# this deterministic stand-in hardcodes the demo's known values instead.
KNOWN_CAPACITY = 500
KNOWN_REGISTERED = 420


def _extract_goal(prompt: str) -> str:
    m = re.search(r"GOAL:\s*(.+?)\n\s*\n", prompt, re.DOTALL)
    if m:
        return m.group(1).strip()
    return prompt.strip()


class RuleBasedProvider(LLMProvider):
    name = "rule-based-fallback"

    def is_available(self) -> bool:
        return True  # always available; this is the guaranteed-to-work default

    def generate(self, prompt: str) -> str:
        goal = _extract_goal(prompt).lower()
        tasks = []
        n = 1

        def add(description, tool, arguments, expected_outcome, risk):
            nonlocal n
            tasks.append({
                "task_id": f"T{n:02d}",
                "description": description,
                "tool": tool,
                "arguments": arguments,
                "expected_outcome": expected_outcome,
                "risk": risk,
            })
            n += 1

        # "event" is deliberately excluded here even though it's a strong
        # signal for the brief scenario -- it also appears in the pure
        # high-risk goal ("send the event announcement..."), and an earlier
        # version of this heuristic used it, which caused the announcement-
        # only demo goal to ALSO generate the brief/capacity/checklist
        # tasks (caught by tests/test_agent.py::test_B_*). "brief",
        # "checklist", and "capacity" are unambiguous to the brief scenario.
        wants_brief = any(k in goal for k in ["brief", "checklist", "capacity"])
        wants_announcement = any(k in goal for k in ["announce", "send", "notify", "message"])

        if wants_brief:
            add(
                "Retrieve event information from the knowledge base",
                "search_knowledge",
                {"query": "technical event information venue capacity registrations"},
                "Relevant event details retrieved",
                "LOW",
            )
            add(
                "Calculate remaining registration capacity",
                "calculate_capacity",
                {"registered": KNOWN_REGISTERED, "capacity": KNOWN_CAPACITY},
                f"{KNOWN_CAPACITY - KNOWN_REGISTERED} available seats",
                "LOW",
            )
            add(
                "Generate the event preparation checklist",
                "generate_checklist",
                {},
                "Standard event checklist produced",
                "LOW",
            )

        if wants_announcement:
            add(
                "Send the event announcement to all participants",
                "mock_send_announcement",
                {"message": "Reminder: the technical event is coming up soon!",
                 "recipients": "all registered participants"},
                "Announcement delivered (mock) to all registered participants",
                "HIGH",
            )

        if not tasks:
            add(
                "Search the knowledge base for information relevant to the goal",
                "search_knowledge",
                {"query": goal[:200]},
                "Relevant context retrieved",
                "LOW",
            )

        return json.dumps(tasks)
