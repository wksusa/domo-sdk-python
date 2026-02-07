"""Dataflow models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from domo_sdk.models.base import DomoModel


class DataflowExecution(DomoModel):
    """Dataflow execution."""

    id: int | None = None
    begin_time: datetime | None = Field(default=None, alias="beginTime")
    end_time: datetime | None = Field(default=None, alias="endTime")
    current_state: str = Field(default="", alias="currentState")


class Dataflow(DomoModel):
    """Dataflow response from API."""

    id: int
    name: str = ""
    description: str = ""
    type: str = ""  # "ETL", "REDSHIFT", "MYSQL", etc.
    owner: dict[str, Any] | None = None
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")
    last_execution: DataflowExecution | None = Field(default=None, alias="lastExecution")
