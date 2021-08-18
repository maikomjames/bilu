import abc
from typing import Any, List, NoReturn


class DatabaseModel(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def find_one(self, query: dict) -> Any:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def get(self, projection=None, **query) -> Any:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def list(
        self,
        skip=0,
        limit=0,
        sort_by=None,
        projection=None,
        **query,
    ) -> List[Any]:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def save(self, data: dict) -> Any:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def delete(self) -> NoReturn:
        pass  # pragma: no cover


class MetaBaseModel:

    database_class = DatabaseModel

    @classmethod
    @property
    def documents(cls) -> DatabaseModel:
        return cls.database_class(model=cls)
