from model_objects import Offer, Product, SpecialOfferType
from receipt import Receipt
from shopping_cart import ShoppingCart
from catalog import SupermarketCatalog


class Teller:
    def __init__(self, catalog: SupermarketCatalog):
        self.catalog = catalog
        self.offers: dict[Product, Offer] = {}

    def add_special_offer(self, offer_type: SpecialOfferType, product: Product, argument: float):
        """
        Register a special offer (e.g., 3-for-2, 10% off) for a specific product.
        :param offer_type: Type of offer from the enum
        :param product: Product object to apply the offer to
        :param argument: Numeric argument depending on the offer type:
                         - discount percentage for TEN_PERCENT_DISCOUNT
                         - price for x-for-amount offers
        """
        if offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
            if argument < 0 or argument > 100:
                raise ValueError("Discount percentage must be between 0 and 100")
        elif offer_type in [SpecialOfferType.TWO_FOR_AMOUNT,
                            SpecialOfferType.FIVE_FOR_AMOUNT]:
            if argument <= 0:
                raise ValueError("Offer price must be positive")
        elif offer_type == SpecialOfferType.THREE_FOR_TWO:
            if argument != 0:  # no argument needed
                raise ValueError("3-for-2 offer should have argument = 0")

        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart: ShoppingCart) -> Receipt:
        """
        Creates a receipt by calculating prices for each product and applying discounts.
        """
        receipt = Receipt()
        for pq in the_cart.items:
            product = pq.product
            quantity = pq.quantity

            unit_price = self.catalog.unit_price(product)
            total_price = quantity * unit_price

            receipt.add_product(product, quantity, unit_price, total_price)

        the_cart.handle_offers(receipt, self.offers, self.catalog)

        return receipt
