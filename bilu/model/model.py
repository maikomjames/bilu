from typing import NoReturn, Optional, Type

from bson.objectid import ObjectId
from pydantic import BaseModel as ODMModel
from pydantic import Extra, PrivateAttr
from pymongo.results import InsertOneResult

from .base import MetaBaseModel
from .database import MongoDatabaseModel


class BaseModel(ODMModel, MetaBaseModel):

    _id: Optional[Type[ObjectId]] = PrivateAttr()

    database_class = MongoDatabaseModel

    def __init__(self, **data) -> NoReturn:
        super().__init__(**data)
        self._id = data.get('_id')

    class Config:
        extra = Extra.ignore
        json_encoders = {
            ObjectId: lambda v: str(v)
        }

    @classmethod
    def get_model_name(cls) -> str:
        return cls.Meta.name

    def build_database_class(self) -> MongoDatabaseModel:
        return self.database_class(
            model=self
        )

    async def save(self) -> InsertOneResult:
        return await self.build_database_class().save(
            self.dict()
        )

    async def delete(self) -> None:
        return await self.build_database_class().delete()
