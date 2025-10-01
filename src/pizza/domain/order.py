from __future__ import annotations

from decimal import Decimal
from typing import Iterable, Mapping, Protocol, Sequence

from delivery import Coordinates, Dispatcher
from inventory import Ingredient, Inventory, Oven
from menu import Menu
from pricing import Money, OrderView, PricingStrategy
from products import Pizza
from status import OrderStatus


class OrderItem:
    """Single order line: one pizza and its quantity."""

    def __init__(self, pizza: Pizza, qty: int):
        self.pizza = pizza
        self.qty = qty


class Order:
    """Order entity: items, pricing, state transitions, and delivery."""

    status: OrderStatus

    def __init__(self, menu: Menu):
        self.menu = menu

    def add_item(self, pizza: Pizza, qty: int = 1) -> None:
        """Add pizza with quantity to order."""
        ...

    def remove_item(self, pizza: Pizza) -> None:
        """Remove pizza from order completely."""
        ...

    def clear(self) -> None:
        """Remove all items from order."""
        ...

    def items(self) -> Iterable[OrderItem]:
        """Return iterable of order items."""
        ...

    def total(self) -> float:
        """Return raw float total (temporary, not for final sums)."""
        ...

    def can_accept(self) -> bool:
        """Return True if order can move NEW -> ACCEPTED."""

    def can_bake(self) -> bool:
        """Return True if order can move ACCEPTED -> BAKING."""

    def can_box(self) -> bool:
        """Return True if order can move BAKING -> BOXED."""

    def can_dispatch(self) -> bool:
        """Return True if order can move BOXED -> DISPATCHED."""

    def can_deliver(self) -> bool:
        """Return True if order can move DISPATCHED -> DELIVERED."""

    def can_cancel(self) -> bool:
        """Return True if order can move to 'CANCELED' (only from NEW or ACCEPTED)."""

    def accept(self) -> None:
        """Set status to ACCEPTED (only from NEW).
        Raise AlreadyFinalized if DELIVERED or CANCELED.
        Raise InvalidTransition otherwise.
        """

    def box(self) -> None:
        """Set status to BOXED (only from BAKING).
        Raise AlreadyFinalized if DELIVERED or CANCELED.
        Raise InvalidTransition otherwise.
        """

    def dispatch(self, dispatcher: "Dispatcher") -> None:
        """Set status to DISPATCHED (only from BOXED).
        Raise AlreadyFinalized if DELIVERED or CANCELED.
        Raise InvalidTransition otherwise.
        """
        raise NotImplementedError

    def deliver(self) -> None:
        """Set status to DELIVERED (only from DISPATCHED).
        Raise AlreadyFinalized if DELIVERED or CANCELED.
        Raise InvalidTransition otherwise.
        """

    def cancel(self) -> None:
        """Set status to CANCELED (only from NEW or ACCEPTED).
        Raise AlreadyFinalized if DELIVERED or CANCELED.
        Raise InvalidTransition otherwise.
        """

    _pricing_strategy: PricingStrategy
    _status: "OrderStatus"

    def set_pricing_strategy(self, strategy: PricingStrategy) -> None:
        """
        Acquire pricing strategy.

        Available ONLY at NEW/ACCEPTED.
        Otherwise, InvalidPricingOperation.
        """

        raise NotImplementedError

    def subtotal(self) -> Money:
        """
        Sum of positions without sales, taxes and delivery.
        """
        raise NotImplementedError

    def final_total(self) -> Money:
        """Total sum taking into account pricing strategy."""

        raise NotImplementedError

    def as_view(self) -> "OrderView":
        """
        Return read-only order representation."""

        raise NotImplementedError

    def to_units(self) -> Sequence[OrderUnit]:
        """
        Give order units individually to oven.
        """
        raise NotImplementedError

    def compute_total_requirements(self) -> Mapping["Ingredient", Decimal]:
        raise NotImplementedError

    def bake(self, inventory: "Inventory", oven: "Oven") -> None:
        """Set status to BAKING (only from ACCEPTED).
        Raise AlreadyFinalized if DELIVERED or CANCELED.
        Raise InvalidTransition otherwise.
        """
        raise NotImplementedError

    delivery_coordinates: "Coordinates"


class OrderUnit(Protocol):
    """One baked unit: pizza + size + toppings."""

    def requirements(self) -> Mapping["Ingredient", Decimal]:
        raise NotImplementedError
