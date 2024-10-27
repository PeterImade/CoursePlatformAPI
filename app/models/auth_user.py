from typing import ClassVar
import uuid

from sqlalchemy import (
    Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

from app.schemas.base import Role
from app.database.main import Base

class User(Base):
    __tablename__ = "users"

    ID: ClassVar[str] = "id"
    FIRST_NAME: ClassVar[str] = "first_name"
    LAST_NAME: ClassVar[str] = "last_name"
    EMAIL: ClassVar[str] = "email"
    PASSWORD: ClassVar[str] = "password"
    EMAIL_VERIFIED: ClassVar[str] = "email_verified"
    PHONE_VERIFIED: ClassVar[str] = "phone_verified"
    ROLE: ClassVar[str] = "role"
    IS_ACTIVE: ClassVar[str] = "is_active"
    CREATED_AT: ClassVar[str] = "created_at"
    UPDATED_AT: ClassVar[str] = "updated_at"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    email_verified = Column(Boolean, nullable=False, default=False )
    password = Column(String, nullable=False) 
    role = Column(String, default=Role.STUDENT.value)
    is_active = Column(Boolean, default=False)  
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True), 
        server_default=text('now()'), 
        onupdate=text('now()'), 
        nullable=False
    )
    profile = relationship("Profile", back_populates="user", uselist=False)  # One-to-one with Profile
    courses = relationship("Course", back_populates="instructor")  # One-to-many with Course
    notifications = relationship("Notification", back_populates="user")  # One-to-many with Notification


