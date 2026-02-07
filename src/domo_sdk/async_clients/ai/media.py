"""Async AI media client for the Domo API."""

from __future__ import annotations

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/ai/v1"


class AsyncMediaClient(AsyncDomoAPIClient):
    """Async media-oriented AI endpoints: image-to-text, embeddings."""

    async def image_to_text(self, request: dict) -> dict:
        """Extract text from an image.

        POST /ai/v1/image/text
        """
        return await self._create(f"{URL_BASE}/image/text", request)

    async def embed_text(self, request: dict) -> dict:
        """Generate a text embedding vector.

        POST /ai/v1/embedding/text
        """
        return await self._create(f"{URL_BASE}/embedding/text", request)

    async def embed_image(self, request: dict) -> dict:
        """Generate an image embedding vector.

        POST /ai/v1/embedding/image
        """
        return await self._create(f"{URL_BASE}/embedding/image", request)
