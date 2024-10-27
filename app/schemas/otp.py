from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
 
class OTPRequest(BaseModel):
    email: str

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)
