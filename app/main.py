from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import api_config, cors_config
from app.db.base import create_tables
from app.api import api_router

@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_tables()
    yield

app = FastAPI(
    lifespan=lifespan,
    title=api_config.title,
    version=api_config.version,
    description=api_config.description,
    contact=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)