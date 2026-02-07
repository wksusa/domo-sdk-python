"""S3 export client for the Domo API."""

from __future__ import annotations

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/query/v1/export"


class S3ExportClient(DomoAPIClient):
    """Export Domo datasets to S3.

    Docs: https://developer.domo.com/docs/s3-export-api-reference/s3-export
    """

    def start_export(self, dataset_id: str, config: dict) -> dict:
        """Start an S3 export for a dataset."""
        return self._create(f"{URL_BASE}/{dataset_id}", config)

    def get_export_status(self, dataset_id: str) -> dict:
        """Get the export status for a dataset."""
        return self._get(f"{URL_BASE}/{dataset_id}")
