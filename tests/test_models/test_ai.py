"""Tests for AI models."""
from __future__ import annotations

from domo_sdk.models.ai import (
    ChatMessage,
    ChatRequest,
    ClassificationLabel,
    ClassificationRequest,
    DataSourceColumn,
    DataSourceSchema,
    EmbeddingAIResponse,
    ExtractionRequest,
    MessagesAIResponse,
    ModelProviderUsage,
    SentimentRequest,
    StopReason,
    TextAIResponse,
    TextGenerationRequest,
    TextSqlRequest,
    ToolDefinition,
    ToolInputSchema,
)


class TestTextGenerationRequest:
    """Tests for TextGenerationRequest."""

    def test_text_generation_request(self) -> None:
        """Create and serialize a TextGenerationRequest."""
        req = TextGenerationRequest(prompt="Summarize this", input="Some long text")
        assert req.prompt == "Summarize this"
        assert req.input == "Some long text"
        assert req.max_tokens == 1024

        data = req.model_dump(by_alias=True)
        assert data["maxTokens"] == 1024


class TestTextSqlRequest:
    """Tests for TextSqlRequest."""

    def test_text_sql_request_with_schemas(self) -> None:
        """TextSqlRequest with datasource schemas."""
        schemas = [
            DataSourceSchema(
                datasetId="ds-1",
                name="Sales",
                columns=[
                    DataSourceColumn(name="revenue", type="DECIMAL"),
                    DataSourceColumn(name="region", type="STRING"),
                ],
            )
        ]
        req = TextSqlRequest(input="total revenue by region", datasource_schemas=schemas)
        assert req.input == "total revenue by region"
        assert len(req.datasource_schemas) == 1
        assert req.datasource_schemas[0].dataset_id == "ds-1"
        assert len(req.datasource_schemas[0].columns) == 2


class TestChatRequest:
    """Tests for ChatRequest."""

    def test_chat_request_with_messages(self) -> None:
        """ChatRequest with a list of messages."""
        messages = [
            ChatMessage(role="user", content="Hello"),
            ChatMessage(role="assistant", content="Hi there!"),
            ChatMessage(role="user", content="What is Domo?"),
        ]
        req = ChatRequest(messages=messages, max_tokens=512)
        assert len(req.messages) == 3
        assert req.messages[0].role == "user"
        assert req.messages[1].content == "Hi there!"
        assert req.max_tokens == 512


class TestToolDefinition:
    """Tests for ToolDefinition."""

    def test_tool_definition(self) -> None:
        """ToolDefinition with input schema."""
        tool = ToolDefinition(
            name="get_weather",
            description="Get weather for a city",
            inputSchema=ToolInputSchema(
                type="object",
                properties={
                    "city": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                required=["city"],
            ),
        )
        assert tool.name == "get_weather"
        assert tool.description == "Get weather for a city"
        assert tool.input_schema.type == "object"
        assert "city" in tool.input_schema.properties
        assert tool.input_schema.required == ["city"]


class TestSentimentRequest:
    """Tests for SentimentRequest."""

    def test_sentiment_request(self) -> None:
        """Basic SentimentRequest creation."""
        req = SentimentRequest(input="I love this product!")
        assert req.input == "I love this product!"
        assert req.max_tokens == 256


class TestClassificationRequest:
    """Tests for ClassificationRequest."""

    def test_classification_request_with_labels(self) -> None:
        """ClassificationRequest with multiple labels."""
        labels = [
            ClassificationLabel(name="positive", description="Positive sentiment"),
            ClassificationLabel(name="negative", description="Negative sentiment"),
            ClassificationLabel(name="neutral"),
        ]
        req = ClassificationRequest(
            input="This is okay I guess",
            labels=labels,
            multi_label=False,
        )
        assert req.input == "This is okay I guess"
        assert len(req.labels) == 3
        assert req.labels[0].name == "positive"
        assert req.labels[2].description == ""
        assert req.multi_label is False


class TestExtractionRequest:
    """Tests for ExtractionRequest."""

    def test_extraction_request_with_schema(self) -> None:
        """ExtractionRequest with output schema."""
        output_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
            "required": ["name"],
        }
        req = ExtractionRequest(
            input="John is 30 years old",
            outputSchema=output_schema,
        )
        assert req.input == "John is 30 years old"
        assert req.output_schema["type"] == "object"
        assert "name" in req.output_schema["properties"]


class TestTextAIResponse:
    """Tests for TextAIResponse."""

    def test_text_ai_response(self) -> None:
        """Deserialize a TextAIResponse with usage."""
        data = {
            "output": "SELECT SUM(revenue) FROM sales GROUP BY region",
            "stopReason": "end_turn",
            "usage": {
                "inputTokens": 50,
                "outputTokens": 20,
                "totalTokens": 70,
            },
        }
        resp = TextAIResponse.model_validate(data)
        assert resp.output == "SELECT SUM(revenue) FROM sales GROUP BY region"
        assert resp.stop_reason == StopReason.END_TURN
        assert resp.usage is not None
        assert resp.usage.input_tokens == 50
        assert resp.usage.output_tokens == 20
        assert resp.usage.total_tokens == 70


class TestMessagesAIResponse:
    """Tests for MessagesAIResponse."""

    def test_messages_ai_response(self) -> None:
        """Deserialize a MessagesAIResponse with content list."""
        data = {
            "id": "msg-001",
            "content": [{"type": "text", "text": "Hello!"}],
            "model": "claude-3",
            "role": "assistant",
            "stopReason": "end_turn",
            "usage": {
                "inputTokens": 10,
                "outputTokens": 5,
                "totalTokens": 15,
            },
        }
        resp = MessagesAIResponse.model_validate(data)
        assert resp.id == "msg-001"
        assert len(resp.content) == 1
        assert resp.content[0]["type"] == "text"
        assert resp.model == "claude-3"
        assert resp.role == "assistant"
        assert resp.stop_reason == StopReason.END_TURN
        assert resp.usage is not None
        assert resp.usage.total_tokens == 15


class TestEmbeddingResponse:
    """Tests for EmbeddingAIResponse."""

    def test_embedding_response(self) -> None:
        """Deserialize an EmbeddingAIResponse with embeddings list."""
        data = {
            "embeddings": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
            "model": "text-embedding-3-small",
            "usage": {
                "inputTokens": 8,
                "outputTokens": 0,
                "totalTokens": 8,
            },
        }
        resp = EmbeddingAIResponse.model_validate(data)
        assert len(resp.embeddings) == 2
        assert resp.embeddings[0] == [0.1, 0.2, 0.3]
        assert resp.model == "text-embedding-3-small"
        assert resp.usage is not None
        assert resp.usage.input_tokens == 8


class TestModelProviderUsage:
    """Tests for ModelProviderUsage."""

    def test_model_provider_usage(self) -> None:
        """Token counts deserialize correctly."""
        data = {"inputTokens": 100, "outputTokens": 50, "totalTokens": 150}
        usage = ModelProviderUsage.model_validate(data)
        assert usage.input_tokens == 100
        assert usage.output_tokens == 50
        assert usage.total_tokens == 150

    def test_model_provider_usage_defaults(self) -> None:
        """Defaults to zeros when not provided."""
        usage = ModelProviderUsage()
        assert usage.input_tokens == 0
        assert usage.output_tokens == 0
        assert usage.total_tokens == 0
