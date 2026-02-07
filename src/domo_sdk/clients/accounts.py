"""Account client for the Domo API."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/v1/accounts"


class AccountClient(DomoAPIClient):
    """Manage Domo accounts.

    Docs: https://developer.domo.com/docs/accounts-api-reference/accounts-2
    """

    def create(self, **kwargs: Any) -> dict:
        """Create a new account."""
        return self._create(URL_BASE, kwargs)

    def get(self, account_id: str) -> dict:
        """Retrieve a single account by ID."""
        return self._get(f"{URL_BASE}/{account_id}")

    def list(
        self,
        per_page: int = 50,
        offset: int = 0,
        limit: int = 0,
    ) -> Generator[dict, None, None]:
        """Paginating generator over accounts."""
        if per_page not in range(1, 51):
            raise ValueError("per_page must be between 1 and 50 (inclusive)")

        if limit:
            per_page = min(per_page, limit)

        params: dict[str, Any] = {"limit": per_page, "offset": offset}
        account_count = 0
        accounts: list[dict] = self._list(URL_BASE, params=params)

        while accounts:
            for account in accounts:
                yield account
                account_count += 1
                if limit and account_count >= limit:
                    return

            params["offset"] += per_page
            if limit and params["offset"] + per_page > limit:
                params["limit"] = limit - params["offset"]
            accounts = self._list(URL_BASE, params=params)

    def update(self, account_id: str, **kwargs: Any) -> dict:
        """Update an existing account."""
        return self._update(f"{URL_BASE}/{account_id}", kwargs, method="PATCH")

    def delete(self, account_id: str) -> None:
        """Delete an account."""
        self._delete(f"{URL_BASE}/{account_id}")
