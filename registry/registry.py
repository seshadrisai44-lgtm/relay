from datetime import UTC, datetime


def register_agent(
    agent_id: str,
    agent_name: str,
    status: str = "active",
) -> dict:
    """Create a registry record for an agent."""
    if not agent_id.strip() or not agent_name.strip():
        raise ValueError("Agent ID and name are required.")

    if status not in {"active", "disabled"}:
        raise ValueError("Status must be active or disabled.")

    return {
        "agent_id": agent_id,
        "agent_name": agent_name,
        "status": status,
        "registered_at": datetime.now(UTC).isoformat(),
    }
