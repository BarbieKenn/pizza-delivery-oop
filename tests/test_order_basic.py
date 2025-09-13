import pytest


@pytest.mark.xfail(reason="domain not implemented yet")
def test_total_with_two_items():
    """Create order with 2 items and expect correct total()."""
    ...


@pytest.mark.xfail(reason="validation not implemented yet")
def test_cannot_add_zero_or_negative_qty():
    """qty must be greater than 0"""
    ...


@pytest.mark.xfail(reason="menu validation not implemented yet")
def test_cannot_add_item_not_in_menu():
    """Cant add pizza that is not from the menu"""
    ...
