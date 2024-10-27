from typing import Optional
from fastapi import Depends
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from ..database.main import get_db
from .base import CRUDBASE
from ..models.auth_user import User
from ..schemas.user import UserCreate


class CRUDAuthUser(CRUDBASE[User, UserCreate, UserCreate]):
    async def get_user_by_email(self, email) -> Optional[User]:
        response = await self.db.query(self.model).filter(self.model.email == email).first()
        return response

crudAuthUser = CRUDAuthUser(db=get_db(), model=User)

def get_crud_auth_user(db=Depends(get_db)):
    return CRUDAuthUser(db=db, model=User)



