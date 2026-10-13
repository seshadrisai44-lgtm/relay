import re


def check_note(note: str) -> dict:
    if not isinstance(note, str):
        return {"allowed": False, "findings": ["invalid_input"]}
    """Block notes containing email addresses or secret-like patterns."""

    patterns = {
        "email_address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "secret_like_value": r"\b(?:API_KEY|SECRET|PASSWORD)\s*[:=]\s*\S+",
    }

    findings = []

    for name, pattern in patterns.items():
        if re.search(pattern, note, re.IGNORECASE):
            findings.append(name)

    return {
        "allowed": len(findings) == 0,
        "findings": findings,
    }
