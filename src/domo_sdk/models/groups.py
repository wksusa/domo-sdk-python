"""Group models."""

from __future__ import annotations

from domo_sdk.models.base import DomoModel


class CreateGroupRequest(DomoModel):
    """Request to create a group."""

    name: str
    active: bool = True


class Group(DomoModel):
    """Group response from API."""

    id: int
    name: str = ""
    active: bool = True
    default: bool = False
    user_count: int = 0
