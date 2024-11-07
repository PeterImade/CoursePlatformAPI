import uuid 
import jwt
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from redis.asyncio import Redis
from ..schemas.user import Tokens, TokenData, LogoutResponse
from ..models.auth_user import User
from .exceptions import InvalidCredentials, InvalidToken, InvalidRequest, UserNotFound
from .config import Config
from ..core.logger import get_logger
from ..database.main import get_db

logger = get_logger(__name__)
SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = Config.REFRESH_TOKEN_EXPIRE_MINUTES
FORGET_PASSWORD_EXPIRY_TIME = Config.FORGET_PASSWORD_EXPIRY_TIME

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def deactivate_token(token: str, user_id: uuid, redis: Redis)-> bool:
    if not verify_token(token=token):
        raise InvalidToken()
    refresh_token_key = f"refresh_token:{user_id}"
    stored_refresh_token = await redis.get(refresh_token_key)
    logger.info(f"retrieved refresh token from redis: {stored_refresh_token}")
    if not stored_refresh_token:
        raise InvalidRequest("Refresh token expired or not found")
    await redis.delete(refresh_token_key)
    logger.info(f"retrieved deleted refresh token from redis: {stored_refresh_token}")
    
async def regenerate_tokens(token:str, user_id:uuid, redis: Redis) -> Tokens:
    await deactivate_token(token=token, user_id=user_id, redis=redis)
    tokens = await generate_tokens(user_id=user_id, redis=redis)
    return tokens

def encode_jwt(payload: dict, expiry_time: timedelta):
    data_to_encode = payload.copy() 
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=expiry_time)
    data_to_encode.update({"expiry_time": expiration_time.isoformat()})
    encoded_jwt = jwt.encode(payload=data_to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_access_token(user_id: uuid):
    payload = {"user_id": str(user_id), "type": "access"}
    access_token = encode_jwt(payload=payload, expiry_time=ACCESS_TOKEN_EXPIRE_MINUTES)
    return access_token

async def generate_refresh_token(user_id: uuid, redis: Redis):
    payload = {"user_id": str(user_id), "type": "refresh"}
    refresh_token = encode_jwt(payload=payload, expiry_time=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token_key = f"refresh_token:{user_id}" 
    await redis.setex(refresh_token_key, REFRESH_TOKEN_EXPIRE_MINUTES * 60, refresh_token)
    return refresh_token

async def generate_tokens(user_id: uuid, redis: Redis):
    access_token = generate_access_token(user_id=user_id)
    refresh_token = await generate_refresh_token(user_id=user_id, redis=redis)
    tokens = Tokens(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    return tokens
    
def verify_token(token: str):
    token_data = decode_jwt(token=token)
    try:
        token_data = decode_jwt(token=token)
    except InvalidTokenError:
        raise InvalidCredentials("Invalid token")
    except ExpiredSignatureError:
        raise InvalidCredentials("Token has expired")
    return token_data

def decode_jwt(token: str):
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id") 
    if not user_id:
        raise InvalidCredentials("Invalid token")
    token_data = TokenData(user_id=user_id)
    return token_data

# using an OTP instead
async def generate_forgot_password_token(user_id: uuid,  user_agent: str, redis: Redis):
    payload = {"user_id": user_id , "user_agent": user_agent, "type": "forgot_password"}
    forgot_password_token = encode_jwt(payload=payload, expiry_time=FORGET_PASSWORD_EXPIRY_TIME)
    forgot_password_token_key = f"forgot_password_token:{user_id}" 
    await redis.setex(forgot_password_token_key, FORGET_PASSWORD_EXPIRY_TIME, forgot_password_token)
    return forgot_password_token

async def get_verified_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]) -> User:
    token_data = verify_token(token=token)
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user:
        if not user.email_verified:
            raise UserNotFound("email not verified")
        return user
    else:
        raise UserNotFound("user not found")