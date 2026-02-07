"""Dataflows client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/v1/dataflows"


class DataflowsClient(DomoAPIClient):
    """Manage Domo dataflows (ETL/Magic ETL).

    Docs: https://developer.domo.com/docs/dataflows-api-reference/dataflows
    """

    def list(self, per_page: int = 50, offset: int = 0) -> list:
        """List dataflows."""
        params: dict[str, Any] = {"limit": per_page, "offset": offset}
        return self._list(URL_BASE, params=params)

    def get(self, dataflow_id: int) -> dict:
        """Retrieve a single dataflow by ID."""
        return self._get(f"{URL_BASE}/{dataflow_id}")

    def execute(self, dataflow_id: int) -> dict:
        """Execute a dataflow."""
        return self._create(f"{URL_BASE}/{dataflow_id}/executions", None)

    def get_execution(self, dataflow_id: int, execution_id: int) -> dict:
        """Retrieve a specific execution for a dataflow."""
        return self._get(f"{URL_BASE}/{dataflow_id}/executions/{execution_id}")
