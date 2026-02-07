"""Async AI messages client for the Domo API."""

from __future__ import annotations

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/ai/v1/messages"


class AsyncMessagesClient(AsyncDomoAPIClient):
    """Async conversational AI endpoints (chat and tool-use)."""

    async def chat(self, request: dict) -> dict:
        """Send a chat message.

        POST /ai/v1/messages/chat
        """
        return await self._create(f"{URL_BASE}/chat", request)

    async def tools(self, request: dict) -> dict:
        """Invoke tool-use completion.

        POST /ai/v1/messages/tools
        """
        return await self._create(f"{URL_BASE}/tools", request)
