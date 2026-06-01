import unittest

from shop import final_price_cents


class TestPricingScenarios(unittest.TestCase):
    def test_cart_line_with_discount_and_tax(self):
        self.assertEqual(final_price_cents(2500, discount_percent=20, tax_percent=10), 2200)

    def test_free_item_stays_free(self):
        self.assertEqual(final_price_cents(0, discount_percent=0, tax_percent=20), 0)

    def test_no_discount_no_tax_keeps_base(self):
        self.assertEqual(final_price_cents(999, tax_percent=0), 999)

