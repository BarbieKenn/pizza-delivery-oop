from decimal import Decimal

import pytest

from src.pizza.domain.menu import Menu
from src.pizza.domain.products import Pizza, PizzaSize, Topping
from src.pizza.domain.types import quantize_money


@pytest.fixture
def menu_basic() -> Menu:
    pizzas = [
        Pizza("pz-mar", Decimal("10.00"), "Margherita", recipe=[]),
        Pizza("pz-pep", Decimal("11.00"), "Pepperoni", recipe=[]),
        Pizza("pz-4ch", Decimal("12.00"), "Four Cheese", recipe=[]),
    ]
    toppings = [
        Topping("tp-exch", Decimal("2.00"), "Extra Cheese"),
        Topping("tp-ppr", Decimal("1.50"), "Extra Pepper"),
    ]
    return Menu(pizzas=pizzas, toppings=toppings)


def test_size_multiplier_applied_to_price(menu_basic: Menu) -> None:
    for pizza in menu_basic.list_pizzas():
        for size, multiplier in {
            PizzaSize.SMALL: Decimal("0.75"),
            PizzaSize.MEDIUM: Decimal("1"),
            PizzaSize.LARGE: Decimal("1.25"),
        }.items():
            expected = quantize_money(multiplier * pizza.default_price)
            actual_price = pizza.price(size=size)
            assert expected == actual_price, f"{pizza.name} wrong price for {size}"


@pytest.mark.parametrize(
    "name, expected_name",
    [
        ("PEP", ["Pepperoni"]),
        ("  four", ["Four Cheese"]),
        ("ITA  ", ["Margherita"]),
        ("abc", []),
        ("", []),
        ("   ", []),
    ],
)
def test_menu_lookup_and_readonly(menu_basic: Menu, name: str, expected_name: list[str]) -> None:
    result = menu_basic.find_pizza(name=name)
    for pizza in result:
        assert pizza.name == expected_name, f"Expected {expected_name}, but found {pizza.name}"
