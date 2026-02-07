"""Common/shared model types."""

from __future__ import annotations

from enum import Enum

from domo_sdk.models.base import DomoModel


class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class Pagination(DomoModel):
    """Pagination parameters."""

    limit: int = 50
    offset: int = 0


class Owner(DomoModel):
    """Common owner reference."""

    id: int
    name: str = ""
