from __future__ import annotations

from datetime import datetime
import uuid
from sqlalchemy import (
    Column, String, Boolean, TIMESTAMP, ForeignKey, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
 
from ..database.main import Base 

class Notification(Base):
    __tablename__ = "notifications"
 
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4) 
    message: Mapped[str] = mapped_column(nullable=False)
    is_read: Mapped[bool] = mapped_column(nullable=False, default=False) 
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'), nullable=False)

    # Foreign Key & Relationship
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False) 
    user: Mapped["User"] = relationship(back_populates="notifications")
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False) 
    student: Mapped["Student"] = relationship(back_populates="notifications")
    instructor_id: Mapped[UUID] = mapped_column(ForeignKey("instructors.id", ondelete="CASCADE"), nullable=False) 
    instructor: Mapped["Instructor"] = relationship(back_populates="notifications")