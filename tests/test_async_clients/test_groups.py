"""Tests for AsyncGroupClient using respx to mock httpx requests."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from domo_sdk.async_clients.groups import AsyncGroupClient
from domo_sdk.models.groups import Group
from domo_sdk.transport.async_transport import AsyncTransport
from domo_sdk.transport.auth import (
    DeveloperTokenCredentials,
    DeveloperTokenStrategy,
)


def _make_async_client() -> tuple[AsyncGroupClient, str]:
    creds = DeveloperTokenCredentials(
        token="test-token", instance_domain="test.domo.com"
    )
    strategy = DeveloperTokenStrategy(credentials=creds)
    transport = AsyncTransport(auth=strategy)
    client = AsyncGroupClient(transport)
    base_url = strategy.get_base_url()
    return client, base_url


@pytest.mark.asyncio
class TestAsyncGroupCRUD:
    @respx.mock
    async def test_create(self) -> None:
        client, base_url = _make_async_client()
        route = respx.post(f"{base_url}/v1/groups").mock(
            return_value=Response(200, json={"id": 1, "name": "Admins"})
        )

        result = await client.create({"name": "Admins"})

        assert route.called
        assert isinstance(result, Group)
        assert result.name == "Admins"
        await client.transport.close()

    @respx.mock
    async def test_get(self) -> None:
        client, base_url = _make_async_client()
        route = respx.get(f"{base_url}/v1/groups/1").mock(
            return_value=Response(200, json={"id": 1, "name": "Sales"})
        )

        result = await client.get(1)

        assert route.called
        assert isinstance(result, Group)
        assert result.id == 1
        await client.transport.close()

    @respx.mock
    async def test_list(self) -> None:
        client, base_url = _make_async_client()
        respx.get(f"{base_url}/v1/groups").mock(
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

        result = await client.list()

        assert len(result) == 2
        assert all(isinstance(g, Group) for g in result)
        await client.transport.close()

    @respx.mock
    async def test_update(self) -> None:
        client, base_url = _make_async_client()
        route = respx.put(f"{base_url}/v1/groups/1").mock(
            return_value=Response(200, json={"id": 1, "name": "Updated"})
        )

        result = await client.update(1, {"name": "Updated"})

        assert route.called
        assert isinstance(result, Group)
        assert result.name == "Updated"
        await client.transport.close()

    @respx.mock
    async def test_delete(self) -> None:
        client, base_url = _make_async_client()
        route = respx.delete(f"{base_url}/v1/groups/1").mock(
            return_value=Response(204)
        )

        await client.delete(1)

        assert route.called
        await client.transport.close()


@pytest.mark.asyncio
class TestAsyncGroupUsers:
    @respx.mock
    async def test_add_user(self) -> None:
        client, base_url = _make_async_client()
        route = respx.put(f"{base_url}/v1/groups/1/users/42").mock(
            return_value=Response(204)
        )

        await client.add_user(1, 42)

        assert route.called
        await client.transport.close()

    @respx.mock
    async def test_remove_user(self) -> None:
        client, base_url = _make_async_client()
        route = respx.delete(f"{base_url}/v1/groups/1/users/42").mock(
            return_value=Response(204)
        )

        await client.remove_user(1, 42)

        assert route.called
        await client.transport.close()

    @respx.mock
    async def test_list_users(self) -> None:
        client, base_url = _make_async_client()
        respx.get(f"{base_url}/v1/groups/1/users").mock(
            return_value=Response(200, json=[42, 99, 101])
        )

        result = await client.list_users(1)

        assert result == [42, 99, 101]
        await client.transport.close()
