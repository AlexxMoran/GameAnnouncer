from fastapi.concurrency import asynccontextmanager
import uvicorn
from fastapi import FastAPI
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
