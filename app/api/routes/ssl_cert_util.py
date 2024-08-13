from fastapi import APIRouter
from app.api.services.ssl import SSLExtractor
from starlette.requests import Request
TAGS = ['utils']

router = APIRouter(tags=TAGS)


@router.get("/ssl_cert")
def get_ssl_cert_details(domain: str):
    return SSLExtractor.get_detail(domain)


@router.get("whatsmyip")
def get_ip(request: Request):
    print(request.client[0])
    return {"request": "done"}
