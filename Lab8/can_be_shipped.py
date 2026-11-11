from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """An interface contract for anything that supports shipping."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass