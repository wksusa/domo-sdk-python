"""Tests for async AI clients using respx to mock httpx requests."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from domo_sdk.async_clients.base import AsyncDomoAPIClient
from domo_sdk.transport.async_transport import AsyncTransport
from domo_sdk.transport.auth import DeveloperTokenCredentials, DeveloperTokenStrategy


class AsyncTextClient(AsyncDomoAPIClient):
    """Minimal async text client for testing (mirrors TextClient API)."""

    async def generate(self, request: dict) -> dict:
        return await self._create("/ai/v1/text/generation", request)


class AsyncMessagesClient(AsyncDomoAPIClient):
    """Minimal async messages client for testing (mirrors MessagesClient API)."""

    async def chat(self, request: dict) -> dict:
        return await self._create("/ai/v1/messages/chat", request)


class AsyncAnalysisClient(AsyncDomoAPIClient):
    """Minimal async analysis client for testing (mirrors AnalysisClient API)."""

    async def sentiment(self, request: dict) -> dict:
        return await self._create("/ai/v1/sentiment", request)


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
    async def test_async_text_generate(self) -> None:
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
        assert result["output"] == "Here is the generated text."
        assert result["usage"]["totalTokens"] == 30

        await transport.close()


@pytest.mark.asyncio
class TestAsyncMessagesClient:
    """Async messages chat tests using respx."""

    @respx.mock
    async def test_async_chat(self) -> None:
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
        assert result["role"] == "assistant"
        assert result["content"][0]["text"] == "Hello!"

        await transport.close()


@pytest.mark.asyncio
class TestAsyncAnalysisClient:
    """Async sentiment analysis tests using respx."""

    @respx.mock
    async def test_async_sentiment(self) -> None:
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
        assert result["sentiment"] == "POSITIVE"
        assert result["confidence"] == 0.95

        await transport.close()
