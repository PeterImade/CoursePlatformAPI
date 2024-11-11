from fastapi import APIRouter
from .auth import router as auth_router
from .course import router as course_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(course_router)