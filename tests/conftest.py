"""Shared test fixtures for domo-sdk-python."""
from __future__ import annotations

import pytest

from domo_sdk.transport.async_transport import AsyncTransport
from domo_sdk.transport.auth import (
    DeveloperTokenCredentials,
    DeveloperTokenStrategy,
    OAuthCredentials,
    OAuthStrategy,
)
from domo_sdk.transport.sync_transport import SyncTransport


@pytest.fixture
def dev_token_credentials() -> DeveloperTokenCredentials:
    """Developer token credentials for testing."""
    return DeveloperTokenCredentials(
        token="test-token",
        instance_domain="test.domo.com",
    )


@pytest.fixture
def oauth_credentials() -> OAuthCredentials:
    """OAuth credentials for testing."""
    return OAuthCredentials(
        client_id="test-client-id",
        client_secret="test-client-secret",
    )


@pytest.fixture
def dev_token_strategy(dev_token_credentials: DeveloperTokenCredentials) -> DeveloperTokenStrategy:
    """Developer token auth strategy."""
    return DeveloperTokenStrategy(credentials=dev_token_credentials)


@pytest.fixture
def oauth_strategy(oauth_credentials: OAuthCredentials) -> OAuthStrategy:
    """OAuth auth strategy (mocked to avoid real token refresh)."""
    strategy = OAuthStrategy(credentials=oauth_credentials)
    # Pre-set a fake token so get_headers won't try to refresh
    strategy._access_token = "fake-oauth-token"
    strategy._token_expiration = 9999999999.0
    return strategy


@pytest.fixture
def dev_token_transport(dev_token_strategy: DeveloperTokenStrategy) -> SyncTransport:
    """Sync transport with developer token auth."""
    return SyncTransport(auth=dev_token_strategy)


@pytest.fixture
def oauth_transport(oauth_strategy: OAuthStrategy) -> SyncTransport:
    """Sync transport with OAuth auth."""
    return SyncTransport(auth=oauth_strategy)


@pytest.fixture
def async_dev_token_transport(dev_token_strategy: DeveloperTokenStrategy) -> AsyncTransport:
    """Async transport with developer token auth."""
    return AsyncTransport(auth=dev_token_strategy)


@pytest.fixture
def async_oauth_transport(oauth_strategy: OAuthStrategy) -> AsyncTransport:
    """Async transport with OAuth auth."""
    return AsyncTransport(auth=oauth_strategy)
