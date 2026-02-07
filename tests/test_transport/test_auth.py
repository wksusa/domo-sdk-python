"""Tests for authentication strategies."""
from __future__ import annotations

from domo_sdk.transport.auth import (
    DeveloperTokenCredentials,
    DeveloperTokenStrategy,
    OAuthCredentials,
    OAuthStrategy,
)


class TestDeveloperTokenStrategy:
    """Tests for DeveloperTokenStrategy."""

    def test_developer_token_base_url(self, dev_token_strategy: DeveloperTokenStrategy) -> None:
        """Base URL should be https://{domain}/api."""
        assert dev_token_strategy.get_base_url() == "https://test.domo.com/api"

    def test_developer_token_base_url_strips_trailing_slash(self) -> None:
        """Base URL strips trailing slash from domain."""
        creds = DeveloperTokenCredentials(token="t", instance_domain="test.domo.com/")
        strategy = DeveloperTokenStrategy(credentials=creds)
        assert strategy.get_base_url() == "https://test.domo.com/api"

    def test_developer_token_headers(self, dev_token_strategy: DeveloperTokenStrategy) -> None:
        """Headers should include X-DOMO-Developer-Token."""
        headers = dev_token_strategy.get_headers()
        assert headers["X-DOMO-Developer-Token"] == "test-token"
        assert headers["Accept"] == "application/json"

    def test_developer_token_auth_mode(self, dev_token_strategy: DeveloperTokenStrategy) -> None:
        """auth_mode should be 'developer_token'."""
        assert dev_token_strategy.auth_mode == "developer_token"

    def test_developer_token_credentials_model(self) -> None:
        """DeveloperTokenCredentials pydantic model validates correctly."""
        creds = DeveloperTokenCredentials(token="abc123", instance_domain="my.domo.com")
        assert creds.token == "abc123"
        assert creds.instance_domain == "my.domo.com"


class TestOAuthStrategy:
    """Tests for OAuthStrategy."""

    def test_oauth_base_url(self, oauth_strategy: OAuthStrategy) -> None:
        """Default base URL should be https://api.domo.com."""
        assert oauth_strategy.get_base_url() == "https://api.domo.com"

    def test_oauth_auth_mode(self, oauth_strategy: OAuthStrategy) -> None:
        """auth_mode should be 'oauth'."""
        assert oauth_strategy.auth_mode == "oauth"

    def test_oauth_custom_host(self) -> None:
        """Custom api_host should be reflected in base URL."""
        creds = OAuthCredentials(client_id="id", client_secret="secret")
        strategy = OAuthStrategy(credentials=creds, api_host="custom.api.domo.com")
        assert strategy.get_base_url() == "https://custom.api.domo.com"

    def test_oauth_http_scheme(self) -> None:
        """use_https=False should produce http:// URL."""
        creds = OAuthCredentials(client_id="id", client_secret="secret")
        strategy = OAuthStrategy(credentials=creds, use_https=False)
        assert strategy.get_base_url() == "http://api.domo.com"

    def test_oauth_credentials_model(self) -> None:
        """OAuthCredentials pydantic model validates correctly."""
        creds = OAuthCredentials(
            client_id="test-id",
            client_secret="test-secret",
            scope=["data", "user"],
        )
        assert creds.client_id == "test-id"
        assert creds.client_secret == "test-secret"
        assert creds.scope == ["data", "user"]

    def test_oauth_credentials_model_defaults(self) -> None:
        """OAuthCredentials defaults scope to None."""
        creds = OAuthCredentials(client_id="id", client_secret="secret")
        assert creds.scope is None

    def test_oauth_headers_with_preset_token(self, oauth_strategy: OAuthStrategy) -> None:
        """Headers should include bearer token when token is pre-set."""
        headers = oauth_strategy.get_headers()
        assert headers["Authorization"] == "bearer fake-oauth-token"
        assert headers["Accept"] == "application/json"
