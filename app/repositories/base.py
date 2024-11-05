from datetime import datetime
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Type, TypeVar, Generic, Union
from ..database.main import Base
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from ..core.logger import get_logger

logger = get_logger(__name__)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBASE(Generic[ModelType, CreateSchemaType, UpdateSchemaType]): 
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model
    
    async def create(self, data_obj: Union[CreateSchemaType | dict]) -> ModelType:
        if isinstance(data_obj, dict):
            response_obj = self.model(**data_obj)
            self.db.add(response_obj)
            self.db.commit()
            self.db.refresh(response_obj)
            return response_obj
        
        # exclude_none=True removes fields with None value from the ouput
        data_dict = data_obj.model_dump(exclude_none=True)
        response_obj = self.model(**data_dict)
        self.db.add(response_obj)
        self.db.commit()
        self.db.refresh(response_obj)
        return response_obj
    
    
    async def get_all(self) -> Optional[list[ModelType]]: 
        data_obj = self.db.query(self.model).all()
        return data_obj
    
    # rename get_query_by_id_or_none next time
    async def get_query_by_id(self, id):
        query = self.db.query(self.model).filter(self.model.id == id)
        return query
    
    async def get_by_id(self, id) -> Optional[ModelType]: 
        data_obj = self.get_query_by_id(id).first()
        return data_obj
    
    async def delete(self, id) -> bool: 
        self.get_query_by_id(id).delete(synchronize_session=False)
        self.db.commit()
        return True
    
    async def update(self, id: int, data_obj: Union[UpdateSchemaType, dict]) -> Dict[str, Any]:
        try:
            # Fetch the query based on id
            query = await self.get_query_by_id(id)

            if query is None:
                raise Exception("Item not found") 
            
            if isinstance(data_obj, dict):
                data_obj["updated_at"] = datetime.now()
            else:
                data_obj = data_obj.model_dump(exclude_unset=True)
                data_obj["updated_at"] = datetime.now()
            
            # Perform the update and commit
            query.update(data_obj, synchronize_session=False)
            self.db.commit()
            return data_obj

        except SQLAlchemyError as e:
            await self.db.rollback()
            # Consider logging the error if needed
            logger.exception(e)
            raise RuntimeError("Database error occurred") from e

            
    
    
    