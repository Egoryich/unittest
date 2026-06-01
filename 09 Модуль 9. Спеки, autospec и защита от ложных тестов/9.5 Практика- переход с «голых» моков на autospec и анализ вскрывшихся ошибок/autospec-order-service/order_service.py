from dataclasses import dataclass


@dataclass
class Order:
    id: int
    amount: int


class OrderRepo:
    def get(self, order_id: int) -> Order:
        raise NotImplementedError


class PaymentGateway:
    def charge(self, amount: int, currency: str = "RUB") -> str:
        raise NotImplementedError


class AuditClient:
    def __init__(self, endpoint: str, token: str) -> None:
        self.endpoint = endpoint
        self.token = token

    def write(self, event: str, payload: dict) -> None:
        raise NotImplementedError


class OrderService:
    def __init__(self, repo: OrderRepo, gateway: PaymentGateway, *, audit_endpoint: str, audit_token: str):
        self.repo = repo
        self.gateway = gateway
        self.audit_endpoint = audit_endpoint
        self.audit_token = audit_token

    def pay(self, order_id: int) -> str:
        order = self.repo.get(order_id)
        transaction_id = self.gateway.charge(order.amount, currency="RUB")
        audit = AuditClient(endpoint=self.audit_endpoint, token=self.audit_token)
        audit.write("order_paid", {"order_id": order.id, "amount": order.amount, "transaction_id": transaction_id})
        return transaction_id

