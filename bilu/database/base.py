from abc import abstractmethod
from typing import NoReturn


class DatabaseManager(object):

    @property
    def client(self) -> NoReturn:
        raise NotImplementedError  # pragma: no cover

    @property
    def db(self) -> NoReturn:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    async def connect(self, path: str) -> NoReturn:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    async def close_connection(self) -> NoReturn:
        raise NotImplementedError  # pragma: no cover
