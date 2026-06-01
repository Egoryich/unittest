import unittest
from unittest.mock import mock_open, patch

from app.config import load_config


class TestLoadConfig(unittest.TestCase):
    def test_reads_json_config_with_mock_open(self):
        data = '{"base_url": "https://api.example", "api_key": "secret", "timeout": 2}'
        with patch("app.config.open", mock_open(read_data=data)) as mocked_open:
            self.assertEqual(load_config("config.json")["timeout"], 2)
        mocked_open.assert_called_once_with("config.json", encoding="utf-8")

