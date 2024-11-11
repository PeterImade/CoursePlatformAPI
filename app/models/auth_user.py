from __future__ import annotations

from typing import ClassVar, List
import uuid
from datetime import datetime

from sqlalchemy import (
    Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..schemas.base import Role
from ..database.main import Base 

class User(Base):
    __tablename__ = "users"

    ID: ClassVar[str] = "id"
    USERNAME: ClassVar[str] = "username"
    FIRST_NAME: ClassVar[str] = "firstName"
    LAST_NAME: ClassVar[str] = "lastName"
    EMAIL: ClassVar[str] = "email"
    PASSWORD: ClassVar[str] = "password"
    EMAIL_VERIFIED: ClassVar[str] = "email_verified"
    PHONE_VERIFIED: ClassVar[str] = "phone_verified"
    ROLE: ClassVar[str] = "role"
    IS_ACTIVE: ClassVar[str] = "is_active"
    CREATED_AT: ClassVar[str] = "created_at"
    UPDATED_AT: ClassVar[str] = "updated_at"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    bio = Column(String, nullable=False)
    location = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    email_verified = Column(Boolean, nullable=False, default=False)
    password = Column(String(15), nullable=False)
    role = Column(String, nullable=False, default=Role.STUDENT.value)
    is_active = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'), nullable=False)

    # Relationships 
    notifications = relationship("Notification", back_populates="user", passive_deletes=True, cascade="all, delete")
    courses = relationship("Course", back_populates="students", secondary="enrollments")
    payments = relationship("Payment", back_populates="student", passive_deletes=True, cascade="all, delete")