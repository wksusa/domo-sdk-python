"""Domo <-> pandas type mapping utilities."""

from __future__ import annotations

# Domo column types that represent dates
DATE_TYPES = {"DATE", "DATETIME"}

# Mapping from Domo column types to pandas dtypes
DOMO_TO_PANDAS: dict[str, str] = {
    "STRING": "object",
    "DECIMAL": "float64",
    "LONG": "Int64",
    "DOUBLE": "float64",
    "DATE": "datetime64[ns]",
    "DATETIME": "datetime64[ns]",
}


def is_date_type(domo_type: str) -> bool:
    """Check if a Domo column type is a date type."""
    return domo_type.upper() in DATE_TYPES


def convert_domo_type_to_pandas_type(domo_type: str) -> str:
    """Convert a Domo column type to a pandas dtype string."""
    return DOMO_TO_PANDAS.get(domo_type.upper(), "object")
