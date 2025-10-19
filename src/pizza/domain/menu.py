from typing import Sequence

from .errors import DuplicateSku, MenuItemNotFound
from .products import Pizza, Topping


class Menu:
    """
    Catalog: read-only access to Pizza, Topping and search.
    """

    def __init__(self, pizzas: Sequence[Pizza], toppings: Sequence[Topping]) -> None:
        seen_pizzas = set()
        for pizza in pizzas:
            sku = pizza.sku.strip().lower()
            if sku in seen_pizzas:
                raise DuplicateSku(f"Similar pizza sku - {sku}")
            else:
                seen_pizzas.add(sku)

        seen_toppings = set()
        for topping in toppings:
            sku = topping.sku.strip().lower()
            if sku in seen_toppings:
                raise DuplicateSku(f"Similar topping sku - {sku}")
            else:
                seen_toppings.add(sku)

        self._pizzas = tuple(pizzas)
        self._toppings = tuple(toppings)

    def list_pizzas(self) -> Sequence[Pizza]:
        return self._pizzas

    def list_toppings(self) -> Sequence[Topping]:
        return self._toppings

    def find_pizza_name(self, name: str) -> Sequence[Pizza]:
        if not name:
            return ()

        dummy = str(name).strip()
        if not dummy:
            return ()

        _match = []
        nor_name = (str(name).strip()).casefold()
        for pizza in self._pizzas:
            nor_pizza = pizza.name.casefold()
            if nor_name in nor_pizza:
                _match.append(pizza)
        return tuple(_match)

    def find_topping_name(self, name: str) -> Sequence[Topping]:
        if not name:
            return ()

        dummy = str(name).strip()
        if not dummy:
            return ()

        _match = []
        nor_name = (str(name).strip()).casefold()
        for topping in self._toppings:
            nor_topping = topping.name.casefold()
            if nor_name in nor_topping:
                _match.append(topping)
        return tuple(_match)

    def find_topping_sku(self, sku: str) -> Topping:
        if not sku:
            raise MenuItemNotFound(f"{sku} not found.")

        _match_sku = None
        for topping in self._toppings:
            if sku.casefold() == topping.sku.casefold():
                _match_sku = topping
                return _match_sku
        raise MenuItemNotFound(f"{sku} not found.")

    def find_pizza_sku(self, sku: str) -> Pizza:
        if not sku:
            raise MenuItemNotFound(f"{sku} not found.")

        _match_sku = None
        for pizza in self._pizzas:
            if sku.casefold() == pizza.sku.casefold():
                _match_sku = pizza
                return _match_sku

        raise MenuItemNotFound(f"{sku} not found.")
