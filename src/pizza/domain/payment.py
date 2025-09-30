from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal, Protocol, Sequence

from order import Order

Money = Decimal


@dataclass(frozen=True, slots=True)
class PaymentAuthResult:
    payment_id: str
    status: Literal["authorized", "already-authorized"]
    amount: Money
    method: Literal["cash", "card", "online"]
    notes: Sequence[str] = ()
    created_at: str = ""


@dataclass(frozen=True, slots=True)
class PaymentCaptureResult:
    payment_id: str
    status: Literal["captured", "already-captured"]
    amount: Money
    method: Literal["cash", "card", "online"]
    notes: Sequence[str] = ()
    created_at: str = ""


@dataclass(frozen=True, slots=True)
class PaymentRefundResult:
    payment_id: str
    status: Literal["refunded", "partial-refund", "no-op"]
    amount: Money
    method: Literal["cash", "card", "online"]
    notes: Sequence[str] = ()
    created_at: str = ""


class Payment(Protocol):
    method: Literal["cash", "card", "online"]

    def authorize(self, order: "Order") -> PaymentAuthResult:
        raise NotImplementedError

    def capture(self, order: "Order", amount: Money) -> PaymentCaptureResult:
        raise NotImplementedError

    def refund(self, order: "Order", amount: Money) -> PaymentRefundResult:
        raise NotImplementedError


class CashPayment:
    method: Literal["cash"] = "cash"

    def authorize(self, order: "Order") -> PaymentAuthResult:
        raise NotImplementedError

    def capture(self, order: "Order", amount: Money) -> PaymentCaptureResult:
        raise NotImplementedError

    def refund(self, order: "Order", amount: Money) -> PaymentRefundResult:
        raise NotImplementedError


class CardPayment:
    method: Literal["card"] = "card"

    def __init__(self, provider: str = "mock-card") -> None:
        self._provider = provider

    def authorize(self, order: "Order") -> PaymentAuthResult:
        raise NotImplementedError

    def capture(self, order: "Order", amount: Money) -> PaymentCaptureResult:
        raise NotImplementedError

    def refund(self, order: "Order", amount: Money) -> PaymentRefundResult:
        raise NotImplementedError


class OnlinePayment:
    method: Literal["online"] = "online"

    def __init__(self, provider: str = "mock-online") -> None:
        self._provider = provider

    def authorize(self, order: "Order") -> PaymentAuthResult:
        raise NotImplementedError

    def capture(self, order: "Order", amount: Money) -> PaymentCaptureResult:
        raise NotImplementedError

    def refund(self, order: "Order", amount: Money) -> PaymentRefundResult:
        raise NotImplementedError
