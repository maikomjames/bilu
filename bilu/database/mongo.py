import logging
from typing import NoReturn

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from .base import DatabaseManager

logger = logging.getLogger(__name__)

settings = {}


class MongoManager(DatabaseManager):

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    def __init__(
        self,
        host='mongodb://localhost:27017',
        database=None,
        username=None,
        password=None,
        min_pool_size=0,
        max_pool_size=100,
        read_preference='secondaryPreferred'
    ) -> NoReturn:
        super().__init__()
        self.host = host
        self.username = username
        self.password = password
        self.min_pool_size = min_pool_size
        self.max_pool_size = max_pool_size
        self.read_preference = read_preference
        self.database = database

    async def connect(self) -> NoReturn:
        logger.debug('Connecting to MongoDB.')
        self.client = AsyncIOMotorClient(
            host=self.host,
            username=self.username,
            password=self.password,
            minPoolSize=self.min_pool_size,
            maxPoolSize=self.max_pool_size,
            readPreference=self.read_preference
        )
        self.db = self.client.get_database(self.database)
        logger.debug('Connected to MongoDB.')

    async def close_connection(self) -> NoReturn:
        logger.debug('Closing connection with MongoDB.')
        self.client.close()
        logger.debug('Closed connection with MongoDB.')
