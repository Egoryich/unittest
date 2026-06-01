import unittest

from app.service import normalize_product


class TestNormalizeProduct(unittest.TestCase):
    def test_normalizes_product_payload_without_mocks(self):
        payload = {"id": "10", "name": "  Keyboard  ", "price_cents": "1299", "available": 1}
        self.assertEqual(
            normalize_product(payload, "2026-05-13T00:00:00+00:00"),
            {
                "id": 10,
                "name": "Keyboard",
                "price_cents": 1299,
                "available": True,
                "fetched_at": "2026-05-13T00:00:00+00:00",
            },
        )

