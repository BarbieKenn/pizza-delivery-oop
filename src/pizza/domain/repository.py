from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from order import Order, OrderStatus


@dataclass(frozen=True, slots=True)
class PaymentRecord:
    """Lightweight payment snapshot for inspection/CLI.

    Fields:
      payment_id: External/internal payment identifier.
      method: "cash" | "card" | "online".
      authorized_amount: Total authorized (string for v0.1.0).
      captured_amount: Total captured (string).
      refunded_amount: Total refunded (string).
      status: "new" | "authorized" | "captured" | "refunded".
      history: Free-form audit trail lines.
    """

    payment_id: str
    method: str
    authorized_amount: str
    captured_amount: str
    refunded_amount: str
    status: str
    history: Sequence[str] = ()


class OrderRepository(Protocol):
    """Repository contract for orders (v0.1.0: in-memory, synchronous).

    Semantics:
      - save() is upsert: create if no ID, otherwise update existing.
      - IDs are unique.
      - No persistence or concurrency guarantees in v0.1.0.
    """

    def save(self, order: "Order") -> str:
        """Insert or update an order; returns the order ID."""
        raise NotImplementedError

    def get(self, order_id: str) -> "Order":
        """Fetch an order by ID or raise OrderNotFound."""
        raise NotImplementedError

    def find_by_status(self, status: "OrderStatus") -> Sequence["Order"]:
        """Return all orders with the given status."""
        raise NotImplementedError

    def list_all(self) -> Sequence["Order"]:
        """Return all stored orders (unspecified ordering)."""
        raise NotImplementedError

    def link_courier(self, order_id: str, courier_id: str) -> None:
        """Associate an order with a courier (simple link)."""
        raise NotImplementedError

    def payment_record(self, order_id: str) -> PaymentRecord | None:
        """Return the current PaymentRecord for the order, if any."""
        raise NotImplementedError


class InMemoryOrderRepository:
    """Simple in-memory repository for development/tests.

    Storage:
      - _orders: order_id -> Order
      - _courier_links: order_id -> courier_id
      - _payments: order_id -> PaymentRecord

    Notes:
      - No disk persistence.
      - Not thread-safe (single-process test use).
    """

    def __init__(self) -> None:
        self._orders: dict[str, "Order"] = {}
        self._courier_links: dict[str, str] = {}
        self._payments: dict[str, PaymentRecord] = {}

    def save(self, order: "Order") -> str:
        """Upsert an order and return its ID."""
        raise NotImplementedError

    def get(self, order_id: str) -> "Order":
        """Return the order by ID or raise OrderNotFound."""
        raise NotImplementedError

    def find_by_status(self, status: "OrderStatus") -> Sequence["Order"]:
        """List orders filtered by status."""
        raise NotImplementedError

    def list_all(self) -> Sequence["Order"]:
        """List all stored orders."""

        raise NotImplementedError

    def link_courier(self, order_id: str, courier_id: str) -> None:
        """Link courier to order (overwrites previous link)."""

        raise NotImplementedError

    def payment_record(self, order_id: str) -> PaymentRecord | None:
        """Get PaymentRecord for order, or None if not set."""

        raise NotImplementedError
