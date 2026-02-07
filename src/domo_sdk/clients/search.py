"""Search client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.clients.base import DomoAPIClient


class SearchClient(DomoAPIClient):
    """Search across Domo objects.

    The available endpoints differ depending on authentication mode:
    - **developer_token**: access to internal UI search endpoints
    - **oauth**: limited to public API dataset listing with client-side filtering
    """

    def query(self, search_query: dict) -> dict:
        """Execute a raw search query (developer token only).

        POST /search/v1/query
        """
        return self._create("/search/v1/query", search_query)

    def search_datasets(
        self,
        query: str,
        count: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        """Search for datasets by name.

        Automatically selects the correct strategy based on the
        transport's authentication mode:

        - **developer_token**: uses the internal datasource search
          endpoint (``POST /data/ui/v3/datasources/search``).
        - **oauth**: falls back to listing datasets via ``GET /v1/datasets``
          and filtering client-side by name.
        """
        auth_mode: str = self.transport.auth_mode

        if auth_mode == "developer_token":
            return self._search_datasets_dev_token(query, count, offset)
        return self._search_datasets_oauth(query, count, offset)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _search_datasets_dev_token(
        self,
        query: str,
        count: int,
        offset: int,
    ) -> list[dict]:
        """Internal datasource search using developer token."""
        payload: dict[str, Any] = {
            "entities": ["DATASET"],
            "filters": [{"field": "name_sort", "filterType": "wildcard", "query": f"*{query}*"}],
            "combineResults": True,
            "query": query,
            "count": count,
            "offset": offset,
        }
        result = self._create("/data/ui/v3/datasources/search", payload)
        if isinstance(result, dict):
            return result.get("dataSources", [])
        return result if isinstance(result, list) else []

    def _search_datasets_oauth(
        self,
        query: str,
        count: int,
        offset: int,
    ) -> list[dict]:
        """Fallback dataset search using the public API with client-side filtering."""
        params: dict[str, Any] = {
            "limit": count,
            "offset": offset,
            "nameLike": query,
        }
        result = self._list("/v1/datasets", params=params)
        if isinstance(result, list):
            return result
        return []
