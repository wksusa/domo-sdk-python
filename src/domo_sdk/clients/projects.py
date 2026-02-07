"""Projects and tasks client for the Domo API."""

from __future__ import annotations

from typing import Any

from domo_sdk.clients.base import DomoAPIClient

URL_BASE = "/v1/projects"


class ProjectsClient(DomoAPIClient):
    """Manage Domo projects, lists, and tasks.

    Docs: https://developer.domo.com/docs/projects-api-reference/projects
    """

    # ------------------------------------------------------------------
    # Projects
    # ------------------------------------------------------------------

    def create_project(self, project_data: dict) -> dict:
        """Create a new project."""
        return self._create(URL_BASE, project_data)

    def get_project(self, project_id: int) -> dict:
        """Retrieve a single project by ID."""
        return self._get(f"{URL_BASE}/{project_id}")

    def list_projects(self, per_page: int = 50, offset: int = 0) -> list:
        """List projects."""
        params: dict[str, Any] = {"limit": per_page, "offset": offset}
        return self._list(URL_BASE, params=params)

    def update_project(self, project_id: int, project_update: dict) -> dict:
        """Update an existing project."""
        return self._update(f"{URL_BASE}/{project_id}", project_update)

    def delete_project(self, project_id: int) -> None:
        """Delete a project."""
        self._delete(f"{URL_BASE}/{project_id}")

    # ------------------------------------------------------------------
    # Lists
    # ------------------------------------------------------------------

    def create_list(self, project_id: int, list_data: dict) -> dict:
        """Create a list within a project."""
        return self._create(f"{URL_BASE}/{project_id}/lists", list_data)

    def get_list(self, project_id: int, list_id: int) -> dict:
        """Retrieve a single list by ID."""
        return self._get(f"{URL_BASE}/{project_id}/lists/{list_id}")

    # ------------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------------

    def create_task(self, project_id: int, list_id: int, task_data: dict) -> dict:
        """Create a task within a project list."""
        return self._create(f"{URL_BASE}/{project_id}/lists/{list_id}/tasks", task_data)

    def get_task(self, project_id: int, list_id: int, task_id: int) -> dict:
        """Retrieve a single task by ID."""
        return self._get(f"{URL_BASE}/{project_id}/lists/{list_id}/tasks/{task_id}")

    def update_task(self, project_id: int, list_id: int, task_id: int, task_update: dict) -> dict:
        """Update an existing task."""
        return self._update(f"{URL_BASE}/{project_id}/lists/{list_id}/tasks/{task_id}", task_update)
