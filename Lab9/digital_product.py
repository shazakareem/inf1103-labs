import math

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if not math.isfinite(download_size) or download_size <= 0:
            raise ValueError("Download size must be a finite number greater than zero.")
        self.__download_size: float = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download size: {self.__download_size:g} MB")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally through a download."

    def to_dict(self) -> dict[str, str | int | float | dict[str, str]]:
        data = super().to_dict()
        data.update({"type": "digital", "download_size": self.__download_size})
        return data