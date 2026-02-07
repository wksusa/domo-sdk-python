"""Schema detection and conversion utilities."""

from __future__ import annotations

from typing import Any


def detect_column_type(value: Any) -> str:
    """Detect a Domo column type from a Python value."""
    if isinstance(value, bool):
        return "STRING"
    elif isinstance(value, int):
        return "LONG"
    elif isinstance(value, float):
        return "DOUBLE"
    else:
        return "STRING"


def dataframe_to_schema(df: Any) -> dict[str, Any]:
    """Convert a pandas DataFrame to a Domo schema dict.

    Args:
        df: A pandas DataFrame.

    Returns:
        Schema dict with columns list.
    """
    try:
        import pandas  # noqa: F401 — validates pandas is available
    except ImportError:
        raise ImportError(
            "pandas is required for dataframe_to_schema. Install with: pip install domo-sdk[pandas]"
        ) from None

    PANDAS_TO_DOMO = {
        "int64": "LONG",
        "Int64": "LONG",
        "float64": "DOUBLE",
        "object": "STRING",
        "bool": "STRING",
        "datetime64[ns]": "DATETIME",
        "datetime64[ns, UTC]": "DATETIME",
    }

    columns = []
    for col_name, dtype in df.dtypes.items():
        domo_type = PANDAS_TO_DOMO.get(str(dtype), "STRING")
        columns.append({"type": domo_type, "name": str(col_name)})

    return {"columns": columns}
