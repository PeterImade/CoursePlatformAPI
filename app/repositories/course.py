from typing import Optional
from fastapi import Depends
from app.core.exceptions import CourseNotFound
from app.database.main import get_db
from app.models.course import Course
from app.repositories.base import CRUDBASE
from app.schemas.course import CourseCreate, CourseUpdate


class CRUDCourse(CRUDBASE[Course, CourseCreate, CourseUpdate]): 
    def get_course_or_raise_exception(self, id) -> Course:
            query_result = self._db.query(self.model).filter(self.model.id == id).first()
            if not query_result:
                raise CourseNotFound()
            return query_result
    
    def get_all_courses(self, limit = 10, search: Optional[str] = "") -> Optional[list[Course]]: 
        data_obj = self.db.query(self.model.title.contains(search.lower())).limit(limit).all()
        return data_obj
    

def get_crud_course(db=Depends(get_db)) -> CRUDCourse:
    return CRUDCourse(db=db, model=Course)
