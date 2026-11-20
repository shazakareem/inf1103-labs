import json
from pathlib import Path

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier

# Locate the file beside the source, regardless of the terminal's current folder.
INVENTORY_FILE = Path(__file__).with_name("inventory.json")


def load_inventory(filename: str | Path = INVENTORY_FILE) -> Inventory:
    inventory = Inventory()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("No inventory file found. Starting with empty inventory.")
        return inventory

    if not isinstance(data, list):
        raise ValueError("Inventory JSON must contain a list of products.")

    legacy_supplier = Supplier("UNKNOWN", "Unassigned supplier", "")
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each saved product must be a JSON object.")
        product_type = item.get("type")
        common = (item["id"], item["name"], item["price"], item["stock"])
        supplier_data = item.get("supplier")
        supplier = legacy_supplier if supplier_data is None else Supplier(**supplier_data)
        if not isinstance(product_type, str):
            raise ValueError("Each saved product needs a product type.")
        product = ProductFactory.create(
            product_type, *common, supplier,
            weight=item.get("weight", 1.0),
            download_size=item.get("download_size", 1.0),
        )
        inventory.add_product(product)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory, filename: str | Path = INVENTORY_FILE) -> None:
    data = [product.to_dict() for product in inventory.get_products()]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, allow_nan=False)
    print(f"Inventory saved successfully to {Path(filename).name}.")
