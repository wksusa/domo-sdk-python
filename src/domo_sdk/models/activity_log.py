"""Activity log / audit models."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from domo_sdk.models.base import DomoModel


class AuditFilter(DomoModel):
    """Audit log query filter parameters."""

    user: int | None = None
    start: datetime | None = None
    end: datetime | None = None
    limit: int = 50
    offset: int = 0


class AuditEntry(DomoModel):
    """Audit log entry."""

    user_name: str = Field(default="", alias="userName")
    user_id: int = Field(default=0, alias="userId")
    action_type: str = Field(default="", alias="actionType")
    object_type: str = Field(default="", alias="objectType")
    object_name: str = Field(default="", alias="objectName")
    object_id: str = Field(default="", alias="objectId")
    additional_comment: str = Field(default="", alias="additionalComment")
    time: datetime | None = None
    device: str = ""
    browser_details: str = Field(default="", alias="browserDetails")
    ip_address: str = Field(default="", alias="ipAddress")
