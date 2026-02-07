"""Tests for search models."""
from __future__ import annotations

from domo_sdk.models.search import SearchEntity, SearchQuery, SearchResult


class TestSearchEntity:
    """Tests for SearchEntity enum."""

    def test_search_entity_enum(self) -> None:
        """All expected entity types should be present."""
        expected = {
            "DATASET", "USER", "CARD", "DATAFLOW", "APP",
            "ACCOUNT", "ALERT", "PAGE", "PROJECT", "BUZZ_CHANNEL",
        }
        actual = {e.value for e in SearchEntity}
        assert actual == expected


class TestSearchQuery:
    """Tests for SearchQuery model."""

    def test_search_query_defaults(self) -> None:
        """Default values should be sensible."""
        sq = SearchQuery()
        assert sq.query == "*"
        assert sq.count == 50
        assert sq.offset == 0
        assert sq.entities == []
        assert sq.filters == []
        assert sq.combine_results is True
        assert sq.sort is None

    def test_search_query_with_entities(self) -> None:
        """SearchQuery with specific entities."""
        sq = SearchQuery(
            query="revenue",
            count=10,
            offset=5,
            entities=[SearchEntity.DATASET, SearchEntity.CARD],
        )
        assert sq.query == "revenue"
        assert sq.count == 10
        assert sq.offset == 5
        assert len(sq.entities) == 2

    def test_search_query_alias_serialization(self) -> None:
        """combineResults alias works for serialization."""
        sq = SearchQuery(combine_results=False)
        data = sq.model_dump(by_alias=True)
        assert data["combineResults"] is False


class TestSearchResult:
    """Tests for SearchResult model."""

    def test_search_result(self) -> None:
        """Deserialize a search result."""
        data = {
            "id": "ds-abc-123",
            "name": "Revenue Dataset",
            "type": "DATASET",
            "description": "Monthly revenue data",
            "owner": {"id": 42, "name": "Admin User"},
        }
        result = SearchResult.model_validate(data)
        assert result.id == "ds-abc-123"
        assert result.name == "Revenue Dataset"
        assert result.type == "DATASET"
        assert result.description == "Monthly revenue data"
        assert result.owner is not None
        assert result.owner["name"] == "Admin User"

    def test_search_result_defaults(self) -> None:
        """SearchResult defaults are empty strings and None."""
        result = SearchResult()
        assert result.id == ""
        assert result.name == ""
        assert result.type == ""
        assert result.description == ""
        assert result.owner is None
