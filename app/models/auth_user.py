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

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    firstName: Mapped[str] = mapped_column(nullable=False)
    lastName: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    email_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    password: Mapped[str] = mapped_column(String(15), nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, default=Role.STUDENT.value)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'), nullable=False)


    # Relationships
    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False)
    student: Mapped["Student"] = relationship(back_populates="user", uselist=False)
    instructor: Mapped["Instructor"] = relationship(back_populates="user", uselist=False)
    notifications: Mapped[List["Notification"]] = relationship(back_populates="user", passive_deletes=True, cascade="all, delete")