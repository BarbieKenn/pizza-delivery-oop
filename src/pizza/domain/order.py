from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Mapping, Protocol, Sequence

from .delivery import Coordinates, Dispatcher
from .errors import InvalidOrderItem, InvalidQuantity
from .menu import Menu
from .pricing import Money, OrderView, PricingStrategy
from .products import Pizza, PizzaSize, Topping
from .status import OrderStatus
from .types import OrderId, quantize_money

if TYPE_CHECKING:
    from .inventory import Ingredient, Inventory, Oven


class OrderItem:
    """Single order line: one pizza and its quantity."""

    def __init__(self, pizza: Pizza, qty: int, size: PizzaSize, toppings: tuple[Topping, ...]):
        self.pizza = pizza
        self.qty = qty
        self.size = size
        self.toppings = toppings

        if self.qty <= 0:
            raise InvalidQuantity(f"Got quantity = {qty}, expected > 0.")

    def unit_price(self) -> Money:
        unit_price = self.pizza.unit_price(self.size) + sum(
            topping.unit_price for topping in self.toppings
        )
        return quantize_money(unit_price)

    def line_price(self) -> Money:
        return quantize_money(self.unit_price() * self.qty)


class Order:
    """Order entity: items, pricing, state transitions, and delivery."""

    status: OrderStatus

    def __init__(
        self,
        menu: Menu,
        id: OrderId | None,
        customer: str,
        delivery_address: Coordinates,
        items: list[OrderItem],
        status: OrderStatus,
        pricing_strategy: PricingStrategy,
    ):
        self.id = id
        self.menu = menu
        self.customer = customer
        self.delivery_address = delivery_address
        self._items = list(items)
        self.status = status or OrderStatus.NEW
        self.pricing_strategy = pricing_strategy

    def add_item(
        self, pizza_sku: str, size: PizzaSize, qty: int, toppings_sku: Sequence[str]
    ) -> None:
        """Add pizza with quantity to order."""
        toppings = []
        for sku in toppings_sku:
            toppings.append(self.menu.find_topping_sku(sku=sku))
        pizza = self.menu.find_pizza_sku(sku=pizza_sku)
        item = OrderItem(pizza, qty, size, tuple(toppings))
        self._items.append(item)

    def remove_item(self, index: int) -> None:
        """Remove pizza from order."""
        if index < 0 or index > len(self._items):
            raise InvalidOrderItem(f"Invalid index: {index}")
        del self._items[index]

    def clear(self) -> None:
        """Remove all items from order."""
        self._items.clear()

    def items_view(self) -> Sequence[OrderItem]:
        """Return order items."""
        return tuple(self._items)

    def total(self) -> Money:
        """Return raw float total (temporary, not for final sums)."""
        total = 0
        for position in self._items:
            total += position.unit_price()
        return quantize_money(Decimal(total))

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
