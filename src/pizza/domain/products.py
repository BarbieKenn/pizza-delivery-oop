from enum import Enum


class PizzaSize(Enum):
    """
    Pizza sizes. Ratio of the price depends on the pizza size.
    """

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Topping:
    """
    Topping description: Price and name.
    Implementation later.
    """

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class Pizza:
    """
    Pizza: name, default price, size, topping.
    Implementation later.
    """

    def __init__(
        self,
        name: str,
        default_price: float,
        size: PizzaSize,
        toppings: list[Topping] | None = None,
    ):
        self.name = name
        self.default_price = default_price
        self.size = size
        self.toppings = toppings
