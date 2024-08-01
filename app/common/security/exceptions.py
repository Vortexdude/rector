from starlette import status
from starlette.exceptions import HTTPException

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate Credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
