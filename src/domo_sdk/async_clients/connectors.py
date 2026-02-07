"""Async Connectors client for the Domo API."""

from __future__ import annotations

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/streams"


class AsyncConnectorsClient(AsyncDomoAPIClient):
    """Trigger Domo connector runs asynchronously.

    Uses the Streams API execution endpoint to initiate connector runs.
    """

    async def run(self, stream_id: int) -> dict:
        """Trigger a connector run via the Streams execution API.

        Creates a new execution for the given stream, which triggers the
        underlying connector to run.
        """
        url = f"{URL_BASE}/{stream_id}/executions"
        return await self._create(url, {})
