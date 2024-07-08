import os


class BaseConf(object):
    API_TITLE = os.environ.get('API_TITLE', "Image Manipulation")
    API_VERSION = os.environ.get('API_VERSION', "1.0")
    OPENAPI_VERSION = os.environ.get('OPENAPI_VERSION', "3.0.3")
    OPENAPI_URL_PREFIX = os.environ.get('OPENAPI_URL_PREFIX', "/")
    OPENAPI_SWAGGER_UI_PATH = os.environ.get('OPENAPI_SWAGGER_UI_PATH', "/swagger-ui")
    OPENAPI_SWAGGER_UI_URL = os.environ.get('OPENAPI_SWAGGER_UI_URL', "https://cdn.jsdelivr.net/npm/swagger-ui-dist/")
    ENABLE_MODULES = ["IMGPROC"]


class DevConfing(BaseConf):
    pass


class ProdConfing(BaseConf):
    pass


class TestConfig(BaseConf):
    pass


CONF_MAPPING = {
    "dev": DevConfing,
    "test": TestConfig,
    "prod": ProdConfing
}
