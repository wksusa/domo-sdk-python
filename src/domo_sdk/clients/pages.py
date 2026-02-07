"""Page client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/v1/pages"


class PageClient(DomoAPIClient):
    """Manage Domo pages.

    Docs: https://developer.domo.com/docs/page-api-reference/page
    """

    def create(self, name: str, **kwargs: Any) -> dict:
        """Create a new page."""
        body = {"name": name, **kwargs}
        return self._create(URL_BASE, body)

    def get(self, page_id: int) -> dict:
        """Retrieve a single page by ID."""
        return self._get(f"{URL_BASE}/{page_id}")

    def list(self) -> list:
        """List all pages."""
        return self._list(URL_BASE)

    def update(self, page_id: int, **kwargs: Any) -> dict:
        """Update an existing page."""
        return self._update(f"{URL_BASE}/{page_id}", kwargs)

    def delete(self, page_id: int) -> None:
        """Delete a page."""
        self._delete(f"{URL_BASE}/{page_id}")

    def get_collections(self, page_id: int) -> list:
        """List collections on a page."""
        return self._list(f"{URL_BASE}/{page_id}/collections")

    def create_collection(self, page_id: int, title: str, **kwargs: Any) -> dict:
        """Create a collection on a page."""
        body = {"title": title, **kwargs}
        return self._create(f"{URL_BASE}/{page_id}/collections", body)

    def update_collection(self, page_id: int, collection_id: int, **kwargs: Any) -> dict:
        """Update a collection on a page."""
        return self._update(f"{URL_BASE}/{page_id}/collections/{collection_id}", kwargs)

    def delete_collection(self, page_id: int, collection_id: int) -> None:
        """Delete a collection from a page."""
        self._delete(f"{URL_BASE}/{page_id}/collections/{collection_id}")
