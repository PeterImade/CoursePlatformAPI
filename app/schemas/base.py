from enum import Enum

class Role(str, Enum):
    STUDENT = "Student"
    INSTRUCTOR = "Instructor"
    ADMIN = "Admin"
