import math
from model_objects import Product, ProductQuantity, SpecialOfferType, Discount
from receipt import Receipt


class ShoppingCart:
    def __init__(self):
        self._items: list[ProductQuantity] = []
        self._product_quantities: dict[Product, float] = {}

    @property
    def items(self):
        return self._items

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item(self, product: Product):
        self.add_item_quantity(product, 1.0)

    def add_item_quantity(self, product: Product, quantity: float):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities:
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt: Receipt, offers: dict, catalog):
        for product, quantity in self._product_quantities.items():
            if product in offers:
                offer = offers[product]
                unit_price = catalog.unit_price(product)
                quantity_as_int = int(quantity)
                discount = None

                # Delegate offer logic to respective handler
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                    discount = self._apply_three_for_two(product, quantity_as_int, unit_price)
                elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                    discount = self._apply_two_for_amount(product, quantity_as_int, unit_price, offer.argument)
                elif offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                    discount = self._apply_five_for_amount(product, quantity_as_int, unit_price, offer.argument)
                elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                    discount = self._apply_ten_percent_discount(product, quantity, unit_price, offer.argument)
                else:
                    # Unknown offer type: safety check
                    raise ValueError(f"Unsupported offer type: {offer.offer_type}")

                if discount:
                    # Security Note: discount amounts should always be negative
                    if discount.discount_amount > 0:
                        raise ValueError("Discount amount should not be positive")
                    receipt.add_discount(discount)

    def _apply_three_for_two(self, product, quantity: int, unit_price: float):
        if quantity < 3:
            return None

        number_of_trios = quantity // 3  # Each trio of 3 qualifies for a discount
        total_without_discount = quantity * unit_price

        # Pay for 2 out of 3 items
        discounted_total = (number_of_trios * 2 * unit_price) + (quantity % 3 * unit_price)

        discount_amount = total_without_discount - discounted_total
        return Discount(product, "3 for 2", -discount_amount)


    def _apply_two_for_amount(self, product, quantity: int, unit_price: float, offer_price: float):
        if quantity < 2:
            return None
        number_of_pairs = quantity // 2
        discounted_total = number_of_pairs * offer_price + (quantity % 2) * unit_price
        discount_amount = quantity * unit_price - discounted_total
        return Discount(product, f"2 for {offer_price}", -discount_amount)

    def _apply_five_for_amount(self, product, quantity: int, unit_price: float, offer_price: float):
        if quantity < 5:
            return None
        number_of_fives = quantity // 5
        discounted_total = number_of_fives * offer_price + (quantity % 5) * unit_price
        discount_amount = quantity * unit_price - discounted_total
        return Discount(product, f"5 for {offer_price}", -discount_amount)

    def _apply_ten_percent_discount(self, product, quantity: float, unit_price: float, percent: float):
        if percent < 0 or percent > 100:
            raise ValueError("Invalid percentage value")
        discount_amount = quantity * unit_price * percent / 100.0
        return Discount(product, f"{percent}% off", -discount_amount)
