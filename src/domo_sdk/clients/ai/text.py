"""AI text generation client for the Domo API."""

from __future__ import annotations

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/ai/v1/text"


class TextClient(DomoAPIClient):
    """Text-oriented AI endpoints.

    Provides generation, natural-language-to-SQL, summarisation,
    and beastmode formula generation.
    """

    def generate(self, request: dict) -> dict:
        """Generate text.

        POST /ai/v1/text/generation
        """
        return self._create(f"{URL_BASE}/generation", request)

    def to_sql(self, request: dict) -> dict:
        """Convert natural language to SQL.

        POST /ai/v1/text/sql
        """
        return self._create(f"{URL_BASE}/sql", request)

    def summarize(self, request: dict) -> dict:
        """Summarise text.

        POST /ai/v1/text/summarize
        """
        return self._create(f"{URL_BASE}/summarize", request)

    def beastmode(self, request: dict) -> dict:
        """Generate a beastmode formula.

        POST /ai/v1/text/beastmode
        """
        return self._create(f"{URL_BASE}/beastmode", request)
