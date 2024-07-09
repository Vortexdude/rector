from fastapi import FastAPI
from app.core.config import settings
from app.api import api_router
from app.api import models
from app.core.db import engine


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
models.Base.metadata.create_all(bind=engine)
app.include_router(api_router)
