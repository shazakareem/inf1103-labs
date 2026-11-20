import csv
from pathlib import Path

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str | Path, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    except OSError as error:
        print(f"Could not open products file: {error}")
    else:
        loaded = 0
        with file:
            rows = csv.reader(file)
            next(rows, None)
            for line_number, row in enumerate(rows, start=2):
                try:
                    if len(row) != 5:
                        raise ValueError("Expected five CSV fields.")
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        product_type, product_id, name, float(price), int(stock), supplier
                    )
                    inventory.add_product(product)
                except ValueError as error:
                    print(f"Row {line_number} skipped: {error}")
                else:
                    loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
