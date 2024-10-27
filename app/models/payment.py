import uuid 

from sqlalchemy import (
    Column, Float, String, TIMESTAMP, ForeignKey, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.main import Base 
class Payment(Base):
    __tablename__ = "payments"

    # Primary Key (UUID)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    # Fields
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)

    # Foreign Key & Relationship
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="payments")

    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text('now()'),
        onupdate=text('now()'),
        nullable=False
    )
