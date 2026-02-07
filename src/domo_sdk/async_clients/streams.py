"""Async Stream client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/streams"


class AsyncStreamClient(AsyncDomoAPIClient):
    """Manage Domo Streams asynchronously.

    Use Streams for data sources that are massive, constantly changing,
    or rapidly growing.  For simpler cases, use DataSets instead.

    Docs: https://developer.domo.com/docs/streams-api-reference/streams
    """

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    async def create(self, stream_request: dict) -> dict:
        """Create a new Stream."""
        return await self._create(URL_BASE, stream_request)

    async def get(self, stream_id: int) -> dict:
        """Retrieve a single Stream by ID."""
        return await self._get(f"{URL_BASE}/{stream_id}")

    async def list(
        self,
        per_page: int = 50,
        offset: int = 0,
        limit: int = 0,
    ) -> list[dict]:
        """Return a full list of Streams, paginating internally."""
        if per_page not in range(1, 51):
            raise ValueError("per_page must be between 1 and 50 (inclusive)")

        if limit:
            per_page = min(per_page, limit)

        params: dict[str, Any] = {"limit": per_page, "offset": offset}
        result: list[dict] = []
        streams: list[dict] = await self._list(URL_BASE, params=params)

        while streams:
            for stream in streams:
                result.append(stream)
                if limit and len(result) >= limit:
                    return result

            params["offset"] += per_page
            if limit and params["offset"] + per_page > limit:
                params["limit"] = limit - params["offset"]
            streams = await self._list(URL_BASE, params=params)

        return result

    async def update(self, stream_id: int, stream_update: dict) -> dict:
        """Update an existing Stream."""
        return await self._update(f"{URL_BASE}/{stream_id}", stream_update)

    async def delete(self, stream_id: int) -> None:
        """Delete a Stream."""
        await self._delete(f"{URL_BASE}/{stream_id}")

    # ------------------------------------------------------------------
    # Executions
    # ------------------------------------------------------------------

    async def create_execution(self, stream_id: int) -> dict:
        """Create a new execution for a Stream."""
        url = f"{URL_BASE}/{stream_id}/executions"
        return await self._create(url, {})

    async def list_executions(
        self,
        stream_id: int,
        per_page: int = 50,
        offset: int = 0,
    ) -> list:
        """List executions for a Stream."""
        url = f"{URL_BASE}/{stream_id}/executions"
        params: dict[str, Any] = {"limit": per_page, "offset": offset}
        return await self._list(url, params=params)

    async def upload_part(
        self,
        stream_id: int,
        execution_id: int,
        part_num: int,
        csv_data: str,
    ) -> None:
        """Upload a data part for a Stream execution."""
        url = f"{URL_BASE}/{stream_id}/executions/{execution_id}/part/{part_num}"
        await self._upload_csv(url, csv_data.encode("utf-8"))

    async def commit_execution(self, stream_id: int, execution_id: int) -> dict:
        """Commit (finalize) a Stream execution."""
        url = f"{URL_BASE}/{stream_id}/executions/{execution_id}/commit"
        return await self._update(url, {})

    async def abort_execution(self, stream_id: int, execution_id: int) -> None:
        """Abort a Stream execution."""
        url = f"{URL_BASE}/{stream_id}/executions/{execution_id}/abort"
        await self._update(url, {})
