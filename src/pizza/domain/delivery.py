from dataclasses import dataclass
from typing import Literal, Protocol, Sequence


@dataclass(frozen=True, slots=True)
class Coordinates:
    """Simple 2D coordinates for clients and couriers."""

    x: float
    y: float


@dataclass(frozen=True, slots=True)
class Vehicle:
    """Courier's vehicle type and speed factor."""

    kind: Literal["bike", "scooter", "car"]
    speed_coef: float


@dataclass(slots=True)
class Courier:
    """Courier entity with location, vehicle, and availability flag."""

    id: str
    location: Coordinates
    vehicle: Vehicle
    available: bool
    current_load: int | None = None


class AssignmentStrategy(Protocol):
    """Interface for courier assignment strategies."""

    def choose(self, order_address: Coordinates, couriers: Sequence[Courier]) -> Courier:
        """Pick a courier from the given list for an order address."""

        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class AssignmentResult:
    """Result of assigning a courier to an order."""

    order_id: str
    courier_id: str
    strategy_name: str
    eta: float | None = None
    notes: Sequence[str] = ()


class Dispatcher:
    """Dispatcher managing couriers and assignment strategy."""

    def __init__(self, couriers: list[Courier], strategy: AssignmentResult) -> None:
        self.couriers = couriers
        self.strategy = strategy

    def assign(self, order: str) -> AssignmentResult:
        """Assign a courier to the order (allowed only if couriers available)."""

        raise NotImplementedError

    def set_strategy(self, strategy: AssignmentStrategy) -> None:
        """Change assignment strategy (does not affect past assignments)."""

        raise NotImplementedError

    def update_courier_location(self, courier_id: str, new_location: Coordinates) -> None:
        """Update courier coordinates (stub in v0.1.0)."""

        raise NotImplementedError
