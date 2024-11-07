from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    FORGET_PASSWORD_EXPIRY_TIME: int
    OTP_EXPIRY: int
    OTP_MAX_TOKEN: int
    REPLENISH_INTERVAL: int
    ALGORITHM: str
    SECRET_KEY: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    CACHE_EXPIRY: int
    MAIL_PORT: str    
    REDIS_DB_NO: int
    REDIS_HOST: str
    REDIS_PORT: int
    MAIL_FROM: str
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config = Settings()