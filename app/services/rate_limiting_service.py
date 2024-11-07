import time
import asyncio 
from redis.asyncio import Redis

from app.core.exceptions import UserNotFound
from ..repositories.user import CRUDAuthUser
from ..core.config import Config
from ..schemas.otp import ResendOTPRequest 

MAX_TOKEN = Config.OTP_MAX_TOKEN
REPLENISH_INTERVAL = Config.REPLENISH_INTERVAL

class RateLimiter:  
    def __init__(self, redis: Redis):
        self.redis = redis  
    
    async def handle_requests(self, user_email: str) -> bool: 
        bucket_key = f"bucket_key:{user_email}"

        # Initialize bucket if it doesn't exist
        current_token = await self.redis.get(bucket_key)
        if current_token is None:
            await self.redis.set(bucket_key, MAX_TOKEN)
            current_token = MAX_TOKEN
        else:
            current_token = int(current_token)
        
        # Allow request if there are tokens available
        if current_token > 0:
            await self.redis.decrby(bucket_key, 1)
            return True
        return False
        
    async def replenish_bucket(self, user_email: str): 
        bucket_key = f"bucket_key:{user_email}" 
        current_token = int(await self.redis.get(bucket_key) or 0)

        # Replenish tokens until the bucket is full
        while current_token < MAX_TOKEN:
            await asyncio.sleep(REPLENISH_INTERVAL)  # Wait for the defined interval
            await self.redis.incr(bucket_key, 1)
            current_token += 1

    async def replenish_tokens_periodically(self, user_email: str):
        while True:
            await self.replenish_bucket(user_email)
            await asyncio.sleep(REPLENISH_INTERVAL) 