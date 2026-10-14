from app.pipeline import process_note


def test_email_is_blocked():
    result = process_note("Contact: test@example.com")
    assert result["status"] == "blocked"


def test_safe_note_can_continue():
    result = process_note("Completed the design review.")
    assert result["status"] == "ready_for_next_check"


def test_invalid_input_is_blocked():
    result = process_note(None)
    assert result["status"] == "blocked"


def test_gate_error_blocks_processing(monkeypatch):
    def broken_gate(note):
        raise RuntimeError("Simulated gate failure")

    monkeypatch.setattr("app.pipeline.check_note", broken_gate)

    result = process_note("Synthetic weekly status update")

    assert result["status"] == "blocked"
    assert result["findings"] == ["gate_error"]


def test_uncertain_gate_result_blocks_processing(monkeypatch):
    def uncertain_gate(note):
        return {"allowed": None, "findings": ["uncertain"]}

    monkeypatch.setattr(
        "app.pipeline.check_note",
        uncertain_gate,
    )

    result = process_note("Synthetic weekly status update")

    assert result["status"] == "blocked"
