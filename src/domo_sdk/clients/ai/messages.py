"""AI messages client for the Domo API."""

from __future__ import annotations

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/ai/v1/messages"


class MessagesClient(DomoAPIClient):
    """Conversational AI endpoints (chat and tool-use)."""

    def chat(self, request: dict) -> dict:
        """Send a chat message.

        POST /ai/v1/messages/chat
        """
        return self._create(f"{URL_BASE}/chat", request)

    def tools(self, request: dict) -> dict:
        """Invoke tool-use completion.

        POST /ai/v1/messages/tools
        """
        return self._create(f"{URL_BASE}/tools", request)
