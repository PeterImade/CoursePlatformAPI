from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import Config  

DATABASE_URL = Config.DATABASE_URL

engine = create_async_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
Base = declarative_base()