from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI


class Middleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
