import unittest

from shop import final_price_cents


class TestFinalPriceCents(unittest.TestCase):
    def test_adds_default_tax_without_discount(self):
        self.assertEqual(final_price_cents(1000), 1200)

    def test_discount_reduces_base_before_tax(self):
        self.assertEqual(final_price_cents(1000, discount_percent=10), 1080)

    def test_zero_tax_returns_discounted_base(self):
        self.assertEqual(final_price_cents(1000, discount_percent=25, tax_percent=0), 750)

    def test_full_discount_returns_zero(self):
        self.assertEqual(final_price_cents(1000, discount_percent=100), 0)

    def test_invalid_types_raise_type_error(self):
        cases = [(None, 0, 20), (1000, "10", 20), (1000, 10, "20")]
        for args in cases:
            with self.subTest(args=args):
                with self.assertRaises(TypeError):
                    final_price_cents(*args)

    def test_invalid_negative_base_raises_value_error(self):
        with self.assertRaises(ValueError):
            final_price_cents(-1)

    def test_invalid_discount_percent_bounds_raise_value_error(self):
        for value in [-1, 101]:
            with self.subTest(discount=value):
                with self.assertRaises(ValueError):
                    final_price_cents(1000, discount_percent=value)

    def test_invalid_tax_percent_bounds_raise_value_error(self):
        for value in [-1, 101]:
            with self.subTest(tax=value):
                with self.assertRaises(ValueError):
                    final_price_cents(1000, tax_percent=value)

