from redis.asyncio import Redis
from app.schemas.otp import OTPRequest
from app.utils import generate_otp
from app.utils.send_email import send_verification_otp_to_email, send_reset_password_otp_to_email
from core.config import Config

class OTPService:
    def __init__(self, redis: Redis, otp_request_obj: OTPRequest) -> None:
        self.redis = redis
        self.otp_request_obj = otp_request_obj
        
    async def generate_and_store_otp(self):
        if self.otp_request_obj.otp is None:
            self.otp_request_obj.otp = generate_otp()
        otp = self.otp_request_obj.otp 
        otp_key = f"otp:{self.otp_request_obj.email}"
        trials_key = f"trials:{self.otp_request_obj.email}"
        await self.redis.setex(otp_key, Config.OTP_EXPIRY, otp)
        await self.redis.setex(trials_key, Config.OTP_EXPIRY, Config.OTP_MAX_TRIALS)
        return otp
        
    async def send_verification_email(self, data_obj, reciever_name, otp): 
        return await send_verification_otp_to_email(receiver_email=data_obj.email, receiver_name=reciever_name, otp=otp)
    
    async def send_reset_password_email(self, data_obj, reciever_name, otp):
        return await send_reset_password_otp_to_email(receiver_email=data_obj.email, receiver_name=reciever_name, otp=otp)