from redis.asyncio import Redis

redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)
async def get_redis() -> Redis:
    try:
        yield redis
    finally:
        await redis.close()
