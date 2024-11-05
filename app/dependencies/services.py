from fastapi import Depends
from ..services import AuthUserService, OTPService, RateLimiter
from ..schemas.otp import OTPRequest
from ..repositories import get_crud_otp, get_crud_auth_user
from ..core.redis_setup import get_redis

def get_auth_user_service(
        crud_auth_user=Depends(get_crud_auth_user),
        crud_otp = Depends(get_crud_otp)
) -> AuthUserService:
    return AuthUserService (
        crud_auth_user=crud_auth_user,
        crud_otp=crud_otp
    )

def get_otp_service(otp_request_obj: OTPRequest) -> OTPService:
    return OTPService(otp_request_obj=otp_request_obj, redis=Depends(get_redis))

def get_rate_limiter(redis= Depends(get_redis)):
    return RateLimiter(redis=redis)