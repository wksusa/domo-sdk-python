"""Async AI text generation client for the Domo API."""

from __future__ import annotations

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/ai/v1/text"


class AsyncTextClient(AsyncDomoAPIClient):
    """Async text-oriented AI endpoints.

    Provides generation, natural-language-to-SQL, summarisation,
    and beastmode formula generation.
    """

    async def generate(self, request: dict) -> dict:
        """Generate text.

        POST /ai/v1/text/generation
        """
        return await self._create(f"{URL_BASE}/generation", request)

    async def to_sql(self, request: dict) -> dict:
        """Convert natural language to SQL.

        POST /ai/v1/text/sql
        """
        return await self._create(f"{URL_BASE}/sql", request)

    async def summarize(self, request: dict) -> dict:
        """Summarise text.

        POST /ai/v1/text/summarize
        """
        return await self._create(f"{URL_BASE}/summarize", request)

    async def beastmode(self, request: dict) -> dict:
        """Generate a beastmode formula.

        POST /ai/v1/text/beastmode
        """
        return await self._create(f"{URL_BASE}/beastmode", request)
