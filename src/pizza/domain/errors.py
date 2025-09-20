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
