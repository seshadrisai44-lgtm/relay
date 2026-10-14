import pytest

from registry.registry import register_agent


def test_register_agent():
    result = register_agent("agent-001", "Status Agent")

    assert result["agent_id"] == "agent-001"
    assert result["agent_name"] == "Status Agent"
    assert result["status"] == "active"
    assert "registered_at" in result


def test_register_agent_rejects_empty_id():
    with pytest.raises(ValueError):
        register_agent("", "Status Agent")


def test_register_agent_rejects_invalid_status():
    with pytest.raises(ValueError):
        register_agent("agent-001", "Status Agent", "unknown")
