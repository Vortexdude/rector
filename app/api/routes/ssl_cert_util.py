from fastapi import APIRouter
from app.api.services.ssl import SSLExtractor

TAGS = ['utils']

router = APIRouter(tags=TAGS)


@router.get("/ssl_cert")
def get_ssl_cert_details(domain: str):
    return SSLExtractor.get_detail(domain)


@router.get("/generate_thumb")
def thumb_gen():
    return {"status": "done"}
