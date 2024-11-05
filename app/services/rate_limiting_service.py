import time
import asyncio 
from redis.asyncio import Redis

from app.core.exceptions import UserNotFound
from ..repositories.user import CRUDAuthUser
from ..core.config import Config
from ..schemas.otp import ResendOTPRequest 

MAX_TOKEN = Config.OTP_MAX_TRIALS
OTP_RATE_LIMIT_TIME = Config.OTP_RATE_LIMIT_TIME

class RateLimiter:  
    def __init__(self, redis: Redis):
        self.redis = redis  
    
    async def handle_requests(self, user_email: str): 
        bucket_key = f"bucket_key:{user_email}"
        current_token = int(await self.redis.get(bucket_key) or 0)
        if current_token > 0:
            await self.redis.decrby(bucket_key)
            return True
        return False
        
    async def replenish_bucket(self, user_email: str): 
        bucket_key = f"bucket_key:{user_email}" 
        current_token = int(await self.redis.get(bucket_key) or 0)

        while current_token < MAX_TOKEN:
            await asyncio.sleep(1)
            await self.redis.incrby(bucket_key)