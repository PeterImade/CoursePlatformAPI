from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict 


class CourseCreate(BaseModel):
    title: str
    description: str
    price: str
    status: str

class CourseUpdate(BaseModel):
    title: str
    description: str
    price: str 

class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    price: str
    status: str
    created_at: datetime
    updated_at: datetime