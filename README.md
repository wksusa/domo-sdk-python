# domo-sdk

[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://www.opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/domo-sdk)](https://pypi.org/project/domo-sdk/)

Modern Python SDK for the Domo API with async support, Pydantic models, and developer token auth.

Fork of [domoinc/domo-python-sdk](https://github.com/domoinc/domo-python-sdk) (pydomo), modernized with:

- **Async support** via `httpx` (`AsyncDomo` client)
- **Pydantic v2 models** for all API objects
- **Developer token auth** (access internal UI APIs like search)
- **OAuth2 auth** (backward compatible with pydomo)
- **22+ API clients** covering datasets, AI services, roles, search, cards, activity log, projects, alerts, workflows, dataflows, connectors, embed tokens, files, S3 export, and more
- **Typed exceptions** (`DomoAuthError`, `DomoNotFoundError`, `DomoRateLimitError`, etc.)
- **Modern build** with `hatchling`, `ruff`, `mypy`, `pytest`

## Installation

```bash
pip install domo-sdk

# With pandas support
pip install domo-sdk[pandas]

# For development
pip install domo-sdk[dev]
```

## Quick Start

### Sync Client

```python
from domo_sdk import Domo

# OAuth authentication
domo = Domo(client_id="your-id", client_secret="your-secret")

# Developer token authentication (recommended - full API access)
domo = Domo(developer_token="your-token", instance_domain="company.domo.com")

# Auto-detect from environment variables
domo = Domo.from_env()

# Use sub-clients
datasets = list(domo.datasets.list(limit=10))
roles = domo.roles.list()
result = domo.datasets.query("dataset-id", "SELECT * FROM table LIMIT 5")
```

### Async Client

```python
from domo_sdk import AsyncDomo

async with AsyncDomo.from_env() as domo:
    datasets = await domo.datasets.list(limit=10)
    result = await domo.datasets.query("dataset-id", "SELECT * FROM table LIMIT 5")

    # AI Services
    response = await domo.ai.text.generate({"prompt": "Summarize this data"})
    sql = await domo.ai.text.to_sql({"input": "Show top 10 customers by revenue"})
```

## Environment Variables

```bash
# Developer Token (recommended - full access including internal APIs)
DOMO_DEVELOPER_TOKEN=your-developer-token
DOMO_HOST=company.domo.com

# OAuth (alternative - public API only)
DOMO_CLIENT_ID=your-client-id
DOMO_CLIENT_SECRET=your-client-secret
```

## Available Clients

| Client | Description | Auth |
|--------|-------------|------|
| `domo.datasets` | Dataset CRUD, import/export, query, PDP, permissions, versioning | Both |
| `domo.users` | User management | Both |
| `domo.groups` | Group management | Both |
| `domo.pages` | Page and collection management | Both |
| `domo.streams` | Stream management and multi-part upload | Both |
| `domo.accounts` | Account management | Both |
| `domo.roles` | Role and authority management | Both |
| `domo.search` | Global search and dataset search | Dev token for full search |
| `domo.cards` | Card CRUD | Both |
| `domo.activity_log` | Audit log queries | Both |
| `domo.projects` | Projects, task lists, and tasks | Both |
| `domo.alerts` | Alert management and subscriptions | Both |
| `domo.workflows` | Workflow execution and permissions | Both |
| `domo.dataflows` | Dataflow execution | Both |
| `domo.connectors` | Connector execution triggers | Both |
| `domo.embed` | Embed token generation | Both |
| `domo.files` | File upload/download/permissions | Both |
| `domo.s3_export` | S3 export management | Both |
| `domo.ai` | AI Services (sub-clients below) | Both |
| `domo.ai.text` | Text generation, SQL, summarize, beastmode | Both |
| `domo.ai.messages` | Chat and tool-use completions | Both |
| `domo.ai.analysis` | Sentiment, classification, extraction | Both |
| `domo.ai.media` | Image-to-text, text/image embeddings | Both |

## Pydantic Models

All API objects have corresponding Pydantic v2 models:

```python
from domo_sdk.models.datasets import DataSet, Column, ColumnType, Schema, QueryResult
from domo_sdk.models.users import User, CreateUserRequest
from domo_sdk.models.roles import Role, Authority
from domo_sdk.models.ai import TextGenerationRequest, ChatRequest, ChatMessage
from domo_sdk.models.search import SearchQuery, SearchEntity
```

## Exception Handling

```python
from domo_sdk.exceptions import (
    DomoError,           # Base
    DomoAuthError,       # 401/403
    DomoNotFoundError,   # 404
    DomoRateLimitError,  # 429 (includes retry_after)
    DomoAPIError,        # Generic (includes status_code, response_body)
    DomoTimeoutError,    # Timeout
    DomoConnectionError, # Network issues
)

try:
    domo.datasets.get("nonexistent-id")
except DomoNotFoundError:
    print("Dataset not found")
except DomoRateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
```

## Migration from pydomo

See [MIGRATION.md](MIGRATION.md) for a detailed guide on migrating from pydomo to domo-sdk.

Key changes:
- `from pydomo import Domo` → `from domo_sdk import Domo`
- `Domo(client_id, client_secret)` still works (OAuth mode)
- New: `Domo(developer_token="...", instance_domain="...")` for developer token auth
- New: `Domo.from_env()` for environment variable auth
- New: `AsyncDomo` for async usage
- All models are now Pydantic v2 (not dict subclasses)

## Development

```bash
git clone https://github.com/wksusa/domo-sdk-python.git
cd domo-sdk-python
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check src/ tests/

# Type check
mypy src/domo_sdk/ --ignore-missing-imports
```

## License

MIT - See [LICENSE.txt](LICENSE.txt)
