from __future__ import annotations
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TIMESTAMP, UUID, Table, Column, ForeignKey, text

from ..database.main import Base

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, index=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), primary_key=True, index=True)
    enrollment_date = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)