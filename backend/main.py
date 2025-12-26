from fastapi.concurrency import asynccontextmanager
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tasks.broker import startup_broker, shutdown_broker
from core.initializers import initialize_all
from core.middleware.request_logging_middleware import RequestLoggingMiddleware
from exceptions import EXCEPTION_HANDLERS, API_RESPONSES
from core.config import get_settings
from core.logger import setup_logging, logger
from api import router as api_router
from core.db.container import create_db

setup_logging()

db = create_db()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting GameAnnouncer API...")
    initialize_all()
    await startup_broker()

    yield

    await shutdown_broker()
    logger.info("🛑 Shutting down GameAnnouncer API...")
    await db.dispose()


app = FastAPI(
    lifespan=lifespan,
    responses=API_RESPONSES,
)

for exc_class, handler in EXCEPTION_HANDLERS:
    app.add_exception_handler(exc_class, handler)

app.add_middleware(RequestLoggingMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")

if settings.cors.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.all_cors_origins,
        allow_credentials=settings.cors.allow_credentials,
        allow_methods=settings.cors.allow_methods,
        allow_headers=settings.cors.allow_headers,
    )

app.include_router(api_router, prefix=settings.api.prefix)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)

logger.info("🎮 GameAnnouncer API initialized")
