"""AI media client for the Domo API."""

from __future__ import annotations

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/ai/v1"


class MediaClient(DomoAPIClient):
    """Media-oriented AI endpoints: image-to-text, embeddings."""

    def image_to_text(self, request: dict) -> dict:
        """Extract text from an image.

        POST /ai/v1/image/text
        """
        return self._create(f"{URL_BASE}/image/text", request)

    def embed_text(self, request: dict) -> dict:
        """Generate a text embedding vector.

        POST /ai/v1/embedding/text
        """
        return self._create(f"{URL_BASE}/embedding/text", request)

    def embed_image(self, request: dict) -> dict:
        """Generate an image embedding vector.

        POST /ai/v1/embedding/image
        """
        return self._create(f"{URL_BASE}/embedding/image", request)
