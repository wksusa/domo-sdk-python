"""Async AI analysis client for the Domo API."""

from __future__ import annotations

from domo_sdk.async_clients.base import AsyncDomoAPIClient
from domo_sdk.models.ai import (
    ClassificationAIResponse,
    ExtractionAIResponse,
    SentimentAIResponse,
    TargetedSentimentAIResponse,
)

URL_BASE = "/ai/v1"


class AsyncAnalysisClient(AsyncDomoAPIClient):
    """Async analytical AI endpoints: sentiment, classification, extraction."""

    async def sentiment(self, request: dict) -> SentimentAIResponse:
        """Analyse overall sentiment.

        POST /ai/v1/sentiment
        """
        data = await self._create(f"{URL_BASE}/sentiment", request)
        return SentimentAIResponse.model_validate(data)

    async def targeted_sentiment(self, request: dict) -> TargetedSentimentAIResponse:
        """Analyse sentiment targeted at specific aspects.

        POST /ai/v1/targeted-sentiment
        """
        data = await self._create(f"{URL_BASE}/targeted-sentiment", request)
        return TargetedSentimentAIResponse.model_validate(data)

    async def classify(self, request: dict) -> ClassificationAIResponse:
        """Classify text.

        POST /ai/v1/classification
        """
        data = await self._create(f"{URL_BASE}/classification", request)
        return ClassificationAIResponse.model_validate(data)

    async def extract(self, request: dict) -> ExtractionAIResponse:
        """Extract structured data from text.

        POST /ai/v1/extract
        """
        data = await self._create(f"{URL_BASE}/extract", request)
        return ExtractionAIResponse.model_validate(data)
