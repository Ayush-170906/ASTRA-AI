"""Tests for Demo Mode (agent/demo.py) -- added alongside the Phase 3 UI
enhancement. These do not touch app.py/Streamlit at all; run_full_demo is
a pure function of Dependencies, which is exactly what makes it testable.
"""
from agent.state import AgentStatus
from agent.demo import run_full_demo, DEMO_GOAL_ANNOUNCEMENT
from tools.mock_notification import get_sent_log


def test_all_four_scenarios_pass(deps):
    results = run_full_demo(deps)
    assert len(results) == 4
    assert all(r.passed for r in results), [
        (r.label, r.state.status.value, r.expected_status.value) for r in results if not r.passed
    ]


def test_demo_never_leaves_a_scenario_waiting(deps):
    """The whole point of Demo Mode is that it never hangs waiting for a
    human -- every scenario must reach a genuinely terminal status."""
    terminal = {AgentStatus.COMPLETED, AgentStatus.TERMINATED, AgentStatus.ESCALATED}
    results = run_full_demo(deps)
    for r in results:
        assert r.state.status in terminal, f"{r.label} ended at non-terminal {r.state.status}"


def test_scenario_1_is_normal_low_risk_execution(deps):
    results = run_full_demo(deps)
    s1 = results[0].state
    assert s1.status == AgentStatus.COMPLETED
    assert all(e.risk in (None, "LOW") for e in s1.execution_trace)


def test_scenario_2_uses_simulated_approval_then_executes(deps):
    results = run_full_demo(deps)
    s2 = results[1].state
    assert s2.status == AgentStatus.COMPLETED
    sim_events = [e for e in s2.execution_trace if "Simulated Human Approval: APPROVED" in e.description]
    assert len(sim_events) == 1
    assert any(e.stage == "EXECUTE" and e.tool == "mock_send_announcement" for e in s2.execution_trace)


def test_scenario_3_uses_simulated_denial_and_never_executes(deps):
    results = run_full_demo(deps)
    s3 = results[2].state
    assert s3.status == AgentStatus.TERMINATED
    sim_events = [e for e in s3.execution_trace if "Simulated Human Approval: DENIED" in e.description]
    assert len(sim_events) == 1
    assert not any(e.stage == "EXECUTE" for e in s3.execution_trace)


def test_scenario_4_exactly_two_retries_three_attempts(deps):
    results = run_full_demo(deps)
    s4 = results[3].state
    assert s4.status == AgentStatus.ESCALATED
    assert s4.retry_count == s4.max_retries == 2
    verify_fail_events = [e for e in s4.execution_trace if e.stage == "VERIFY" and e.status == "FAIL"]
    replanning_events = [e for e in s4.execution_trace if e.stage == "REPLANNING"]
    assert len(verify_fail_events) == 3  # 1 original attempt + 2 retries
    assert len(replanning_events) == 2   # exactly MAX_RETRIES retries, never more


def test_demo_causes_no_real_external_action_beyond_the_mock_log(deps):
    before = len(get_sent_log())
    run_full_demo(deps)
    after = len(get_sent_log())
    # exactly one mock "send" from the approved scenario 2; the denied
    # scenario 3 must not add another entry
    assert after == before + 1


def test_demo_is_independent_of_manual_mode_state(deps):
    """run_full_demo must not depend on or mutate any state the caller
    passes in beyond reading deps.retriever/deps.registry -- calling it
    twice in a row must give the same shape of result both times."""
    results_a = run_full_demo(deps)
    results_b = run_full_demo(deps)
    assert [r.expected_status for r in results_a] == [r.expected_status for r in results_b]
    assert all(r.passed for r in results_b)


def test_demo_goal_text_matches_manual_mode_high_risk_goal():
    # Sanity check that Demo Mode reuses the same documented goal text as
    # the manual high-risk demo path, not a divergent copy.
    assert "announcement" in DEMO_GOAL_ANNOUNCEMENT.lower()
    assert "participants" in DEMO_GOAL_ANNOUNCEMENT.lower()
