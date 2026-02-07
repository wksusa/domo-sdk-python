"""AI analysis client for the Domo API."""

from __future__ import annotations

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/ai/v1"


class AnalysisClient(DomoAPIClient):
    """Analytical AI endpoints: sentiment, classification, extraction."""

    def sentiment(self, request: dict) -> dict:
        """Analyse overall sentiment.

        POST /ai/v1/sentiment
        """
        return self._create(f"{URL_BASE}/sentiment", request)

    def targeted_sentiment(self, request: dict) -> dict:
        """Analyse sentiment targeted at specific aspects.

        POST /ai/v1/targeted-sentiment
        """
        return self._create(f"{URL_BASE}/targeted-sentiment", request)

    def classify(self, request: dict) -> dict:
        """Classify text.

        POST /ai/v1/classification
        """
        return self._create(f"{URL_BASE}/classification", request)

    def extract(self, request: dict) -> dict:
        """Extract structured data from text.

        POST /ai/v1/extract
        """
        return self._create(f"{URL_BASE}/extract", request)
