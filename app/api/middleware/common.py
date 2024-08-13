from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware


class Middleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
