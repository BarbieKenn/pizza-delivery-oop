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
    final_total: Money
    discount_amount: Money
    strategy_name: str
    breakdown: Sequence[str] = ()
    warnings: Sequence[str] = ()


class PricingStrategy(Protocol):
    def apply(self, order: "OrderView") -> PricingResult:
        raise NotImplementedError


class OrderView(Protocol):
    def subtotal(self) -> Money: ...

    @property
    def items(self) -> Sequence["OrderItemView"]: ...

    @property
    def metadata(self) -> Mapping[str, Any]: ...


class OrderItemView(Protocol):
    @property
    def unit_price(self) -> Money: ...

    @property
    def sku(self) -> str: ...


class NoDiscount(PricingStrategy):
    def apply(self, order: OrderView) -> PricingResult:
        raise NotImplementedError


class PercentOff(PricingStrategy):
    def __init__(self, percentage: Decimal) -> None:
        self._percentage = percentage

    def apply(self, order: OrderView) -> PricingResult:
        raise NotImplementedError


class BuyNGetMFree(PricingStrategy):
    def __init__(self, n: int, m: int, scope: str = "pizza_only") -> None:
        self._n = n
        self._m = m
        self._scope = scope

    def apply(self, order: OrderView) -> PricingResult:
        raise NotImplementedError


class FirstOrderCoupon(PricingStrategy):
    def __init__(self, code: str, percent: Decimal, expires_at: "date|None" = None) -> None: ...

    def apply(self, order: OrderView) -> PricingResult:
        raise NotImplementedError
