"""DataSet client for the Domo API."""

from __future__ import annotations

import os
from collections.abc import Generator
from typing import Any

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/v1/datasets"


class DataSetClient(DomoAPIClient):
    """Manage Domo DataSets.

    Use DataSets for fairly static data sources that only require
    occasional updates via data replacement.  Use Streams if your
    data source is massive, constantly changing, or rapidly growing.

    Docs: https://developer.domo.com/docs/data-apis/data
    """

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def create(self, dataset_request: dict) -> dict:
        """Create a new DataSet."""
        return self._create(URL_BASE, dataset_request)

    def get(self, dataset_id: str) -> dict:
        """Retrieve a single DataSet by ID."""
        url = f"{URL_BASE}/{dataset_id}"
        return self._get(url)

    def list(
        self,
        sort: str | None = None,
        per_page: int = 50,
        offset: int = 0,
        limit: int = 0,
        name_like: str = "",
    ) -> Generator[dict, None, None]:
        """Paginating generator over DataSets.

        Yields individual DataSet dicts.  The Domo API enforces a max
        of 50 results per page; *per_page* is clamped accordingly.
        If *limit* is non-zero the generator stops after that many items.
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

        dataset_count = 0
        datasets: list[dict] = self._list(URL_BASE, params=params)

        while datasets:
            for dataset in datasets:
                yield dataset
                dataset_count += 1
                if limit and dataset_count >= limit:
                    return

            params["offset"] += per_page
            if limit and params["offset"] + per_page > limit:
                params["limit"] = limit - params["offset"]
            datasets = self._list(URL_BASE, params=params)

    def update(self, dataset_id: str, dataset_update: dict) -> dict:
        """Update an existing DataSet."""
        url = f"{URL_BASE}/{dataset_id}"
        return self._update(url, dataset_update)

    def delete(self, dataset_id: str) -> None:
        """Delete a DataSet."""
        url = f"{URL_BASE}/{dataset_id}"
        self._delete(url)

    # ------------------------------------------------------------------
    # Data import / export
    # ------------------------------------------------------------------

    def data_import(
        self,
        dataset_id: str,
        csv_data: str,
        update_method: str = "REPLACE",
    ) -> None:
        """Import data from a CSV string."""
        url = f"{URL_BASE}/{dataset_id}/data?updateMethod={update_method}"
        self._upload_csv(url, csv_data.encode("utf-8"))

    def data_import_from_file(
        self,
        dataset_id: str,
        filepath: str,
        update_method: str = "REPLACE",
    ) -> None:
        """Import data from a CSV file on disk."""
        with open(os.path.expanduser(filepath), "rb") as csvfile:
            url = f"{URL_BASE}/{dataset_id}/data?updateMethod={update_method}"
            self._upload_csv(url, csvfile.read())

    def data_export(
        self,
        dataset_id: str,
        include_csv_header: bool = True,
    ) -> str:
        """Export DataSet data as a CSV string."""
        url = f"{URL_BASE}/{dataset_id}/data"
        return self._download_csv(url, include_header=include_csv_header)

    def data_export_to_file(
        self,
        dataset_id: str,
        file_path: str,
        include_csv_header: bool = True,
    ) -> str:
        """Export DataSet data to a CSV file. Returns the file path."""
        csv_data = self.data_export(dataset_id, include_csv_header=include_csv_header)
        file_path = str(file_path)
        if not file_path.endswith(".csv"):
            file_path += ".csv"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(csv_data)
        return file_path

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def query(self, dataset_id: str, sql: str) -> dict:
        """Execute a SQL query against a DataSet."""
        url = f"{URL_BASE}/query/execute/{dataset_id}"
        return self._create(url, {"sql": sql})

    # ------------------------------------------------------------------
    # Schema & metadata (internal/v2/v3 APIs)
    # ------------------------------------------------------------------

    def get_schema(self, dataset_id: str) -> dict:
        """Get the latest schema for a DataSet."""
        url = f"/data/v2/datasources/{dataset_id}/schemas/latest"
        return self._get(url)

    def get_metadata(self, dataset_id: str) -> dict:
        """Get core metadata for a DataSet."""
        url = f"/data/v3/datasources/{dataset_id}"
        return self._get(url, params={"part": "core"})

    def alter_schema(self, dataset_id: str, schema: dict) -> dict:
        """Create or alter the schema for a DataSet."""
        url = f"/data/v2/datasources/{dataset_id}/schemas"
        return self._create(url, schema)

    # ------------------------------------------------------------------
    # Permissions
    # ------------------------------------------------------------------

    def get_permissions(self, dataset_id: str) -> list:
        """Get permissions for a DataSet."""
        url = f"/data/v3/datasources/{dataset_id}/permissions"
        return self._get(url)

    def set_permissions(self, dataset_id: str, permissions: list) -> None:
        """Set (replace) permissions for a DataSet."""
        url = f"/data/v3/datasources/{dataset_id}/permissions"
        self._update(url, permissions)

    # ------------------------------------------------------------------
    # Versions & indexes
    # ------------------------------------------------------------------

    def list_versions(self, dataset_id: str) -> list:
        """List data version details for a DataSet."""
        url = f"/data/v3/datasources/{dataset_id}/dataversions/details"
        return self._get(url)

    def create_index(self, dataset_id: str, columns: list[str]) -> dict:
        """Create an index on the specified columns."""
        url = f"/data/v3/datasources/{dataset_id}/indexes"
        return self._create(url, columns)

    # ------------------------------------------------------------------
    # PDP (Personalized Data Policies)
    # ------------------------------------------------------------------

    def create_pdp(self, dataset_id: str, pdp_request: dict) -> dict:
        """Create a Personalized Data Policy."""
        url = f"{URL_BASE}/{dataset_id}/policies"
        return self._create(url, pdp_request)

    def get_pdp(self, dataset_id: str, policy_id: int) -> dict:
        """Get a specific PDP for a DataSet."""
        url = f"{URL_BASE}/{dataset_id}/policies/{policy_id}"
        return self._get(url)

    def list_pdps(self, dataset_id: str) -> list:
        """List all PDPs for a DataSet."""
        url = f"{URL_BASE}/{dataset_id}/policies"
        return self._list(url)

    def update_pdp(
        self,
        dataset_id: str,
        policy_id: int,
        policy_update: dict,
    ) -> dict:
        """Update a specific PDP for a DataSet."""
        url = f"{URL_BASE}/{dataset_id}/policies/{policy_id}"
        return self._update(url, policy_update)

    def delete_pdp(self, dataset_id: str, policy_id: int) -> None:
        """Delete a specific PDP for a DataSet."""
        url = f"{URL_BASE}/{dataset_id}/policies/{policy_id}"
        self._delete(url)
