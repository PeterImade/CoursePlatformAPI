from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Table, Column, ForeignKey

from ..database.main import Base

class StudentCourse(DeclarativeBase):
    student_course_association = Table(
        "student_course",
        Base.metadata,
        Column("student_id", ForeignKey("students.id"), primary_key=True),
        Column("course_id", ForeignKey("courses.id"), primary_key=True)
    )