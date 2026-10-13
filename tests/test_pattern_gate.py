from gate.pattern_gate import check_note


def test_safe_note_is_allowed():
    result = check_note("Project update: completed the design review.")
    assert result["allowed"] is True


def test_email_address_is_blocked():
    result = check_note("Contact: test@example.com")
    assert result["allowed"] is False
    assert "email_address" in result["findings"]


def test_secret_like_value_is_blocked():
    result = check_note("API_KEY = fake_test_value")
    assert result["allowed"] is False
    assert "secret_like_value" in result["findings"]


def test_invalid_input_is_not_allowed():
    result = check_note(None)
    assert result["allowed"] is False


def test_empty_input_is_allowed_to_be_checked():
    result = check_note("")
    assert result["allowed"] is True
