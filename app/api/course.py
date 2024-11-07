from uuid import UUID
from typing import Annotated, List
from fastapi import APIRouter, Depends, status

from ..core.tokens import get_verified_current_user
from ..models.auth_user import User
from ..dependencies.services import get_course_service
from ..schemas.course import CourseCreate, CourseResponse, CourseUpdate
from ..services.course_service import CourseService
from ..core.role_checker import RoleChecker
from ..schemas.base import Role

router = APIRouter(prefix="/api/v1/courses", tags=["Course"])
role_checker = RoleChecker([Role.INSTRUCTOR.value])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CourseResponse)
async def create_course(
    data_obj: CourseCreate,
    course_service: Annotated[CourseService, Depends(get_course_service)],
    check_role: bool = Depends(role_checker)
):
    return await course_service.create_course(data_obj=data_obj)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CourseResponse)
async def get_course(
    id: UUID,
    course_service: Annotated[CourseService, Depends(get_course_service)],
    current_user: User = Depends(get_verified_current_user),
):
    return await course_service.get_course(course_id=id)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CourseResponse])
async def get_courses( 
    course_service: Annotated[CourseService, Depends(get_course_service)],
    current_user: User = Depends(get_verified_current_user)
):
    return await course_service.get_courses_from_cache_or_db()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course( 
    id: UUID,
    course_service: Annotated[CourseService, Depends(get_course_service)],
    check_role: bool = Depends(role_checker)
):
    return await course_service.delete_course(course_id=id)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=CourseResponse)
async def update_course( 
    id: UUID,
    data_obj: CourseUpdate,
    course_service: Annotated[CourseService, Depends(get_course_service)],
    check_role: bool = Depends(role_checker)
):
    return await course_service.update_course(course_id=id, data_obj=data_obj)

