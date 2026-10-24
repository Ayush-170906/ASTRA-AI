from agent.state import RiskLevel
from tools.calculator import calculate_capacity_tool
from tools.knowledge_lookup import generate_checklist_tool
from tools.mock_notification import mock_send_announcement_tool, get_sent_log


def test_calculate_capacity_success():
    result = calculate_capacity_tool.execute(registered=420, capacity=500)
    assert result.success
    assert result.result == 80


def test_calculate_capacity_negative_input_fails_cleanly():
    result = calculate_capacity_tool.execute(registered=-1, capacity=500)
    assert not result.success


def test_generate_checklist_returns_standard_items():
    result = generate_checklist_tool.execute()
    assert result.success
    assert "Venue" in result.result
    assert "Feedback collection" in result.result


def test_mock_send_announcement_is_high_risk_and_never_really_sends():
    assert mock_send_announcement_tool.risk_level == RiskLevel.HIGH
    before = len(get_sent_log())
    result = mock_send_announcement_tool.execute(message="hello", recipients="test group")
    assert result.success
    assert "MOCK" in result.message
    assert len(get_sent_log()) == before + 1
