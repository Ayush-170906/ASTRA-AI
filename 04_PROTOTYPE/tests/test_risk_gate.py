from agent.state import AgentState, RiskLevel
from safety.approval import gate, GateDecision
from safety.risk import requires_approval


def test_low_risk_never_requires_approval():
    assert requires_approval(RiskLevel.LOW) is False
    assert requires_approval(RiskLevel.MEDIUM) is False


def test_high_risk_requires_approval():
    assert requires_approval(RiskLevel.HIGH) is True


def test_gate_proceeds_immediately_for_low_risk():
    state = AgentState()
    state.risk_level = RiskLevel.LOW
    assert gate(state) == GateDecision.PROCEED


def test_gate_waits_for_high_risk_with_no_decision_yet():
    state = AgentState()
    state.risk_level = RiskLevel.HIGH
    state.approval_status = None
    assert gate(state) == GateDecision.WAIT


def test_gate_proceeds_only_after_explicit_approval():
    state = AgentState()
    state.risk_level = RiskLevel.HIGH
    state.approval_status = "APPROVED"
    assert gate(state) == GateDecision.PROCEED


def test_gate_denies_and_never_proceeds_when_denied():
    state = AgentState()
    state.risk_level = RiskLevel.HIGH
    state.approval_status = "DENIED"
    assert gate(state) == GateDecision.DENIED
    # A denied gate must never be reinterpreted as PROCEED under any
    # other combination of fields -- this is the core safety invariant.
    state.retry_count = 0
    state.verification_result = True
    assert gate(state) == GateDecision.DENIED
