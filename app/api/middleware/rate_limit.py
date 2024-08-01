from fastapi import FastAPI
from .common import Middleware
from app.core.config import settings
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
from app.common.utils.timezone import timezone

__all__ = ["RateLimitMiddleware"]


class RateLimitMiddleware(Middleware):

    # Rate limiting configurations
    RATE_LIMIT_DURATION = timezone.timedelta(minutes=1)
    RATE_LIMIT_REQUEST = settings.API_REQUEST_PER_MINUTE

    def __init__(self, app: FastAPI):
        super().__init__(app)
        # Dictionary to store request counts for each IP
        self.request_count = {}

    async def dispatch(self, request: Request, call_next) -> Response:

        # skip the route for video stream paths
        for un_auth_filter in settings.UNAUTHENTICATED_FILTER:
            if un_auth_filter in request.url.path:
                return await call_next(request)

        # Get the client's IP address
        _client_ip = request.client.host
        # Check if IP is already present in request_counts
        request_count, last_request = self.request_count.get(_client_ip, (0, timezone.min))

        # Calculate the time elapsed since the last request
        elapse_time = timezone.now_tz - last_request
        if elapse_time > self.RATE_LIMIT_DURATION:
            # If the elapsed time is greater than the rate limit duration, reset the count
            request_count = 1
        else:
            if request_count >= self.RATE_LIMIT_REQUEST:
                # If the request count exceeds the rate limit, return a JSON response with an error message
                return JSONResponse(
                    status_code=429,
                    content={"message": "Rate limit exceeded. Please try again later."}
                )
            request_count += 1

        # Update the request count and last request timestamp for the IP
        self.request_count[_client_ip] = (request_count, timezone.now_tz)

        # Proceed with the request
        return await call_next(request)
