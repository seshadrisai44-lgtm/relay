def can_write_back(approved: bool) -> bool:
    """Allow write-back only after explicit human approval."""
    return approved is True
