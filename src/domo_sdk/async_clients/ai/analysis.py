"""Async AI analysis client for the Domo API."""

from __future__ import annotations

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/ai/v1"


class AsyncAnalysisClient(AsyncDomoAPIClient):
    """Async analytical AI endpoints: sentiment, classification, extraction."""

    async def sentiment(self, request: dict) -> dict:
        """Analyse overall sentiment.

        POST /ai/v1/sentiment
        """
        return await self._create(f"{URL_BASE}/sentiment", request)

    async def targeted_sentiment(self, request: dict) -> dict:
        """Analyse sentiment targeted at specific aspects.

        POST /ai/v1/targeted-sentiment
        """
        return await self._create(f"{URL_BASE}/targeted-sentiment", request)

    async def classify(self, request: dict) -> dict:
        """Classify text.

        POST /ai/v1/classification
        """
        return await self._create(f"{URL_BASE}/classification", request)

    async def extract(self, request: dict) -> dict:
        """Extract structured data from text.

        POST /ai/v1/extract
        """
        return await self._create(f"{URL_BASE}/extract", request)
