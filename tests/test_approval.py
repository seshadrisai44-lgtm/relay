from app.approval import can_write_back


def test_write_back_blocked_without_approval():
    assert can_write_back(False) is False


def test_write_back_allowed_after_approval():
    assert can_write_back(True) is True


def test_write_back_blocked_when_approval_is_missing():
    assert can_write_back(None) is False
