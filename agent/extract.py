CATEGORIES = {
    "access": ["access", "approval", "permission"],
    "dependency": ["waiting on", "depends", "dependency"],
    "scope": ["scope", "change request"],
    "staffing": ["staff", "resource", "headcount"],
}


def _category(text: str) -> str:
    t = text.lower()
    for cat, words in CATEGORIES.items():
        if any(w in t for w in words):
            return cat
    return "other"


def _severity(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ("stopped", "cannot proceed", "deadline")):
        return "high"
    if "waiting" in t:
        return "medium"
    return "low"


def extract_note(note: dict) -> dict:
    """Stand-in extraction: rules only, no model call."""
    return {
        "note_id": note.get("note_id"),
        "engagement_code": note.get("engagement_code"),
        "milestones_done": note.get("milestones_done", []),
        "tasks": [{"title": t.strip()[:80]} for t in note.get("next_week", [])],
        "blockers": [
            {
                "summary": b.strip()[:200],
                "category": _category(b),
                "severity": _severity(b),
            }
            for b in note.get("blockers", [])
        ],
        "questions": [],
    }
