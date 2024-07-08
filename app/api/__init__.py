from fastapi import APIRouter
from app.api.routes import manipulation, users

api_router = APIRouter()
api_router.include_router(manipulation.router, tags=["Image Manipulation"])
api_router.include_router(users.router, tags=["User Authentication"])
