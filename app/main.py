from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.webhook import router as webhook_router
from app.config import settings
from app.db.models import Base
from app.db.session import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("brajpath.app")


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Application lifecycle: startup and shutdown."""
    # Startup
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created or verified")
    except Exception as e:
        logger.exception("❌ Database initialization failed: %s", e)
        raise

    # Validate production config
    if settings.APP_ENV == "production":
        try:
            settings.validate_prod_config()
            logger.info("✅ Production configuration validated")
        except AssertionError as e:
            logger.error("❌ Production config missing: %s", e)
            raise
            
    yield
    
    # Shutdown (cleanup if needed)
    logger.info("Application shutting down")


app = FastAPI(
    title="BrajPath",
    description="A multilingual WhatsApp assistant for temple guidance in Mathura and Vrindavan",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS if settings.ALLOWED_ORIGINS else [],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

app.include_router(webhook_router, tags=["WhatsApp"])


@app.get("/", tags=["Health"])
@app.get("/health", tags=["Health"])
def health():
    """Health check endpoint. Returns application status."""
    return {"status": "ok", "service": "BrajPath", "version": "1.0.0"}
