from __future__ import annotations
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TIMESTAMP, UUID, Table, Column, ForeignKey, text

from ..database.main import Base

# enrollments = Table(
#     "enrollments_table",
#     Base.metadata,
#     Column("student_id", UUID(as_uuid=True), ForeignKey("students.id"), primary_key=True),
#     Column("course_id", UUID(as_uuid=True), ForeignKey("courses.id"), primary_key=True),
#     Column("enrollment_date", TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False),
# )

class Enrollment(Base):
    __tablename__ = "enrollments"
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id"), primary_key=True, index=True)
    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"), primary_key=True, index=True)
    enrollment_date:Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)

    student: Mapped["Student"] = relationship(back_populates="enrollments")
    course: Mapped["Course"] = relationship(back_populates="enrollments")