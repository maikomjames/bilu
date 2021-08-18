from unittest.mock import Mock, patch

import pytest

from bilu.database.mongo import MongoManager

pytestmark = pytest.mark.asyncio


class TestMongoManager:

    @pytest.fixture
    def database_manager(self):
        return MongoManager(
            host='mongod://10.30.40.50',
            username='xpto',
            password='123',
            min_pool_size=10,
            max_pool_size=12,
            read_preference='firstFound'
        )

    async def test_connect(self, database_manager):
        with patch(
            'bilu.database.mongo.AsyncIOMotorClient'
        ) as motor_client_mock:
            await database_manager.connect()

            motor_client_mock.assert_called_once_with(
                host='mongod://10.30.40.50',
                username='xpto',
                password='123',
                minPoolSize=10,
                maxPoolSize=12,
                readPreference='firstFound'
            )

    async def test_client_db(self, database_manager):
        with patch(
            'bilu.database.mongo.AsyncIOMotorClient',
            autospec=True
        ) as motor_client_mock:
            client = Mock()
            db = Mock()
            motor_client_mock.return_value = client
            client.get_database.return_value = db

            await database_manager.connect()
            assert database_manager.client == client
            assert database_manager.db == db

    async def test_close(self, database_manager):
        with patch.object(database_manager, 'client') as client_mock:
            await database_manager.close_connection()
            assert client_mock.close.called
