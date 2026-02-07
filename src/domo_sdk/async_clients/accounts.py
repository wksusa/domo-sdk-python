"""Async Account client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/accounts"


class AsyncAccountClient(AsyncDomoAPIClient):
    """Manage Domo accounts asynchronously.

    Docs: https://developer.domo.com/docs/accounts-api-reference/accounts
    """

    async def create(self, **kwargs: Any) -> dict:
        """Create a new account."""
        return await self._create(URL_BASE, kwargs)

    async def get(self, account_id: str) -> dict:
        """Retrieve a single account by ID."""
        return await self._get(f"{URL_BASE}/{account_id}")

    async def list(
        self,
        per_page: int = 50,
        offset: int = 0,
        limit: int = 0,
    ) -> list[dict]:
        """Return a full list of accounts, paginating internally."""
        if per_page not in range(1, 51):
            raise ValueError("per_page must be between 1 and 50 (inclusive)")

        if limit:
            per_page = min(per_page, limit)

        params: dict[str, Any] = {"limit": per_page, "offset": offset}
        result: list[dict] = []
        accounts: list[dict] = await self._list(URL_BASE, params=params)

        while accounts:
            for account in accounts:
                result.append(account)
                if limit and len(result) >= limit:
                    return result

            params["offset"] += per_page
            if limit and params["offset"] + per_page > limit:
                params["limit"] = limit - params["offset"]
            accounts = await self._list(URL_BASE, params=params)

        return result

    async def update(self, account_id: str, **kwargs: Any) -> dict:
        """Update an existing account."""
        return await self._update(f"{URL_BASE}/{account_id}", kwargs)

    async def delete(self, account_id: str) -> None:
        """Delete an account."""
        await self._delete(f"{URL_BASE}/{account_id}")
