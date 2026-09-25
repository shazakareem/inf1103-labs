import json

MAX_CAPACITY = 500
TAX_RATE = 0.10
INVENTORY_FILE = "inventory.txt"


def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
            return data["inventory"], data["transactions"]
    except FileNotFoundError:
        return 0, []


def get_valid_input():
    # Count rejected entries during this input request.
    failed_attempts = 0

    while True:
        user_input = input(
            "Enter stock quantity (or type 'quit' to exit): "
        ).strip()

        if user_input.lower() == "quit":
            return "quit", failed_attempts

        try:
            value = int(user_input)

            if value < 0:
                raise ValueError

            return value, failed_attempts

        except ValueError:
            print("Error: Please enter a non-negative whole number.")
            failed_attempts += 1


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * TAX_RATE


def generate_report(total_units, failed_entries):
    print("\n--- Inventory Report ---")
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_entries)


def main():
    failed_entries = 0
    exit_program = False
    inventory, transaction_history = load_inventory()

    print("Loaded inventory:", inventory)
    print("Loaded transaction history:", transaction_history)

    while not exit_program:
        stock, failed_attempts = get_valid_input()
        failed_entries += failed_attempts

        if stock == "quit":
            exit_program = True
        else:
            inventory = process_delivery(inventory, stock)
            transaction_history.append(stock)
            tax_amount = calculate_tax(stock)

            print("Stock added successfully.")
            print(f"Tax for this delivery: {tax_amount:.2f}")
            print("Current inventory:", inventory)

            if inventory > MAX_CAPACITY:
                print("ALERT: Overstock! Inventory exceeds 500 units.")

    generate_report(inventory, failed_entries)
    print("Total Deliveries Processed:", len(transaction_history))
    print("Transaction History:", transaction_history)


if __name__ == "__main__":
    main()