"""Async Roles client for the Domo API."""

from __future__ import annotations

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/authorization/v1/roles"


class AsyncRolesClient(AsyncDomoAPIClient):
    """Manage Domo roles and authorities asynchronously.

    Docs: https://developer.domo.com/docs/roles-api-reference/roles
    """

    async def list(self) -> list:
        """List all roles."""
        return await self._list(URL_BASE)

    async def create(self, role_data: dict) -> dict:
        """Create a new role."""
        return await self._create(URL_BASE, role_data)

    async def get(self, role_id: int) -> dict:
        """Retrieve a single role by ID."""
        url = f"{URL_BASE}/{role_id}"
        return await self._get(url)

    async def delete(self, role_id: int) -> None:
        """Delete a role."""
        url = f"{URL_BASE}/{role_id}"
        await self._delete(url)

    async def list_authorities(self, role_id: int) -> list:
        """List authorities granted to a role."""
        url = f"{URL_BASE}/{role_id}/authorities"
        return await self._get(url)

    async def update_authorities(self, role_id: int, authorities: list[dict]) -> dict:
        """Update (patch) the authorities for a role."""
        url = f"{URL_BASE}/{role_id}/authorities"
        return await self._update(url, authorities, method="PATCH")
