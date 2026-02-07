"""Authentication strategies for Domo API."""

from __future__ import annotations

import base64
import json
import logging
import threading
import time
from abc import ABC, abstractmethod
from typing import Any

import httpx
import requests
from pydantic import BaseModel

from domo_sdk.exceptions import DomoAuthError

logger = logging.getLogger("domo_sdk.transport.auth")


class OAuthCredentials(BaseModel):
    """OAuth2 client credentials."""

    client_id: str
    client_secret: str
    scope: list[str] | None = None


class DeveloperTokenCredentials(BaseModel):
    """Developer token credentials."""

    token: str
    instance_domain: str


class AuthStrategy(ABC):
    """Abstract base class for authentication strategies."""

    @abstractmethod
    def get_base_url(self) -> str:
        """Return the base URL for API requests."""

    @abstractmethod
    def get_headers(self) -> dict[str, str]:
        """Return authentication headers (sync)."""

    @abstractmethod
    async def get_headers_async(self) -> dict[str, str]:
        """Return authentication headers (async)."""

    @property
    @abstractmethod
    def auth_mode(self) -> str:
        """Return the authentication mode identifier."""


class OAuthStrategy(AuthStrategy):
    """OAuth2 client credentials authentication.

    Uses api.domo.com for all calls. Automatically refreshes
    tokens based on JWT expiry parsing.
    """

    def __init__(
        self,
        credentials: OAuthCredentials,
        api_host: str = "api.domo.com",
        use_https: bool = True,
        request_timeout: float | None = None,
    ) -> None:
        self._credentials = credentials
        self._api_host = api_host
        self._use_https = use_https
        self._request_timeout = request_timeout
        self._access_token: str | None = None
        self._token_expiration: float = 0
        self._lock = threading.Lock()
        self._async_lock: Any = None  # Lazy init asyncio.Lock

    @property
    def auth_mode(self) -> str:
        return "oauth"

    def get_base_url(self) -> str:
        scheme = "https" if self._use_https else "http"
        return f"{scheme}://{self._api_host}"

    def _is_token_expired(self) -> bool:
        return not self._access_token or time.time() >= (self._token_expiration - 60)

    def _extract_expiration(self, access_token: str) -> float:
        try:
            parts = access_token.split(".")
            if len(parts) < 2:
                return 0
            payload_bytes = base64.urlsafe_b64decode(parts[1] + "==")
            payload = json.loads(payload_bytes.decode("utf-8"))
            return float(payload.get("exp", 0))
        except Exception:
            logger.debug("Failed to parse token expiration, defaulting to 0")
            return 0

    def _refresh_token_sync(self) -> None:
        with self._lock:
            if not self._is_token_expired():
                return

            scope = " ".join(self._credentials.scope) if self._credentials.scope else None
            kwargs: dict[str, Any] = {
                "method": "POST",
                "url": f"{self.get_base_url()}/oauth/token",
                "data": {"grant_type": "client_credentials", "scope": scope},
                "auth": (self._credentials.client_id, self._credentials.client_secret),
            }
            if self._request_timeout:
                kwargs["timeout"] = self._request_timeout

            response = requests.request(**kwargs)
            if response.status_code == 200:
                data = response.json()
                self._access_token = data["access_token"]
                self._token_expiration = self._extract_expiration(self._access_token)
                logger.debug("OAuth token refreshed (sync)")
            else:
                raise DomoAuthError(f"OAuth token refresh failed: {response.text}", status_code=response.status_code)

    async def _refresh_token_async(self) -> None:
        import asyncio

        if self._async_lock is None:
            self._async_lock = asyncio.Lock()

        async with self._async_lock:
            if not self._is_token_expired():
                return

            scope = " ".join(self._credentials.scope) if self._credentials.scope else None
            timeout = httpx.Timeout(self._request_timeout) if self._request_timeout else httpx.Timeout(30.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    f"{self.get_base_url()}/oauth/token",
                    data={"grant_type": "client_credentials", "scope": scope},
                    auth=(self._credentials.client_id, self._credentials.client_secret),
                )
                if response.status_code == 200:
                    data = response.json()
                    self._access_token = data["access_token"]
                    self._token_expiration = self._extract_expiration(self._access_token)
                    logger.debug("OAuth token refreshed (async)")
                else:
                    raise DomoAuthError(
                        f"OAuth token refresh failed: {response.text}",
                        status_code=response.status_code,
                    )

    def get_headers(self) -> dict[str, str]:
        if self._is_token_expired():
            self._refresh_token_sync()
        return {
            "Authorization": f"bearer {self._access_token}",
            "Accept": "application/json",
        }

    async def get_headers_async(self) -> dict[str, str]:
        if self._is_token_expired():
            await self._refresh_token_async()
        return {
            "Authorization": f"bearer {self._access_token}",
            "Accept": "application/json",
        }


class DeveloperTokenStrategy(AuthStrategy):
    """Developer token authentication.

    Uses instance-specific domain (e.g. wksusa.domo.com/api).
    Provides access to internal UI APIs (search, extended dataset ops).
    """

    def __init__(self, credentials: DeveloperTokenCredentials) -> None:
        self._credentials = credentials

    @property
    def auth_mode(self) -> str:
        return "developer_token"

    def get_base_url(self) -> str:
        domain = self._credentials.instance_domain.rstrip("/")
        if not domain.startswith("http"):
            domain = f"https://{domain}"
        return f"{domain}/api"

    def get_headers(self) -> dict[str, str]:
        return {
            "X-DOMO-Developer-Token": self._credentials.token,
            "Accept": "application/json",
        }

    async def get_headers_async(self) -> dict[str, str]:
        return self.get_headers()
