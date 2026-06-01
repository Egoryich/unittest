from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Protocol


@dataclass
class Response:
    status: int
    payload: dict


class ApiTimeoutError(RuntimeError):
    pass


class ApiResponseError(RuntimeError):
    pass


class AsyncTransport(Protocol):
    async def send(self, method: str, path: str) -> Response:
        ...


class UserClient:
    def __init__(self, transport: AsyncTransport, *, timeout: float = 1, retries: int = 0, retry_delay: float = 0.1):
        self._transport = transport
        self._timeout = timeout
        self._retries = retries
        self._retry_delay = retry_delay

    async def get_user(self, user_id: int) -> dict:
        path = f"/users/{user_id}"
        for attempt in range(self._retries + 1):
            try:
                response = await asyncio.wait_for(self._transport.send("GET", path), timeout=self._timeout)
            except TimeoutError as exc:
                if attempt >= self._retries:
                    raise ApiTimeoutError("user request timed out") from exc
                await asyncio.sleep(self._retry_delay)
                continue

            if response.status >= 500:
                if attempt >= self._retries:
                    raise ApiResponseError(f"server error: {response.status}")
                await asyncio.sleep(self._retry_delay)
                continue
            if response.status != 200:
                raise ApiResponseError(f"unexpected status: {response.status}")

            return {
                "id": response.payload["id"],
                "name": response.payload["name"].strip().lower(),
            }
        raise ApiTimeoutError("user request timed out")

