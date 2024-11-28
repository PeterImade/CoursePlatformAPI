from uuid import UUID
from fastapi import APIRouter, Depends, status

from app.core.tokens import get_verified_current_user
from app.dependencies.services import get_auth_user_service
from app.models.auth_user import User
from app.schemas.base import Role
from app.schemas.user import UserProfile, UserProfileUpdate
from app.services.auth_user_service import AuthUserService
from app.core.role_checker import RoleChecker

role_checker = RoleChecker([Role.INSTRUCTOR.value, Role.STUDENT.value])

router = APIRouter(prefix="/api/v1/users", tags=["User"])

@router.get("/{user_id}", status_code= status.HTTP_200_OK, response_model=UserProfile)
async def get_user(
    user_id: UUID, 
    auth_user_service: AuthUserService = Depends(get_auth_user_service),
    current_user: User = Depends(get_verified_current_user)
):
    return await auth_user_service.get_user_by_id(user_id=user_id)

@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserProfile)
async def update_user_profile(
    user_id: UUID,
    data_obj: UserProfileUpdate,
    auth_user_service: AuthUserService = Depends(get_auth_user_service),
    current_user: User = Depends(get_verified_current_user),
):
    return await auth_user_service.update_user_profile(user_id=user_id, data_obj=data_obj)

@router.get("/{user_id}/courses", status_code=status.HTTP_200_OK)
async def get_courses_created_by_instructor(
    user_id: UUID,
    data_obj: UserProfileUpdate,
    auth_user_service: AuthUserService = Depends(get_auth_user_service),
    current_user: User = Depends(get_verified_current_user),
):
    pass