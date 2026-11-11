import math

from product import Product
from supplier import Supplier
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if not math.isfinite(weight) or weight <= 0:
            raise ValueError("Weight must be a finite number greater than zero.")
        self.__weight: float = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight:g} kg")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        # Example rule: $5 per kilogram, for one unit of this product.
        return round(self.__weight * 5.0, 2)

    def to_dict(self) -> dict[str, str | int | float | dict[str, str]]:
        data = super().to_dict()
        data.update({"type": "physical", "weight": self.__weight})
        return data