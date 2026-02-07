"""Async Dataflows client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/dataflows"


class AsyncDataflowsClient(AsyncDomoAPIClient):
    """Manage Domo dataflows asynchronously.

    Docs: https://developer.domo.com/docs/dataflows-api-reference/dataflows
    """

    async def list(self, per_page: int = 50, offset: int = 0, limit: int = 0) -> list:
        """Return a full list of dataflows, paginating internally."""
        if per_page not in range(1, 51):
            raise ValueError("per_page must be between 1 and 50 (inclusive)")

        if limit:
            per_page = min(per_page, limit)

        params: dict[str, Any] = {"limit": per_page, "offset": offset}
        result: list[dict] = []
        dataflows: list[dict] = await self._list(URL_BASE, params=params)

        while dataflows:
            for dataflow in dataflows:
                result.append(dataflow)
                if limit and len(result) >= limit:
                    return result

            params["offset"] += per_page
            if limit and params["offset"] + per_page > limit:
                params["limit"] = limit - params["offset"]
            dataflows = await self._list(URL_BASE, params=params)

        return result

    async def get(self, dataflow_id: int) -> dict:
        """Retrieve a single dataflow by ID."""
        return await self._get(f"{URL_BASE}/{dataflow_id}")

    async def execute(self, dataflow_id: int) -> dict:
        """Start a dataflow execution."""
        url = f"{URL_BASE}/{dataflow_id}/executions"
        return await self._create(url, {})

    async def get_execution(self, dataflow_id: int, execution_id: int) -> dict:
        """Get the status of a dataflow execution."""
        url = f"{URL_BASE}/{dataflow_id}/executions/{execution_id}"
        return await self._get(url)
