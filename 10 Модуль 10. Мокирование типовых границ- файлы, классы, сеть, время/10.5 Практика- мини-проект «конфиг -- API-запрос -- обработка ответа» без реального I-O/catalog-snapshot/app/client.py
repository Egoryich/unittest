try:
    import requests
except ImportError:  # pragma: no cover
    class _RequestsFallback:
        class Timeout(Exception):
            pass

        class HTTPError(Exception):
            pass

        def get(self, *args, **kwargs):
            raise RuntimeError("requests is not installed")

    requests = _RequestsFallback()


class CatalogTimeoutError(RuntimeError):
    pass


class CatalogResponseError(RuntimeError):
    pass


class CatalogClient:
    def __init__(self, base_url: str, api_key: str, timeout: float):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def fetch_product(self, product_id: int) -> dict:
        url = f"{self.base_url}/products/{product_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.Timeout as exc:
            raise CatalogTimeoutError("catalog request timed out") from exc
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise CatalogResponseError("catalog request failed") from exc
        return response.json()

