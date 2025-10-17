from decimal import Decimal

import pytest

from src.pizza.domain.inventory import Ingredient, IngredientRequirement
from src.pizza.domain.menu import Menu
from src.pizza.domain.products import Pizza, PizzaSize, Topping
from src.pizza.domain.types import quantize_money


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


def test_size_multiplier_applied_to_price(menu_basic: Menu) -> None:
    for pizza in menu_basic.list_pizzas():
        for size, multiplier in {
            PizzaSize.SMALL: Decimal("0.75"),
            PizzaSize.MEDIUM: Decimal("1"),
            PizzaSize.LARGE: Decimal("1.25"),
        }.items():
            expected = quantize_money(multiplier * pizza.default_price)
            actual_price = pizza.unit_price(size=size)
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
    result = menu_basic.find_pizza_name(name=name)
    for pizza in result:
        result_names = [pizza.name for pizza in result]
        assert result_names == expected_name, f"Expected {expected_name}, but found {pizza.name}"
