from enum import Enum


class OrderStatus(Enum):
    """
    Order status and available transitions
    NEW -> ACCEPTED -> BAKING -> BOXED -> DISPATCHED -> DELIVERED
    NEW -> CANCELED
    ACCEPTED -> CANCELED
    No cancellation after BAKING.
    """

    NEW = "new"
    """Order created, but not accepted in the restaurant."""
    ACCEPTED = "accepted"
    """Order accepted, but not baking."""
    BAKING = "baking"
    """Order is baking."""
    BOXED = "boxed"
    """Order baked and boxed."""
    DISPATCHED = "dispatched"
    """Courier received order."""
    DELIVERED = "delivered"
    """Order delivered."""
    CANCELED = "canceled"
    """Order canceled."""
