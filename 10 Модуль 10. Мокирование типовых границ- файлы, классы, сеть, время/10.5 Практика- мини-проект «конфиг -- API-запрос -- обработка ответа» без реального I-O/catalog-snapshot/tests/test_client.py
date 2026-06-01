import unittest
from unittest.mock import Mock, patch

from app.client import CatalogClient, CatalogResponseError, CatalogTimeoutError, requests


class TestCatalogClient(unittest.TestCase):
    @patch("app.client.requests.get")
    def test_fetch_product_success(self, mocked_get):
        response = Mock()
        response.json.return_value = {"id": 1}
        mocked_get.return_value = response
        client = CatalogClient("https://api.example", "secret", 3)

        self.assertEqual(client.fetch_product(1), {"id": 1})

        mocked_get.assert_called_once_with(
            "https://api.example/products/1",
            headers={"Authorization": "Bearer secret"},
            timeout=3,
        )
        response.raise_for_status.assert_called_once_with()

    @patch("app.client.requests.get")
    def test_timeout_is_domain_error(self, mocked_get):
        mocked_get.side_effect = requests.Timeout()
        with self.assertRaises(CatalogTimeoutError):
            CatalogClient("https://api.example", "secret", 3).fetch_product(1)

    @patch("app.client.requests.get")
    def test_http_error_is_domain_error(self, mocked_get):
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("500")
        mocked_get.return_value = response
        with self.assertRaises(CatalogResponseError):
            CatalogClient("https://api.example", "secret", 3).fetch_product(1)

