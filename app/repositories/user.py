from typing import Optional
from fastapi import Depends
from pydantic import EmailStr
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from ..database.main import get_db
from .base import CRUDBASE
from ..models.auth_user import User
from ..schemas.user import UserCreate


class CRUDAuthUser(CRUDBASE[User, UserCreate, UserCreate]):
    def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        response = self.db.query(self.model).filter(self.model.email == email.lower()).first()
        return response if response else None

crudAuthUser = CRUDAuthUser(db=get_db(), model=User)

def get_crud_auth_user(db=Depends(get_db)):
    return CRUDAuthUser(db=db, model=User)



