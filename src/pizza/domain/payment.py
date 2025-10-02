from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal, Protocol, Sequence

from order import Order

Money = Decimal


@dataclass(frozen=True, slots=True)
class PaymentAuthResult:
    """Result of authorize(): freeze funds for an order."""

    payment_id: str
    status: Literal["authorized", "already-authorized"]
    amount: Money
    method: Literal["cash", "card", "online"]
    notes: Sequence[str] = ()
    created_at: str = ""


@dataclass(frozen=True, slots=True)
class PaymentCaptureResult:
    """Result of capture(): charge funds."""

    payment_id: str
    status: Literal["captured", "already-captured"]
    amount: Money
    method: Literal["cash", "card", "online"]
    notes: Sequence[str] = ()
    created_at: str = ""


@dataclass(frozen=True, slots=True)
class PaymentRefundResult:
    """Result of refund(): return funds after capture."""

    payment_id: str
    status: Literal["refunded", "partial-refund", "no-op"]
    amount: Money
    method: Literal["cash", "card", "online"]
    notes: Sequence[str] = ()
    created_at: str = ""


class Payment(Protocol):
    """Common interface for all payment methods (cash, card, online)."""

    method: Literal["cash", "card", "online"]

    def authorize(self, order: "Order") -> PaymentAuthResult:
        """Freeze funds (or no-op for cash)."""

        raise NotImplementedError

    def capture(self, order: "Order", amount: Money) -> PaymentCaptureResult:
        """Charge funds up to the final_total of the order."""

        raise NotImplementedError

    def refund(self, order: "Order", amount: Money) -> PaymentRefundResult:
        """Refund funds after capture, within captured amount."""

        raise NotImplementedError


class CashPayment:
    """Cash payment: capture immediately, authorize is optional."""

    method: Literal["cash"] = "cash"

    def authorize(self, order: "Order") -> PaymentAuthResult:
        """Optional: mark as authorized; usually skipped for cash."""

        raise NotImplementedError

    def capture(self, order: "Order", amount: Money) -> PaymentCaptureResult:
        """Mark order as paid in cash."""

        raise NotImplementedError

    def refund(self, order: "Order", amount: Money) -> PaymentRefundResult:
        """Refund cash (theoretical in v0.1.0)."""

        raise NotImplementedError


class CardPayment:
    """Card payment: requires authorize before capture."""

    method: Literal["card"] = "card"

    def __init__(self, provider: str = "mock-card") -> None:
        self._provider = provider

    def authorize(self, order: "Order") -> PaymentAuthResult:
        """Freeze funds on card provider."""

        raise NotImplementedError

    def capture(self, order: "Order", amount: Money) -> PaymentCaptureResult:
        """Charge card up to authorized amount."""

        raise NotImplementedError

    def refund(self, order: "Order", amount: Money) -> PaymentRefundResult:
        """Refund card charge within captured amount."""

        raise NotImplementedError


class OnlinePayment:
    """Online payment: same flow as card, different provider."""

    method: Literal["online"] = "online"

    def __init__(self, provider: str = "mock-online") -> None:
        self._provider = provider

    def authorize(self, order: "Order") -> PaymentAuthResult:
        """Freeze funds through online provider."""

        raise NotImplementedError

    def capture(self, order: "Order", amount: Money) -> PaymentCaptureResult:
        """Charge online provider up to authorized amount."""

        raise NotImplementedError

    def refund(self, order: "Order", amount: Money) -> PaymentRefundResult:
        """Refund online charge within captured amount."""

        raise NotImplementedError
