"""Generic pagination helpers."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any


def paginate_sync(
    fetch_fn: Any,
    per_page: int = 50,
    offset: int = 0,
    limit: int = 0,
) -> Generator[dict[str, Any], None, None]:
    """Generic sync pagination helper.

    Args:
        fetch_fn: Callable that takes (limit, offset) and returns a list.
        per_page: Number of items per page (max 50 for most Domo APIs).
        offset: Starting offset.
        limit: Maximum total items to return (0 = unlimited).

    Yields:
        Individual items from each page.
    """
    if per_page < 1 or per_page > 50:
        per_page = 50

    effective_per_page = min(per_page, limit) if limit else per_page
    count = 0

    while True:
        page = fetch_fn(effective_per_page, offset)
        if not page:
            break

        for item in page:
            yield item
            count += 1
            if limit and count >= limit:
                return

        if len(page) < effective_per_page:
            break

        offset += len(page)
        if limit:
            remaining = limit - count
            effective_per_page = min(per_page, remaining)


async def paginate_async(
    fetch_fn: Any,
    per_page: int = 50,
    offset: int = 0,
    limit: int = 0,
) -> list[dict[str, Any]]:
    """Generic async pagination helper.

    Args:
        fetch_fn: Async callable that takes (limit, offset) and returns a list.
        per_page: Number of items per page.
        offset: Starting offset.
        limit: Maximum total items (0 = unlimited).

    Returns:
        List of all paginated items.
    """
    if per_page < 1 or per_page > 50:
        per_page = 50

    effective_per_page = min(per_page, limit) if limit else per_page
    results: list[dict[str, Any]] = []

    while True:
        page = await fetch_fn(effective_per_page, offset)
        if not page:
            break

        results.extend(page)

        if limit and len(results) >= limit:
            return results[:limit]

        if len(page) < effective_per_page:
            break

        offset += len(page)
        if limit:
            remaining = limit - len(results)
            effective_per_page = min(per_page, remaining)

    return results
