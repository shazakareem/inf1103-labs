import json
from pathlib import Path

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
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
        if product_type == "physical":
            product = PhysicalProduct(*common, item["weight"], supplier)
        elif product_type == "digital":
            product = DigitalProduct(*common, item["download_size"], supplier)
        else:
            raise ValueError(
                f"Missing or unknown product type: {product_type!r}. "
                "Each product needs type 'physical' or 'digital' and its extra attribute."
            )
        inventory.add_product(product)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory, filename: str | Path = INVENTORY_FILE) -> None:
    data = [product.to_dict() for product in inventory.get_products()]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, allow_nan=False)
    print(f"Inventory saved successfully to {Path(filename).name}.")