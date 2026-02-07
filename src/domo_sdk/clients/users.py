"""User client for the Domo API."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/v1/users"


class UserClient(DomoAPIClient):
    """Manage Domo users.

    Docs: https://developer.domo.com/docs/users-api-reference/users-2
    """

    def create(self, user_request: dict, send_invite: bool = False) -> dict:
        """Create a new user."""
        return self._create(URL_BASE, user_request, params={"sendInvite": send_invite})

    def get(self, user_id: int) -> dict:
        """Retrieve a single user by ID."""
        return self._get(f"{URL_BASE}/{user_id}")

    def list(
        self,
        per_page: int = 50,
        offset: int = 0,
        limit: int = 0,
    ) -> Generator[dict, None, None]:
        """Paginating generator over users."""
        if per_page not in range(1, 51):
            raise ValueError("per_page must be between 1 and 50 (inclusive)")

        if limit:
            per_page = min(per_page, limit)

        params: dict[str, Any] = {"limit": per_page, "offset": offset}
        user_count = 0
        users: list[dict] = self._list(URL_BASE, params=params)

        while users:
            for user in users:
                yield user
                user_count += 1
                if limit and user_count >= limit:
                    return

            params["offset"] += per_page
            if limit and params["offset"] + per_page > limit:
                params["limit"] = limit - params["offset"]
            users = self._list(URL_BASE, params=params)

    def update(self, user_id: int, user_update: dict) -> dict:
        """Update an existing user."""
        return self._update(f"{URL_BASE}/{user_id}", user_update)

    def delete(self, user_id: int) -> None:
        """Delete a user."""
        self._delete(f"{URL_BASE}/{user_id}")
