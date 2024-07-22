from starlette.exceptions import HTTPException
from starlette import status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate Credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
