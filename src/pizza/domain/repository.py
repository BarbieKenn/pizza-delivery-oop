from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from order import Order, OrderStatus


@dataclass(frozen=True, slots=True)
class PaymentRecord:
    payment_id: str
    method: str
    authorized_amount: str
    captured_amount: str
    refunded_amount: str
    status: str
    history: Sequence[str] = ()


class OrderRepository(Protocol):
    def save(self, order: "Order") -> str:
        raise NotImplementedError

    def get(self, order_id: str) -> "Order":
        raise NotImplementedError

    def find_by_status(self, status: "OrderStatus") -> Sequence["Order"]:
        raise NotImplementedError

    def list_all(self) -> Sequence["Order"]:
        raise NotImplementedError

    def link_courier(self, order_id: str, courier_id: str) -> None:
        raise NotImplementedError

    def payment_record(self, order_id: str) -> PaymentRecord | None:
        raise NotImplementedError


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[str, "Order"] = {}
        self._courier_links: dict[str, str] = {}
        self._payments: dict[str, PaymentRecord] = {}

    def save(self, order: "Order") -> str:
        raise NotImplementedError

    def get(self, order_id: str) -> "Order":
        raise NotImplementedError

    def find_by_status(self, status: "OrderStatus") -> Sequence["Order"]:
        raise NotImplementedError

    def list_all(self) -> Sequence["Order"]:
        raise NotImplementedError

    def link_courier(self, order_id: str, courier_id: str) -> None:
        raise NotImplementedError

    def payment_record(self, order_id: str) -> PaymentRecord | None:
        raise NotImplementedError
