"""Roles client for the Domo API."""

from __future__ import annotations

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/authorization/v1/roles"


class RolesClient(DomoAPIClient):
    """Manage Domo roles and authorities.

    Docs: https://developer.domo.com/docs/roles-api-reference/roles
    """

    def list(self) -> list:
        """List all roles."""
        return self._list(URL_BASE)

    def create(self, role_data: dict) -> dict:
        """Create a new role."""
        return self._create(URL_BASE, role_data)

    def get(self, role_id: int) -> dict:
        """Retrieve a single role by ID."""
        url = f"{URL_BASE}/{role_id}"
        return self._get(url)

    def delete(self, role_id: int) -> None:
        """Delete a role."""
        url = f"{URL_BASE}/{role_id}"
        self._delete(url)

    def list_authorities(self, role_id: int) -> list:
        """List authorities granted to a role."""
        url = f"{URL_BASE}/{role_id}/authorities"
        return self._get(url)

    def update_authorities(self, role_id: int, authorities: list[dict]) -> dict:
        """Update (patch) the authorities for a role."""
        url = f"{URL_BASE}/{role_id}/authorities"
        return self._update(url, authorities, method="PATCH")
