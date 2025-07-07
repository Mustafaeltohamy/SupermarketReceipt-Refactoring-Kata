import pytest

from model_objects import Product, ProductUnit, SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from receipt_printer import ReceiptPrinter


def create_catalog_with_products():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    cereal = Product("cereal", ProductUnit.EACH)
    gum = Product("gum", ProductUnit.EACH)

    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 2.00)
    catalog.add_product(cereal, 4.50)
    catalog.add_product(gum, 0.75)

    return catalog, toothbrush, apples, cereal, gum


def test_three_for_two_offer_applies_correctly():
    catalog, _, _, _, gum = create_catalog_with_products()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, gum, 0)

    cart = ShoppingCart()
    cart.add_item_quantity(gum, 3)

    receipt = teller.checks_out_articles_from(cart)

    assert len(receipt.discounts) == 1
    discount = receipt.discounts[0]
    assert discount.description == "3 for 2"
    assert discount.discount_amount == pytest.approx(-0.75, 0.01)

def test_two_for_amount_offer_applies_correctly():
    catalog, toothbrush, *_ = create_catalog_with_products()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 1.5)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 2)

    receipt = teller.checks_out_articles_from(cart)

    assert len(receipt.discounts) == 1
    assert receipt.total_price() == pytest.approx(1.50, 0.01)


def test_five_for_amount_offer_with_remainder():
    catalog, _, _, cereal, _ = create_catalog_with_products()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, cereal, 18.0)

    cart = ShoppingCart()
    cart.add_item_quantity(cereal, 6)

    receipt = teller.checks_out_articles_from(cart)

    # 5 for 18.0, 1 left at 4.5 = 22.5 total
    assert receipt.total_price() == pytest.approx(22.5, 0.01)
    assert len(receipt.discounts) == 1


def test_ten_percent_discount_applies_correctly():
    catalog, toothbrush, *_ = create_catalog_with_products()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    assert len(receipt.discounts) == 1
    assert receipt.total_price() == pytest.approx(0.89, 0.01)


def test_no_offer_applied_when_not_enough_quantity():
    catalog, _, apples, *_ = create_catalog_with_products()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, apples, 0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2)  # Not enough for offer

    receipt = teller.checks_out_articles_from(cart)

    assert len(receipt.discounts) == 0
    assert receipt.total_price() == pytest.approx(4.00, 0.01)


def test_receipt_printer_basic_output():
    catalog, toothbrush, apples, *_ = create_catalog_with_products()
    teller = Teller(catalog)
    printer = ReceiptPrinter()

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 1)
    cart.add_item_quantity(apples, 1.5)

    receipt = teller.checks_out_articles_from(cart)
    output = printer.print_receipt(receipt)

    assert "toothbrush" in output
    assert "apples" in output
    assert "Total:" in output
    assert "1.5" in output or "1.500" in output  # Quantity line
