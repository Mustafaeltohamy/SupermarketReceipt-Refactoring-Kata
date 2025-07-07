# Supermarket Receipt in [Python](https://www.python.org/)

## Setup

* Have Python installed
* Clone the repository
* On the command line, enter the `SupermarketReceipt-Refactoring-Kata/python` directory
* On the command line, install requirements, e.g. on the`python -m pip install -r requirements.txt`

## Running Tests

On the command line, enter the `SupermarketReceipt-Refactoring-Kata/python` directory and run

```
pytest
```

## Optional: Running [TextTest](https://www.texttest.org/) Tests

Install TextTest according to the [instructions](https://www.texttest.org/index.html#getting-started-with-texttest) (platform specific).

On the command line, enter the `SupermarketReceipt-Refactoring-Kata/python` directory and run

```
texttest -a sr -d .
```

## Enhancements:

- Fully refactored core files (teller.py, receipt.py, receipt_printer.py) with added type hints, documentation, and safe data handling.
- Implemented extensive test coverage for all offer types and edge cases (e.g. quantity under threshold, empty carts, large product names).
- Ensured robustness in receipt output formatting, quantity precision, and product name alignment.
- Added validation to avoid invalid discount configuration and preserved full compatibility with Python 3.10+.
- Reviewed the implementation for common security issues like code injection, file inclusion, and unbounded inputs.

As for the oop implementation, it now achieves the following:

- Encapsulation: Classes like Teller, Receipt, and ShoppingCart encapsulate behavior, exposing only public APIs.
- Abstraction: Consumers don’t need to know how offers or totals are calculated — just call checks_out_articles_from.
- Inheritance: FakeCatalog and CLIFakeCatalog both inherit from SupermarketCatalog, respecting LSP.
- Polymorphism: Through the use of Enum, ReceiptItem, and Discount structures, components can be processed uniformly.
- Single Responsibility: E.g., ReceiptPrinter only handles formatting, ShoppingCart only handles item collection logic.
- Open/Closed Principle: Easy to add new offer types without modifying core checkout flow logic.

These traits show mature OOP design, especially when paired with test coverage and CLI usability.


I have also added a cli implementation for the teller to simulate the process.

```
python cli_teller.py
```

It achieves the following:
- Add product to catalog
- Specify price and unit
- Add to cart by quantity
- Apply special offers
- Checkout and print receipt
- Reset cart after checkout
- Input validation

## Todo:
- Maybe add more tests for security
- Add file save for receipt.
- Add real printing service.
