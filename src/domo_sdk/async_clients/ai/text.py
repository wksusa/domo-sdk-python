"""Async AI text generation client for the Domo API."""

from __future__ import annotations

from domo_sdk.async_clients.base import AsyncDomoAPIClient
from domo_sdk.models.ai import TextAIResponse

URL_BASE = "/ai/v1/text"


class AsyncTextClient(AsyncDomoAPIClient):
    """Async text-oriented AI endpoints.

    Provides generation, natural-language-to-SQL, summarisation,
    and beastmode formula generation.
    """

    async def generate(self, request: dict) -> TextAIResponse:
        """Generate text.

        POST /ai/v1/text/generation
        """
        data = await self._create(f"{URL_BASE}/generation", request)
        return TextAIResponse.model_validate(data)

    async def to_sql(self, request: dict) -> TextAIResponse:
        """Convert natural language to SQL.

        POST /ai/v1/text/sql
        """
        data = await self._create(f"{URL_BASE}/sql", request)
        return TextAIResponse.model_validate(data)

    async def summarize(self, request: dict) -> TextAIResponse:
        """Summarise text.

        POST /ai/v1/text/summarize
        """
        data = await self._create(f"{URL_BASE}/summarize", request)
        return TextAIResponse.model_validate(data)

    async def beastmode(self, request: dict) -> TextAIResponse:
        """Generate a beastmode formula.

        POST /ai/v1/text/beastmode
        """
        data = await self._create(f"{URL_BASE}/beastmode", request)
        return TextAIResponse.model_validate(data)
