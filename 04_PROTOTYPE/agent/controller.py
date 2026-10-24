"""The agent controller: a resumable finite-state machine implementing the
seminar's reliability loop end to end --

  Goal -> Decompose -> Plan -> Retrieve -> Tool Selection -> Risk Gate ->
  Human Approval -> Execute -> Observe -> Verify -> Bounded Retry -> Result

Why a step machine instead of the TRD's blocking `while` pseudocode:
Streamlit reruns the entire script on every user interaction (e.g. clicking
Approve/Deny), so a blocking call waiting on human input is not possible.
Instead, `run_until_pause` advances one micro-stage at a time and returns
control to the caller (the Streamlit app) whenever it reaches
WAITING_FOR_APPROVAL or a terminal status. The exact same function also
drives the CLI/test harness: tests just pre-set `state.approval_status`
before calling it, so the loop never needs to pause.

The one rule this whole module exists to enforce (seminar Principle 1):
`safety.approval.gate` is the ONLY function that decides whether a task's
tool is allowed to run, and its authoritative input is the TOOL'S OWN
registered risk_level from the tool registry -- never whatever risk label
an LLM proposed during decomposition, since trusting a model's own risk
self-assessment would let it talk its way past the gate.
"""
from __future__ import annotations

from dataclasses import dataclass

from agent.state import AgentState, AgentStatus, RiskLevel, SubTask
from agent.decomposer import analyze_goal, decompose
from agent.planner import Planner
from llm.base import LLMProvider
from rag.retriever import Retriever
from tools.registry import ToolRegistry, ToolResult
from safety.approval import gate, GateDecision
from verification.verifier import verify

PAUSE_STATUSES = {
    AgentStatus.WAITING_FOR_APPROVAL,
    AgentStatus.COMPLETED,
    AgentStatus.ESCALATED,
    AgentStatus.TERMINATED,
}


@dataclass
class Dependencies:
    llm: LLMProvider
    retriever: Retriever
    registry: ToolRegistry


def start(state: AgentState, goal: str, deps: Dependencies) -> None:
    """Kick off a fresh run. Caller is responsible for having reset `state`
    (or constructing a new one) first."""
    state.goal = goal
    state.log("GOAL", "User goal received", result=goal)

    analysis = analyze_goal(goal)
    state.constraints = analysis["constraints"]
    if analysis["potentially_risky"]:
        state.log("GOAL_ANALYSIS", f"Potentially risky intent keywords detected: {analysis['potentially_risky']}")

    state.tasks = decompose(goal, deps.llm, deps.registry.names())
    state.current_task_index = 0
    state.log("DECOMPOSE", f"{len(state.tasks)} subtask(s) generated",
               result="; ".join(t.description for t in state.tasks))

    state.status = AgentStatus.PLANNING


def _apply_demo_force_fail(state: AgentState, task: SubTask) -> tuple[bool, str]:
    if (state.demo_force_fail_remaining > 0
            and state.demo_force_fail_task_desc_contains
            and state.demo_force_fail_task_desc_contains.lower() in task.description.lower()):
        state.demo_force_fail_remaining -= 1
        return True, "Demo-forced failure (retry/escalation demonstration control)"
    return False, ""


def _step(state: AgentState, deps: Dependencies) -> None:
    """Advance exactly one micro-stage. Mutates `state` in place."""
    task = state.current_task

    if task is None:
        state.status = AgentStatus.COMPLETED
        state.final_result = _build_final_result(state)
        state.log("FINAL_RESULT", "Goal completed", result="All subtasks verified")
        return

    status = state.status

    if status == AgentStatus.PLANNING:
        state.log("PLAN", f"Executing subtask {task.task_id}: {task.description}")
        state.status = AgentStatus.RETRIEVING

    elif status == AgentStatus.RETRIEVING:
        query = task.arguments.get("query", task.description)
        chunks = deps.retriever.retrieve(query, top_k=3)
        state.retrieved_context = chunks
        state.log("RETRIEVE", f"{len(chunks)} knowledge chunk(s) retrieved for this subtask",
                   result="; ".join(chunks) if chunks else "(no relevant chunks)")
        state.status = AgentStatus.SELECTING_TOOL

    elif status == AgentStatus.SELECTING_TOOL:
        tool = deps.registry.get(task.tool)
        if tool is None:
            state.log("TOOL_SELECT", f"Requested tool '{task.tool}' is not in the allowlisted registry",
                       tool=task.tool, status="ERROR")
            state.status = AgentStatus.ESCALATED
            state.final_result = _build_final_result(state, unresolved=f"Unknown tool: {task.tool}")
            return
        state.selected_tool = tool.name
        state.log("TOOL_SELECT", f"Selected tool for subtask {task.task_id}", tool=tool.name)
        state.status = AgentStatus.RISK_CHECK

    elif status == AgentStatus.RISK_CHECK:
        # Authoritative risk = the tool's OWN registered level, never the
        # LLM-proposed one on the SubTask (see module docstring).
        tool = deps.registry.get(task.tool)
        state.risk_level = tool.risk_level
        state.log("RISK_CHECK", f"Risk classified as {tool.risk_level.value}",
                   tool=tool.name, risk=tool.risk_level.value)
        decision = gate(state)
        if decision == GateDecision.WAIT:
            state.status = AgentStatus.WAITING_FOR_APPROVAL
            state.approval_status = "PENDING"
            state.log("HUMAN_APPROVAL", f"Waiting for human approval: {tool.approval_reason}",
                       tool=tool.name, risk=tool.risk_level.value, status="WAITING")
        elif decision == GateDecision.DENIED:
            state.log("HUMAN_APPROVAL", "Human denied the action; reason logged", tool=tool.name, status="DENIED")
            state.status = AgentStatus.TERMINATED
            state.final_result = _build_final_result(state, unresolved="High-risk action denied by human")
        else:
            state.status = AgentStatus.EXECUTING

    elif status == AgentStatus.EXECUTING:
        if state.approval_status == "APPROVED":
            state.log("HUMAN_APPROVAL", "Human approved the action", tool=task.tool, status="APPROVED")
        tool = deps.registry.get(task.tool)
        result: ToolResult = tool.execute(**task.arguments)
        state.tool_result = result
        state.log("EXECUTE", f"Tool '{tool.name}' executed", tool=tool.name,
                   risk=state.risk_level.value if state.risk_level else None,
                   status="OK" if result.success else "FAILED", result=result.message)
        state.status = AgentStatus.OBSERVING

    elif status == AgentStatus.OBSERVING:
        state.observation = state.tool_result
        state.log("OBSERVE", "Execution result recorded as observation",
                   result=str(state.tool_result.result))
        state.status = AgentStatus.VERIFYING

    elif status == AgentStatus.VERIFYING:
        force_fail, reason = _apply_demo_force_fail(state, task)
        outcome = verify(task, state.tool_result, force_fail=force_fail, force_fail_reason=reason)
        state.verification_result = outcome.verified
        state.log("VERIFY", outcome.reason, tool=task.tool,
                   status="PASS" if outcome.verified else "FAIL")

        if outcome.verified:
            task.done = True
            state.approval_status = None
            planner = Planner(state)
            planner.advance()
            state.status = AgentStatus.PLANNING
        else:
            if state.retry_count < state.max_retries:
                planner = Planner(state)
                planner.replan()
                state.log("REPLANNING", f"Retry {state.retry_count}/{state.max_retries} for subtask {task.task_id}")
                state.status = AgentStatus.RETRIEVING
            else:
                state.log("ESCALATE", f"Retries exhausted ({state.max_retries}); escalating to human",
                           tool=task.tool, status="ESCALATED")
                state.status = AgentStatus.ESCALATED
                state.final_result = _build_final_result(
                    state, unresolved=f"Subtask {task.task_id} failed verification after {state.max_retries} retries")


def _build_final_result(state: AgentState, unresolved: str | None = None) -> dict:
    completed = [t.task_id for t in state.tasks if t.done]
    tool_actions = [e.tool for e in state.execution_trace if e.stage == "EXECUTE" and e.tool]
    return {
        "goal": state.goal,
        "completed_steps": completed,
        "tool_actions": tool_actions,
        "verification_status": state.status.value,
        "unresolved_issues": unresolved,
        "final_result": "Goal completed and verified" if unresolved is None else "Goal not fully completed",
    }


def run_until_pause(state: AgentState, deps: Dependencies, max_steps: int = 200) -> None:
    """Advance the state machine until it needs human input or reaches a
    terminal status. `max_steps` is a hard safety bound so a bug in this
    code can never spin the Streamlit server forever.

    WAITING_FOR_APPROVAL is both the status we pause *at* and one of the
    PAUSE_STATUSES we stop *for* -- so a second call after the human has
    made a decision would otherwise see we're "already at a pause status"
    and do nothing. Re-enter RISK_CHECK here so the gate gets evaluated
    against the now-set approval_status (caught by
    tests/test_agent.py::test_B_high_risk_action_never_executes_when_denied,
    which failed before this fix because DENIED never actually terminated
    the run)."""
    if state.status == AgentStatus.WAITING_FOR_APPROVAL and state.approval_status in ("APPROVED", "DENIED"):
        state.status = AgentStatus.RISK_CHECK

    steps = 0
    while state.status not in PAUSE_STATUSES and steps < max_steps:
        _step(state, deps)
        steps += 1
    if steps >= max_steps and state.status not in PAUSE_STATUSES:
        state.status = AgentStatus.ESCALATED
        state.final_result = _build_final_result(state, unresolved="Internal step limit reached")
        state.log("ESCALATE", "Internal step limit reached; escalating as a safety measure", status="ESCALATED")
