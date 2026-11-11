import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from storage import load_inventory, save_inventory
from main import add_product_from_input


class Lab7Tests(unittest.TestCase):
    def setUp(self):
        self.physical = PhysicalProduct(" p001 ", "Laptop", 1200.0, 15, 2.0)
        self.digital = DigitalProduct("D001", "Python eBook", 19.99, 100, 15.5)
        self.inventory = Inventory()
        self.inventory.add_product(self.physical)
        self.inventory.add_product(self.digital)

    def test_product_is_abstract(self):
        with self.assertRaises(TypeError):
            Product("P000", "Generic", 1.0, 1)

    def test_incomplete_subclass_is_abstract(self):
        class IncompleteProduct(Product):
            pass
        with self.assertRaises(TypeError):
            IncompleteProduct("P000", "Incomplete", 1.0, 1)

    def test_interface_is_abstract(self):
        with self.assertRaises(TypeError):
            CanBeShipped()
        class MissingShipping(Product, CanBeShipped):
            def get_fulfilment_info(self):
                return "Physical shipping"
        with self.assertRaises(TypeError):
            MissingShipping("P000", "Incomplete", 1.0, 1)

    def test_display_reuses_common_details_and_adds_type_details(self):
        for product, expected in [(self.physical, "Weight: 2 kg"),
                                  (self.digital, "Download size: 15.5 MB")]:
            with self.subTest(product=type(product).__name__):
                stream = io.StringIO()
                with redirect_stdout(stream):
                    product.display_information()
                output = stream.getvalue()
                for text in ["ID:", "Name:", "Price:", "Stock:", expected]:
                    self.assertIn(text, output)

    def test_fulfilment_for_both_types(self):
        self.assertIn("shipping", self.physical.get_fulfilment_info())
        self.assertIn("download", self.digital.get_fulfilment_info())

    def test_shipping_varies_with_weight(self):
        self.assertIsInstance(self.physical, CanBeShipped)
        self.assertEqual(self.physical.calculate_shipping_cost(), 10.0)
        lighter = PhysicalProduct("P002", "Mouse", 25.5, 50, 0.1)
        self.assertEqual(lighter.calculate_shipping_cost(), 0.5)
        self.assertNotIsInstance(self.digital, CanBeShipped)
        self.assertFalse(hasattr(self.digital, "calculate_shipping_cost"))

    def test_search_duplicates_and_stock(self):
        self.assertIs(self.inventory.search_product(" p001 "), self.physical)
        self.assertIsNone(self.inventory.search_product("missing"))
        with self.assertRaises(ValueError):
            self.inventory.add_product(self.physical)
        self.inventory.update_stock("p001", 7)
        self.assertEqual(self.physical.to_dict()["stock"], 7)
        with self.assertRaises(ValueError):
            self.inventory.update_stock("missing", 2)
        with self.assertRaises(ValueError):
            self.inventory.update_stock("P001", -1)
        self.assertEqual(self.physical.to_dict()["stock"], 7)

    def test_inventory_display_and_empty_inventory(self):
        stream = io.StringIO()
        with redirect_stdout(stream):
            Inventory().display_all()
            self.inventory.display_all()
        for text in ["Inventory is empty.", "Laptop", "Python eBook", "Weight:", "Download size:"]:
            self.assertIn(text, stream.getvalue())

    def test_invalid_product_data(self):
        cases = [
            (PhysicalProduct, ("", "Laptop", 10.0, 1, 2.0)),
            (PhysicalProduct, ("P1", " ", 10.0, 1, 2.0)),
            (PhysicalProduct, ("P1", "Laptop", -1.0, 1, 2.0)),
            (PhysicalProduct, ("P1", "Laptop", float("nan"), 1, 2.0)),
            (PhysicalProduct, ("P1", "Laptop", 10.0, 1.5, 2.0)),
            (PhysicalProduct, ("P1", "Laptop", 10.0, True, 2.0)),
            (PhysicalProduct, ("P1", "Laptop", 10.0, 1, 0.0)),
            (PhysicalProduct, ("P1", "Laptop", 10.0, 1, float("inf"))),
            (DigitalProduct, ("D1", "Book", 10.0, 1, -5.0)),
            (DigitalProduct, ("D1", "Book", 10.0, 1, float("nan"))),
        ]
        for cls, args in cases:
            with self.subTest(cls=cls.__name__, args=args):
                with self.assertRaises(ValueError):
                    cls(*args)

    def test_json_round_trip_restores_types_and_all_attributes(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "inventory.json"
            with redirect_stdout(io.StringIO()):
                save_inventory(self.inventory, filename)
                restored = load_inventory(filename)
            self.assertIsNot(restored, self.inventory)
            self.assertIsInstance(restored.search_product("P001"), PhysicalProduct)
            self.assertIsInstance(restored.search_product("D001"), DigitalProduct)
            self.assertEqual([p.to_dict() for p in self.inventory.get_products()],
                             [p.to_dict() for p in restored.get_products()])
            self.assertEqual(restored.search_product("P001").calculate_shipping_cost(), 10.0)

    def test_missing_and_invalid_saved_data(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "inventory.json"
            with redirect_stdout(io.StringIO()):
                self.assertEqual(load_inventory(filename).get_products(), ())
            for data in [{}, [42], [{"id": "P1", "name": "Old", "price": 1, "stock": 1}],
                         [{"id": "P1", "name": "Unknown", "price": 1, "stock": 1, "type": "other"}]]:
                with self.subTest(data=data):
                    filename.write_text(json.dumps(data))
                    with self.assertRaises(ValueError):
                        load_inventory(filename)
            filename.write_text("not JSON")
            with self.assertRaises(json.JSONDecodeError):
                load_inventory(filename)

    def test_menu_creates_both_types(self):
        inventory = Inventory()
        for answers in [["1", "P5", "Guitar", "100", "2", "3"],
                        ["2", "D5", "Music", "10", "5", "25"]]:
            with patch("builtins.input", side_effect=answers), redirect_stdout(io.StringIO()):
                add_product_from_input(inventory)
        self.assertIsInstance(inventory.search_product("P5"), PhysicalProduct)
        self.assertIsInstance(inventory.search_product("D5"), DigitalProduct)


if __name__ == "__main__":
    unittest.main(verbosity=2)
