"""Tests for role models."""
from __future__ import annotations

from domo_sdk.models.roles import Authority, CreateRoleRequest, Role


class TestRole:
    """Tests for Role model."""

    def test_role_creation(self) -> None:
        """Create a Role from a dict."""
        data = {
            "id": 1,
            "name": "Admin",
            "description": "Full access role",
            "is_system": True,
            "user_count": 5,
            "authorities": [
                {"authority": "DATA_MANAGE", "grant_type": "ROLE"},
                {"authority": "USER_MANAGE", "grant_type": "ROLE"},
            ],
        }
        role = Role.model_validate(data)
        assert role.id == 1
        assert role.name == "Admin"
        assert role.description == "Full access role"
        assert role.is_system is True
        assert role.user_count == 5
        assert len(role.authorities) == 2
        assert role.authorities[0].authority == "DATA_MANAGE"

    def test_role_defaults(self) -> None:
        """Role defaults are set correctly."""
        role = Role(id=2)
        assert role.name == ""
        assert role.description == ""
        assert role.is_system is False
        assert role.user_count == 0
        assert role.authorities == []


class TestCreateRoleRequest:
    """Tests for CreateRoleRequest model."""

    def test_create_role_request(self) -> None:
        """Serialize a CreateRoleRequest."""
        req = CreateRoleRequest(name="Editor", description="Can edit content")
        data = req.model_dump()
        assert data["name"] == "Editor"
        assert data["description"] == "Can edit content"


class TestAuthority:
    """Tests for Authority model."""

    def test_authority(self) -> None:
        """Create an Authority model."""
        auth = Authority(authority="DATA_MANAGE", grant_type="ROLE")
        assert auth.authority == "DATA_MANAGE"
        assert auth.grant_type == "ROLE"

    def test_authority_default_grant_type(self) -> None:
        """grant_type defaults to empty string."""
        auth = Authority(authority="USER_MANAGE")
        assert auth.grant_type == ""
