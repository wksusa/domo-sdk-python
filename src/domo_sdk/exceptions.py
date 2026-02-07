"""Domo SDK exception hierarchy."""

from __future__ import annotations


class DomoError(Exception):
    """Base exception for all Domo SDK errors."""

    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__(self.message)


class DomoAuthError(DomoError):
    """Authentication or authorization failure (HTTP 401/403)."""

    def __init__(self, message: str = "Authentication failed", status_code: int = 401) -> None:
        self.status_code = status_code
        super().__init__(message)


class DomoNotFoundError(DomoError):
    """Resource not found (HTTP 404)."""

    def __init__(self, message: str = "Resource not found", resource_type: str = "", resource_id: str = "") -> None:
        self.resource_type = resource_type
        self.resource_id = resource_id
        if resource_type and resource_id:
            message = f"{resource_type} '{resource_id}' not found"
        super().__init__(message)


class DomoRateLimitError(DomoError):
    """Rate limit exceeded (HTTP 429)."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: float | None = None) -> None:
        self.retry_after = retry_after
        if retry_after:
            message = f"{message}. Retry after {retry_after}s"
        super().__init__(message)


class DomoValidationError(DomoError):
    """Client-side validation error."""

    def __init__(self, message: str = "Validation error", field: str = "", details: str = "") -> None:
        self.field = field
        self.details = details
        if field:
            message = f"Validation error on '{field}': {details}" if details else f"Validation error on '{field}'"
        super().__init__(message)


class DomoAPIError(DomoError):
    """Generic API error with status code and response body."""

    def __init__(
        self,
        message: str = "API error",
        status_code: int = 0,
        response_body: str = "",
    ) -> None:
        self.status_code = status_code
        self.response_body = response_body
        if status_code:
            message = (
                f"API error (HTTP {status_code}): {response_body}"
                if response_body
                else f"API error (HTTP {status_code})"
            )
        super().__init__(message)


class DomoTimeoutError(DomoError):
    """Request timed out."""

    def __init__(self, message: str = "Request timed out", url: str = "", timeout: float = 0) -> None:
        self.url = url
        self.timeout = timeout
        if url and timeout:
            message = f"Request to {url} timed out after {timeout}s"
        super().__init__(message)


class DomoConnectionError(DomoError):
    """Connection error (network issues)."""

    def __init__(self, message: str = "Connection error", url: str = "") -> None:
        self.url = url
        if url:
            message = f"Connection error for {url}"
        super().__init__(message)
