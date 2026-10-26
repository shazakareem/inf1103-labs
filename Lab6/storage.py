import json

from inventory import Inventory
from product import Product

INVENTORY_FILE = "inventory.json"


def load_inventory():
    inventory = Inventory()

    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        print(
            "No inventory.json found. "
            "Starting with empty inventory."
        )
        return inventory

    for item in data:
        product = Product(
            item["id"],
            item["name"],
            item["price"],
            item["stock"]
        )

        inventory.add_product(product)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    data = [
        product.to_dict()
        for product in inventory.get_products()
    ]

    with open(INVENTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully to inventory.json.")