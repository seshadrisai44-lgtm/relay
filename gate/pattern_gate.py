import re

PATTERNS = {
    "PG-01": r"\b\d{1,3}(?:\.\d{1,3}){3}(?:/\d{1,2})?\b",
    "PG-02": r"\b[\w-]+\.(?:corp|local)\b|\bSRV-[\w-]+|\bDC\d{2}\b|-prod-\w*",
    "PG-03": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b|https?://\S+",
    "PG-04": r"\b[A-Za-z]+\\{1,2}svc_\w+|\bsvc_\w+",
    "PG-05": r"\b(?:API_KEY|SECRET|PASSWORD)\s*[:=]\s*\S+|\bAKIA[A-Z0-9]{16}\b",
    "PG-06": r"\b[0-9a-fA-F]{32}\b|\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b|\b[A-Za-z]:\\{1,2}\w+",
    "PG-07": r"\b(?:INC|CHG|RITM)\d{5,}\b",
    "PG-08": r"\bexamplecorp\b",
    "PG-09": r"\b(?:Maria Lopez|John Carter|Priya Nair)\b",
    "PG-10": r"\bCVE-\d{4}-\d{4,}\b",
}


def check_note(note: str) -> dict:
    """Block notes that hit any pattern rule."""
    if not isinstance(note, str):
        return {"allowed": False, "findings": ["invalid_input"]}
    findings = [r for r, p in PATTERNS.items() if re.search(p, note, re.IGNORECASE)]
    return {"allowed": not findings, "findings": findings}
