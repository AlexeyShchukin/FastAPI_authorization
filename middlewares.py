from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi import Request

from loggers.loggers import logger

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.now()
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        process_time = datetime.now() - start_time
        logger.info(f"Response: {response.status_code} (handling {process_time.total_seconds():.4f} seconds)")

        return response
