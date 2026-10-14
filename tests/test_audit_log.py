from audit.audit_log import create_audit_event


def test_audit_event_contains_basic_details():
    event = create_audit_event("note_check", "blocked")

    assert event["action"] == "note_check"
    assert event["status"] == "blocked"
    assert "timestamp" in event


def test_audit_event_does_not_store_note_contents():
    event = create_audit_event("note_check", "blocked")

    assert "note" not in event
    assert "content" not in event
    assert "secret" not in event
