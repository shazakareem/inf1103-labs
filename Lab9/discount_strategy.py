import math
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        if not math.isfinite(percentage) or not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        if not math.isfinite(threshold) or threshold < 0:
            raise ValueError("Threshold must be finite and non-negative.")
        if not math.isfinite(amount) or amount < 0:
            raise ValueError("Discount amount must be finite and non-negative.")
        self.threshold: float = threshold
        self.amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return max(0.0, total - self.amount)
        return total


class StudentDiscount(PercentageDiscount):
    def __init__(self) -> None:
        super().__init__(5)
