"""Connectors client for the Domo API."""

from __future__ import annotations

from domo_sdk.clients.base import DomoAPIClient


class ConnectorsClient(DomoAPIClient):
    """Run Domo connector executions.

    Docs: https://developer.domo.com/docs/connectors-api-reference/connectors
    """

    def run(self, stream_id: int) -> dict:
        """Trigger an execution for a connector stream."""
        return self._create(f"/data/v1/streams/{stream_id}/executions", None)
