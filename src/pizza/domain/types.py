from decimal import ROUND_HALF_EVEN, Decimal

Money = Decimal
MONEY_QUANT = Decimal("0.01")
MONEY_ROUNDING = ROUND_HALF_EVEN


def quantize_money(value: Money) -> Money:
    return value.quantize(MONEY_QUANT, rounding=MONEY_ROUNDING)
