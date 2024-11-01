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

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    price: Mapped[float] = mapped_column(nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'), nullable=False)


    # Relationships
    payments: Mapped[List["Payment"]] = relationship(back_populates="course", passive_deletes=True, cascade="all, delete")
    instructor_id: Mapped[UUID] = mapped_column(ForeignKey("instructors.id", ondelete="CASCADE"), nullable=False)
    instructor: Mapped["Instructor"] = relationship(back_populates="courses")
    students: Mapped[List["Student"]] = relationship(back_populates="courses", secondary=lambda: student_course_association)