from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_EVEN, Decimal, getcontext
from typing import Any, Mapping, Protocol, Sequence

Money = Decimal
MONEY_QUANT = Decimal("0.01")
MONEY_ROUNDING = ROUND_HALF_EVEN
getcontext().prec = 28


@dataclass(frozen=True)
class PricingResult:
    """Result of applying a pricing strategy."""

    final_total: Money
    discount_amount: Money
    strategy_name: str
    breakdown: Sequence[str] = ()
    warnings: Sequence[str] = ()


class PricingStrategy(Protocol):
    """Interface for pricing strategies."""

    def apply(self, order: "OrderView") -> PricingResult:
        """Return PricingResult for given order (must be pure/idempotent)."""

        raise NotImplementedError


class OrderView(Protocol):
    """Read-only view of an order for pricing."""

    def subtotal(self) -> Money:
        """Return subtotal without discounts, taxes, or delivery."""
        ...

    @property
    def items(self) -> Sequence["OrderItemView"]:
        """Flat list of items (unit-level) in the order."""
        ...

    @property
    def metadata(self) -> Mapping[str, Any]:
        """Metadata like {'is_first_order': True, 'coupon_code': 'WELCOME'}."""
        ...


class OrderItemView(Protocol):
    """Read-only unit-level order item."""

    @property
    def unit_price(self) -> Money:
        """Unit price of this item (after size/options)."""
        ...

    @property
    def sku(self) -> str:
        """SKU identifier of the product."""
        ...


class NoDiscount(PricingStrategy):
    """Default strategy: no discount applied."""

    def apply(self, order: OrderView) -> PricingResult:
        """Return subtotal as final_total with discount=0."""

        raise NotImplementedError


class PercentOff(PricingStrategy):
    """Percentage discount off subtotal."""

    def __init__(self, percentage: Decimal) -> None:
        """Initialize with percentage in [0, 100]."""

        self._percentage = percentage

    def apply(self, order: OrderView) -> PricingResult:
        """Apply percentage discount, respecting rounding rules."""

        raise NotImplementedError


class BuyNGetMFree(PricingStrategy):
    """Buy-N-Get-M-Free discount based on item scope."""

    def __init__(self, n: int, m: int, scope: str = "pizza_only") -> None:
        self._n = n
        self._m = m
        self._scope = scope

    def apply(self, order: OrderView) -> PricingResult:
        """Apply discount: in each group, mark M the cheapest items free."""

        raise NotImplementedError


class FirstOrderCoupon(PricingStrategy):
    """Coupon discount for first-time orders."""

    def __init__(self, code: str, percent: Decimal, expires_at: "date|None" = None) -> None: ...

    def apply(self, order: OrderView) -> PricingResult:
        """Apply coupon if order is first and coupon is valid; else error."""

        raise NotImplementedError
