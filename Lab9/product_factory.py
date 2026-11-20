from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        *,
        weight: float = 1.0,
        download_size: float = 1.0,
    ) -> Product:
        product_type = product_type.strip().lower()
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, weight, supplier)
        if product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, download_size, supplier)
        raise ValueError(f"Unknown product type: {product_type}")
