import uuid
import jwt # type: ignore
import datetime
from datetime import timedelta
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from schemas.user import Token, TokenData, LogoutResponse
from .config import Config
from redis.asyncio import Redis
from errors import InvalidCredentials, InvalidToken, InvalidRequest

SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = Config.REFRESH_TOKEN_EXPIRE_MINUTES
FORGET_PASSWORD_EXPIRY_TIME = Config.FORGET_PASSWORD_EXPIRY_TIME

async def deactivate_token(token: str, user_id: uuid, redis: Redis)-> bool:
    if not verify_token(token=token):
        raise InvalidToken()
    refresh_token_key = f"refresh_token:{user_id}"
    stored_refresh_token = await redis.get(refresh_token_key)
    if not stored_refresh_token:
        raise InvalidRequest("Refresh token expired or not found")
    await redis.delete(refresh_token_key)
    return True

def encode_jwt(payload: dict, expiry_time: timedelta):
    data_to_encode = payload.copy()
    expiration_time = datetime.now() + datetime.timedelta(minutes=expiry_time)  
    data_to_encode.update({"expiry_time": expiration_time})
    encoded_jwt = jwt.encode(payload=data_to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_access_token(user_id: str, user_agent: str):
    payload = {"user_id": user_id, "type": "access", "user_agent": user_agent}
    access_token = encode_jwt(payload=payload, expiry_time=ACCESS_TOKEN_EXPIRE_MINUTES)
    return access_token

async def generate_refresh_token(user_id, user_agent, redis: Redis):
    payload = {"user_id": user_id, "type": "refresh" ,"user_agent": user_agent}
    refresh_token = encode_jwt(payload=payload, expiry_time=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token_key = f"refresh_token:{user_id}" 
    await redis.setex(refresh_token_key, REFRESH_TOKEN_EXPIRE_MINUTES, refresh_token)
    return refresh_token

def generate_tokens(user_id, user_agent):
    access_token = generate_access_token(user_id=user_id, user_agent=user_agent)
    refresh_token = generate_refresh_token(user_id=user_id, user_agent=user_agent)
    token = Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    return token
    
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
    user_agent = payload.get("user_agent")
    if not user_id:
        raise InvalidCredentials("Invalid token")
    token_data = TokenData(user_id=user_id, user_agent=user_agent)
    return token_data

async def generate_forgot_password_token(user_id: uuid,  user_agent: str, redis: Redis):
    payload = {"user_id": user_id , "user_agent": user_agent, "type": "forgot_password"}
    forgot_password_token = encode_jwt(payload=payload, expiry_time=FORGET_PASSWORD_EXPIRY_TIME)
    forgot_password_token_key = f"forgot_password_token:{user_id}" 
    await redis.setex(forgot_password_token_key, FORGET_PASSWORD_EXPIRY_TIME, forgot_password_token)
    return forgot_password_token
    