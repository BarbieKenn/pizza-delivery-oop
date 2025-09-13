from typing import Iterable

from menu import Menu
from products import Pizza


class OrderItem:
    """ """

    def __init__(self, pizza: Pizza, qty: int):
        self.pizza = pizza
        self.qty = qty


class Order:
    """ """

    def __init__(self, menu: Menu):
        self.menu = menu

    def add_item(self, pizza: Pizza, qty: int = 1) -> None: ...
    def remove_item(self, pizza: Pizza) -> None: ...
    def clear(self) -> None: ...
    def items(self) -> Iterable[OrderItem]: ...
    def total(self) -> float: ...
