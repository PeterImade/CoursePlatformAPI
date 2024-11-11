from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List
import uuid

from sqlalchemy import (
    Column, String, Float, ForeignKey, TIMESTAMP, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column 
from ..database.main import Base  

class Course(Base):
    __tablename__ = "courses"

    ID: ClassVar[str] = "id"
    TITLE: ClassVar[str] = "title"
    DESCRIPTION: ClassVar[str] = "description"
    PRICE: ClassVar[str] = "price"
    STATUS: ClassVar[str] = "status" 
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=True)
    rating = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'), nullable=False)

    # Relationships
    payments = relationship("Payment", back_populates="course", passive_deletes=True, cascade="all, delete")
    students = relationship("User", back_populates="courses", secondary="enrollments")