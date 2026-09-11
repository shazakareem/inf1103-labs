inventory = 0
failed_entries = 0

while True:
        stock = input("Enter stock quantity (or type 'quit' to exit): ")
        if stock == 'quit':
                break

        if not stock.isdigit():
                print("Error: Invalid input. Please enter a valid number.")
                failed_entries += 1
                continue
        stock = int(stock)

        inventory += stock

        print("Stock added sucessfully.")
        print("Current inventory:", inventory)

        if inventory > 500:
                print("ALERT: Overstock! Inventory exceeds 500 units.")
                break

print("\n---Inventory Report---")
print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)