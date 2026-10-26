from product import Product
from storage import load_inventory, save_inventory


def get_valid_stock():
    while True:
        try:
            quantity = int(input("Stock Quantity: ").strip())

            if quantity < 0:
                raise ValueError

            return quantity

        except ValueError:
            print("Please enter a non-negative whole number.")


def add_product_from_input(inventory):
    product_id = input("Product ID: ").strip().upper()
    name = input("Product Name: ").strip()
    price = float(input("Price: ").strip())
    stock = get_valid_stock()

    product = Product(product_id, name, price, stock)

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock_from_input(inventory):
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    product.display_information()
    print("Enter the new total stock quantity.")

    quantity = get_valid_stock()

    inventory.update_stock(product_id, quantity)
    print("Stock updated successfully!")


def main():
    print("=" * 40)
    print("OOP INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    try:
        inventory = load_inventory()

    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Could not load inventory:", error)
        return

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

        try:
            if option == "1":
                inventory.display_all()

            elif option == "2":
                add_product_from_input(inventory)

            elif option == "3":
                update_stock_from_input(inventory)

            elif option == "4":
                product_id = input(
                    "Enter Product ID: "
                ).strip().upper()

                product = inventory.search_product(product_id)

                if product is None:
                    print("Product not found.")
                else:
                    product.display_information()

            elif option == "5":
                save_inventory(inventory)

            elif option == "6":
                save_inventory(inventory)
                print("Thank you. Program terminated.")
                break

            else:
                print("Invalid option. Please enter 1 to 6.")

        except ValueError as error:
            print("Invalid entry:", error)

        except OSError as error:
            print("Could not save inventory:", error)


if __name__ == "__main__":
    main()