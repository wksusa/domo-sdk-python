"""Async Workflows client for the Domo API."""

from __future__ import annotations

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/workflows"


class AsyncWorkflowsClient(AsyncDomoAPIClient):
    """Manage Domo workflows asynchronously.

    Docs: https://developer.domo.com/docs/workflows-api-reference/workflows
    """

    async def start(self, workflow_id: int, body: dict | None = None) -> dict:
        """Start a workflow execution."""
        url = f"{URL_BASE}/{workflow_id}/start"
        return await self._create(url, body or {})

    async def get_instance(self, workflow_id: int, instance_id: int) -> dict:
        """Get a specific workflow instance."""
        url = f"{URL_BASE}/{workflow_id}/instances/{instance_id}"
        return await self._get(url)

    async def cancel(self, workflow_id: int, instance_id: int) -> None:
        """Cancel a running workflow instance."""
        url = f"{URL_BASE}/{workflow_id}/instances/{instance_id}/cancel"
        await self._create(url, {})

    async def get_permissions(self, workflow_id: int) -> list:
        """Get permissions for a workflow."""
        url = f"{URL_BASE}/{workflow_id}/permissions"
        return await self._get(url)

    async def set_permissions(self, workflow_id: int, permissions: list) -> None:
        """Set permissions for a workflow."""
        url = f"{URL_BASE}/{workflow_id}/permissions"
        await self._update(url, permissions)
