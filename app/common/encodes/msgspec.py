import msgspec
from typing import Any
from starlette.responses import JSONResponse


class MsgSpecJsonResponse(JSONResponse):
    """
    Json Response using high-performance msgspec library to serialize data into JSON
    """

    def render(self, content: Any) -> bytes:
        return msgspec.json.encode(content)
