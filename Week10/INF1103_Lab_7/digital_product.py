import math

from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        if not math.isfinite(download_size) or download_size <= 0:
            raise ValueError("Download size must be a finite number greater than zero.")
        self.__download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Download size: {self.__download_size:g} MB")

    def get_fulfilment_info(self):
        return "Delivered digitally through a download."

    def to_dict(self):
        data = super().to_dict()
        data.update({"type": "digital", "download_size": self.__download_size})
        return data
