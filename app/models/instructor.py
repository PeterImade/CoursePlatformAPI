import uuid 
from sqlalchemy import (
    Column, String, TIMESTAMP, ForeignKey, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 

from app.database.main import Base

class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    expertise = Column(String(200), nullable=False)

    # Foreign Key & Relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    courses = relationship("Course", back_populates="instructor")

    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text('now()'),
        onupdate=text('now()'),
        nullable=False
    )
