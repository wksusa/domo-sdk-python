"""Async Embed client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/embed"


class AsyncEmbedClient(AsyncDomoAPIClient):
    """Create embed tokens for Domo cards and dashboards asynchronously.

    Docs: https://developer.domo.com/docs/embed-api-reference/embed
    """

    async def create_card_token(
        self,
        card_id: int,
        expiration: int | None = None,
        **kwargs: Any,
    ) -> dict:
        """Create an embed token for a card.

        Parameters
        ----------
        card_id:
            The ID of the card to embed.
        expiration:
            Optional token expiration in seconds.
        """
        body: dict[str, Any] = {"cardId": card_id, **kwargs}
        if expiration is not None:
            body["expiration"] = expiration
        return await self._create(f"{URL_BASE}/card", body)

    async def create_dashboard_token(
        self,
        page_id: int,
        expiration: int | None = None,
        **kwargs: Any,
    ) -> dict:
        """Create an embed token for a dashboard (page).

        Parameters
        ----------
        page_id:
            The ID of the page/dashboard to embed.
        expiration:
            Optional token expiration in seconds.
        """
        body: dict[str, Any] = {"pageId": page_id, **kwargs}
        if expiration is not None:
            body["expiration"] = expiration
        return await self._create(f"{URL_BASE}/dashboard", body)
