from fastapi.concurrency import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api import router as api_router
from core.db import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here (if any)
    yield
    # Shutdown code here (if any)
    await db.dispose()


app = FastAPI(
    lifespan=lifespan,
)

if settings.cors.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.all_cors_origins,
        allow_credentials=settings.cors.allow_credentials,
        allow_methods=settings.cors.allow_methods,
        allow_headers=settings.cors.allow_headers,
    )

app.include_router(
    api_router,
    prefix=settings.api.prefix
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port, 
        reload=True
    )
