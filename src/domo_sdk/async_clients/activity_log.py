"""Async Activity Log client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/audit"


class AsyncActivityLogClient(AsyncDomoAPIClient):
    """Query the Domo activity log asynchronously.

    Docs: https://developer.domo.com/docs/activity-log-api-reference/activity-log
    """

    async def query(
        self,
        start: int = 0,
        end: int = 0,
        limit: int = 50,
        offset: int = 0,
        user: int | None = None,
    ) -> list[dict]:
        """Query activity log entries.

        Parameters
        ----------
        start:
            Start time in epoch milliseconds.
        end:
            End time in epoch milliseconds.
        limit:
            Maximum number of entries to return.
        offset:
            Offset for pagination.
        user:
            Optional user ID to filter by.
        """
        params: dict[str, Any] = {
            "start": start,
            "end": end,
            "limit": limit,
            "offset": offset,
        }
        if user is not None:
            params["user"] = user

        return await self._list(URL_BASE, params=params)
