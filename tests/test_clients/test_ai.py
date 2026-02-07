"""Tests for AI clients with mocked transport."""
from __future__ import annotations

from unittest.mock import MagicMock

from domo_sdk.clients.ai.analysis import AnalysisClient
from domo_sdk.clients.ai.media import MediaClient
from domo_sdk.clients.ai.messages import MessagesClient
from domo_sdk.clients.ai.text import TextClient


def _make_transport() -> MagicMock:
    """Create a mocked transport."""
    transport = MagicMock()
    transport.auth_mode = "developer_token"
    return transport


class TestTextClient:
    """Tests for TextClient."""

    def test_text_generate(self) -> None:
        """POST /ai/v1/text/generation."""
        transport = _make_transport()
        transport.post.return_value = {"output": "Generated text", "stopReason": "end_turn"}
        client = TextClient(transport)

        body = {"prompt": "Write something", "input": "context", "maxTokens": 512}
        result = client.generate(body)

        transport.post.assert_called_once_with(
            "/ai/v1/text/generation",
            body=body,
            params=None,
        )
        assert result["output"] == "Generated text"

    def test_text_to_sql(self) -> None:
        """POST /ai/v1/text/sql."""
        transport = _make_transport()
        transport.post.return_value = {"output": "SELECT * FROM sales"}
        client = TextClient(transport)

        body = {"input": "show me all sales", "datasourceSchemas": [], "maxTokens": 1024}
        result = client.to_sql(body)

        transport.post.assert_called_once_with(
            "/ai/v1/text/sql",
            body=body,
            params=None,
        )
        assert "SELECT" in result["output"]

    def test_text_summarize(self) -> None:
        """POST /ai/v1/text/summarize."""
        transport = _make_transport()
        transport.post.return_value = {"output": "Summary of the text"}
        client = TextClient(transport)

        body = {"input": "Very long text...", "maxTokens": 256}
        result = client.summarize(body)

        transport.post.assert_called_once_with(
            "/ai/v1/text/summarize",
            body=body,
            params=None,
        )
        assert result["output"] == "Summary of the text"


class TestMessagesClient:
    """Tests for MessagesClient."""

    def test_messages_chat(self) -> None:
        """POST /ai/v1/messages/chat."""
        transport = _make_transport()
        transport.post.return_value = {
            "id": "msg-1",
            "content": [{"type": "text", "text": "Hi!"}],
            "role": "assistant",
            "stopReason": "end_turn",
        }
        client = MessagesClient(transport)

        body = {
            "messages": [{"role": "user", "content": "Hello"}],
            "maxTokens": 1024,
        }
        result = client.chat(body)

        transport.post.assert_called_once_with(
            "/ai/v1/messages/chat",
            body=body,
            params=None,
        )
        assert result["role"] == "assistant"

    def test_messages_tools(self) -> None:
        """POST /ai/v1/messages/tools."""
        transport = _make_transport()
        transport.post.return_value = {
            "id": "msg-2",
            "content": [{"type": "tool_use", "id": "t1", "name": "get_weather", "input": {"city": "NYC"}}],
            "stopReason": "tool_use",
        }
        client = MessagesClient(transport)

        body = {
            "messages": [{"role": "user", "content": "What's the weather in NYC?"}],
            "tools": [{"name": "get_weather", "description": "Get weather", "inputSchema": {"type": "object"}}],
            "maxTokens": 512,
        }
        result = client.tools(body)

        transport.post.assert_called_once_with(
            "/ai/v1/messages/tools",
            body=body,
            params=None,
        )
        assert result["content"][0]["type"] == "tool_use"


class TestAnalysisClient:
    """Tests for AnalysisClient."""

    def test_sentiment(self) -> None:
        """POST /ai/v1/sentiment."""
        transport = _make_transport()
        transport.post.return_value = {"sentiment": "POSITIVE", "confidence": 0.95}
        client = AnalysisClient(transport)

        body = {"input": "I love this!", "maxTokens": 256}
        result = client.sentiment(body)

        transport.post.assert_called_once_with(
            "/ai/v1/sentiment",
            body=body,
            params=None,
        )
        assert result["sentiment"] == "POSITIVE"

    def test_classify(self) -> None:
        """POST /ai/v1/classification."""
        transport = _make_transport()
        transport.post.return_value = {
            "classifications": [{"label": "tech", "confidence": 0.9}],
        }
        client = AnalysisClient(transport)

        body = {
            "input": "New GPU release",
            "labels": [{"name": "tech"}, {"name": "sports"}],
            "maxTokens": 256,
        }
        result = client.classify(body)

        transport.post.assert_called_once_with(
            "/ai/v1/classification",
            body=body,
            params=None,
        )
        assert result["classifications"][0]["label"] == "tech"


class TestMediaClient:
    """Tests for MediaClient."""

    def test_embed_text(self) -> None:
        """POST /ai/v1/embedding/text."""
        transport = _make_transport()
        transport.post.return_value = {
            "embeddings": [[0.1, 0.2, 0.3]],
            "model": "text-embedding-3-small",
        }
        client = MediaClient(transport)

        body = {"input": "Hello world", "model": "text-embedding-3-small"}
        result = client.embed_text(body)

        transport.post.assert_called_once_with(
            "/ai/v1/embedding/text",
            body=body,
            params=None,
        )
        assert len(result["embeddings"]) == 1
        assert result["embeddings"][0] == [0.1, 0.2, 0.3]
