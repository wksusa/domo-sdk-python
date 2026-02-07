"""Async Files client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/files"


class AsyncFilesClient(AsyncDomoAPIClient):
    """Manage Domo file uploads and downloads asynchronously."""

    async def upload(self, file_data: bytes, name: str, **kwargs: Any) -> dict:
        """Upload a new file.

        Parameters
        ----------
        file_data:
            The raw file content as bytes.
        name:
            The file name.
        """
        body: dict[str, Any] = {"name": name, **kwargs}
        # Use POST with the file metadata; actual upload may vary by endpoint
        return await self._create(URL_BASE, body)

    async def update(self, file_id: str, **kwargs: Any) -> dict:
        """Update file metadata.

        Parameters
        ----------
        file_id:
            The ID of the file to update.
        """
        return await self._update(f"{URL_BASE}/{file_id}", kwargs)

    async def get_details(self, file_id: str) -> dict:
        """Get file details.

        Parameters
        ----------
        file_id:
            The ID of the file.
        """
        return await self._get(f"{URL_BASE}/{file_id}")

    async def download(self, file_id: str) -> str:
        """Download file contents.

        Parameters
        ----------
        file_id:
            The ID of the file to download.

        Returns the file content as a string (CSV-compatible endpoint).
        """
        url = f"{URL_BASE}/{file_id}/content"
        return await self._download_csv(url, include_header=True)

    async def set_permissions(self, file_id: str, permissions: list) -> None:
        """Set permissions for a file.

        Parameters
        ----------
        file_id:
            The ID of the file.
        permissions:
            List of permission entries.
        """
        url = f"{URL_BASE}/{file_id}/permissions"
        await self._update(url, permissions)
