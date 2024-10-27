from typing import ClassVar
import uuid

from sqlalchemy import (
    Column, String, Float, ForeignKey, TIMESTAMP, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.main import Base

class Course(Base):
    __tablename__ = "courses"

    ID: ClassVar[str] = "id"
    TITLE: ClassVar[str] = "title"
    DESCRIPTION: ClassVar[str] = "description"
    PRICE: ClassVar[str] = "price"
    STATUS: ClassVar[str] = "status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, default=0.0)
    status = Column(String(50), nullable=False)
    instructor_id = Column(UUID(as_uuid=True), ForeignKey("instructors.id"), nullable=False)
    instructor = relationship("User", back_populates="courses")
    payments = relationship("Payment", back_populates="course")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text('now()'),
        onupdate=text('now()'),
        nullable=False
    )
