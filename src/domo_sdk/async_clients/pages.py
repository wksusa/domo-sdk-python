"""Async Page client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/pages"


class AsyncPageClient(AsyncDomoAPIClient):
    """Manage Domo pages asynchronously.

    Docs: https://developer.domo.com/docs/page-api-reference/page
    """

    async def create(self, name: str, **kwargs: Any) -> dict:
        """Create a new page."""
        body: dict[str, Any] = {"name": name, **kwargs}
        return await self._create(URL_BASE, body)

    async def get(self, page_id: int) -> dict:
        """Retrieve a single page by ID."""
        return await self._get(f"{URL_BASE}/{page_id}")

    async def list(self) -> list:
        """List all pages."""
        return await self._list(URL_BASE)

    async def update(self, page_id: int, **kwargs: Any) -> dict:
        """Update an existing page."""
        return await self._update(f"{URL_BASE}/{page_id}", kwargs)

    async def delete(self, page_id: int) -> None:
        """Delete a page."""
        await self._delete(f"{URL_BASE}/{page_id}")

    # ------------------------------------------------------------------
    # Collections
    # ------------------------------------------------------------------

    async def get_collections(self, page_id: int) -> list:
        """List collections on a page."""
        url = f"{URL_BASE}/{page_id}/collections"
        return await self._list(url)

    async def create_collection(self, page_id: int, title: str, **kwargs: Any) -> dict:
        """Create a new collection on a page."""
        url = f"{URL_BASE}/{page_id}/collections"
        body: dict[str, Any] = {"title": title, **kwargs}
        return await self._create(url, body)

    async def update_collection(
        self, page_id: int, collection_id: int, **kwargs: Any
    ) -> dict:
        """Update a collection on a page."""
        url = f"{URL_BASE}/{page_id}/collections/{collection_id}"
        return await self._update(url, kwargs)

    async def delete_collection(self, page_id: int, collection_id: int) -> None:
        """Delete a collection from a page."""
        url = f"{URL_BASE}/{page_id}/collections/{collection_id}"
        await self._delete(url)
