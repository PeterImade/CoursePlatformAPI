from redis.asyncio import Redis
from .config import Config

redis = Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB_NO, decode_responses=True)

async def get_redis():
    try:
        yield redis
    finally:
        redis.close()
