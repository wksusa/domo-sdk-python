"""Card client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/v1/cards"


class CardClient(DomoAPIClient):
    """Manage Domo cards.

    Docs: https://developer.domo.com/docs/cards-api-reference/cards
    """

    def create(self, card_request: dict) -> dict:
        """Create a new card."""
        return self._create(URL_BASE, card_request)

    def get(self, card_id: int) -> dict:
        """Retrieve a single card by ID."""
        return self._get(f"{URL_BASE}/{card_id}")

    def list(self, per_page: int = 50, offset: int = 0) -> list:
        """List cards."""
        params: dict[str, Any] = {"limit": per_page, "offset": offset}
        return self._list(URL_BASE, params=params)

    def update(self, card_id: int, card_update: dict) -> dict:
        """Update an existing card."""
        return self._update(f"{URL_BASE}/{card_id}", card_update)

    def delete(self, card_id: int) -> None:
        """Delete a card."""
        self._delete(f"{URL_BASE}/{card_id}")
