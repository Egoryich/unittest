from datetime import datetime, timezone

from .client import CatalogClient
from .config import load_config


def normalize_product(payload: dict, fetched_at: str) -> dict:
    return {
        "id": int(payload["id"]),
        "name": str(payload["name"]).strip(),
        "price_cents": int(payload["price_cents"]),
        "available": bool(payload.get("available", False)),
        "fetched_at": fetched_at,
    }


def build_product_snapshot(config_path: str, product_id: int) -> dict:
    config = load_config(config_path)
    client = CatalogClient(
        base_url=config["base_url"],
        api_key=config["api_key"],
        timeout=config.get("timeout", 5),
    )
    payload = client.fetch_product(product_id)
    fetched_at = datetime.now(timezone.utc).isoformat()
    return normalize_product(payload, fetched_at)

