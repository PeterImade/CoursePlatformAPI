import uuid

from sqlalchemy import (
    Column, String, TIMESTAMP, ForeignKey, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.main import Base
class Profile(Base):
    __tablename__ = "profiles"

    # Primary Key (UUID)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    # Fields
    profile_img = Column(String, nullable=True)
    name = Column(String, nullable=False)
    bio = Column(String, nullable=False)
    location = Column(String, nullable=False)

    # Foreign Key & Relationship
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="profile")

    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text('now()'),
        onupdate=text('now()'),
        nullable=False
    )
