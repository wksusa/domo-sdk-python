"""Domo SDK — Modern Python SDK for the Domo API.

Usage:
    # Sync client with OAuth
    from domo_sdk import Domo
    domo = Domo(client_id="...", client_secret="...")

    # Sync client with developer token
    domo = Domo(developer_token="...", instance_domain="instance.domo.com")

    # Auto-detect from environment variables
    domo = Domo.from_env()

    # Async client
    from domo_sdk import AsyncDomo
    async with AsyncDomo.from_env() as domo:
        datasets = await domo.datasets.list()
"""

from domo_sdk._version import __version__
from domo_sdk.domo import AsyncDomo, Domo

__all__ = ["Domo", "AsyncDomo", "__version__"]
