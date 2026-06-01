import unittest
from unittest.mock import Mock, create_autospec, patch

from order_service import Order, OrderRepo, OrderService, PaymentGateway


class TestOrderServiceAutospec(unittest.TestCase):
    @patch("order_service.AuditClient")
    def test_plain_mocks_can_be_configured_but_do_not_protect_contracts(self, MockAuditClient):
        repo = Mock()
        gateway = Mock()
        repo.get.return_value = Order(10, 1500)
        gateway.charge.return_value = "tx-10"
        service = OrderService(repo, gateway, audit_endpoint="https://audit", audit_token="secret")

        self.assertEqual(service.pay(10), "tx-10")

        MockAuditClient.return_value.write.assert_called_once()

    @patch("order_service.AuditClient", autospec=True)
    def test_strict_doubles_lock_down_final_contract(self, MockAuditClient):
        repo = create_autospec(OrderRepo, instance=True)
        gateway = create_autospec(PaymentGateway, instance=True)
        repo.get.return_value = Order(10, 1500)
        gateway.charge.return_value = "tx-10"
        service = OrderService(repo, gateway, audit_endpoint="https://audit", audit_token="secret")

        self.assertEqual(service.pay(10), "tx-10")

        repo.get.assert_called_once_with(10)
        gateway.charge.assert_called_once_with(1500, currency="RUB")
        MockAuditClient.assert_called_once_with(endpoint="https://audit", token="secret")
        MockAuditClient.return_value.write.assert_called_once_with(
            "order_paid",
            {"order_id": 10, "amount": 1500, "transaction_id": "tx-10"},
        )

