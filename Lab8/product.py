import math
from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        if not product_id.strip() or not name.strip():
            raise ValueError("Product ID and name cannot be empty.")

        if not math.isfinite(price) or price < 0:
            raise ValueError(
                "Price must be a finite, non-negative number."
            )

        self.__product_id = product_id.strip().upper()
        self.__name = name.strip()
        self.__price: float = price
        self.supplier: Supplier = supplier
        self.update_stock(stock)

    @property
    def price(self) -> float:
        return self.__price

    def get_product_id(self) -> str:
        return self.__product_id

    def update_stock(self, quantity: int) -> None:
        if type(quantity) is not int or quantity < 0:
            raise ValueError(
                "Stock must be a non-negative whole number."
            )

        self.__stock = quantity

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

    def to_dict(self) -> dict[str, str | int | float | dict[str, str]]:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": {
                "supplier_id": self.supplier.supplier_id,
                "name": self.supplier.name,
                "contact_email": self.supplier.contact_email,
            },
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Subclasses must explain how the product is delivered."""
        pass