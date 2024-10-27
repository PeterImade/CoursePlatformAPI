from typing import Annotated
import uuid
from fastapi import Depends, Header, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from redis.asyncio import Redis
from app.models.auth_user import User
from crud.user import (
    CRUDAuthUser
)
from schemas.user import ChangePasswordRequest, ForgotPasswordResponse, NewPasswordRequest, OTPVerified, PasswordChanged, LogoutResponse, ResetPasswordResponse, UserCreate, RegisterUserResponse, EmailRequest
from core.errors import UserAlreadyExists, UserNotFound, InvalidOTP, InvalidCredentials, InvalidToken, InvalidRequest
from schemas.otp import OTPRequest, OTPVerifyRequest
from services.otp_service import OTPService
from crud.otp import CRUD_OTP
from models.auth_user import User
from utils.hash_password import verify_password, hash_password
from core.tokens import generate_tokens, deactivate_token

class AuthUserService: 
    def __init__(self, crud_auth_user: CRUDAuthUser, crud_otp: CRUD_OTP):
        self.crud_auth_user = crud_auth_user
        self.crud_otp = crud_otp

    async def register_auth_user(self, data_obj: UserCreate, background_task: BackgroundTasks, redis: Redis): 
        user = await self.crud_auth_user.get_user_by_email(data_obj.email.lower())
        if user:
            raise UserAlreadyExists()
        data_obj.password = hash_password(data_obj.password)
        new_user = await self.crud_auth_user.create(data_obj)
        otp_obj = OTPRequest(email=new_user.email)
        otp_service = OTPService(redis=Redis, otp_request_obj=otp_obj)
        otp = await otp_service.generate_and_store_otp()
        background_task.add_task(otp_service.send_verification_email, otp_obj, new_user.first_name, otp)
        return RegisterUserResponse(auth_user=new_user)
    
    async def verify_otp(self, data_obj: OTPVerifyRequest, redis: Redis):
        otp_user = await self.crud_auth_user.get_user_by_email(data_obj.email.lower())
        if otp_user is None:
            raise UserNotFound("User with this email does not exist")
        otp_verify = await self.crud_otp.verify_otp(user_obj=otp_user, user_otp=data_obj.otp, redis=redis)
        if not otp_verify:
            raise InvalidOTP("Invalid OTP")
        await self.crud_auth_user.update(id=otp_user.id, data_obj={User.EMAIL_VERIFIED: True})
        return OTPVerified(verified=True)
    
    async def login_user(
        self, 
        form_data: OAuth2PasswordRequestForm,
        user_agent: str = Header(None), 
    ):
        auth_user = await self.crud_auth_user.get_user_by_email(form_data.username.lower())
        if not auth_user:
            raise InvalidCredentials()
        if not auth_user.email_verified:
            raise InvalidCredentials("Email not verified. Please verify your email.")
        is_password = verify_password(form_data.password, auth_user.password)
        if not is_password:
            raise InvalidCredentials()
        tokens = await generate_tokens(user_id=auth_user.id, user_agent=user_agent)
        return tokens
    
    # Done
    async def logout_user(self, token: str, user_id: uuid):
        user = await self.crud_auth_user.get_query_by_id(id=user_id)
        if not user:
            raise UserNotFound()
        if not deactivate_token(token=token, user_id=user.id):
          raise InvalidToken()
        return LogoutResponse(logged_out=True)
    
    # Done
    async def forgot_password(self, data_obj: EmailRequest, background_tasks: BackgroundTasks, redis: Redis):
        user = await self.crud_auth_user.get_user_by_email(email=data_obj.email.lower())
        if not user:
            raise UserNotFound() 
        otp_service = OTPService(otp_request_obj=data_obj, redis=redis)
        otp = await otp_service.generate_and_store_otp()
        background_tasks.add_task(otp_service.send_reset_password_email, data_obj, user.firstName, otp)  
        return ForgotPasswordResponse()
    
    # Done
    async def reset_password(self, data_obj: NewPasswordRequest):
        user = await self.crud_auth_user.get_user_by_email(data_obj.email)
        if not user:
            raise UserNotFound() 
        if verify_password(data_obj.new_password, hashed_password=user.password):
            raise InvalidRequest("Cannot change password to old password")
        new_password = hash_password(plain_password=data_obj.new_password)
        await self.crud_auth_user.update(id=user.id, data_obj={User.PASSWORD: new_password}) 
        return ResetPasswordResponse()
    
    # Done
    async def change_password(self, data_obj: ChangePasswordRequest, current_user_id: str, current_user_password: str):
        if not verify_password(plain_password=data_obj.old_password, hashed_password=current_user_password):
            raise InvalidRequest("Wrong old password")
        
        if verify_password(plain_password=data_obj.new_password, hashed_password=current_user_password):
            raise InvalidRequest("Cannot change to old password")
        
        self.crud_auth_user.update(id=current_user_id, data_obj={User.PASSWORD: data_obj.new_password})
        return PasswordChanged()
        
