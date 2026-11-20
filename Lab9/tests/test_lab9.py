import io
import math
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from csv_loader import load_products
from discount_strategy import BulkDiscount, DiscountStrategy, NoDiscount, PercentageDiscount, StudentDiscount
from input_helpers import get_positive_float
from inventory import Inventory
from order import Order
from order_line import OrderLine
from product_factory import ProductFactory
from supplier import Supplier


class Lab9Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Demo Supplier", "demo@example.com")
        self.product = ProductFactory.create("physical", "P001", "Demo", 125.0, 10, self.supplier)

    def test_strategy_switching_and_student_extension(self) -> None:
        order = Order("O001")
        order.add_order_line(self.product, 2)
        self.assertEqual(order.calculate_total(), 250.0)
        order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)
        order.set_discount(StudentDiscount())
        self.assertEqual(order.calculate_total(), 237.5)

    def test_strategy_can_be_shared_and_replaced_by_custom_strategy(self) -> None:
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2
        shared = HalfPrice()
        for order_id in ("O001", "O002"):
            order = Order(order_id, shared)
            order.add_order_line(self.product, 2)
            self.assertIs(order.discount, shared)
            self.assertEqual(order.calculate_total(), 125.0)

    def test_bulk_boundaries_and_discount_validation(self) -> None:
        discount = BulkDiscount(200, 20)
        self.assertEqual(discount.apply(199), 199)
        self.assertEqual(discount.apply(200), 180)
        self.assertEqual(BulkDiscount(0, 20).apply(5), 0)
        self.assertEqual(NoDiscount().apply(250), 250)
        self.assertEqual(PercentageDiscount(100).apply(250), 0)
        for value in (-1, 101, math.nan, math.inf):
            with self.subTest(value=value), self.assertRaises(ValueError):
                PercentageDiscount(value)
        for threshold, amount in ((-1, 5), (5, -1), (math.inf, 5), (5, math.nan)):
            with self.subTest(threshold=threshold, amount=amount), self.assertRaises(ValueError):
                BulkDiscount(threshold, amount)

    def test_factory_returns_both_subtypes_with_requested_fields(self) -> None:
        self.assertEqual(self.product.to_dict()["weight"], 1.0)
        digital = ProductFactory.create("digital", "D001", "Editor", 49.9, 100,
                                        self.supplier, download_size=25)
        self.assertEqual(digital.to_dict()["type"], "digital")
        self.assertEqual(digital.to_dict()["download_size"], 25)
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            ProductFactory.create("service", "S001", "Install", 30, 5, self.supplier)

    def test_product_prices_and_stock_are_validated_for_both_types(self) -> None:
        for kind in ("physical", "digital"):
            for price in (0, -5, math.nan, math.inf):
                with self.subTest(kind=kind, price=price), self.assertRaises(ValueError):
                    ProductFactory.create(kind, "P", "Demo", price, 1, self.supplier)
            for stock in (-1, 1.5, True):
                with self.subTest(kind=kind, stock=stock), self.assertRaises(ValueError):
                    ProductFactory.create(kind, "P", "Demo", 10, stock, self.supplier)

    def test_order_line_owns_quantity_validation(self) -> None:
        for quantity in (0, -1, 1.5, True):
            with self.subTest(quantity=quantity), self.assertRaises(ValueError):
                OrderLine(self.product, quantity)
        self.assertEqual(OrderLine(self.product, 2).calculate_subtotal(), 250)

    def test_price_input_retries_until_valid(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(output):
            result = get_positive_float("Price: ")
        self.assertEqual(result, 12.50)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_price_input_rejects_nonfinite_and_zero_values(self) -> None:
        with patch("builtins.input", side_effect=["nan", "inf", "0", "1"]), redirect_stdout(io.StringIO()):
            self.assertEqual(get_positive_float("Price: "), 1)

    def test_csv_loads_three_and_reports_invalid_rows_in_order(self) -> None:
        inventory = Inventory()
        output = io.StringIO()
        path = Path(__file__).resolve().parents[1] / "products.csv"
        with redirect_stdout(output):
            load_products(path, inventory, self.supplier)
        self.assertEqual([p.get_product_id() for p in inventory.get_products()], ["P001", "D001", "P003"])
        lines = output.getvalue().splitlines()
        self.assertIn("Row 4 skipped: Unknown product type: service", lines[0])
        self.assertIn("Row 5 skipped:", lines[1])
        self.assertEqual(lines[2:], ["3 products loaded.", "Load attempt finished."])

    def test_missing_csv_prints_message_then_finally(self) -> None:
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as folder, redirect_stdout(output):
            path = Path(folder) / "missing.csv"
            inventory = Inventory()
            load_products(path, inventory, self.supplier)
        self.assertEqual(output.getvalue().splitlines(), [
            f"Products file not found: {path}", "Load attempt finished.",
        ])
        self.assertEqual(inventory.get_products(), ())

    def test_csv_skips_bad_shape_negative_stock_and_duplicate_ids(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "rows.csv"
            path.write_text(
                "product_type,product_id,name,price,stock_quantity\n"
                "physical,P1,Valid,10,2\n"
                "physical,P1,Duplicate,10,2\n"
                "digital,D1,Negative,10,-1\n"
                "bad,row\n"
                "digital,D2,Valid,10,3\n", encoding="utf-8"
            )
            inventory = Inventory()
            output = io.StringIO()
            with redirect_stdout(output):
                load_products(path, inventory, self.supplier)
            self.assertEqual(len(inventory.get_products()), 2)
            self.assertEqual(output.getvalue().count("skipped:"), 3)
            self.assertIn("2 products loaded.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
