from fastapi import APIRouter
from app.api.routes.transform_image.main import router as img_router
from app.api.routes.users.main import router as user_router
from app.api.routes.auth.main import router as AuthRouter

api_router = APIRouter()
api_router.include_router(img_router, tags=["Image Manipulation"])
api_router.include_router(user_router, tags=["User Authentication"])
api_router.include_router(AuthRouter, tags=["Auth Router"])
