from redis.asyncio import Redis
from ..schemas.otp import OTPRequest
from ..utils.generate_otp import generate_otp
from ..utils.send_email import send_verification_otp_to_email, send_reset_password_otp_to_email
from ..core.config import Config
from ..core.logger import get_logger
logger = get_logger(__name__)

class OTPService:
    def __init__(self, redis: Redis, otp_request_obj: OTPRequest) -> None:
        self.redis = redis
        self.otp_request_obj = otp_request_obj
        
    async def generate_and_store_otp(self): 
        logger.info("generating otp......")
        otp = generate_otp()
        otp_key = f"otp:{self.otp_request_obj.email}"
        trials_key = f"trials:{self.otp_request_obj.email}"
        logger.info("setting otp token in redis......")
        await self.redis.setex(otp_key, Config.OTP_EXPIRY, otp)
        logger.info("setting otp trials in redis......")
        await self.redis.setex(trials_key, Config.OTP_EXPIRY, Config.OTP_MAX_TRIALS)
        otp_value = await self.redis.get(otp_key)
        return otp_value
        
    async def send_verification_email(self, data_obj, reciever_name, otp): 
        logger.info("Sending email.....")
        return await send_verification_otp_to_email(receiver_email=data_obj.email, receiver_name=reciever_name, otp=otp)
    
    async def send_reset_password_email(self, data_obj, reciever_name, otp):
        return await send_reset_password_otp_to_email(receiver_email=data_obj.email, receiver_name=reciever_name, otp=otp)