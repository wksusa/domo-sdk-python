"""Tests for AsyncUserClient using respx to mock httpx requests."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from domo_sdk.async_clients.users import AsyncUserClient
from domo_sdk.models.users import User
from domo_sdk.transport.async_transport import AsyncTransport
from domo_sdk.transport.auth import (
    DeveloperTokenCredentials,
    DeveloperTokenStrategy,
)


def _make_async_client() -> tuple[AsyncUserClient, str]:
    creds = DeveloperTokenCredentials(
        token="test-token", instance_domain="test.domo.com"
    )
    strategy = DeveloperTokenStrategy(credentials=creds)
    transport = AsyncTransport(auth=strategy)
    client = AsyncUserClient(transport)
    base_url = strategy.get_base_url()
    return client, base_url


@pytest.mark.asyncio
class TestAsyncUserCRUD:
    @respx.mock
    async def test_create(self) -> None:
        client, base_url = _make_async_client()
        route = respx.post(f"{base_url}/v1/users").mock(
            return_value=Response(
                200,
                json={
                    "id": 1,
                    "name": "Alice",
                    "email": "alice@co.com",
                    "role": "Admin",
                },
            )
        )

        result = await client.create(
            {"name": "Alice", "email": "alice@co.com", "role": "Admin"}
        )

        assert route.called
        assert isinstance(result, User)
        assert result.name == "Alice"
        await client.transport.close()

    @respx.mock
    async def test_create_with_invite(self) -> None:
        client, base_url = _make_async_client()
        route = respx.post(f"{base_url}/v1/users").mock(
            return_value=Response(200, json={"id": 1, "name": "Bob"})
        )

        await client.create({"name": "Bob"}, send_invite=True)

        assert route.called
        await client.transport.close()

    @respx.mock
    async def test_get(self) -> None:
        client, base_url = _make_async_client()
        route = respx.get(f"{base_url}/v1/users/42").mock(
            return_value=Response(200, json={"id": 42, "name": "Alice"})
        )

        result = await client.get(42)

        assert route.called
        assert isinstance(result, User)
        assert result.id == 42
        await client.transport.close()

    @respx.mock
    async def test_list(self) -> None:
        client, base_url = _make_async_client()
        respx.get(f"{base_url}/v1/users").mock(
            side_effect=[
                Response(
                    200,
                    json=[
                        {"id": 1, "name": "A"},
                        {"id": 2, "name": "B"},
                    ],
                ),
                Response(200, json=[]),
            ]
        )

        result = await client.list(per_page=2)

        assert len(result) == 2
        assert all(isinstance(u, User) for u in result)
        await client.transport.close()

    @respx.mock
    async def test_update(self) -> None:
        client, base_url = _make_async_client()
        route = respx.put(f"{base_url}/v1/users/1").mock(
            return_value=Response(200, json={"id": 1, "name": "Updated"})
        )

        result = await client.update(1, {"name": "Updated"})

        assert route.called
        assert isinstance(result, User)
        assert result.name == "Updated"
        await client.transport.close()

    @respx.mock
    async def test_delete(self) -> None:
        client, base_url = _make_async_client()
        route = respx.delete(f"{base_url}/v1/users/1").mock(
            return_value=Response(204)
        )

        await client.delete(1)

        assert route.called
        await client.transport.close()
