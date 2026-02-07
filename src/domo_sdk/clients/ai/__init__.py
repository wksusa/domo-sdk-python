"""AI client composing text, messages, analysis, and media sub-clients."""

from __future__ import annotations

import logging

from domo_sdk.clients.ai.analysis import AnalysisClient
from domo_sdk.clients.ai.media import MediaClient
from domo_sdk.clients.ai.messages import MessagesClient
from domo_sdk.clients.ai.text import TextClient
from domo_sdk.transport.sync_transport import SyncTransport


class AIClient:
    """Composite client for the Domo AI API.

    Delegates to specialised sub-clients:

    - ``text``     -- text generation, SQL, summarisation, beastmode
    - ``messages`` -- chat and tool-use completions
    - ``analysis`` -- sentiment, classification, extraction
    - ``media``    -- image-to-text, embeddings
    """

    def __init__(self, transport: SyncTransport, logger_: logging.Logger | None = None) -> None:
        self.text = TextClient(transport, logger_)
        self.messages = MessagesClient(transport, logger_)
        self.analysis = AnalysisClient(transport, logger_)
        self.media = MediaClient(transport, logger_)

    def __repr__(self) -> str:
        return (
            f"AIClient(text={self.text!r}, messages={self.messages!r}, "
            f"analysis={self.analysis!r}, media={self.media!r})"
        )
