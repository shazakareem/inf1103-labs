inventory = 0
failed_entries = 0
deliveries_processed = 0


def get_valid_input():
    global failed_entries

    while True:
        stock = input(
            "Enter stock quantity (or type 'quit' to exit): "
        ).strip()

        if stock.lower() == "quit":
            return "quit"

        try:
            quantity = int(stock)

            if quantity < 0:
                raise ValueError

            return quantity

        except ValueError:
            print("Error: Please enter a non-negative whole number.")
            failed_entries += 1


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    print("\n--- Inventory Report ---")
    print("Total Units Processed:", total_units)
    print("Total Deliveries Processed:", deliveries_processed)
    print("Number of Failed/Rejected Entries:", failed_attempts)


while True:
    stock = get_valid_input()

    if stock == "quit":
        break

    inventory = process_delivery(inventory, stock)
    tax = calculate_tax(stock)
    deliveries_processed += 1

    print("Stock added successfully.")
    print(f"Tax for this delivery: {tax:.2f}")
    print("Current inventory:", inventory)

    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")


generate_report(inventory, failed_entries)