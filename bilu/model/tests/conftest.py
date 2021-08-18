import pytest

from bilu.database import db_manager


@pytest.fixture
async def clean_db():

    async def _clean_db():
        collections = await db_manager.db.list_collection_names()

        for collection in collections:
            if collection.startswith('system'):
                continue
            await db_manager.db.drop_collection(collection)

    return _clean_db


@pytest.fixture
async def setup_db(clean_db):

    await db_manager.connect()

    await clean_db()
