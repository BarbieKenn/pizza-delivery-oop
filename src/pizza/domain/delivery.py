from dataclasses import dataclass
from typing import Literal, Protocol, Sequence


@dataclass(frozen=True, slots=True)
class Coordinates:
    x: float
    y: float


@dataclass(frozen=True, slots=True)
class Vehicle:
    kind: Literal["bike", "scooter", "car"]
    speed_coef: float


@dataclass(slots=True)
class Courier:
    id: str
    location: Coordinates
    vehicle: Vehicle
    available: bool
    current_load: int | None = None


class AssignmentStrategy(Protocol):
    def choose(self, order_address: Coordinates, couriers: Sequence[Courier]) -> Courier:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class AssignmentResult:
    order_id: str
    courier_id: str
    strategy_name: str
    eta: float | None = None
    notes: Sequence[str] = ()


class Dispatcher:
    def __init__(self, couriers: list[Courier], strategy: AssignmentResult) -> None:
        self.couriers = couriers
        self.strategy = strategy

    def assign(self, order: str) -> AssignmentResult:
        raise NotImplementedError

    def set_strategy(self, strategy: AssignmentStrategy) -> None:
        raise NotImplementedError

    def update_courier_location(self, courier_id: str, new_location: Coordinates) -> None:
        raise NotImplementedError
