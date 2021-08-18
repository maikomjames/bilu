# bilu

Asynchronous ODM (Object Document Mapper) for MongoDB

### Requirements

**Python**: 3.6 and later (tested against 3.6, 3.7, 3.8 and 3.9)

**MongoDB**: 4.0 and later

**pydantic**: 1.8.2 and later

Two direct dependencies:

- <a href="https://pydantic-docs.helpmanual.io/" target="_blank">pydantic</a>: makes
  data validation and schema definition both handy and elegant.

- <a href="https://motor.readthedocs.io/en/stable/" target="_blank">motor</a>: an
  asyncio MongoDB driver officially developed by the MongoDB team.


### Installation

```shell
pip install Bilu
```

### Environments
```shell
export MONGODB_URI='mongodb://localhost:27017'
export MONGODB_USERNAME=''
export MONGODB_PASSWORD=''
export MONGODB_DATABASE='test'
export MONGODB_MIN_POOL_SIZE=0
export MONGODB_MAX_POOL_SIZE=100
```

### Example

**Connecting to mongodb**
```python
from bilu.database import db_manager
db_manager.connect()
```

**Define model**
```python
from bilu.model import BaseModel

class TesteModel(BaseModel):
    attr_str: str
    attr_int: int

    class Meta:
        name = 'testemodel'
```

**Creating a document**
```python
data = {
    'attr_str': 'bla',
    'attr_int': 123
}
model = TesteModel(**data)
await model.save()
```

**Listing documents**
```python
await model.documents.list(attr_int=123)
```

**Getting a document**
```python
item = await model.documents.get(attr_int=123)
```

**Removing a document**
```python
await item.delete()
```
