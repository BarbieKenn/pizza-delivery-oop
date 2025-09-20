import pytest


@pytest.mark.parametrize(
    "path",
    [
        ("NEW", "BAKING"),
        ("NEW", "DISPATCHED"),
        ("NEW", "DELIVERED"),
        ("NEW", "BOXED"),
        ("ACCEPTED", "DELIVERED"),
        ("ACCEPTED", "DISPATCHED"),
        ("ACCEPTED", "BOXED"),
        ("BAKING", "DELIVERED"),
        ("BAKING", "DISPATCHED"),
        ("BAKING", "CANCELED"),
        ("BOXED", "DELIVERED"),
        ("BOXED", "CANCELED"),
        ("DISPATCHED", "CANCELED"),
    ],
)
@pytest.mark.xfail(reason="transitions not implemented yet")
def test_invalid_transitions_raise(path):
    """Invalid Transitions raises error."""
    ...


@pytest.mark.parametrize("final_status", ["DELIVERED", "CANCELED"])
@pytest.mark.xfail(reason="finalization rules not implemented")
def test_no_changes_after_final(final_status):
    """No changes available after DELIVERED/CANCELED."""
    ...


@pytest.mark.xfail(reason="workflow not implemented")
def test_happy_path():
    """Expected chain."""
    # chain = ["NEW", "ACCEPTED", "BAKING", "BOXED", "DISPATCHED", "DELIVERED"]
    ...
