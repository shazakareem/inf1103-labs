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


def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:
            inventory = json.load(file)

        print("inventory.json found.")
        print("Inventory loaded successfully.")
        return inventory

    except FileNotFoundError:
        print("inventory.json not found. Starting with empty inventory.")
        return []

def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)

    print("Inventory saved successfully to inventory.json.")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")

        option = input("Enter option: ").strip()

        if option == "1":
            display_all(inventory)

        elif option == "2":
            add_product(inventory)

        elif option == "3":
            update_stock(inventory)

        elif option == "4":
            print("\nSearch Product")
            product_id = input("Enter Product ID: ").strip().upper()
            product = search_product(inventory, product_id)

            if product is None:
                print("Product not found.")
            else:
                print("\nProduct Found")
                print("-" * 40)
                print("ID:", product["id"])
                print("Name:", product["name"])
                print(f"Price: ${product['price']:.2f}")
                print("Stock:", product["stock"])
                print("-" * 40)

        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)

        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()