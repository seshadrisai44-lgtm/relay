import pytest

from gate.denylist import contains_denylisted_term as hit


@pytest.mark.parametrize(
    "text",
    [
        "Met the Examplecorp team today.",
        "Examplecorp's review is scheduled.",
        "Waiting on EXAMPLECORP for access.",
    ],
)
def test_denylist_positive(text):
    assert hit(text) is True


@pytest.mark.parametrize(
    "text",
    [
        "Finished the onboarding review.",
        "Example slide deck was reviewed.",
        "Met the client team today.",
    ],
)
def test_denylist_negative(text):
    assert hit(text) is False
