"""Async AI messages client for the Domo API."""

from __future__ import annotations

from domo_sdk.async_clients.base import AsyncDomoAPIClient
from domo_sdk.models.ai import MessagesAIResponse

URL_BASE = "/ai/v1/messages"


class AsyncMessagesClient(AsyncDomoAPIClient):
    """Async conversational AI endpoints (chat and tool-use)."""

    async def chat(self, request: dict) -> MessagesAIResponse:
        """Send a chat message.

        POST /ai/v1/messages/chat
        """
        data = await self._create(f"{URL_BASE}/chat", request)
        return MessagesAIResponse.model_validate(data)

    async def tools(self, request: dict) -> MessagesAIResponse:
        """Invoke tool-use completion.

        POST /ai/v1/messages/tools
        """
        data = await self._create(f"{URL_BASE}/tools", request)
        return MessagesAIResponse.model_validate(data)
