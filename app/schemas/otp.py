from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
 
class OTPRequest(BaseModel):
    email: EmailStr     

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)

class OTPVerified(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    verified: bool

class ResendOTPResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    sent: bool

class ResendOTPRequest(BaseModel):
    email: EmailStr