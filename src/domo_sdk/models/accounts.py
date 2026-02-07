"""Account models."""

from __future__ import annotations

from typing import Any

from domo_sdk.models.base import DomoModel


class AccountType(DomoModel):
    """Account type definition."""

    id: str = ""
    properties: dict[str, Any] = {}


class Account(DomoModel):
    """Account response from API."""

    id: str = ""
    name: str = ""
    valid: bool = True
    type: AccountType | None = None
