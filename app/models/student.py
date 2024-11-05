from __future__ import annotations
from datetime import datetime
from typing import List
import uuid

from sqlalchemy import (
    Column, ForeignKey, TIMESTAMP, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship 

from ..database.main import Base  
class Student(Base):
    __tablename__ = "students" 
 
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'), nullable=False)

    # Foreign Key
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="student", uselist=False)
    notifications: Mapped[List["Notification"]] = relationship(back_populates="student", passive_deletes=True, cascade="all, delete")
    payments: Mapped[List["Payment"]] = relationship(back_populates="student", passive_deletes=True, cascade="all, delete")
    courses: Mapped[List["Course"]] = relationship(back_populates="students", secondary= "enrollments")
    enrollments: Mapped[List["Enrollment"]] = relationship(back_populates="student")