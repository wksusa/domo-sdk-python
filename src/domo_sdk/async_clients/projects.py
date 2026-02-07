"""Async Projects and Tasks client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.async_clients.base import AsyncDomoAPIClient

URL_BASE = "/v1/projects"


class AsyncProjectsClient(AsyncDomoAPIClient):
    """Manage Domo projects, lists, and tasks asynchronously.

    Docs: https://developer.domo.com/docs/projects-api-reference/projects
    """

    # ------------------------------------------------------------------
    # Projects
    # ------------------------------------------------------------------

    async def create_project(self, project_request: dict) -> dict:
        """Create a new project."""
        return await self._create(URL_BASE, project_request)

    async def get_project(self, project_id: int) -> dict:
        """Retrieve a single project by ID."""
        return await self._get(f"{URL_BASE}/{project_id}")

    async def list_projects(self, per_page: int = 50, offset: int = 0) -> list:
        """List all projects."""
        params: dict[str, Any] = {"limit": per_page, "offset": offset}
        return await self._list(URL_BASE, params=params)

    async def update_project(self, project_id: int, project_update: dict) -> dict:
        """Update an existing project."""
        return await self._update(f"{URL_BASE}/{project_id}", project_update)

    async def delete_project(self, project_id: int) -> None:
        """Delete a project."""
        await self._delete(f"{URL_BASE}/{project_id}")

    # ------------------------------------------------------------------
    # Lists
    # ------------------------------------------------------------------

    async def create_list(self, project_id: int, list_request: dict) -> dict:
        """Create a new list within a project."""
        url = f"{URL_BASE}/{project_id}/lists"
        return await self._create(url, list_request)

    async def get_list(self, project_id: int, list_id: int) -> dict:
        """Retrieve a specific list from a project."""
        url = f"{URL_BASE}/{project_id}/lists/{list_id}"
        return await self._get(url)

    # ------------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------------

    async def create_task(self, project_id: int, list_id: int, task_request: dict) -> dict:
        """Create a new task within a project list."""
        url = f"{URL_BASE}/{project_id}/lists/{list_id}/tasks"
        return await self._create(url, task_request)

    async def get_task(self, project_id: int, list_id: int, task_id: int) -> dict:
        """Retrieve a specific task."""
        url = f"{URL_BASE}/{project_id}/lists/{list_id}/tasks/{task_id}"
        return await self._get(url)

    async def update_task(
        self,
        project_id: int,
        list_id: int,
        task_id: int,
        task_update: dict,
    ) -> dict:
        """Update an existing task."""
        url = f"{URL_BASE}/{project_id}/lists/{list_id}/tasks/{task_id}"
        return await self._update(url, task_update)
