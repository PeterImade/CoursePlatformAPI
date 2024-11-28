from __future__ import annotations

from typing import ClassVar, List
import uuid
from datetime import datetime

from sqlalchemy import (
    Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.auth_user import User
from ..schemas.base import Role
from ..database.main import Base 

class Instructor(User):
    __tablename__ = "instructors"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    courses = relationship('Course', back_populates='instructor')

    user = relationship('User', backref='instructors')
    
    __mapper_args__ = {
        'inherit_condition': id == User.id  
    }