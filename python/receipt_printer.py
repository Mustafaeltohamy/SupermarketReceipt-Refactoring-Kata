from model_objects import ProductUnit
from receipt import Receipt, ReceiptItem
from model_objects import Discount


class ReceiptPrinter:
    def __init__(self, columns: int = 40):
        """
        Initializes the receipt printer.
        :param columns: Number of characters per line
        """
        self.columns = columns

    def print_receipt(self, receipt: Receipt) -> str:
        """
        Generates a printable receipt string from the receipt data.
        """
        result = ""

        for item in receipt.items:
            result += self.print_receipt_item(item)

        for discount in receipt.discounts:
            result += self.print_discount(discount)

        result += "\n"
        result += self.present_total(receipt)
        return result

    def print_receipt_item(self, item: ReceiptItem) -> str:
        """
        Prints the line for a purchased item, possibly including price breakdown.
        """
        name = item.product.name
        total_price_str = self.print_price(item.total_price)

        # Align product name and total price
        line = self.format_line_with_whitespace(name, total_price_str)

        # If multiple items were purchased, show unit price and quantity
        if item.quantity != 1:
            line += f"  {self.print_price(item.price)} * {self.print_quantity(item)}\n"

        return line

    def format_line_with_whitespace(self, left: str, right: str) -> str:
        """
        Aligns a line to the specified width with padding whitespace.
        """
        whitespace_size = self.columns - len(left) - len(right)
        if whitespace_size < 0:
            # Edge case: names too long. Truncate name to fit.
            left = left[:self.columns - len(right) - 1] + " "
            whitespace_size = 1

        return f"{left}{' ' * whitespace_size}{right}\n"

    def print_price(self, price: float) -> str:
        """
        Formats a price to 2 decimal places.
        """
        return f"{price:.2f}"

    def print_quantity(self, item: ReceiptItem) -> str:
        """
        Formats quantity depending on unit type.
        """
        if item.product.unit == ProductUnit.EACH:
            return f"{int(item.quantity)}"
        else:
            return f"{item.quantity:.3f}"

    def print_discount(self, discount: Discount) -> str:
        """
        Prints a discount line with label and discount amount.
        """
        name = f"{discount.description} ({discount.product.name})"
        amount = self.print_price(discount.discount_amount)
        return self.format_line_with_whitespace(name, amount)

    def present_total(self, receipt: Receipt) -> str:
        """
        Prints the final total amount of the receipt.
        """
        total_str = self.print_price(receipt.total_price())
        return self.format_line_with_whitespace("Total: ", total_str)
