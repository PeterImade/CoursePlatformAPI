from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional, Type, TypeVar, Generic, Union
from app.database.main import Base
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", BaseModel)


class CRUDBASE(Generic([ModelType, CreateSchemaType, UpdateSchemaType])): 
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model
    
    async def create(self, data_obj: Union[CreateSchemaType | dict]) -> ModelType:
        if isinstance(data_obj, dict):
            response_obj = self.model(**data_obj)
            await self.db.add(response_obj)
            await self.db.commit()
            await self.db.refresh(response_obj)
            return response_obj
        
        # exclude_none=True removes fields with None value from the ouput
        data_dict = data_obj.model_dump(exclude_none=True)
        response_obj = self.model(**data_dict)
        await self.db.add(response_obj)
        await self.db.commit()
        await self.db.refresh()
        return response_obj
    
    
    async def get_all(self) -> Optional[list[ModelType]]: 
        data_obj = await self.db.query(self.model).all()
        return data_obj
    
    async def get_query_by_id(self, id):
        query = await self.db.query(self.model).filter(self.model.id == id)
        return query
    
    async def get_by_id(self, id) -> Optional[ModelType]: 
        data_obj = await self.get_query_by_id(id).first()
        return data_obj
    
    async def delete(self, id) -> bool: 
        await self.get_query_by_id(id).delete(synchronize_session=False)
        await self.db.commit()
        return True
    
    async def update(self, id, data_obj: Union[UpdateSchemaType | dict]) -> ModelType:
        if isinstance(data_obj, dict):
            query = await self.get_query_by_id(id)
            data_obj["updated_at"] = datetime.now()
            await query.update(**data_obj, synchronize_session=False)
            await self.db.commit()
            return data_obj

        query = await self.get_query_by_id(id)
        data_obj["updated_at"] = datetime.now()
        updated_obj = await query.update(**data_obj.model_dump(exclude_unset=True), synchronize_session=False)
        await self.db.commit()
        return updated_obj

            
    
    
    