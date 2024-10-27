import uuid
from sqlalchemy import (
    Column, String, Boolean, TIMESTAMP, ForeignKey, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
 
from app.database.main import Base

class Notification(Base):
    __tablename__ = "notifications"

    # Primary Key (UUID)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    # Fields
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)

    # Foreign Key & Relationship
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="notifications")

    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text('now()'),
        onupdate=text('now()'),
        nullable=False
    )
