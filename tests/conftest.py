"""Shared pytest fixtures for all test modules."""
from __future__ import annotations

from collections.abc import Iterable

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.models import Base
from app.db.seed import (
    seed_banke_bihari,
    seed_iskcon_vrindavan,
    seed_partner_categories,
    seed_prem_mandir,
    seed_route_points,
)


@pytest.fixture()
def db_session() -> Iterable[Session]:
    """Create an in-memory SQLite database for testing with seeded data."""
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    seed_route_points(session)
    seed_partner_categories(session)
    seed_banke_bihari(session)
    seed_prem_mandir(session)
    seed_iskcon_vrindavan(session)
    session.commit()

    try:
        yield session
    finally:
        session.close()
        engine.dispose()
