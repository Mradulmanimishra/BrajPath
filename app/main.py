from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.webhook import router as webhook_router
from app.db.models import Base
from app.db.session import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("brajpath.app")


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        logger.exception("Database initialization failed during startup")
    yield


app = FastAPI(
    title="BrajPath",
    description="A multilingual WhatsApp assistant for temple guidance in Mathura and Vrindavan",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

app.include_router(webhook_router, tags=["WhatsApp"])


@app.get("/", tags=["Health"])
def health():
    return {"status": "ok", "service": "BrajPath", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
