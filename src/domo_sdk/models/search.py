"""Search models."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import Field

from domo_sdk.models.base import DomoModel


class SearchEntity(str, Enum):
    """Searchable entity types."""

    DATASET = "DATASET"
    USER = "USER"
    CARD = "CARD"
    DATAFLOW = "DATAFLOW"
    APP = "APP"
    ACCOUNT = "ACCOUNT"
    ALERT = "ALERT"
    PAGE = "PAGE"
    PROJECT = "PROJECT"
    BUZZ_CHANNEL = "BUZZ_CHANNEL"


class SearchQuery(DomoModel):
    """Search query parameters."""

    query: str = "*"
    count: int = 50
    offset: int = 0
    entities: list[SearchEntity] = []
    filters: list[dict[str, Any]] = []
    combine_results: bool = Field(default=True, alias="combineResults")
    sort: dict[str, Any] | None = None


class SearchResult(DomoModel):
    """Individual search result."""

    id: str = ""
    name: str = ""
    type: str = ""
    description: str = ""
    owner: dict[str, Any] | None = None


class SearchResponse(DomoModel):
    """Search response containing results."""

    data_sources: list[SearchResult] = Field(default=[], alias="dataSources")
    users: list[SearchResult] = []
    cards: list[SearchResult] = []
    total_count: int = Field(default=0, alias="totalCount")
