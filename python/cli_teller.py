"""
Command Line Interface for Supermarket Teller Simulation

This CLI lets you:
- Add products to a catalog
- Add items to a shopping cart
- Apply discount offers
- Checkout and print the receipt
"""
from model_objects import Product, ProductUnit, SpecialOfferType
from teller import Teller
from receipt_printer import ReceiptPrinter
from shopping_cart import ShoppingCart
from catalog import SupermarketCatalog


class CLIFakeCatalog(SupermarketCatalog):
    """
    A CLI version of the FakeCatalog for adding products via user input.
    """
    def __init__(self):
        self.products = {}
        self.prices = {}

    def add_product(self, product: Product, price: float):
        self.products[product.name] = product
        self.prices[product.name] = price

    def unit_price(self, product: Product) -> float:
        return self.prices[product.name]


def get_product_unit():
    while True:
        unit = input("Enter unit (each/kilo): ").strip().lower()
        if unit == "each":
            return ProductUnit.EACH
        elif unit == "kilo":
            return ProductUnit.KILO
        else:
            print("Invalid unit. Try again.")


def get_offer_type():
    print("Choose offer type:")
    for idx, offer in enumerate(SpecialOfferType, 1):
        print(f"{idx}. {offer.name}")
    while True:
        try:
            choice = int(input("Enter offer number: "))
            return list(SpecialOfferType)[choice - 1]
        except (ValueError, IndexError):
            print("Invalid selection. Try again.")


def main():
    catalog = CLIFakeCatalog()
    teller = Teller(catalog)
    cart = ShoppingCart()

    print("\n=== Supermarket CLI Teller ===")

    while True:
        print("\nOptions:")
        print("1. Add product to catalog")
        print("2. Add item to cart")
        print("3. Apply special offer")
        print("4. Checkout and print receipt")
        print("5. Quit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            name = input("Product name: ").strip()
            unit = get_product_unit()
            price = float(input("Price: "))
            product = Product(name, unit)
            catalog.add_product(product, price)
            print(f"Added '{name}' to catalog.")

        elif choice == "2":
            name = input("Product name (must exist in catalog): ").strip()
            if name not in catalog.products:
                print("Product not found in catalog.")
                continue
            quantity = float(input("Quantity: "))
            cart.add_item_quantity(catalog.products[name], quantity)
            print(f"Added {quantity} of '{name}' to cart.")

        elif choice == "3":
            name = input("Product name to discount: ").strip()
            if name not in catalog.products:
                print("Product not found in catalog.")
                continue
            offer_type = get_offer_type()
            argument = float(input("Enter discount argument (e.g. percent or amount): "))
            teller.add_special_offer(offer_type, catalog.products[name], argument)
            print(f"Offer applied on '{name}'.")

        elif choice == "4":
            receipt = teller.checks_out_articles_from(cart)
            printer = ReceiptPrinter()
            output = printer.print_receipt(receipt)
            print("\nReceipt:")
            print(output)
            # Reset cart for next session
            cart = ShoppingCart()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
