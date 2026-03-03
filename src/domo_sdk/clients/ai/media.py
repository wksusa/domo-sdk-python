"""AI media client for the Domo API."""

from __future__ import annotations

from domo_sdk.clients.base import DomoAPIClient
from domo_sdk.models.ai import EmbeddingAIResponse, TextAIResponse

URL_BASE = "/ai/v1"


class MediaClient(DomoAPIClient):
    """Media-oriented AI endpoints: image-to-text, embeddings."""

    def image_to_text(self, request: dict) -> TextAIResponse:
        """Extract text from an image.

        POST /ai/v1/image/text
        """
        data = self._create(f"{URL_BASE}/image/text", request)
        return TextAIResponse.model_validate(data)

    def embed_text(self, request: dict) -> EmbeddingAIResponse:
        """Generate a text embedding vector.

        POST /ai/v1/embedding/text
        """
        data = self._create(f"{URL_BASE}/embedding/text", request)
        return EmbeddingAIResponse.model_validate(data)

    def embed_image(self, request: dict) -> EmbeddingAIResponse:
        """Generate an image embedding vector.

        POST /ai/v1/embedding/image
        """
        data = self._create(f"{URL_BASE}/embedding/image", request)
        return EmbeddingAIResponse.model_validate(data)
