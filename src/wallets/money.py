from dataclasses import dataclass
from decimal import Decimal
from typing import Self

from src.wallets.currency import Currency
from src.wallets.exceptions import NegativeValueException, NotComparisonException


@dataclass(slots=True)
class Money:
    value: Decimal
    currency: Currency

    def __add__(self, other: Money) -> Money:
        self.compare_currency(other)
        a = Money(self.value + other.value, self.currency)
        return a

    def __sub__(self, other: Money) -> Money:
        self.compare_currency(other)

        return Money(self.value - other.value, self.currency)

    def compare_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise NotComparisonException


class Wallet:
    def __init__(self, money: Money) -> None:
        self.balances: dict[Currency, Money] = {}
        self.balances[money.currency] = money

    def __getitem__(self, key: Currency) -> Money:
        return self.balances.get(key, Money(Decimal(0), key))

    def __setitem__(self, key: Currency, value: Money) -> None:
        self.balances[key] = self[key] + value

    def __delitem__(self, key: Currency) -> None:
        if key in self.balances:
            del self.balances[key]

    def __len__(self) -> int:
        return len(self.balances)

    def __contains__(self, item: Currency) -> bool:
        return item in self.balances

    @property
    def currencies(self) -> set[Currency]:
        return set(self.balances.keys())

    def add(self, money: Money) -> Self:
        self[money.currency] = money
        return self

    def sub(self, money: Money) -> Self:
        result_money = self.balances[money.currency] - money
        if result_money.value < 0:
            raise NegativeValueException

        self.balances[money.currency] = result_money

        return self
