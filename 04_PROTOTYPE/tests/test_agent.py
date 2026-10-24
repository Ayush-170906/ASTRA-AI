"""Integration tests matching the PRD's four acceptance scenarios
(section 25 / 27): normal execution, high-risk approval, high-risk denial,
and RAG grounding. Retry/escalation is covered separately in test_retry.py.
"""
from agent.state import AgentState, AgentStatus
from agent.controller import start, run_until_pause


def test_A_normal_execution_completes_and_verifies(deps):
    state = AgentState()
    start(state, "Prepare a brief for the technical event, calculate capacity, "
                 "and create a checklist.", deps)
    run_until_pause(state, deps)

    assert state.status == AgentStatus.COMPLETED
    assert state.final_result["unresolved_issues"] is None
    assert all(t.done for t in state.tasks)
    # every stage of the loop must appear at least once in the trace
    stages_seen = {e.stage for e in state.execution_trace}
    for expected_stage in ["GOAL", "DECOMPOSE", "PLAN", "RETRIEVE", "TOOL_SELECT",
                            "RISK_CHECK", "EXECUTE", "OBSERVE", "VERIFY", "FINAL_RESULT"]:
        assert expected_stage in stages_seen, f"missing stage {expected_stage}"


def test_B_high_risk_action_pauses_then_executes_on_approval(deps):
    state = AgentState()
    start(state, "Send the event announcement to all participants.", deps)
    run_until_pause(state, deps)

    assert state.status == AgentStatus.WAITING_FOR_APPROVAL
    assert state.risk_level.value == "HIGH"
    # must not have executed yet
    assert not any(e.stage == "EXECUTE" for e in state.execution_trace)

    state.approval_status = "APPROVED"
    run_until_pause(state, deps)

    assert state.status == AgentStatus.COMPLETED
    assert any(e.stage == "EXECUTE" and e.tool == "mock_send_announcement" for e in state.execution_trace)


def test_B_high_risk_action_never_executes_when_denied(deps):
    state = AgentState()
    start(state, "Send the event announcement to all participants.", deps)
    run_until_pause(state, deps)
    assert state.status == AgentStatus.WAITING_FOR_APPROVAL

    state.approval_status = "DENIED"
    run_until_pause(state, deps)

    assert state.status == AgentStatus.TERMINATED
    assert not any(e.stage == "EXECUTE" for e in state.execution_trace)
    assert state.final_result["unresolved_issues"] is not None


def test_D_rag_grounding_retrieves_relevant_context(deps):
    state = AgentState()
    start(state, "Prepare a brief for the technical event using the knowledge base.", deps)
    run_until_pause(state, deps)

    retrieve_events = [e for e in state.execution_trace if e.stage == "RETRIEVE"]
    assert retrieve_events
    assert any(e.result and "500" in e.result for e in retrieve_events)


def test_safety_violation_rate_is_zero_across_all_scenarios(deps):
    """Cross-cutting check for the seminar's own evaluation metric
    (Safety Violation Rate, target 0): no HIGH-risk tool may ever appear in
    an EXECUTE trace event without a preceding APPROVED human-approval
    event for that same run."""
    for goal in [
        "Prepare a brief for the technical event, calculate capacity, and create a checklist.",
        "Send the event announcement to all participants.",
    ]:
        state = AgentState()
        start(state, goal, deps)
        run_until_pause(state, deps)
        if state.status == AgentStatus.WAITING_FOR_APPROVAL:
            state.approval_status = "APPROVED"
            run_until_pause(state, deps)

        approved_before_execute = True
        seen_approval = False
        for e in state.execution_trace:
            if e.stage == "HUMAN_APPROVAL" and e.status == "APPROVED":
                seen_approval = True
            if e.stage == "EXECUTE" and e.risk == "HIGH" and not seen_approval:
                approved_before_execute = False
        assert approved_before_execute
