import asyncio
import unittest
from unittest.mock import AsyncMock, Mock, call, patch

from app.client import ApiResponseError, ApiTimeoutError, Response, UserClient


class TestUserClient(unittest.IsolatedAsyncioTestCase):
    async def test_success_returns_normalized_user_and_awaits_transport(self):
        transport = Mock()
        transport.send = AsyncMock(return_value=Response(200, {"id": 1, "name": " Alice "}))
        client = UserClient(transport)

        self.assertEqual(await client.get_user(1), {"id": 1, "name": "alice"})

        transport.send.assert_awaited_once_with("GET", "/users/1")

    async def test_retry_after_timeout(self):
        transport = Mock()
        transport.send = AsyncMock(side_effect=[TimeoutError(), Response(200, {"id": 2, "name": " Bob "})])
        client = UserClient(transport, retries=1, retry_delay=5)

        with patch("app.client.asyncio.sleep", return_value=None) as sleep:
            self.assertEqual(await client.get_user(2), {"id": 2, "name": "bob"})

        sleep.assert_awaited_once_with(5)
        transport.send.assert_has_awaits([call("GET", "/users/2"), call("GET", "/users/2")])

    async def test_retry_after_500(self):
        transport = Mock()
        transport.send = AsyncMock(side_effect=[Response(500, {}), Response(200, {"id": 3, "name": " Cara "})])
        client = UserClient(transport, retries=1, retry_delay=2)

        with patch("app.client.asyncio.sleep", return_value=None) as sleep:
            self.assertEqual(await client.get_user(3), {"id": 3, "name": "cara"})

        sleep.assert_awaited_once_with(2)

    async def test_timeout_after_attempts_are_exhausted(self):
        transport = Mock()
        transport.send = AsyncMock(side_effect=[TimeoutError(), TimeoutError()])
        client = UserClient(transport, retries=1)

        with patch("app.client.asyncio.sleep", return_value=None):
            with self.assertRaises(ApiTimeoutError):
                await client.get_user(4)

    async def test_404_is_not_retried_and_has_no_backoff(self):
        transport = Mock()
        transport.send = AsyncMock(return_value=Response(404, {}))
        client = UserClient(transport, retries=3)

        with patch("app.client.asyncio.sleep", return_value=None) as sleep:
            with self.assertRaises(ApiResponseError):
                await client.get_user(5)

        sleep.assert_not_awaited()
        transport.send.assert_awaited_once_with("GET", "/users/5")

    async def test_wait_for_receives_configured_timeout(self):
        transport = Mock()
        send_coro = AsyncMock(return_value=Response(200, {"id": 6, "name": " Dana "}))
        transport.send = send_coro
        client = UserClient(transport, timeout=7)

        async def immediate(awaitable, *, timeout):
            self.assertEqual(timeout, 7)
            return await awaitable

        with patch("app.client.asyncio.wait_for", side_effect=immediate) as wait_for:
            self.assertEqual(await client.get_user(6), {"id": 6, "name": "dana"})

        wait_for.assert_awaited_once()

