from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Mapping, Protocol, Sequence

from order import OrderUnit


@dataclass(frozen=True, slots=True)
class Ingredient:
    name: str
    unit: str
    sku: str | None = None


@dataclass(frozen=True, slots=True)
class IngredientRequirement:
    ingredient: Ingredient
    amount: Decimal


class Inventory(Protocol):
    def availability(self, requirements: Mapping[Ingredient, Decimal]) -> bool:
        raise NotImplementedError

    def reserve(self, requirements: Mapping[Ingredient, Decimal]) -> ReservationToken:
        raise NotImplementedError

    def commit(self, token: ReservationToken) -> None:
        raise NotImplementedError

    def release(self, token: ReservationToken) -> None:
        raise NotImplementedError

    def current_stock(self) -> Mapping[Ingredient, Decimal]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class ReservationToken:
    id: str
    requirements_snapshot: Mapping[Ingredient, Decimal]


class Oven(Protocol):
    def can_bake(self, count: int) -> bool:
        raise NotImplementedError

    def bake_batch(self, items: Sequence[OrderUnit]) -> None:
        raise NotImplementedError
