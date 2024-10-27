import uuid

from sqlalchemy import (
    Column, ForeignKey, TIMESTAMP, text
)
from sqlalchemy.dialects.postgresql import UUID 

from app.database.main import Base

class Student(Base):
    __tablename__ = "students"

    # Primary Key (UUID)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    # Foreign Key
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text('now()'),
        onupdate=text('now()'),
        nullable=False
    )
