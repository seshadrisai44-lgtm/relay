from datetime import UTC, datetime


def create_audit_event(action: str, status: str) -> dict:
    """Create a minimal audit event without recording note contents."""
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "action": action,
        "status": status,
    }
