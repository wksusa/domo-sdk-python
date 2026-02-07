"""Embed token client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.clients.base import DomoAPIClient


class EmbedClient(DomoAPIClient):
    """Generate embed tokens for Domo cards and dashboards.

    Docs: https://developer.domo.com/docs/embed-api-reference/embed
    """

    def create_card_token(self, card_id: int, **kwargs: Any) -> dict:
        """Create an embed token for a card."""
        body = {"cardId": card_id, **kwargs}
        return self._create("/v1/cards/embed/auth", body)

    def create_dashboard_token(self, dashboard_id: int, **kwargs: Any) -> dict:
        """Create an embed token for a dashboard."""
        body = {"dashboardId": dashboard_id, **kwargs}
        return self._create("/v1/stories/embed/auth", body)
