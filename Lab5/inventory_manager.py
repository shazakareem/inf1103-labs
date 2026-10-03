import json

INVENTORY_FILE = "inventory.json"


def display_all(inventory):
    if not inventory:
        print("Inventory is empty.")
        return

    print("\nCurrent Inventory")
    print("-" * 60)

    for product in inventory:
        print(
            f"ID: {product['id']} | "
            f"Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | "
            f"Stock: {product['stock']}"
        )

    print("-" * 60)


def search_product(inventory, product_id):
    for product in inventory:
        if product["id"] == product_id:
            return product

    return None


def get_valid_stock():
    while True:
        try:
            stock = int(input("Stock Quantity: ").strip())

            if stock < 0:
                print("Stock cannot be negative.")
                continue

            return stock

        except ValueError:
            print("Please enter a non-negative whole number.")


def get_valid_price():
    while True:
        try:
            price = float(input("Price: ").strip())

            if not 0 <= price < float("inf"):
                print("Please enter a finite, non-negative price.")
                continue

            return price

        except ValueError:
            print("Please enter a valid number.")


def add_product(inventory):
    print("\nAdd New Product")

    product_id = input("Product ID: ").strip().upper()

    if not product_id:
        print("Product ID cannot be empty.")
        return

    if search_product(inventory, product_id) is not None:
        print("A product with that ID already exists.")
        return

    name = input("Product Name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    price = get_valid_price()
    stock = get_valid_stock()

    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }

    inventory.append(product)
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ").strip().upper()
    product = search_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print("Name:", product["name"])
    print("Current Stock:", product["stock"])
    print("Enter the new total stock quantity.")

    product["stock"] = get_valid_stock()
    print("Stock updated successfully!")