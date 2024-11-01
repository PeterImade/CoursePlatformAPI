from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base 

from ..core.config import Config  

DATABASE_URL = Config.DATABASE_URL

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, bind=engine, class_=Session)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
        
Base = declarative_base()