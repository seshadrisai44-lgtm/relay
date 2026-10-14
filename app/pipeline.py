from gate.pattern_gate import check_note


def process_note(note: str) -> dict:
    try:
        gate_result = check_note(note)
    except (TypeError, ValueError, RuntimeError):
        return {
            "status": "blocked",
            "findings": ["gate_error"],
        }

    if not isinstance(gate_result, dict):
        return {
            "status": "blocked",
            "findings": ["gate_error"],
        }

    if gate_result.get("allowed") is not True:
        return {
            "status": "blocked",
            "findings": gate_result.get("findings", ["gate_failed"]),
        }

    return {
        "status": "ready_for_next_check",
        "findings": [],
    }
