"""Workflows client for the Domo API."""

from __future__ import annotations

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/workflow/v1"


class WorkflowsClient(DomoAPIClient):
    """Manage Domo workflows.

    Docs: https://developer.domo.com/docs/workflows-api-reference/workflows
    """

    def start(self, message_data: dict) -> dict:
        """Start a workflow by sending a message."""
        return self._create(f"{URL_BASE}/instances/message", message_data)

    def get_instance(self, instance_id: str) -> dict:
        """Retrieve a workflow instance by ID."""
        return self._get(f"{URL_BASE}/instances/{instance_id}")

    def cancel(self, instance_id: str) -> None:
        """Cancel a running workflow instance."""
        self._create(f"{URL_BASE}/instances/{instance_id}/cancel", None)

    def get_permissions(self, model_id: int) -> list:
        """Get permissions for a workflow model."""
        return self._get(f"{URL_BASE}/models/{model_id}/permissions")

    def set_permissions(self, model_id: int, permissions: list) -> None:
        """Set permissions for a workflow model."""
        self._create(f"{URL_BASE}/models/{model_id}/permissions", permissions)
