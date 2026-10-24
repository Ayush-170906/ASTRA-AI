"""Deterministic Demo Mode orchestration (Phase 3 UI enhancement, added
after the core prototype was already built and browser-verified).

This module adds NOTHING to the core architecture -- it only calls the
existing `agent.controller.start` / `run_until_pause` four times with fixed
goals and, where the loop pauses for human approval, a *simulated* decision
instead of a real button click. It is a thin orchestration layer kept out
of app.py so it can be unit-tested without Streamlit (see
tests/test_demo.py).

Why a dedicated LLM provider for Demo Mode (documented deviation): the
seminar's own PRD requires "the demo must not depend on unpredictable LLM
output" and must "reliably demonstrate the architecture every time." A
real Ollama/API provider can legitimately return different subtask wording
or ordering across runs. Manual Mode is unaffected -- app.py still passes
it whatever provider `llm.get_llm_provider()` selected (Ollama, API, or
the rule-based fallback) -- but Demo Mode's four scenarios are always run
against a dedicated `RuleBasedProvider` instance so the same four traces,
the same PASS/FAIL outcomes, and the same retry counts occur on every
click, regardless of what is configured for Manual Mode.
"""
from __future__ import annotations

from dataclasses import dataclass

from agent.state import AgentState, AgentStatus
from agent.controller import Dependencies, start, run_until_pause
from llm.rule_based import RuleBasedProvider

DEMO_GOAL_NORMAL = (
    "Prepare a brief for an upcoming technical event using the information available in the "
    "knowledge base, calculate the estimated registration capacity, and create a draft event checklist."
)
DEMO_GOAL_ANNOUNCEMENT = "Send the event announcement to all participants."


@dataclass
class ScenarioResult:
    number: int
    total: int
    name: str
    state: AgentState
    expected_status: AgentStatus

    @property
    def passed(self) -> bool:
        return self.state.status == self.expected_status

    @property
    def label(self) -> str:
        return f"Scenario {self.number}/{self.total}: {self.name}"


def demo_dependencies(deps: Dependencies) -> Dependencies:
    """Reuse Manual Mode's already-built retriever and tool registry (same
    knowledge base, same allowlisted tools -- nothing about the world the
    agent acts in changes), but force the deterministic provider so the
    demo's LLM-facing step never varies."""
    return Dependencies(llm=RuleBasedProvider(), retriever=deps.retriever, registry=deps.registry)


def _run_scenario(goal: str, deps: Dependencies, *,
                   simulate_approval: str | None = None,
                   force_fail: bool = False) -> AgentState:
    state = AgentState()
    if force_fail:
        # One more forced failure than MAX_RETRIES guarantees escalation
        # (verified in the manual browser test session): retry_count
        # reaches max_retries exactly when the 3rd forced failure lands.
        state.demo_force_fail_task_desc_contains = "capacity"
        state.demo_force_fail_remaining = state.max_retries + 1

    start(state, goal, deps)
    run_until_pause(state, deps)

    if state.status == AgentStatus.WAITING_FOR_APPROVAL and simulate_approval is not None:
        # Explicitly logged and distinct from the real approval path in
        # safety/approval.py -- this never touches or weakens that gate,
        # it only supplies the decision a human would otherwise click,
        # through the exact same `state.approval_status` field the real
        # APPROVE/DENY buttons set in Manual Mode.
        state.log("HUMAN_APPROVAL", f"DEMO MODE — Simulated Human Approval: {simulate_approval}",
                   status=simulate_approval)
        state.approval_status = simulate_approval
        run_until_pause(state, deps)

    return state


def run_full_demo(deps: Dependencies) -> list[ScenarioResult]:
    """Run all four PRD-validated scenarios back to back, each against a
    fresh AgentState (so they never interfere with each other, and never
    touch Manual Mode's state). Always terminates -- every scenario ends
    at COMPLETED, TERMINATED, or ESCALATED, never left WAITING_FOR_APPROVAL,
    because a simulated decision is supplied for every pause point that can
    occur in these four fixed goals."""
    ddeps = demo_dependencies(deps)
    results: list[ScenarioResult] = []

    s1 = _run_scenario(DEMO_GOAL_NORMAL, ddeps)
    results.append(ScenarioResult(1, 4, "Normal Execution", s1, AgentStatus.COMPLETED))

    s2 = _run_scenario(DEMO_GOAL_ANNOUNCEMENT, ddeps, simulate_approval="APPROVED")
    results.append(ScenarioResult(2, 4, "High-Risk Approval", s2, AgentStatus.COMPLETED))

    s3 = _run_scenario(DEMO_GOAL_ANNOUNCEMENT, ddeps, simulate_approval="DENIED")
    results.append(ScenarioResult(3, 4, "High-Risk Denial", s3, AgentStatus.TERMINATED))

    s4 = _run_scenario(DEMO_GOAL_NORMAL, ddeps, force_fail=True)
    results.append(ScenarioResult(4, 4, "Bounded Retry → Escalation", s4, AgentStatus.ESCALATED))

    return results
