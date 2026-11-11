import io
import unittest
from contextlib import redirect_stdout

from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


class Lab8Tests(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S001", "Demo Supplier", "demo@example.com")
        self.physical = PhysicalProduct("P001", "Mouse", 25.50, 10, 0.1, supplier)
        self.digital = DigitalProduct("D001", "eBook", 19.99, 20, 15.5, supplier)

    def test_products_keep_supplier_after_del(self) -> None:
        supplier = Supplier("S002", "Shared Supplier", "shared@example.com")
        physical = PhysicalProduct("P002", "Keyboard", 45.0, 8, 0.8, supplier)
        digital = DigitalProduct("D002", "Guide", 10.0, 12, 5.0, supplier)
        del supplier

        self.assertIs(physical.supplier, digital.supplier)
        output = io.StringIO()
        with redirect_stdout(output):
            physical.supplier.display_information()
            digital.supplier.display_information()
        self.assertEqual(output.getvalue().count("Shared Supplier"), 2)

    def test_same_product_can_move_between_inventories(self) -> None:
        inventory_a = Inventory()
        inventory_b = Inventory()
        inventory_a.add_product(self.physical)

        inventory_a.remove_product("P001")
        self.assertIsNone(inventory_a.find_product("P001"))
        self.assertEqual(self.physical.get_product_id(), "P001")

        inventory_b.add_product(self.physical)
        self.assertIs(inventory_b.find_product("P001"), self.physical)

    def test_orders_create_separate_lines_and_calculate_totals(self) -> None:
        first_order = Order("O001")
        second_order = Order("O002")

        first_order.add_order_line(self.physical, 2)
        first_order.add_order_line(self.digital, 1)
        second_order.add_order_line(self.physical, 1)

        self.assertIsNot(first_order.get_order_lines()[0], second_order.get_order_lines()[0])
        self.assertIs(first_order.get_order_lines()[0].product, self.physical)
        self.assertIs(second_order.get_order_lines()[0].product, self.physical)
        self.assertAlmostEqual(first_order.calculate_total(), 70.99)
        self.assertAlmostEqual(second_order.calculate_total(), 25.50)

        del first_order
        self.assertAlmostEqual(second_order.calculate_total(), 25.50)
        self.assertIs(second_order.get_order_lines()[0].product, self.physical)

    def test_stock_and_display_work_through_product(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)

        output = io.StringIO()
        with redirect_stdout(output):
            for product in inventory.get_products():
                inventory.update_stock(product.get_product_id(), 7)
                self.assertEqual(product.to_dict()["stock"], 7)
                show_product_details(product)

        for message in (
            "Weight: 0.1 kg",
            "Download size: 15.5 MB",
            "Requires physical shipping.",
            "Delivered digitally through a download.",
        ):
            self.assertIn(message, output.getvalue())


if __name__ == "__main__":
    unittest.main()