"""Embed token models."""

from __future__ import annotations

from domo_sdk.models.base import DomoModel


class EmbedPermission(DomoModel):
    """Embed permission."""

    permission: str = ""  # "READ", "FILTER", "EXPORT"


class EmbedPolicy(DomoModel):
    """Embed policy with filters."""

    column: str = ""
    operator: str = ""
    values: list[str] = []


class EmbedToken(DomoModel):
    """Embed authentication token."""

    token: str = ""
    expiration: int = 0
    policies: list[EmbedPolicy] = []
    permissions: list[str] = []
