from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from .errors import InvalidProductData
from .types import Money, quantize_money

if TYPE_CHECKING:
    from .inventory import IngredientRequirement


class PizzaSize(Enum):
    """
    Pizza sizes. Ratio of the price depends on the pizza size.
    """

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


MULTIPLIERS: dict[PizzaSize, Decimal] = {
    PizzaSize.SMALL: Decimal("0.75"),
    PizzaSize.MEDIUM: Decimal("1.0"),
    PizzaSize.LARGE: Decimal("1.25"),
}


class Topping:
    """
    Topping: unique SKU, name, unit price (per 1 portion), optional requirements.
    Price ≥ 0. Requirements amounts > 0 (if provided).
    """

    __slots__ = ("name", "_unit_price", "sku", "requirements")

    def __init__(
        self,
        name: str,
        unit_price: Money,
        sku: str,
        requirements: list["IngredientRequirement"] | None = None,
    ):
        self.name = name
        self._unit_price = unit_price
        self.sku = sku
        self.requirements = requirements or []

        if self._unit_price < 0:
            raise InvalidProductData(f"Topping {sku} must be >= 0.")
        if not all(req.amount > 0 for req in self.requirements):
            raise InvalidProductData(f"Topping {sku}: all requirements must be > 0")

    def unit_price(self) -> Money:
        return self._unit_price


class Pizza:
    """
    Pizza product definition.
    - default_price: Money (for MEDIUM, canonical baseline)
    - recipe: list of base IngredientRequirements (for MEDIUM)
    Invariants:
    - default_price ≥ 0
    - recipe is non-empty; all amounts > 0
    """

    __slots__ = ("name", "default_price", "sku", "recipe")

    def __init__(
        self,
        name: str,
        default_price: Money,
        sku: str,
        recipe: list["IngredientRequirement"],
    ):
        self.name = name
        self.default_price = default_price
        self.sku = sku
        self.recipe = list(recipe)

        if default_price < 0:
            raise InvalidProductData(f"Pizza {sku}: price must be >= 0.")
        if not self.recipe:
            raise InvalidProductData(f"Pizza {sku}: recipe must be non-empty.")
        if not all(ing.amount > 0 for ing in recipe):
            raise InvalidProductData(f"Pizza {sku}: all ingredients must be > 0")

    def unit_price(self, size: PizzaSize) -> Money:
        multiplier = MULTIPLIERS[size]
        return quantize_money(self.default_price * multiplier)

    def requirements(self, size: PizzaSize) -> list["IngredientRequirement"]:
        multiplier = MULTIPLIERS[size]
        result: list["IngredientRequirement"] = []
        for req in self.recipe:
            result.append(
                IngredientRequirement(ingredient=req.ingredient, amount=req.amount * multiplier)
            )
        return result
