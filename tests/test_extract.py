from agent.extract import extract_note


def test_extract_basic():
    note = {
        "note_id": "n1",
        "next_week": ["Review phase 2 runbook"],
        "blockers": ["Waiting on access approval"],
        "milestones_done": ["M1"],
    }
    r = extract_note(note)
    assert r["tasks"][0]["title"] == "Review phase 2 runbook"
    assert r["blockers"][0]["category"] == "access"
    assert r["milestones_done"] == ["M1"]


def test_long_title_trimmed():
    r = extract_note({"next_week": ["x" * 200]})
    assert len(r["tasks"][0]["title"]) <= 80
