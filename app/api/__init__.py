from fastapi import APIRouter
from app.api.routes import manipulation

api_router = APIRouter()
api_router.include_router(manipulation.router, tags=["Image Manipulation"])
