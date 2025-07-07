from model_objects import Discount
from model_objects import Product
from typing import List


class ReceiptItem:
    def __init__(self, product: Product, quantity: float, price: float, total_price: float):
        """
        Represents one line item on a receipt.
        :param product: The product purchased
        :param quantity: Quantity purchased
        :param price: Unit price
        :param total_price: Total cost for the item (before discount)
        """
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price


class Receipt:
    def __init__(self):
        self._items: List[ReceiptItem] = []
        self._discounts: List[Discount] = []

    def total_price(self) -> float:
        """
        Calculates the grand total including discounts.
        """
        total = sum(item.total_price for item in self._items)
        total += sum(discount.discount_amount for discount in self._discounts)
        return total

    def add_product(self, product: Product, quantity: float, price: float, total_price: float):
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount: Discount):
        self._discounts.append(discount)

    @property
    def items(self) -> List[ReceiptItem]:
        return self._items[:]

    @property
    def discounts(self) -> List[Discount]:
        return self._discounts[:]
