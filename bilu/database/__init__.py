from decouple import config

from bilu.database.mongo import MongoManager

db_manager = MongoManager(
    host=config('MONGODB_URI', 'mongodb://localhost:27017'),
    username=config('MONGODB_USERNAME', ''),
    password=config('MONGODB_PASSWORD', ''),
    database=config('MONGODB_DATABASE', None),
    min_pool_size=config('MONGODB_MIN_POOL_SIZE', 0),
    max_pool_size=config('MONGODB_MAX_POOL_SIZE', 100),
    read_preference=config(
        'MONGODB_READ_PREFERENCE',
        'secondaryPreferred'
    )
)
