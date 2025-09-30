class DomainError(Exception):
    """Base domain pizza-delivery error"""

    pass


class InvalidQuantity(DomainError):
    """Invalid products quantity. Quantity must be > 0."""

    pass


class ItemNotInMenu(DomainError):
    """Product not in menu."""

    pass


class InvalidTransition(DomainError):
    """Invalid status transition.
    NEW -> ACCEPTED -> BAKING -> BOXED -> DISPATCHED -> DELIVERED
    NEW -> CANCELED
    ACCEPTED -> CANCELED
    No cancellation after BAKING."""

    pass


class AlreadyFinalized(DomainError):
    """Invalid status transition.
    No callouts from DELIVERED/CANCELED.
    """

    pass


class PricingError(Exception):
    """Base pricing error"""

    pass


class InvalidPricingOperation(PricingError):
    """Invalid pricing operation"""

    pass


class CouponExpired(PricingError):
    """Expired coupon."""

    pass


class CouponNotFirstOrder(PricingError):
    """Not first order."""

    pass


class IncompatibleStrategy(PricingError):
    """Incompatible Strategy."""

    pass


class InsufficientIngredients(DomainError):
    def __init__(self, needed, available):
        self.needed = needed
        self.available = available

    def __str__(self) -> str:
        return f"Insufficient ingredients: need {self.needed}, have {self.available}"


class ReservationError(DomainError):
    def __init__(self, reason: str):
        self.reason = reason

    def __str__(self) -> str:
        return f"Reservation error: {self.reason}"


class OvenCapacityExceeded(DomainError):
    def __init__(self, requested: int, capacity: int):
        self.requested = requested
        self.capacity = capacity

    def __str__(self) -> str:
        return f"Oven capacity exceeded: requested {self.requested}, capacity {self.capacity}"


class OvenUnavailable(DomainError):
    def __init__(self, reason: str):
        self.reason = reason

    def __str__(self) -> str:
        return f"Oven unavailable: {self.reason}"


class InvalidOrderState(DomainError):
    def __init__(self, state: str, action: str):
        self.state = state
        self.action = action

    def __str__(self) -> str:
        return f"Invalid order state: cannot {self.action} from {self.state}"


class NoCouriersAvailable(DomainError):
    def __str__(self) -> str:
        return "No couriers available"


class CourierUnavailable(DomainError):
    def __init__(self, courier_id: str):
        self.courier_id = courier_id

    def __str__(self) -> str:
        return f"Courier {self.courier_id} unavailable"


class OrderNotFound(DomainError):
    def __init__(self, order_id: str):
        self.order_id = order_id

    def __str__(self) -> str:
        return f"Order not found: {self.order_id}"


class DuplicateOrderId(DomainError):
    def __init__(self, order_id: str):
        self.order_id = order_id

    def __str__(self) -> str:
        return f"Duplicate order id: {self.order_id}"


class PaymentError(DomainError):
    """Base payment error."""


class PaymentAlreadyAuthorized(PaymentError):
    def __str__(self) -> str:
        return "Payment already authorized"


class PaymentNotAuthorized(PaymentError):
    def __str__(self) -> str:
        return "Payment not authorized"


class PaymentAlreadyCaptured(PaymentError):
    def __str__(self) -> str:
        return "Payment already captured"


class PaymentAmountMismatch(PaymentError):
    def __init__(self, amount: str, reason: str = ""):
        self.amount = amount
        self.reason = reason

    def __str__(self) -> str:
        return f"Invalid capture amount: {self.amount}. {self.reason}".strip()


class RefundExceedsCapture(PaymentError):
    def __init__(self, amount: str):
        self.amount = amount

    def __str__(self) -> str:
        return f"Refund exceeds captured amount: {self.amount}"
