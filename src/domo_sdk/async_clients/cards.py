"""Async Card client for the Domo API."""

from __future__ import annotations

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/cards"


class AsyncCardClient(AsyncDomoAPIClient):
    """Manage Domo cards asynchronously.

    Docs: https://developer.domo.com/docs/cards-api-reference/cards
    """

    async def create(self, card_request: dict) -> dict:
        """Create a new card."""
        return await self._create(URL_BASE, card_request)

    async def get(self, card_id: int) -> dict:
        """Retrieve a single card by ID."""
        return await self._get(f"{URL_BASE}/{card_id}")

    async def list(self, per_page: int = 50, offset: int = 0) -> list:
        """List cards."""
        return await self._list(URL_BASE, params={"limit": per_page, "offset": offset})

    async def update(self, card_id: int, card_update: dict) -> dict:
        """Update an existing card."""
        return await self._update(f"{URL_BASE}/{card_id}", card_update)

    async def delete(self, card_id: int) -> None:
        """Delete a card."""
        await self._delete(f"{URL_BASE}/{card_id}")
