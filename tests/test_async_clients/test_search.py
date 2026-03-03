"""Tests for AsyncSearchClient using respx to mock httpx requests."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from domo_sdk.async_clients.search import AsyncSearchClient
from domo_sdk.models.search import SearchResponse
from domo_sdk.transport.async_transport import AsyncTransport
from domo_sdk.transport.auth import (
    DeveloperTokenCredentials,
    DeveloperTokenStrategy,
    OAuthCredentials,
    OAuthStrategy,
)


def _make_async_client(
    auth_mode: str = "developer_token",
) -> tuple[AsyncSearchClient, str]:
    if auth_mode == "developer_token":
        creds = DeveloperTokenCredentials(
            token="test-token", instance_domain="test.domo.com"
        )
        strategy = DeveloperTokenStrategy(credentials=creds)
    else:
        creds = OAuthCredentials(
            client_id="test-id", client_secret="test-secret"
        )
        strategy = OAuthStrategy(credentials=creds)
    transport = AsyncTransport(auth=strategy)
    client = AsyncSearchClient(transport)
    base_url = strategy.get_base_url()
    return client, base_url


@pytest.mark.asyncio
class TestAsyncSearchClient:
    @respx.mock
    async def test_query(self) -> None:
        """POST /search/v1/query returns SearchResponse."""
        client, base_url = _make_async_client()
        route = respx.post(f"{base_url}/search/v1/query").mock(
            return_value=Response(
                200,
                json={
                    "dataSources": [{"id": "ds-1", "name": "Revenue"}],
                    "totalCount": 1,
                },
            )
        )

        query = {
            "query": "revenue",
            "count": 10,
            "entities": ["DATASET"],
        }
        result = await client.query(query)

        assert route.called
        assert isinstance(result, SearchResponse)
        assert result.total_count == 1
        assert len(result.data_sources) == 1
        await client.transport.close()

    @respx.mock
    async def test_search_datasets_dev_token(self) -> None:
        """Developer token mode uses POST /data/ui/v3/datasources/search."""
        client, base_url = _make_async_client(auth_mode="developer_token")
        respx.post(f"{base_url}/data/ui/v3/datasources/search").mock(
            return_value=Response(
                200,
                json={
                    "dataSources": [{"id": "ds-1", "name": "Sales"}],
                },
            )
        )

        results = await client.search_datasets("Sales", count=20, offset=0)

        assert results == [{"id": "ds-1", "name": "Sales"}]
        await client.transport.close()

    @respx.mock
    async def test_search_datasets_dev_token_empty(self) -> None:
        """Developer token mode handles empty response."""
        client, base_url = _make_async_client(auth_mode="developer_token")
        respx.post(f"{base_url}/data/ui/v3/datasources/search").mock(
            return_value=Response(200, json={"dataSources": []})
        )

        results = await client.search_datasets("nonexistent")

        assert results == []
        await client.transport.close()
