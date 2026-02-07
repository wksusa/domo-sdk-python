"""Tests for SearchClient with mocked transport."""
from __future__ import annotations

from unittest.mock import MagicMock

from domo_sdk.clients.search import SearchClient


def _make_client(auth_mode: str = "developer_token") -> tuple[SearchClient, MagicMock]:
    """Create a SearchClient with a fully mocked transport."""
    transport = MagicMock()
    transport.auth_mode = auth_mode
    client = SearchClient(transport)
    return client, transport


class TestSearchClient:
    """Tests for SearchClient operations."""

    def test_search_query(self) -> None:
        """POST /search/v1/query."""
        client, transport = _make_client()
        transport.post.return_value = {
            "dataSources": [{"id": "ds-1", "name": "Revenue"}],
            "totalCount": 1,
        }

        query = {
            "query": "revenue",
            "count": 10,
            "entities": ["DATASET"],
        }
        result = client.query(query)

        transport.post.assert_called_once_with(
            "/search/v1/query",
            body=query,
            params=None,
        )
        assert result["totalCount"] == 1

    def test_search_datasets_dev_token(self) -> None:
        """Developer token mode uses POST /data/ui/v3/datasources/search."""
        client, transport = _make_client(auth_mode="developer_token")
        transport.post.return_value = {
            "dataSources": [{"id": "ds-1", "name": "Sales"}],
        }

        results = client.search_datasets("Sales", count=20, offset=0)

        transport.post.assert_called_once()
        call_args = transport.post.call_args
        assert call_args[0][0] == "/data/ui/v3/datasources/search"
        body = call_args[1]["body"] if "body" in call_args[1] else call_args[0][1]
        assert body["query"] == "Sales"
        assert body["count"] == 20
        assert body["entities"] == ["DATASET"]
        assert results == [{"id": "ds-1", "name": "Sales"}]

    def test_search_datasets_oauth(self) -> None:
        """OAuth mode uses GET /v1/datasets with nameLike."""
        client, transport = _make_client(auth_mode="oauth")
        transport.get.return_value = [
            {"id": "ds-1", "name": "Sales Data"},
        ]

        results = client.search_datasets("Sales", count=25, offset=5)

        transport.get.assert_called_once()
        call_args = transport.get.call_args
        assert call_args[0][0] == "/v1/datasets"
        params = call_args[1].get("params") or call_args[0][1] if len(call_args[0]) > 1 else call_args[1]["params"]
        assert params["nameLike"] == "Sales"
        assert params["limit"] == 25
        assert params["offset"] == 5
        assert results == [{"id": "ds-1", "name": "Sales Data"}]

    def test_search_datasets_dev_token_empty_result(self) -> None:
        """Developer token mode handles empty response."""
        client, transport = _make_client(auth_mode="developer_token")
        transport.post.return_value = {"dataSources": []}

        results = client.search_datasets("nonexistent")
        assert results == []

    def test_search_datasets_oauth_empty_result(self) -> None:
        """OAuth mode handles empty list response."""
        client, transport = _make_client(auth_mode="oauth")
        transport.get.return_value = []

        results = client.search_datasets("nonexistent")
        assert results == []
