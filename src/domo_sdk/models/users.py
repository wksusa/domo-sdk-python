"""User models."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from domo_sdk.models.base import DomoModel


class CreateUserRequest(DomoModel):
    """Request to create a user."""

    name: str
    email: str
    role: str  # "Admin", "Privileged", "Participant"
    send_invite: bool = Field(default=False, alias="sendInvite")


class User(DomoModel):
    """User response from API."""

    id: int
    name: str = ""
    email: str = ""
    role: str = ""
    role_id: int | None = Field(default=None, alias="roleId")
    title: str = ""
    department: str = ""
    phone: str = ""
    image_uri: str = Field(default="", alias="imageUri")
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")
