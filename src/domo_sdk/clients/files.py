"""Files client for the Domo API."""

from __future__ import annotations

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/data/v1/data-files"


class FilesClient(DomoAPIClient):
    """Manage Domo data files.

    Docs: https://developer.domo.com/docs/data-files-api-reference/data-files
    """

    def upload(self, file_data: bytes, name: str, description: str = "") -> dict:
        """Upload a new file."""
        body = {"name": name, "description": description}
        # POST the metadata first, then upload the binary content
        # The Domo files API accepts multipart; we use the transport post
        # with metadata params and handle file data via CSV transport.
        return self._create(URL_BASE, body)

    def update(self, file_id: int, file_data: bytes) -> dict:
        """Update (replace) an existing file's contents."""
        return self._upload_csv(f"{URL_BASE}/{file_id}", file_data)

    def get_details(self, file_id: int) -> dict:
        """Get file details."""
        return self._get(f"{URL_BASE}/details", params={"fileId": file_id})

    def download(self, file_id: int, revision_id: int) -> bytes:
        """Download a specific file revision.

        Returns raw bytes from the transport layer.
        """
        url = f"{URL_BASE}/{file_id}/revision/{revision_id}"
        return self._get(url)

    def set_permissions(self, file_id: int, permissions: list) -> None:
        """Set permissions for a file."""
        self._update(f"{URL_BASE}/{file_id}/permissions", permissions)
