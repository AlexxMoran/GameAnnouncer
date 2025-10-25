import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        client_ip = request.client.host if request.client else "unknown"

        logger.info(
            f"📥 {request.method} {request.url.path} | IP: {client_ip} | User-Agent: {request.headers.get('user-agent', 'unknown')[:50]}..."
        )

        try:
            response = await call_next(request)

            duration = round((time.time() - start_time) * 1000, 2)

            logger.info(
                f"📤 {request.method} {request.url.path} | Status: {response.status_code} | Duration: {duration}ms"
            )

            return response

        except Exception as e:
            duration = round((time.time() - start_time) * 1000, 2)

            logger.error(
                f"💥 {request.method} {request.url.path} | ERROR: {str(e)} | Duration: {duration}ms"
            )

            raise
