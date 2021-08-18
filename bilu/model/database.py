import logging
from typing import Any, List, NoReturn
from bilu.database import db_manager

from bilu.model.base import DatabaseModel

logger = logging.getLogger(__name__)


class MongoDatabaseModel(DatabaseModel):

    def __init__(self, model, *args, **kwargs) -> NoReturn:
        self.model = model

    def get_collection(self) -> Any:
        return db_manager.db.get_collection(
            self.model.get_model_name()
        )

    async def find_one(self, query: dict) -> Any:
        result = await self.get_collection().find_one(
            query
        )

        if result:
            return self.model(**result)

    async def get(self, projection=None, **query) -> Any:
        result = await self.get_collection().find_one(
            query,
            projection=projection
        )

        if result:
            return self.model(**result)

    async def list(
        self,
        skip=0,
        limit=0,
        sort_by=None,
        projection=None,
        **query,
    ) -> List[Any]:
        cursor = self.get_collection().find(
            query or {}
        )
        result = []

        async for document in cursor:
            result.append(self.model(**document))

        return result

    async def _insert(self, data: dict) -> Any:
        logger.info('Save new document in collection "{}"'.format(
            self.model.get_model_name()
        ))
        result_insert = await self.get_collection().insert_one(
            data
        )
        self.model._id = result_insert.inserted_id
        return result_insert

    async def _update(self, data: dict) -> Any:
        logger.info('Edit document "{}" in collection "{}"'.format(
            str(self.model._id), self.model.get_model_name()
        ))
        result = await self.get_collection().update_one(
            {'_id': self.model._id},
            {'$set': data},
            upsert=False
        )
        return result

    async def save(self, data: dict) -> Any:
        self.model.validate(data)

        if self.model._id:
            return await self._update(data)
        else:
            return await self._insert(data)

    async def delete(self) -> NoReturn:
        await self.get_collection().delete_one(
            {'_id': self.model._id}
        )
