import unittest
from unittest.mock import patch

from app.service import build_product_snapshot


class TestBuildProductSnapshot(unittest.TestCase):
    @patch("app.service.datetime")
    @patch("app.service.CatalogClient", autospec=True)
    @patch("app.service.load_config")
    def test_orchestrates_config_client_time_and_normalization(self, mocked_config, MockClient, mocked_datetime):
        mocked_config.return_value = {"base_url": "https://api.example", "api_key": "secret", "timeout": 3}
        MockClient.return_value.fetch_product.return_value = {
            "id": "7",
            "name": "  Mouse  ",
            "price_cents": "999",
            "available": True,
        }
        mocked_datetime.now.return_value.isoformat.return_value = "2026-05-13T00:00:00+00:00"

        result = build_product_snapshot("config.json", 7)

        self.assertEqual(result["name"], "Mouse")
        self.assertEqual(result["fetched_at"], "2026-05-13T00:00:00+00:00")
        MockClient.assert_called_once_with(base_url="https://api.example", api_key="secret", timeout=3)
        MockClient.return_value.fetch_product.assert_called_once_with(7)

