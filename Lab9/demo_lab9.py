import argparse
from pathlib import Path

from csv_loader import load_products
from discount_strategy import BulkDiscount, PercentageDiscount, StudentDiscount
from input_helpers import get_positive_float
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 9 screenshot demonstrations")
    parser.add_argument("demo", choices=["strategy", "factory", "input", "csv", "missing"])
    demo = parser.parse_args().demo
    supplier = Supplier("S001", "Demo Supplier", "demo@example.com")

    if demo == "strategy":
        product = ProductFactory.create("physical", "P001", "Demo", 125, 10, supplier)
        order = Order("O001")
        order.add_order_line(product, 2)
        print(f"No discount: ${order.calculate_total():.2f}")
        order.set_discount(BulkDiscount(200, 20))
        print(f"Bulk discount: ${order.calculate_total():.2f}")
        order.set_discount(PercentageDiscount(10))
        print(f"10% discount: ${order.calculate_total():.2f}")
        order.set_discount(StudentDiscount())
        print(f"Student discount: ${order.calculate_total():.2f}")
    elif demo == "factory":
        for kind in ("physical", "digital", "service"):
            try:
                product = ProductFactory.create(kind, kind.upper(), "Demo", 25, 10, supplier)
            except ValueError as error:
                print(error)
            else:
                print(type(product).__name__, product.get_fulfilment_info())
    elif demo == "input":
        print(f"Accepted price: ${get_positive_float('Price: '):.2f}")
    else:
        filename = "products.csv" if demo == "csv" else "missing_products.csv"
        path = Path(__file__).with_name(filename)
        load_products(path, Inventory(), supplier)


if __name__ == "__main__":
    main()
