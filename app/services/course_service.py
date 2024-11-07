import json
from typing import List
from uuid import UUID

from redis import Redis
from app.core.exceptions import CourseNotFound
from app.models.course import Course
from app.repositories.course import CRUDCourse
from app.schemas.course import CourseCreate, CourseUpdate
from ..core.logger import get_logger
from ..core.config import Config

logger = get_logger(__name__)

class CourseService:
    def __init__(self, crud_course: CRUDCourse, redis_client: Redis):
        self.crud_course = crud_course
        self.redis_client = redis_client

    async def generate_cache_key(self):
        return "courses_list"
    
    async def create_course(self, data_obj: CourseCreate) -> Course:
        logger.info("Creating course..........")
        course = self.crud_course.create(data_obj=data_obj)
        logger.info(f"Course created successfully..........\ncourse: {course}")
        return course
    
    async def get_course(self, course_id: UUID) -> Course:
        logger.info("Fetching a course..........")
        course = self.crud_course.get_course_or_raise_exception(id=course_id)
        logger.info("Course retrieved successfully..........")
        return course
    
    async def get_courses_from_cache_or_db(self) -> List[Course]:
        # Check cache first
        cache_key = self.generate_cache_key()
        cached_courses = await self.redis_client.get(cache_key)

        if cached_courses:
            # Return cached courses if available
            return json.loads(cached_courses)  # Deserialize JSON back into list of dicts
    
        # If cache not found, fetch from the database
        courses = self.crud_course.get_all()
        
        logger.info("Fetching all courses..........")
        if not courses:
            raise CourseNotFound()
        logger.info("Courses retrieved successfully..........")

        # Store the courses in cache for subsequent requests
        await self.redis_client.setex(cache_key, Config.CACHE_EXPIRY, courses)
        return courses
    
    async def delete_course(self, course_id: UUID) -> bool:
        course = self.crud_course.get_course_or_raise_exception(id=course_id) 
        return self.crud_course.delete(id=course.id)
    
    async def update_course(self, course_id: UUID, data_obj: CourseUpdate) -> Course:
        logger.info("Fetching course to be updated..........")
        course = self.crud_course.get_course_or_raise_exception(id=course_id) 
        updated_course = self.crud_course.update(id=course.id, data_obj=data_obj)
        logger.info(f"Course updated successfully..........\nupdated_course: f{updated_course}")
        return updated_course