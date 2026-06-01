import unittest
from unittest.mock import Mock, patch

from payment_router import charge_order, choose_payment_mode


class TestPaymentRouter(unittest.TestCase):
    def test_default_prod_mode_uses_gateway(self):
        sandbox = Mock()
        gateway = Mock()
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(choose_payment_mode(), "gateway")
            self.assertEqual(charge_order(100, sandbox, gateway), "gateway")
        gateway.charge.assert_called_once_with(100)
        sandbox.charge.assert_not_called()

    def test_test_env_uses_sandbox(self):
        sandbox = Mock()
        gateway = Mock()
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            self.assertEqual(charge_order(100, sandbox, gateway), "sandbox")
        sandbox.charge.assert_called_once_with(100)
        gateway.charge.assert_not_called()

    def test_dev_env_uses_sandbox(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "dev"}, clear=True):
            self.assertEqual(choose_payment_mode(), "sandbox")

    def test_dry_run_skips_clients_and_has_priority(self):
        sandbox = Mock()
        gateway = Mock()
        with patch.dict("os.environ", {"PAYMENT_ENV": "prod", "PAYMENT_DRY_RUN": "1"}, clear=True):
            self.assertEqual(charge_order(100, sandbox, gateway), "skipped")
        sandbox.charge.assert_not_called()
        gateway.charge.assert_not_called()

    def test_unsupported_env_raises_value_error(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "stage"}, clear=True):
            with self.assertRaisesRegex(ValueError, "unsupported payment env"):
                choose_payment_mode()

