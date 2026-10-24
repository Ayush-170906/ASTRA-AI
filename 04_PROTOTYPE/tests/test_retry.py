from agent.state import AgentState, AgentStatus
from agent.controller import start, run_until_pause


def test_bounded_retry_then_success(deps):
    """Force exactly 1 failure (fewer than MAX_RETRIES=2) -> should retry
    once and then pass, reaching COMPLETED, never ESCALATED."""
    state = AgentState()
    state.demo_force_fail_task_desc_contains = "capacity"
    state.demo_force_fail_remaining = 1

    start(state, "Prepare an event brief and calculate capacity", deps)
    run_until_pause(state, deps)

    assert state.status == AgentStatus.COMPLETED
    replanning_events = [e for e in state.execution_trace if e.stage == "REPLANNING"]
    assert len(replanning_events) == 1


def test_retries_exhausted_escalates(deps):
    """Force failures for MORE attempts than MAX_RETRIES allows -> the
    loop must stop and escalate, never retry indefinitely."""
    state = AgentState()
    state.max_retries = 2
    state.demo_force_fail_task_desc_contains = "capacity"
    state.demo_force_fail_remaining = 10  # far more than MAX_RETRIES

    start(state, "Prepare an event brief and calculate capacity", deps)
    run_until_pause(state, deps)

    assert state.status == AgentStatus.ESCALATED
    assert state.retry_count == state.max_retries
    verify_fail_events = [e for e in state.execution_trace if e.stage == "VERIFY" and e.status == "FAIL"]
    # exactly MAX_RETRIES + 1 verification attempts: the original try plus
    # MAX_RETRIES retries, then escalate -- never a bare infinite loop.
    assert len(verify_fail_events) == state.max_retries + 1
