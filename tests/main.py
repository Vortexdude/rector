from app.main import app
from app.core.config import settings
from fastapi.testclient import TestClient

client = TestClient(app)
API_VERSION = settings.API_V1_STR


def test_docs_path():
    response = client.get(f"{API_VERSION}/docs")
    assert response.status_code == 200


def test_redoc_path():
    response = client.get(f"{API_VERSION}/redocs")
    assert response.status_code == 200


def test_openapi_path():
    response = client.get(f"{API_VERSION}/openapi")
    assert response.status_code == 200


def test_me_route():
    response = client.get(f"{API_VERSION}/me")
    if settings.ENV == 'dev':
        assert response.status_code == 200
        assert response.json() == {"status": "done"}
    if settings.ENV == 'prod':
        assert response.status_code == 401
