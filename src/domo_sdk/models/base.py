"""Base model for all Domo SDK Pydantic models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class DomoModel(BaseModel):
    """Base model for all Domo API objects.

    Configured with:
    - extra="ignore": Ignore unknown fields from API responses
    - populate_by_name=True: Allow field population by alias or name
    - str_strip_whitespace=True: Strip whitespace from string fields
    """

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        str_strip_whitespace=True,
        protected_namespaces=(),
    )
