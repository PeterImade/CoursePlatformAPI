from datetime import datetime
from typing import ClassVar
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
from ..utils.validate_password import validate_password
from ..utils.email_validation import validate_email
from ..core.exceptions import InvalidCredentials
from ..schemas.base import Role

class UserCreate(BaseModel):
    PASSWORD: ClassVar[str] = "password"
    EMAIL: ClassVar[str] = "email"

    username: str = Field(max_length=25)
    email: EmailStr = Field(max_length=40)
    firstName: str = Field(max_length=25)
    location: str = Field(max_length=25)
    lastName: str = Field(max_length=25)
    password: str = Field(max_length=60)
    bio: str = Field(max_length=300)

    @model_validator(mode="before")
    @classmethod
    def validate_password(cls, values):
        password = values.get(cls.PASSWORD)
        if not validate_password(password):
             raise ValueError(
                "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number or one special character"
            )
        return values
    
    @model_validator(mode="before")
    @classmethod
    def validate_email(cls, values):
        email = values.get(cls.EMAIL)
        if not validate_email(email):
            raise InvalidCredentials("Invalid Email Format")
        return values
    

class UserResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    id: ClassVar[str] = "id"

    id: UUID
    username: str
    firstName: str
    lastName: str
    bio: str
    location: str
    email: EmailStr
    email_verified: bool
    role: Role  
    is_active: bool
    created_at: datetime
    updated_at: datetime

class UserProfile(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    username: str
    firstName: str
    lastName: str
    bio: str
    location: str
    email: EmailStr

class UserProfileUpdate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    username: str
    firstName: str
    lastName: str
    bio: str
    location: str   


class RegisterUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    auth_user: UserResponse
        
class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_id: UUID
        
class LogoutResponse(BaseModel):
    logged_out: bool = False

class EmailRequest(BaseModel):
    email: EmailStr
    
    
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenDeactivate(BaseModel):
    refresh_token: str
    
   
class NewPasswordRequest(BaseModel):
    NEW_PASSWORD: ClassVar[str] = "new_password"
    
    email: EmailStr
    new_password: str
    
    @model_validator(mode="before")
    @classmethod
    def validate_password(cls, values):
        new_password = values.get(cls.NEW_PASSWORD)
        if not validate_password(password=new_password):
            raise ValueError(
                "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number or one special character"
            )
        return values
        
class ResetPasswordResponse(BaseModel):
    password_reset: bool = True 
    
class ChangePasswordRequest(BaseModel):
    NEW_PASSWORD: ClassVar[str] = "new_password"
    
    old_password: str
    new_password: str
    
    @model_validator(mode="before")
    @classmethod
    def validate_password(cls, values):
        password = values.get(cls.NEW_PASSWORD)
        if not validate_password(password=password):
            raise ValueError(
                "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number or one special character"
            )
        return values
    
class PasswordChanged(BaseModel):
    password_changed: bool = True
    
class ForgotPasswordResponse(BaseModel):
    reset_password_link_sent: bool = True

class ChangeRoleRequest(BaseModel): 
    role: str