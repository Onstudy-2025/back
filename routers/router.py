from fastapi import APIRouter
from .user import router as user_router  
from .lesson import router as lesson_router 
from .tests import router as tests_router 
api_router = APIRouter()

api_router.include_router(user_router, tags=["authentication"])
api_router.include_router(lesson_router , tags=["Courses"])
# api_router.include_router(tests_router , tags=["Tests"])
