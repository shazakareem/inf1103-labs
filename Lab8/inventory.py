class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            raise ValueError(
                "A product with that ID already exists."
            )

        self.__products.append(product)

    def search_product(self, product_id):
        product_id = product_id.strip().upper()

        for product in self.__products:
            if product.get_product_id() == product_id:
                return product

        return None

    def update_stock(self, product_id, quantity):
        product = self.search_product(product_id)

        if product is None:
            raise ValueError("Product not found.")

        product.update_stock(quantity)

    def display_all(self):
        if not self.__products:
            print("Inventory is empty.")
            return

        print("\nCurrent Inventory")
        print("-" * 60)

        for product in self.__products:
            product.display_information()

        print("-" * 60)

    def get_products(self):
        return tuple(self.__products)