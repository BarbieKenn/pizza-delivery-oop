from abc import ABC, abstractmethod

from products import Pizza, Topping


class Menu(ABC):
    """
    Catalog: read-only access to Pizza, Topping and search.
    """

    @abstractmethod
    def pizzas(self) -> list[Pizza]: ...

    @abstractmethod
    def toppings(self) -> list[Topping]: ...

    @abstractmethod
    def find_pizza(self, name: str) -> Pizza | None: ...

    @abstractmethod
    def find_topping(self, name: str) -> Topping | None: ...
