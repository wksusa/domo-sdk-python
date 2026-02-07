"""Tests for AsyncDataSetClient using respx to mock httpx requests."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from domo_sdk.async_clients.datasets import AsyncDataSetClient
from domo_sdk.transport.async_transport import AsyncTransport
from domo_sdk.transport.auth import DeveloperTokenCredentials, DeveloperTokenStrategy


def _make_async_client() -> tuple[AsyncDataSetClient, str]:
    """Create an AsyncDataSetClient backed by a real AsyncTransport with DeveloperTokenStrategy."""
    creds = DeveloperTokenCredentials(token="test-token", instance_domain="test.domo.com")
    strategy = DeveloperTokenStrategy(credentials=creds)
    transport = AsyncTransport(auth=strategy)
    client = AsyncDataSetClient(transport)
    base_url = strategy.get_base_url()
    return client, base_url


@pytest.mark.asyncio
class TestAsyncDataSetClient:
    """Async dataset client tests using respx."""

    @respx.mock
    async def test_async_get_dataset(self) -> None:
        """GET /v1/datasets/{id} returns dataset dict."""
        client, base_url = _make_async_client()

        route = respx.get(f"{base_url}/v1/datasets/ds-123").mock(
            return_value=Response(200, json={"id": "ds-123", "name": "Sales"})
        )

        result = await client.get("ds-123")

        assert route.called
        assert result["id"] == "ds-123"
        assert result["name"] == "Sales"

        await client.transport.close()

    @respx.mock
    async def test_async_query_dataset(self) -> None:
        """POST /v1/datasets/query/execute/{id} executes SQL."""
        client, base_url = _make_async_client()

        route = respx.post(f"{base_url}/v1/datasets/query/execute/ds-123").mock(
            return_value=Response(200, json={
                "columns": ["name", "revenue"],
                "rows": [["Alice", "1000"]],
                "numRows": 1,
                "numColumns": 2,
            })
        )

        result = await client.query("ds-123", "SELECT name, revenue FROM sales")

        assert route.called
        assert result["numRows"] == 1
        assert result["columns"] == ["name", "revenue"]

        await client.transport.close()

    @respx.mock
    async def test_async_list_datasets(self) -> None:
        """Pagination through datasets."""
        client, base_url = _make_async_client()

        # First call returns 2 datasets, second returns empty list (stops pagination)
        respx.get(f"{base_url}/v1/datasets").mock(
            side_effect=[
                Response(200, json=[{"id": "ds-1"}, {"id": "ds-2"}]),
                Response(200, json=[]),
            ]
        )

        result = await client.list(per_page=2)

        assert len(result) == 2
        assert result[0]["id"] == "ds-1"
        assert result[1]["id"] == "ds-2"

        await client.transport.close()

    @respx.mock
    async def test_async_get_dataset_with_headers(self) -> None:
        """Verify that developer token header is sent."""
        client, base_url = _make_async_client()

        route = respx.get(f"{base_url}/v1/datasets/ds-abc").mock(
            return_value=Response(200, json={"id": "ds-abc", "name": "Test"})
        )

        await client.get("ds-abc")

        assert route.called
        request = route.calls[0].request
        assert request.headers["x-domo-developer-token"] == "test-token"

        await client.transport.close()
