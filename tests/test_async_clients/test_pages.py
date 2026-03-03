"""Tests for AsyncPageClient using respx to mock httpx requests."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from domo_sdk.async_clients.pages import AsyncPageClient
from domo_sdk.models.pages import Page, PageCollection
from domo_sdk.transport.async_transport import AsyncTransport
from domo_sdk.transport.auth import (
    DeveloperTokenCredentials,
    DeveloperTokenStrategy,
)


def _make_async_client() -> tuple[AsyncPageClient, str]:
    creds = DeveloperTokenCredentials(
        token="test-token", instance_domain="test.domo.com"
    )
    strategy = DeveloperTokenStrategy(credentials=creds)
    transport = AsyncTransport(auth=strategy)
    client = AsyncPageClient(transport)
    base_url = strategy.get_base_url()
    return client, base_url


@pytest.mark.asyncio
class TestAsyncPageCRUD:
    @respx.mock
    async def test_create(self) -> None:
        client, base_url = _make_async_client()
        route = respx.post(f"{base_url}/v1/pages").mock(
            return_value=Response(200, json={"id": 1, "name": "Dashboard"})
        )

        result = await client.create("Dashboard")

        assert route.called
        assert isinstance(result, Page)
        assert result.name == "Dashboard"
        await client.transport.close()

    @respx.mock
    async def test_get(self) -> None:
        client, base_url = _make_async_client()
        route = respx.get(f"{base_url}/v1/pages/1").mock(
            return_value=Response(200, json={"id": 1, "name": "Sales"})
        )

        result = await client.get(1)

        assert route.called
        assert isinstance(result, Page)
        assert result.id == 1
        await client.transport.close()

    @respx.mock
    async def test_list(self) -> None:
        client, base_url = _make_async_client()
        respx.get(f"{base_url}/v1/pages").mock(
            return_value=Response(
                200,
                json=[
                    {"id": 1, "name": "A"},
                    {"id": 2, "name": "B"},
                ],
            )
        )

        result = await client.list()

        assert len(result) == 2
        assert all(isinstance(p, Page) for p in result)
        await client.transport.close()

    @respx.mock
    async def test_update(self) -> None:
        client, base_url = _make_async_client()
        route = respx.put(f"{base_url}/v1/pages/1").mock(
            return_value=Response(200, json={"id": 1, "name": "Updated"})
        )

        result = await client.update(1, name="Updated")

        assert route.called
        assert isinstance(result, Page)
        assert result.name == "Updated"
        await client.transport.close()

    @respx.mock
    async def test_delete(self) -> None:
        client, base_url = _make_async_client()
        route = respx.delete(f"{base_url}/v1/pages/1").mock(
            return_value=Response(204)
        )

        await client.delete(1)

        assert route.called
        await client.transport.close()


@pytest.mark.asyncio
class TestAsyncPageCollections:
    @respx.mock
    async def test_get_collections(self) -> None:
        client, base_url = _make_async_client()
        respx.get(f"{base_url}/v1/pages/1/collections").mock(
            return_value=Response(
                200,
                json=[
                    {"id": 10, "title": "KPIs"},
                    {"id": 11, "title": "Charts"},
                ],
            )
        )

        result = await client.get_collections(1)

        assert len(result) == 2
        assert all(isinstance(c, PageCollection) for c in result)
        assert result[0].title == "KPIs"
        await client.transport.close()

    @respx.mock
    async def test_create_collection(self) -> None:
        client, base_url = _make_async_client()
        route = respx.post(f"{base_url}/v1/pages/1/collections").mock(
            return_value=Response(200, json={"id": 10, "title": "New"})
        )

        result = await client.create_collection(1, "New")

        assert route.called
        assert isinstance(result, PageCollection)
        assert result.title == "New"
        await client.transport.close()

    @respx.mock
    async def test_update_collection(self) -> None:
        client, base_url = _make_async_client()
        route = respx.put(
            f"{base_url}/v1/pages/1/collections/10"
        ).mock(
            return_value=Response(200, json={"id": 10, "title": "Updated"})
        )

        result = await client.update_collection(1, 10, title="Updated")

        assert route.called
        assert isinstance(result, PageCollection)
        await client.transport.close()

    @respx.mock
    async def test_delete_collection(self) -> None:
        client, base_url = _make_async_client()
        route = respx.delete(
            f"{base_url}/v1/pages/1/collections/10"
        ).mock(return_value=Response(204))

        await client.delete_collection(1, 10)

        assert route.called
        await client.transport.close()
