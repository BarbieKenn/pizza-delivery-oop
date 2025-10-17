import uuid
from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, Decimal

Money = Decimal
MONEY_QUANT = Decimal("0.01")
MONEY_ROUNDING = ROUND_HALF_EVEN


@dataclass(frozen=True, slots=True)
class OrderId:
    value: uuid.UUID

    @classmethod
    def generate(cls) -> "OrderId":
        return cls(uuid.uuid4())

    @classmethod
    def from_str(cls, text: str):
        return cls(uuid.UUID(text))

    def __str__(self):
        return str(self.value)


def quantize_money(value: Money) -> Money:
    return value.quantize(MONEY_QUANT, rounding=MONEY_ROUNDING)
