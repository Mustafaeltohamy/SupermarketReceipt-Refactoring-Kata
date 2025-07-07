import pytest

from model_objects import Product, ProductUnit, SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from receipt_printer import ReceiptPrinter


# Helper to setup reusable test data
def setup_test_environment():
    catalog = FakeCatalog()
    banana = Product("banana", ProductUnit.KILO)
    apple = Product("apple", ProductUnit.KILO)
    gum = Product("chewing gum", ProductUnit.EACH)
    watermelon = Product("extra large watermelon from mexico", ProductUnit.EACH)

    catalog.add_product(banana, 1.10)
    catalog.add_product(apple, 2.50)
    catalog.add_product(gum, 0.30)
    catalog.add_product(watermelon, 7.99)

    return catalog, banana, apple, gum, watermelon


def test_three_for_two_exact_match():
    catalog, _, _, gum, _ = setup_test_environment()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, gum, 0)

    cart = ShoppingCart()
    cart.add_item_quantity(gum, 3)
    receipt = teller.checks_out_articles_from(cart)

    assert len(receipt.discounts) == 1
    assert receipt.total_price() == pytest.approx(0.60, 0.01)


def test_three_for_two_surplus():
    catalog, _, _, gum, _ = setup_test_environment()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, gum, 0)

    cart = ShoppingCart()
    cart.add_item_quantity(gum, 4)
    receipt = teller.checks_out_articles_from(cart)

    # Pay for 3: 2 for first 3, 1 full
    assert receipt.total_price() == pytest.approx(0.90, 0.01)


def test_two_for_amount_edge_quantity():
    catalog, _, apple, _, _ = setup_test_environment()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, apple, 3.00)

    cart = ShoppingCart()
    cart.add_item_quantity(apple, 3)
    receipt = teller.checks_out_articles_from(cart)

    # Two for 3.0, one at 2.5 => 5.5 total
    assert receipt.total_price() == pytest.approx(5.5, 0.01)


def test_five_for_amount_exact():
    catalog, banana, _, _, _ = setup_test_environment()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, banana, 4.50)

    cart = ShoppingCart()
    cart.add_item_quantity(banana, 5)
    receipt = teller.checks_out_articles_from(cart)

    assert len(receipt.discounts) == 1
    assert receipt.total_price() == pytest.approx(4.50, 0.01)


def test_five_for_amount_with_extra():
    catalog, banana, _, _, _ = setup_test_environment()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, banana, 4.50)

    cart = ShoppingCart()
    cart.add_item_quantity(banana, 6)  # 5 for 4.5, 1 at 1.1
    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(5.6, 0.01)


def test_ten_percent_discount_zero_percent():
    catalog, _, apple, _, _ = setup_test_environment()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apple, 0)

    cart = ShoppingCart()
    cart.add_item_quantity(apple, 1)
    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(2.5, 0.01)
    assert len(receipt.discounts) == 1  # Still applied, but zero


def test_ten_percent_discount_100_percent():
    catalog, _, apple, _, _ = setup_test_environment()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apple, 100)

    cart = ShoppingCart()
    cart.add_item_quantity(apple, 1)
    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(0.0, 0.01)
    assert len(receipt.discounts) == 1


def test_long_product_name_printing():
    catalog, _, _, _, watermelon = setup_test_environment()
    teller = Teller(catalog)

    cart = ShoppingCart()
    cart.add_item_quantity(watermelon, 1)

    receipt = teller.checks_out_articles_from(cart)
    printer = ReceiptPrinter()
    output = printer.print_receipt(receipt)

    # Assert truncated or formatted long names still produce a line
    assert "Total" in output
    assert "watermelon" in output.lower()


def test_empty_cart_total_zero():
    catalog, *_ = setup_test_environment()
    teller = Teller(catalog)
    cart = ShoppingCart()
    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == 0
    assert receipt.items == []


def test_quantity_less_than_required_offer():
    catalog, _, apple, _, _ = setup_test_environment()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, apple, 8.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apple, 4)  # Not enough to trigger 5-for-amount
    receipt = teller.checks_out_articles_from(cart)

    assert len(receipt.discounts) == 0
    assert receipt.total_price() == pytest.approx(10.0, 0.01)


def test_discount_never_positive():
    catalog, _, apple, _, _ = setup_test_environment()
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apple, 20)

    cart = ShoppingCart()
    cart.add_item_quantity(apple, 1)

    receipt = teller.checks_out_articles_from(cart)

    for d in receipt.discounts:
        assert d.discount_amount <= 0
