# INF1103 Lab 7 — based on your Lab 6 project

This is a separate Lab 7 copy of your Lab 6 Inventory Management System. Your original Desktop/Lab6 folder has not been edited. No extra Python packages are needed.

## Run it

1. Extract the ZIP and open the `INF1103_Lab_7` folder in VS Code.
2. Open a terminal in that folder.
3. Run:

```bash
python3 main.py
```

The included JSON has your four original products, now marked as physical, plus a digital eBook to demonstrate both types. **The added weights (2, 0.1, 0.8 and 4 kg) and the eBook are illustrative test data**, not specifications supplied in Lab 6. Replace them if you have actual values. The original IDs, names, prices and stock counts are retained.

The program loads inventory at startup, saves through option 5, and saves before exiting through option 6. Search for `P001` to see weight, fulfilment and shipping cost. Search for `D001` to see download size and digital fulfilment.

## What changed from your Lab 6

| File | Change |
| --- | --- |
| `product.py` | Inherits `ABC` and adds abstract `get_fulfilment_info()`. Your private attributes, getters, display, stock updates and `to_dict()` remain. Boolean stock values are also rejected. |
| `physical_product.py` | New subclass with private weight, overridden display and serialization, fulfilment, and shipping calculation. |
| `digital_product.py` | New subclass with private download size, overridden display and serialization, and fulfilment. |
| `can_be_shipped.py` | New interface-style ABC with only an abstract shipping method. |
| `inventory.py` | Unchanged from your Lab 6: it already delegates product behaviour correctly. |
| `storage.py` | Saves subtype fields through `to_dict()` and recreates the correct subclass from `type` when loading. Accepts an optional filename for isolated tests. |
| `main.py` | Adds a product-type choice and asks for weight or download size. Search also shows fulfilment and physical shipping cost. |
| `inventory.json` | Adds `type` and the appropriate subtype attribute. Includes both types for testing. |
| `Dockerfile` | Copies the new Python files and sample JSON as well as the original files. |

Stock updates still mean **set the new total**, as in your Lab 6. Setting stock to 7 replaces the old quantity; it does not add 7.

## Understand the main ideas

### 1. Inheritance and `super()`

`PhysicalProduct` and `DigitalProduct` are each a `Product`. Their constructors call:

```python
super().__init__(product_id, name, price, stock)
```

That reuses the existing validation and initializes the private Product attributes. Each child then validates and stores its own extra attribute.

### 2. Method overriding

Each child defines `display_information()` with the same name as the parent method. Calling it on a child selects the child's version. Inside that version:

```python
super().display_information()
```

prints the common product details first; the child then prints weight or download size. `to_dict()` uses the same pattern: reuse the common dictionary and add subtype data.

### 3. Abstraction

`Product` inherits from `ABC` and declares `get_fulfilment_info()` with `@abstractmethod`. Its body is `pass`, so each concrete child must supply the behaviour.

Trying this raises `TypeError`:

```python
from product import Product
Product("P000", "Generic product", 1.0, 1)
```

That failure is expected. A subclass that does not implement the abstract method cannot be instantiated either. Other Product methods are concrete and can still be reused.

### 4. Interface contract

`CanBeShipped` says that an implementing class must define `calculate_shipping_cost()`. It stores no product data and contains no shipping formula.

```python
class PhysicalProduct(Product, CanBeShipped):
```

Python technically expresses this with multiple base classes. Conceptually it is one implementation parent (`Product`) plus one interface contract (`CanBeShipped`), matching the lab's allowance for a single class inheritance relationship plus interfaces. `DigitalProduct` inherits only from `Product`.

The illustrative shipping formula is **$5 per kg per unit**, rounded to two decimal places. A 2 kg product costs $10.00 to ship; a 0.1 kg product costs $0.50. Inventory stock does not multiply this per-unit quote.

### 5. Persistence and responsibilities

Product classes know their own attributes and provide their dictionary representations. Storage handles JSON and reconstructs the subtype. Inventory manages the collection, checks IDs, and delegates stock/display behaviour to product objects. The menu handles interaction.

A saved physical product includes:

```json
{"id": "P001", "name": "Laptop", "price": 1200.0, "stock": 15,
 "type": "physical", "weight": 2.0}
```

A saved digital product has `"type": "digital"` and `"download_size"` instead. The loader intentionally rejects old Lab 6 records that lack a type: it cannot infer a weight or download size. Use the updated sample or add the correct type and extra field to your own data.

## Tests and restart demonstration

```bash
python3 -m unittest -v
```

There are 12 tests covering displays, abstract classes, the interface contract, shipping for different weights, invalid input, searching, duplicate IDs, stock, both menu choices, and saving/loading all fields with the correct object types. Temporary files are used so tests do not change the sample JSON.

To demonstrate persistence yourself:

1. Run `python3 main.py`.
2. Choose 2, then 1, and create a physical product with a unique ID and weight.
3. Choose 2, then 2, and create a digital product with a unique ID and download size.
4. Choose 5 to save, then 6 to exit.
5. Run `python3 main.py` again.
6. Choose 1 to display both products, then 4 to search each ID.
7. Verify their weight/download size and fulfilment remain correct.

`verification.txt` records the checks run while preparing this copy, including a save/exit/restart check using a temporary copy. The provided sample data remains unchanged.

## UML diagram

Open `UML_lab7.png` to view the diagram. `UML_lab7.svg` is the scalable version; `UML_lab7.mmd` is editable Mermaid source.

- Solid lines with hollow triangles point towards Product.
- The dashed line with a hollow triangle points towards CanBeShipped.
- Product is marked `<<abstract>>`; CanBeShipped is marked `<<interface>>`.
- The hollow diamond at Inventory indicates it holds a collection of product objects.
- `+` means public, `-` means private; italic methods marked `{abstract}` must be implemented.

## Git, Docker and your screenshots

Docker was not running in the preparation environment, so the container build/run has **not** been verified. The Dockerfile uses Python 3.11 and the application uses only its standard library. Run the following commands in your own project and capture genuine screenshots for the submission.

With Docker Desktop running, in the Lab 7 folder:

```bash
docker build -t inf1103-lab7 .
docker run --rm inf1103-lab7 python -m unittest -v
docker run --rm -it --mount "type=bind,source=$(pwd)/inventory.json,target=/app/inventory.json" inf1103-lab7
```

The file mount makes saves update your local `inventory.json`, so data survives container removal. If your class has a prescribed Docker command, use that established workflow instead.

For Git, use your existing course repository. If this is a new independent folder that is not already inside a repository, first run `git init`. Do not initialize another repository inside your existing course repository.

```bash
git status
git add .
git diff --cached --stat
git diff --cached
git commit -m "Add physical and digital products with inheritance and JSON persistence"
git push
git log --oneline -5
```

Review the staged changes before committing. `git push` requires your existing remote and branch setup. These commands have not been run for you. The `.gitignore` excludes caches, virtual environments, local environment variables and IDE settings while keeping the sample JSON.

Capture screenshots of your Git status/staged changes, commit/history and successful push, plus the Docker build, tests, and running menu with both product types. Follow any additional screenshot requirements from the earlier labs. Old Lab 6 screenshots do not demonstrate the Lab 7 implementation.

## Optional reflection (section 8)

The optional `SubscriptionProduct` extension is not implemented in this core solution. A useful reflection to adapt after trying it:

- A new concrete subclass could reuse Product without changing Product itself. Inventory could also handle it unchanged because it calls the common methods.
- The current menu has a physical/digital choice, so it would need another choice and prompts. The loader also has explicit branches for physical/digital, so it would need another branch.
- Therefore inheritance alone does not make the entire application closed to modification.
- A registry of product-type creators and loaders could replace those branches. A new type could register its creation prompts and deserialization function during application setup. The menu and loader could use the registry without gaining new type-specific branches. This is a factory/registration design improvement, rather than another inheritance relationship.

## Submission checklist

- Python source files and updated Dockerfile.
- Updated UML diagram.
- JSON data demonstrating both product types.
- Your own Git and Docker workflow screenshots (still to be captured).
- Review the implementation and explain the methods in your own words before submitting.
