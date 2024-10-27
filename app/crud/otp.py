from fastapi import Depends
from redis.asyncio import Redis
from app.database.main import get_db
from app.schemas.otp import OTPRequest
from base import CRUDBASE
from models.auth_user import User
from utils.send_email import send_verification_otp_to_email, send_reset_password_otp_to_email
from utils.generate_otp import generate_otp
from core.errors import InvalidOTP, InvalidCredentials, InvalidRequest
from core.redis_setup import get_redis
from core.config import Config


class CRUD_OTP(CRUDBASE[User, OTPRequest, OTPRequest]):
    async def verify_otp(self, user_obj, user_otp, redis: Redis) -> bool:
        otp_key = f"otp:{user_obj.email}"
        trials_key = f"trials:{user_obj.email}"
        attempts_key = f"otp_attempts:{user_obj.email}"
        
        # Rate limiting logic 
        attempts  = await redis.get(attempts_key)
        if not attempts:
            await redis.setex(attempts_key, Config.OTP_RATE_LIMIT_TIME, 1)
        else:
            attempts = int(attempts)
            if attempts >= 5:
                raise InvalidRequest("Too many attempts. Please try again later.")
    
        stored_otp = await redis.get(otp_key)
        trials_left = await int(redis.get(trials_key) or 0)
        if stored_otp is None:
            raise InvalidOTP("OTP expired or not found")
        if trials_left <= 0:
            raise InvalidRequest("Max trials exceeded.")
        if user_otp != stored_otp:
            await redis.decr(trials_key)
            await redis.incr(attempts_key)
            raise InvalidOTP(f"Incorrect OTP. {trials_left - 1} trials left.")
        await redis.delete(otp_key)
        await redis.delete(trials_key)
        return True
    
crud_otp = CRUD_OTP(db=get_db(), model=User)

def get_crud_otp(db=Depends(get_db)):
    return CRUD_OTP(db=db, model=User)