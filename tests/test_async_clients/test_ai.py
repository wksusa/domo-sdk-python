"""Tests for async AI clients using respx to mock httpx requests."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from domo_sdk.async_clients.ai.analysis import AsyncAnalysisClient
from domo_sdk.async_clients.ai.media import AsyncMediaClient
from domo_sdk.async_clients.ai.messages import AsyncMessagesClient
from domo_sdk.async_clients.ai.text import AsyncTextClient
from domo_sdk.models.ai import (
    EmbeddingAIResponse,
    MessagesAIResponse,
    SentimentAIResponse,
    TextAIResponse,
)
from domo_sdk.transport.async_transport import AsyncTransport
from domo_sdk.transport.auth import DeveloperTokenCredentials, DeveloperTokenStrategy


def _make_transport() -> tuple[AsyncTransport, str]:
    """Create an AsyncTransport with DeveloperTokenStrategy."""
    creds = DeveloperTokenCredentials(token="test-token", instance_domain="test.domo.com")
    strategy = DeveloperTokenStrategy(credentials=creds)
    transport = AsyncTransport(auth=strategy)
    base_url = strategy.get_base_url()
    return transport, base_url


@pytest.mark.asyncio
class TestAsyncTextClient:
    """Async text generation tests using respx."""

    @respx.mock
    async def test_generate(self) -> None:
        """POST /ai/v1/text/generation."""
        transport, base_url = _make_transport()
        client = AsyncTextClient(transport)

        route = respx.post(f"{base_url}/ai/v1/text/generation").mock(
            return_value=Response(200, json={
                "output": "Here is the generated text.",
                "stopReason": "end_turn",
                "usage": {"inputTokens": 10, "outputTokens": 20, "totalTokens": 30},
            })
        )

        body = {"prompt": "Write something", "input": "context", "maxTokens": 512}
        result = await client.generate(body)

        assert route.called
        assert isinstance(result, TextAIResponse)
        assert result.output == "Here is the generated text."
        assert result.usage.total_tokens == 30

        await transport.close()

    @respx.mock
    async def test_to_sql(self) -> None:
        """POST /ai/v1/text/sql."""
        transport, base_url = _make_transport()
        client = AsyncTextClient(transport)

        respx.post(f"{base_url}/ai/v1/text/sql").mock(
            return_value=Response(200, json={"output": "SELECT * FROM sales"})
        )

        result = await client.to_sql({"input": "show me all sales"})

        assert isinstance(result, TextAIResponse)
        assert "SELECT" in result.output
        await transport.close()


@pytest.mark.asyncio
class TestAsyncMessagesClient:
    """Async messages chat tests using respx."""

    @respx.mock
    async def test_chat(self) -> None:
        """POST /ai/v1/messages/chat."""
        transport, base_url = _make_transport()
        client = AsyncMessagesClient(transport)

        route = respx.post(f"{base_url}/ai/v1/messages/chat").mock(
            return_value=Response(200, json={
                "id": "msg-001",
                "content": [{"type": "text", "text": "Hello!"}],
                "model": "claude-3",
                "role": "assistant",
                "stopReason": "end_turn",
            })
        )

        body = {
            "messages": [{"role": "user", "content": "Hi"}],
            "maxTokens": 1024,
        }
        result = await client.chat(body)

        assert route.called
        assert isinstance(result, MessagesAIResponse)
        assert result.role == "assistant"
        assert result.content[0]["text"] == "Hello!"

        await transport.close()


@pytest.mark.asyncio
class TestAsyncAnalysisClient:
    """Async analysis tests using respx."""

    @respx.mock
    async def test_sentiment(self) -> None:
        """POST /ai/v1/sentiment."""
        transport, base_url = _make_transport()
        client = AsyncAnalysisClient(transport)

        route = respx.post(f"{base_url}/ai/v1/sentiment").mock(
            return_value=Response(200, json={
                "sentiment": "POSITIVE",
                "confidence": 0.95,
                "usage": {"inputTokens": 5, "outputTokens": 3, "totalTokens": 8},
            })
        )

        body = {"input": "I love this product!", "maxTokens": 256}
        result = await client.sentiment(body)

        assert route.called
        assert isinstance(result, SentimentAIResponse)
        assert result.sentiment == "POSITIVE"
        assert result.confidence == 0.95

        await transport.close()


@pytest.mark.asyncio
class TestAsyncMediaClient:
    """Async media tests using respx."""

    @respx.mock
    async def test_embed_text(self) -> None:
        """POST /ai/v1/embedding/text."""
        transport, base_url = _make_transport()
        client = AsyncMediaClient(transport)

        route = respx.post(f"{base_url}/ai/v1/embedding/text").mock(
            return_value=Response(200, json={
                "embeddings": [[0.1, 0.2, 0.3]],
                "model": "text-embedding-3-small",
            })
        )

        result = await client.embed_text({"input": "Hello world"})

        assert route.called
        assert isinstance(result, EmbeddingAIResponse)
        assert result.embeddings[0] == [0.1, 0.2, 0.3]

        await transport.close()
