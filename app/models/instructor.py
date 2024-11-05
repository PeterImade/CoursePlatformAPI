from __future__ import annotations

from datetime import datetime
from typing import List
import uuid 
from sqlalchemy import (
    Column, String, TIMESTAMP, ForeignKey, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
from ..database.main import Base 

class Instructor(Base):
    __tablename__ = "instructors"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    expertise: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'), nullable=False)

    # Relationships 
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    user: Mapped["User"] = relationship(back_populates="instructor", uselist=False)
    notifications: Mapped[List["Notification"]] = relationship(back_populates="instructor", passive_deletes=True, cascade="all, delete")
    courses: Mapped[List["Course"]] = relationship(back_populates="instructor", passive_deletes=True, cascade="all, delete") 



