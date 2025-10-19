from decimal import Decimal

import pytest

from src.pizza.domain.delivery import Coordinates
from src.pizza.domain.errors import (
    DuplicateSku,
    InvalidOrderItem,
    InvalidQuantity,
    MenuItemNotFound,
)
from src.pizza.domain.inventory import Ingredient, IngredientRequirement
from src.pizza.domain.menu import Menu
from src.pizza.domain.order import Order
from src.pizza.domain.products import Pizza, PizzaSize, Topping


@pytest.fixture
def menu_basic() -> Menu:
    dough = Ingredient(name="Dough", unit="kg")
    cheese = Ingredient(name="Cheese", unit="kg")

    pizzas = [
        Pizza(
            sku="pz-mar",
            default_price=Decimal("10.00"),
            name="Margherita",
            recipe=[
                IngredientRequirement(dough, Decimal("1.0")),
                IngredientRequirement(cheese, Decimal("0.3")),
            ],
        ),
        Pizza(
            sku="pz-pep",
            default_price=Decimal("11.00"),
            name="Pepperoni",
            recipe=[
                IngredientRequirement(dough, Decimal("1.0")),
                IngredientRequirement(cheese, Decimal("0.3")),
            ],
        ),
        Pizza(
            sku="pz-4ch",
            default_price=Decimal("12.00"),
            name="Four Cheese",
            recipe=[
                IngredientRequirement(dough, Decimal("1.0")),
                IngredientRequirement(cheese, Decimal("0.45")),
            ],
        ),
    ]
    toppings = [
        Topping(name="Extra Cheese", unit_price=Decimal("2.00"), sku="tp-exch", requirements=None),
        Topping(name="Extra Pepper", unit_price=Decimal("1.50"), sku="tp-ppr", requirements=None),
    ]
    return Menu(pizzas=pizzas, toppings=toppings)


def test_total_with_two_items(menu_basic: Menu) -> None:
    """Create order with 2 items and expect correct total()."""
    menu = menu_basic
    order = Order(
        menu=menu,
        id=None,
        customer="test-user",
        delivery_address=Coordinates(0, 0),
        items=[],
        status=None,
        pricing_strategy=None,
    )
    order.add_item("pz-mar", PizzaSize.SMALL, 1, ("tp-ppr", "tp-exch"))
    order.add_item("pz-pep", PizzaSize.LARGE, 2, ["tp-exch"])

    expected = sum(pos.line_total() for pos in order.items_view())
    actual = order.subtotal()

    assert expected == actual, f"Wrong total price: expected {expected}, got {actual}"


def test_cannot_add_zero_or_negative_qty(menu_basic: Menu) -> None:
    """qty must be greater than 0"""
    menu = menu_basic
    order = Order(
        menu=menu,
        id=None,
        customer="test-user",
        delivery_address=Coordinates(0, 0),
        items=[],
        status=None,
        pricing_strategy=None,
    )
    qty = -1
    with pytest.raises(InvalidQuantity):
        order.add_item("pz-mar", PizzaSize.SMALL, qty, ("tp-ppr", "tp-exch"))


def test_cannot_add_item_not_in_menu(menu_basic: Menu) -> None:
    """Cant add pizza that is not from the menu"""
    menu = menu_basic
    order = Order(
        menu=menu,
        id=None,
        customer="test-user",
        delivery_address=Coordinates(0, 0),
        items=[],
        status=None,
        pricing_strategy=None,
    )
    with pytest.raises(MenuItemNotFound):
        order.add_item("pz-margi", PizzaSize.SMALL, 1, ("tp-ppr", "tp-exch"))


def test_duplicate_toppings_sku() -> None:
    """Duplicate toppings sku raises DuplicateSku error."""
    dough = Ingredient(name="Dough", unit="kg")
    cheese = Ingredient(name="Cheese", unit="kg")

    pizzas = [
        Pizza(
            sku="pz-mar",
            default_price=Decimal("10.00"),
            name="Margherita",
            recipe=[
                IngredientRequirement(dough, Decimal("1.0")),
                IngredientRequirement(cheese, Decimal("0.3")),
            ],
        ),
    ]
    toppings = [
        Topping(name="Extra Cheese", unit_price=Decimal("2.00"), sku="tp-exch"),
        Topping(name="Extra Pepper", unit_price=Decimal("1.50"), sku="tp-exch"),
    ]

    with pytest.raises(DuplicateSku):
        Menu(pizzas=pizzas, toppings=toppings)


def test_clear_order(menu_basic: Menu) -> None:
    """Clear order removes all items and resets subtotal to zero."""
    menu = menu_basic
    order = Order(
        menu=menu,
        id=None,
        customer="test-user",
        delivery_address=Coordinates(0, 0),
        items=[],
        status=None,
        pricing_strategy=None,
    )
    order.clear()
    items_len = len(order.items_view())
    subtotal = order.subtotal()
    assert items_len == 0, f"Length of orders items is {items_len}, expected 0."
    assert subtotal == 0, f"Order subtotal is {subtotal}, expected 0."


def test_remove_item(menu_basic: Menu) -> None:
    menu = menu_basic
    order = Order(
        menu=menu,
        id=None,
        customer="test-user",
        delivery_address=Coordinates(0, 0),
        items=[],
        status=None,
        pricing_strategy=None,
    )
    idx = -1
    with pytest.raises(InvalidOrderItem):
        order.remove_item(idx)


def test_read_only_items(menu_basic: Menu) -> None:
    """items_view() must return read-only (immutable) sequence."""
    menu = menu_basic
    order = Order(
        menu=menu,
        id=None,
        customer="test-user",
        delivery_address=Coordinates(0, 0),
        items=[],
        status=None,
        pricing_strategy=None,
    )
    items_view = order.items_view()

    assert isinstance(items_view, tuple), "items_view() must return a tuple."

    with pytest.raises(AttributeError):
        items_view.append("hack")

    assert items_view == tuple(order._items), "items_view() should reflect current items."
