from typing import Iterable

from menu import Menu
from products import Pizza
from status import OrderStatus


class OrderItem:
    """ """

    def __init__(self, pizza: Pizza, qty: int):
        self.pizza = pizza
        self.qty = qty


class Order:
    """ """

    status: OrderStatus

    def __init__(self, menu: Menu):
        self.menu = menu

    def add_item(self, pizza: Pizza, qty: int = 1) -> None: ...
    def remove_item(self, pizza: Pizza) -> None: ...
    def clear(self) -> None: ...
    def items(self) -> Iterable[OrderItem]: ...
    def total(self) -> float: ...

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

    def bake(self) -> None:
        """Set status to BAKING (only from ACCEPTED).
        Raise AlreadyFinalized if DELIVERED or CANCELED.
        Raise InvalidTransition otherwise.
        """

    def box(self) -> None:
        """Set status to BOXED (only from BAKING).
        Raise AlreadyFinalized if DELIVERED or CANCELED.
        Raise InvalidTransition otherwise.
        """

    def dispatch(self) -> None:
        """Set status to DISPATCHED (only from BOXED).
        Raise AlreadyFinalized if DELIVERED or CANCELED.
        Raise InvalidTransition otherwise.
        """

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
