from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


def _normalized_database_url(raw_url: str) -> str:
    if raw_url.startswith("postgresql://"):
        return raw_url.replace("postgresql://", "postgresql+pg8000://", 1)
    return raw_url


database_url = _normalized_database_url(settings.DATABASE_URL)
engine_kwargs: dict[str, object] = {"pool_pre_ping": True}
if database_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(database_url, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
