import unittest
from unittest.mock import Mock

from invoice_service import ChargeResult, Invoice, InvoiceService


class TestInvoiceService(unittest.TestCase):
    def setUp(self):
        self.repo = Mock()
        self.gateway = Mock()
        self.service = InvoiceService(self.repo, self.gateway)

    def test_successful_payment_marks_invoice_paid(self):
        self.repo.get_by_id.return_value = Invoice(1, "cust-1", 500, "new")
        self.gateway.charge.return_value = ChargeResult(True, transaction_id="tx-1")

        self.assertEqual(self.service.pay(1), "paid")

        self.gateway.charge.assert_called_once_with("cust-1", 500)
        self.repo.mark_paid.assert_called_once_with(1, "tx-1")

    def test_declined_payment_marks_invoice_failed(self):
        self.repo.get_by_id.return_value = Invoice(1, "cust-1", 500, "new")
        self.gateway.charge.return_value = ChargeResult(False, reason="declined")

        self.assertEqual(self.service.pay(1), "failed")

        self.repo.mark_failed.assert_called_once_with(1, "declined")

    def test_already_paid_invoice_does_not_call_gateway(self):
        self.repo.get_by_id.return_value = Invoice(1, "cust-1", 500, "paid")

        self.assertEqual(self.service.pay(1), "already_paid")

        self.gateway.charge.assert_not_called()

    def test_missing_invoice_raises_lookup_error(self):
        self.repo.get_by_id.return_value = None

        with self.assertRaisesRegex(LookupError, "invoice not found"):
            self.service.pay(404)

        self.gateway.charge.assert_not_called()

    def test_non_positive_amount_raises_value_error(self):
        self.repo.get_by_id.return_value = Invoice(1, "cust-1", 0, "new")

        with self.assertRaisesRegex(ValueError, "positive"):
            self.service.pay(1)

        self.gateway.charge.assert_not_called()

    def test_gateway_timeout_marks_retry(self):
        self.repo.get_by_id.return_value = Invoice(1, "cust-1", 500, "new")
        self.gateway.charge.side_effect = TimeoutError("gateway timeout")

        self.assertEqual(self.service.pay(1), "retry")

        self.repo.mark_retry.assert_called_once_with(1)

