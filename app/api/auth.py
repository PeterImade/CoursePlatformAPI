from typing import Annotated
from redis.asyncio import Redis
from fastapi import APIRouter, Depends, BackgroundTasks, status, Header, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import TooManyRequests, UserNotFound
from ..services.auth_user_service import AuthUserService
from ..services.rate_limiting_service import RateLimiter
from ..models.auth_user import User
from ..schemas.otp import OTPVerifyRequest, OTPVerified, ResendOTPRequest, ResendOTPResponse
from ..schemas.user import ChangePasswordRequest, ChangeRoleRequest, EmailRequest, LogoutResponse, NewPasswordRequest, PasswordChanged, RefreshTokenRequest, RegisterUserResponse, ResetPasswordResponse, TokenDeactivate, Tokens, UserCreate, ForgotPasswordResponse, UserResponse
from ..core.tokens import get_verified_current_user
from ..core.redis_setup import get_redis
from ..dependencies.services import get_auth_user_service, get_rate_limiter

router = APIRouter(prefix="/api/v1/auth", tags=["User"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponse)
async def register_user(
    data_obj: UserCreate,
    redis: Annotated[Redis, Depends(get_redis)],
    background_task: BackgroundTasks,
    auth_user_service: Annotated[AuthUserService, Depends(get_auth_user_service)]
):
    return await auth_user_service.register_auth_user(data_obj=data_obj, redis=redis, background_task=background_task)

@router.post("/verify-otp", status_code=status.HTTP_200_OK, response_model=OTPVerified)
async def verify_otp(
    data_obj: OTPVerifyRequest,
    redis: Annotated[Redis, Depends(get_redis)],
    auth_user_service: Annotated[AuthUserService, Depends(get_auth_user_service)]
):
    return await auth_user_service.verify_otp(data_obj=data_obj, redis=redis)

@router.post("/resend-otp", response_model=ResendOTPResponse)
async def resend_otp(
    data_obj: ResendOTPRequest, 
    background_task: BackgroundTasks,
    redis: Annotated[Redis, Depends(get_redis)],
    rate_limiting_service: Annotated[RateLimiter, Depends(get_rate_limiter)],
    auth_user_service: Annotated[AuthUserService, Depends(get_auth_user_service)]):

    user_email = data_obj.email.lower()
    background_task.add_task(rate_limiting_service.replenish_tokens_periodically, user_email)

    user = auth_user_service.crud_auth_user.get_user_by_email(data_obj.email.lower())
    if user is None:
        raise UserNotFound("User with this email does not exist")
    
      # Start the background task to replenish tokens if not already running
    
    if not await rate_limiting_service.handle_requests(user_email=user.email): 
        raise TooManyRequests("Rate limit exceeded. Please try again later.")

    return await auth_user_service.resend_otp(data_obj=data_obj,background_task=background_task, redis=redis)



@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=Tokens)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    redis: Redis = Depends(get_redis),
    auth_user_service: AuthUserService = Depends(get_auth_user_service)
):
    return await auth_user_service.login_user(form_data=form_data, redis=redis)

@router.post("/refresh-token", status_code=status.HTTP_200_OK, response_model=Tokens)
async def refresh_token(
    data_obj: RefreshTokenRequest,
    user: User = Depends(get_verified_current_user),
    redis: Redis = Depends(get_redis), 
    auth_user_service: AuthUserService = Depends(get_auth_user_service)
):
    return await auth_user_service.refresh_token(data_obj=data_obj, user_id=user.id, redis=redis)

@router.post("/logout", status_code=status.HTTP_200_OK, response_model=LogoutResponse)
async def logout_user(
    token: TokenDeactivate,
    user: User = Depends(get_verified_current_user),
    auth_user_service: AuthUserService = Depends(get_auth_user_service),
    redis: Redis = Depends(get_redis)
):
    return await auth_user_service.logout_user(token=token, user=user, redis=redis)


@router.post("/forgot-password", status_code=status.HTTP_201_CREATED, response_model=ForgotPasswordResponse)
async def forgot_password(
    email: EmailRequest,
    background_tasks: BackgroundTasks,
    auth_user_service: Annotated[AuthUserService, Depends(get_auth_user_service)],
    redis: Annotated[Redis, Depends(get_redis)]
):
    return await auth_user_service.forgot_password(data_obj=email, background_tasks=background_tasks, redis=redis)

@router.post("/reset-password", status_code=status.HTTP_200_OK, response_model=ResetPasswordResponse)
async def reset_password(
    data_obj: NewPasswordRequest,
    auth_user_service: Annotated[AuthUserService, Depends(get_auth_user_service)]
):
    return await auth_user_service.reset_password(data_obj=data_obj)

@router.patch("/change-password", status_code=status.HTTP_200_OK, response_model=PasswordChanged)
async def change_password(
    data_obj: ChangePasswordRequest,
    auth_user_service: Annotated[AuthUserService, Depends(get_auth_user_service)],
    current_user: Annotated[User, Depends(get_verified_current_user)]
):
    return await auth_user_service.change_password(data_obj=data_obj, current_user=current_user  )

@router.patch("/apply-instructor", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def change_role(
    data_obj: ChangeRoleRequest, 
    auth_user_service: Annotated[AuthUserService, Depends(get_auth_user_service)],
    current_user: Annotated[User, Depends(get_verified_current_user)]
):
    try:
        return await auth_user_service.change_role(user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred")