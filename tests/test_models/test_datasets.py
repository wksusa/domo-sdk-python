"""Tests for dataset models."""
from __future__ import annotations

from domo_sdk.models.datasets import (
    Column,
    ColumnType,
    DataSet,
    DataSetRequest,
    FilterOperator,
    PolicyFilter,
    QueryResult,
    Schema,
    UpdateMethod,
)


class TestColumn:
    """Tests for Column model."""

    def test_column_creation(self) -> None:
        """Create a Column with type and name."""
        col = Column(type=ColumnType.STRING, name="customer_name")
        assert col.type == ColumnType.STRING
        assert col.name == "customer_name"

    def test_column_type_enum(self) -> None:
        """Verify all ColumnType enum values exist."""
        expected = {"STRING", "DECIMAL", "LONG", "DOUBLE", "DATE", "DATETIME"}
        actual = {ct.value for ct in ColumnType}
        assert actual == expected


class TestSchema:
    """Tests for Schema model."""

    def test_schema_creation(self) -> None:
        """Create a Schema with a list of columns."""
        columns = [
            Column(type=ColumnType.STRING, name="name"),
            Column(type=ColumnType.LONG, name="age"),
            Column(type=ColumnType.DATE, name="created"),
        ]
        schema = Schema(columns=columns)
        assert len(schema.columns) == 3
        assert schema.columns[0].name == "name"
        assert schema.columns[1].type == ColumnType.LONG
        assert schema.columns[2].type == ColumnType.DATE


class TestDataSetRequest:
    """Tests for DataSetRequest model."""

    def test_dataset_request_serialization(self) -> None:
        """DataSetRequest serializes to and from dict."""
        schema = Schema(
            columns=[
                Column(type=ColumnType.STRING, name="col1"),
                Column(type=ColumnType.DECIMAL, name="col2"),
            ]
        )
        req = DataSetRequest(name="Test Dataset", description="A test", schema=schema)
        data = req.model_dump()
        assert data["name"] == "Test Dataset"
        assert data["description"] == "A test"
        assert len(data["schema"]["columns"]) == 2

        # Round-trip
        req2 = DataSetRequest.model_validate(data)
        assert req2.name == req.name
        assert req2.schema is not None
        assert len(req2.schema.columns) == 2


class TestDataSet:
    """Tests for DataSet model."""

    def test_dataset_deserialization(self) -> None:
        """Create DataSet from API-like dict with camelCase aliases."""
        api_data = {
            "id": "abc-123",
            "name": "Sales Data",
            "description": "Quarterly sales",
            "rows": 1000,
            "columns": 5,
            "createdAt": "2024-01-15T10:30:00Z",
            "updatedAt": "2024-06-01T14:00:00Z",
            "dataCurrentAt": "2024-06-01T12:00:00Z",
            "pdpEnabled": True,
            "owner": {"id": 42, "name": "Admin"},
            "schema": {
                "columns": [
                    {"type": "STRING", "name": "region"},
                    {"type": "DECIMAL", "name": "revenue"},
                ]
            },
        }
        ds = DataSet.model_validate(api_data)
        assert ds.id == "abc-123"
        assert ds.name == "Sales Data"
        assert ds.rows == 1000
        assert ds.columns == 5
        assert ds.pdp_enabled is True
        assert ds.created_at is not None
        assert ds.updated_at is not None
        assert ds.data_current_at is not None
        assert ds.owner is not None
        assert ds.owner["id"] == 42
        assert ds.schema is not None
        assert len(ds.schema.columns) == 2
        assert ds.schema.columns[0].name == "region"


class TestQueryResult:
    """Tests for QueryResult model."""

    def test_query_result(self) -> None:
        """QueryResult deserializes from API response."""
        data = {
            "columns": ["name", "age", "city"],
            "rows": [["Alice", "30", "NYC"], ["Bob", "25", "LA"]],
            "numRows": 2,
            "numColumns": 3,
        }
        result = QueryResult.model_validate(data)
        assert result.columns == ["name", "age", "city"]
        assert len(result.rows) == 2
        assert result.num_rows == 2
        assert result.num_columns == 3


class TestPolicyFilter:
    """Tests for PolicyFilter model."""

    def test_policy_filter_with_not_alias(self) -> None:
        """The 'not' JSON key maps to not_ field."""
        data = {
            "column": "region",
            "values": ["US", "CA"],
            "operator": "EQUALS",
            "not": True,
        }
        pf = PolicyFilter.model_validate(data)
        assert pf.not_ is True
        assert pf.column == "region"
        assert pf.values == ["US", "CA"]
        assert pf.operator == FilterOperator.EQUALS

    def test_policy_filter_not_default(self) -> None:
        """not_ defaults to False."""
        pf = PolicyFilter(column="col", values=["v"], operator=FilterOperator.LIKE)
        assert pf.not_ is False


class TestFilterOperator:
    """Tests for FilterOperator enum."""

    def test_filter_operator_enum(self) -> None:
        """All FilterOperator values should be present."""
        expected = {
            "EQUALS", "LIKE", "GREATER_THAN", "LESS_THAN",
            "GREATER_THAN_EQUAL", "LESS_THAN_EQUAL", "BETWEEN",
            "BEGINS_WITH", "ENDS_WITH", "CONTAINS",
        }
        actual = {op.value for op in FilterOperator}
        assert actual == expected


class TestUpdateMethod:
    """Tests for UpdateMethod enum."""

    def test_update_method_enum(self) -> None:
        """APPEND and REPLACE should be the only values."""
        assert UpdateMethod.APPEND.value == "APPEND"
        assert UpdateMethod.REPLACE.value == "REPLACE"
        assert len(UpdateMethod) == 2
