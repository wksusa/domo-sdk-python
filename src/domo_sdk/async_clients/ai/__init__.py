"""Async AI client composing text, messages, analysis, and media sub-clients."""

from __future__ import annotations

import logging

from domo_sdk.async_clients.ai.analysis import AsyncAnalysisClient
from domo_sdk.async_clients.ai.media import AsyncMediaClient
from domo_sdk.async_clients.ai.messages import AsyncMessagesClient
from domo_sdk.async_clients.ai.text import AsyncTextClient
from domo_sdk.transport.async_transport import AsyncTransport


class AsyncAIClient:
    """Async composite client for the Domo AI API.

    Delegates to specialised sub-clients:

    - ``text``     -- text generation, SQL, summarisation, beastmode
    - ``messages`` -- chat and tool-use completions
    - ``analysis`` -- sentiment, classification, extraction
    - ``media``    -- image-to-text, embeddings
    """

    def __init__(self, transport: AsyncTransport, logger_: logging.Logger | None = None) -> None:
        self.text = AsyncTextClient(transport, logger_)
        self.messages = AsyncMessagesClient(transport, logger_)
        self.analysis = AsyncAnalysisClient(transport, logger_)
        self.media = AsyncMediaClient(transport, logger_)

    def __repr__(self) -> str:
        return (
            f"AsyncAIClient(text={self.text!r}, messages={self.messages!r}, "
            f"analysis={self.analysis!r}, media={self.media!r})"
        )
