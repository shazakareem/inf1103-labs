import math

from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        if not math.isfinite(weight) or weight <= 0:
            raise ValueError("Weight must be a finite number greater than zero.")
        self.__weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:g} kg")

    def get_fulfilment_info(self):
        return "Requires physical shipping."

    def calculate_shipping_cost(self):
        # Example rule: $5 per kilogram, for one unit of this product.
        return round(self.__weight * 5.0, 2)

    def to_dict(self):
        data = super().to_dict()
        data.update({"type": "physical", "weight": self.__weight})
        return data
