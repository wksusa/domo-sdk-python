# Migrating from pydomo to domo-sdk

## Import Changes

```python
# Before (pydomo)
from pydomo import Domo
from pydomo.datasets import DataSetRequest, Schema, Column, ColumnType

# After (domo-sdk)
from domo_sdk import Domo
from domo_sdk.models.datasets import DataSetRequest, Schema, Column, ColumnType
```

## Authentication

```python
# Before: OAuth only
domo = Domo('client-id', 'client-secret')

# After: OAuth (same pattern)
domo = Domo(client_id='client-id', client_secret='client-secret')

# After: Developer Token (NEW - recommended)
domo = Domo(developer_token='your-token', instance_domain='company.domo.com')

# After: From environment variables (NEW)
domo = Domo.from_env()
```

## Models

pydomo used `DomoObject` (dict subclass). domo-sdk uses Pydantic v2 models:

```python
# Before
from pydomo.datasets import DataSetRequest, Schema, Column
ds_request = DataSetRequest()
ds_request.name = 'My Dataset'
ds_request.schema = Schema([Column(ColumnType.STRING, 'name')])

# After
from domo_sdk.models.datasets import DataSetRequest, Schema, Column, ColumnType
ds_request = DataSetRequest(
    name='My Dataset',
    schema=Schema(columns=[Column(type=ColumnType.STRING, name='name')])
)
# Or use dicts directly - all client methods accept dicts
ds_request = {'name': 'My Dataset', 'schema': {'columns': [{'type': 'STRING', 'name': 'name'}]}}
```

## Client API

Client method signatures are largely unchanged:

```python
# Before
domo.datasets.get(dataset_id)
domo.datasets.create(dataset_request)
list(domo.datasets.list())

# After (same)
domo.datasets.get(dataset_id)
domo.datasets.create(dataset_request)
list(domo.datasets.list())
```

## Async Support (NEW)

```python
from domo_sdk import AsyncDomo

async with AsyncDomo.from_env() as domo:
    datasets = await domo.datasets.list()
    result = await domo.datasets.query(dataset_id, sql)
```

## Error Handling

```python
# Before: generic Exception
try:
    domo.datasets.get('bad-id')
except Exception as e:
    print(e)

# After: typed exceptions
from domo_sdk.exceptions import DomoNotFoundError, DomoAuthError
try:
    domo.datasets.get('bad-id')
except DomoNotFoundError:
    print("Not found")
except DomoAuthError:
    print("Auth failed")
```

## New Features

- **AI Services**: `domo.ai.text`, `domo.ai.messages`, `domo.ai.analysis`, `domo.ai.media`
- **Roles**: `domo.roles.list()`, `domo.roles.create()`, etc.
- **Search**: `domo.search.search_datasets(query)`
- **Cards**: `domo.cards.list()`, `domo.cards.get(id)`, etc.
- **Activity Log**: `domo.activity_log.query()`
- **Projects & Tasks**: `domo.projects.create_project()`, etc.
- **Alerts**: `domo.alerts.query()`, `domo.alerts.subscribe(id)`
- **Workflows**: `domo.workflows.start()`, etc.
- **Dataflows**: `domo.dataflows.execute(id)`, etc.
- **Embed Tokens**: `domo.embed.create_card_token(id)`
- **Files**: `domo.files.upload()`, etc.
