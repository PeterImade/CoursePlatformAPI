from typing import Annotated
from redis.asyncio import Redis
from fastapi import APIRouter, Depends, BackgroundTasks, status, Header, Query
from fastapi.security import OAuth2PasswordRequestForm
from ..services.auth_user_service import AuthUserService
from ..models.auth_user import User
from ..schemas.otp import OTPVerifyRequest, OTPVerified
from ..schemas.user import ChangePasswordRequest, EmailRequest, LogoutResponse, NewPasswordRequest, PasswordChanged, RefreshTokenRequest, RegisterUserResponse, ResetPasswordResponse, TokenDeactivate, Tokens, UserCreate, ForgotPasswordResponse
from ..core.tokens import get_verified_current_user
from ..core.redis_setup import get_redis
from ..dependencies.services import get_auth_user_service

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponse)
async def register_user(
    data_obj: UserCreate,
    redis: Annotated[Redis, Depends(get_redis)],
    background_task: BackgroundTasks,
    auth_user_service: Annotated[AuthUserService, Depends(get_auth_user_service)]
):
    return await auth_user_service.register_auth_user(data_obj=data_obj, redis=redis, background_task=background_task)

@router.post("/verify", status_code=status.HTTP_200_OK, response_model=OTPVerified)
async def verify_otp(
    data_obj: OTPVerifyRequest,
    redis: Annotated[Redis, Depends(get_redis)],
    auth_user_service: Annotated[AuthUserService, Depends(get_auth_user_service)]
):
    return await auth_user_service.verify_otp(data_obj=data_obj, redis=redis)

@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=Tokens)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_user_service: AuthUserService = Depends(get_auth_user_service),
    user_agent: str = Header(None),
):
    return await auth_user_service.login_user(form_data=form_data, user_agent=user_agent)

@router.post("/refresh_token", status_code=status.HTTP_200_OK, response_model=Tokens)
async def refresh_token(
    data_obj: RefreshTokenRequest,
    user: User = Depends(get_verified_current_user),
    redis: Redis = Depends(get_redis),
    user_agent: str = Header(None),
    auth_user_service: AuthUserService = Depends(get_auth_user_service)
):
    return auth_user_service.refresh_token(data_obj=data_obj, user_id=user.id, user_agent=user_agent, redis=redis)

@router.post("/logout", status_code=status.HTTP_200_OK, response_model=LogoutResponse)
async def logout_user(
    token: TokenDeactivate,
    user: User = Depends(get_verified_current_user),
    auth_user_service: AuthUserService = Depends(get_auth_user_service),
    redis: Redis = Depends(get_redis)
):
    return await auth_user_service.logout_user(token=token, user=user, redis=redis)


@router.post("/forgot_password", status_code=status.HTTP_201_CREATED, response_model=ForgotPasswordResponse)
async def forgot_password(
    email: EmailRequest,
    background_tasks: BackgroundTasks,
    auth_user_service: Annotated[AuthUserService, Depends(get_auth_user_service)],
    redis: Annotated[Redis, Depends(get_redis)]
):
    return await auth_user_service.forgot_password(data_obj=email, background_tasks=background_tasks, redis=redis)

@router.post("/reset_password", status_code=status.HTTP_200_OK, response_model=ResetPasswordResponse)
async def reset_password(
    data_obj: NewPasswordRequest,
    auth_user_service: Annotated[AuthUserService, Depends(get_auth_user_service)]
):
    return await auth_user_service.reset_password(data_obj=data_obj)

@router.put("/change_password", status_code=status.HTTP_200_OK, response_model=PasswordChanged)
async def change_password(
    data_obj: ChangePasswordRequest,
    auth_user_service: Annotated[AuthUserService, Depends(get_auth_user_service)],
    user: Annotated[User, Depends(get_verified_current_user)]
):
    return await auth_user_service.change_password(data_obj=data_obj, current_user=user)
