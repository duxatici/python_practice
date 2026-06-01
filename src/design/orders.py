from dataclasses import dataclass
from decimal import Decimal
from abc import ABC, abstractmethod


@dataclass
class Order:
    """There is no need to describe anything here."""


class Discount(ABC):
    @abstractmethod
    def apply_discount(self, amount: Decimal) -> Decimal:
        pass

    @abstractmethod
    def is_applicable(self, order: Order) -> bool:
        pass


class FixPriceDiscount(Discount):
    def apply_discount(self, amount: Decimal) -> Decimal: ...

    def is_applicable(self, order: Order) -> bool: ...


class PercentageDiscount(Discount):
    def apply_discount(self, amount: Decimal) -> Decimal: ...

    def is_applicable(self, order: Order) -> bool: ...


class LoyaltyDiscount(Discount):
    def apply_discount(self, amount: Decimal) -> Decimal: ...

    def is_applicable(self, order: Order) -> bool: ...


class DiscountApplier:
    def __init__(self) -> None:
        self._strategies: list[Discount] = []

    def register_strategy(self, strategy: Discount) -> None:
        self._strategies.append(strategy)

    def calculate(self, order: Order, amount: Decimal) -> Decimal:
        total = amount
        for strategy in self._strategies:
            if strategy.is_applicable(order):
                total = strategy.apply_discount(total)

        return total
