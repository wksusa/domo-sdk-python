"""Async DataSet client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/datasets"


class AsyncDataSetClient(AsyncDomoAPIClient):
    """Manage Domo DataSets asynchronously.

    Use DataSets for fairly static data sources that only require
    occasional updates via data replacement.  Use Streams if your
    data source is massive, constantly changing, or rapidly growing.

    Docs: https://developer.domo.com/docs/data-apis/data
    """

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    async def create(self, dataset_request: dict) -> dict:
        """Create a new DataSet."""
        return await self._create(URL_BASE, dataset_request)

    async def get(self, dataset_id: str) -> dict:
        """Retrieve a single DataSet by ID."""
        url = f"{URL_BASE}/{dataset_id}"
        return await self._get(url)

    async def list(
        self,
        sort: str | None = None,
        per_page: int = 50,
        offset: int = 0,
        limit: int = 0,
        name_like: str = "",
    ) -> list[dict]:
        """Return a full list of DataSets, paginating internally.

        The Domo API enforces a max of 50 results per page; *per_page*
        is clamped accordingly.  If *limit* is non-zero, stops after
        that many items.
        """
        if per_page not in range(1, 51):
            raise ValueError("per_page must be between 1 and 50 (inclusive)")

        if limit:
            per_page = min(per_page, limit)

        params: dict[str, Any] = {
            "limit": per_page,
            "offset": offset,
            "nameLike": name_like,
        }
        if sort is not None:
            params["sort"] = sort

        result: list[dict] = []
        datasets: list[dict] = await self._list(URL_BASE, params=params)

        while datasets:
            for dataset in datasets:
                result.append(dataset)
                if limit and len(result) >= limit:
                    return result

            params["offset"] += per_page
            if limit and params["offset"] + per_page > limit:
                params["limit"] = limit - params["offset"]
            datasets = await self._list(URL_BASE, params=params)

        return result

    async def update(self, dataset_id: str, dataset_update: dict) -> dict:
        """Update an existing DataSet."""
        url = f"{URL_BASE}/{dataset_id}"
        return await self._update(url, dataset_update)

    async def delete(self, dataset_id: str) -> None:
        """Delete a DataSet."""
        url = f"{URL_BASE}/{dataset_id}"
        await self._delete(url)

    # ------------------------------------------------------------------
    # Data import / export
    # ------------------------------------------------------------------

    async def data_import(
        self,
        dataset_id: str,
        csv_data: str,
        update_method: str = "REPLACE",
    ) -> None:
        """Import data from a CSV string."""
        url = f"{URL_BASE}/{dataset_id}/data?updateMethod={update_method}"
        await self._upload_csv(url, csv_data.encode("utf-8"))

    async def data_export(
        self,
        dataset_id: str,
        include_csv_header: bool = True,
    ) -> str:
        """Export DataSet data as a CSV string."""
        url = f"{URL_BASE}/{dataset_id}/data"
        return await self._download_csv(url, include_header=include_csv_header)

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    async def query(self, dataset_id: str, sql: str) -> dict:
        """Execute a SQL query against a DataSet."""
        url = f"{URL_BASE}/query/execute/{dataset_id}"
        return await self._create(url, {"sql": sql})

    # ------------------------------------------------------------------
    # Schema & metadata (internal/v2/v3 APIs)
    # ------------------------------------------------------------------

    async def get_schema(self, dataset_id: str) -> dict:
        """Get the latest schema for a DataSet.

        GET /data/v2/datasources/{id}/schemas/latest
        """
        url = f"/data/v2/datasources/{dataset_id}/schemas/latest"
        return await self._get(url)

    async def get_metadata(self, dataset_id: str) -> dict:
        """Get core metadata for a DataSet.

        GET /data/v3/datasources/{id}?part=core
        """
        url = f"/data/v3/datasources/{dataset_id}"
        return await self._get(url, params={"part": "core"})

    async def alter_schema(self, dataset_id: str, schema: dict) -> dict:
        """Create or alter the schema for a DataSet."""
        url = f"/data/v2/datasources/{dataset_id}/schemas"
        return await self._create(url, schema)

    # ------------------------------------------------------------------
    # Permissions
    # ------------------------------------------------------------------

    async def get_permissions(self, dataset_id: str) -> list:
        """Get permissions for a DataSet."""
        url = f"/data/v3/datasources/{dataset_id}/permissions"
        return await self._get(url)

    async def set_permissions(self, dataset_id: str, permissions: list) -> None:
        """Set (replace) permissions for a DataSet."""
        url = f"/data/v3/datasources/{dataset_id}/permissions"
        await self._update(url, permissions)

    # ------------------------------------------------------------------
    # Versions & indexes
    # ------------------------------------------------------------------

    async def list_versions(self, dataset_id: str) -> list:
        """List data version details for a DataSet."""
        url = f"/data/v3/datasources/{dataset_id}/dataversions/details"
        return await self._get(url)

    async def create_index(self, dataset_id: str, columns: list[str]) -> dict:
        """Create an index on the specified columns."""
        url = f"/data/v3/datasources/{dataset_id}/indexes"
        return await self._create(url, columns)

    # ------------------------------------------------------------------
    # PDP (Personalized Data Policies)
    # ------------------------------------------------------------------

    async def create_pdp(self, dataset_id: str, pdp_request: dict) -> dict:
        """Create a Personalized Data Policy."""
        url = f"{URL_BASE}/{dataset_id}/policies"
        return await self._create(url, pdp_request)

    async def get_pdp(self, dataset_id: str, policy_id: int) -> dict:
        """Get a specific PDP for a DataSet."""
        url = f"{URL_BASE}/{dataset_id}/policies/{policy_id}"
        return await self._get(url)

    async def list_pdps(self, dataset_id: str) -> list:
        """List all PDPs for a DataSet."""
        url = f"{URL_BASE}/{dataset_id}/policies"
        return await self._list(url)

    async def update_pdp(
        self,
        dataset_id: str,
        policy_id: int,
        policy_update: dict,
    ) -> dict:
        """Update a specific PDP for a DataSet."""
        url = f"{URL_BASE}/{dataset_id}/policies/{policy_id}"
        return await self._update(url, policy_update)

    async def delete_pdp(self, dataset_id: str, policy_id: int) -> None:
        """Delete a specific PDP for a DataSet."""
        url = f"{URL_BASE}/{dataset_id}/policies/{policy_id}"
        await self._delete(url)
