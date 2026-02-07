"""Async S3 Export client for the Domo API."""

from __future__ import annotations

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/datasets"


class AsyncS3ExportClient(AsyncDomoAPIClient):
    """Manage Domo dataset S3 exports asynchronously."""

    async def start_export(
        self,
        dataset_id: str,
        export_config: dict | None = None,
    ) -> dict:
        """Start an S3 export for a dataset.

        Parameters
        ----------
        dataset_id:
            The ID of the dataset to export.
        export_config:
            Optional export configuration (S3 bucket, path, format, etc.).
        """
        url = f"{URL_BASE}/{dataset_id}/exports"
        return await self._create(url, export_config or {})

    async def get_export_status(self, dataset_id: str, export_id: str) -> dict:
        """Get the status of an S3 export.

        Parameters
        ----------
        dataset_id:
            The ID of the dataset.
        export_id:
            The ID of the export job.
        """
        url = f"{URL_BASE}/{dataset_id}/exports/{export_id}"
        return await self._get(url)
