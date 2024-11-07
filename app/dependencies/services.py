from fastapi import Depends
from ..services import AuthUserService, OTPService, RateLimiter, CourseService
from ..schemas.otp import OTPRequest
from ..repositories import get_crud_otp, get_crud_auth_user, get_crud_course
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

def get_course_service(crud_course = Depends(get_crud_course), redis_client = Depends(get_redis)) -> CourseService:
    return CourseService(crud_course=crud_course, redis_client=redis_client)

def get_rate_limiter(redis= Depends(get_redis)):
    return RateLimiter(redis=redis)