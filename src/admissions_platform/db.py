"""Database engine/session factory.

Same abstraction as the sibling Student Retention System project: PostgreSQL
when DATABASE_URL is set (the real target here, via Docker Compose), SQLite
otherwise — fast, dependency-free unit tests through the identical code path
every other module uses, never a second maintained path.
"""
from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from admissions_platform.config import DB_PATH

DATABASE_URL = os.environ.get("DATABASE_URL")

_engine: Engine | None = None
_SessionFactory: sessionmaker | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL or f"sqlite:///{DB_PATH}")
    return _engine


def is_postgres(engine: Engine) -> bool:
    return engine.dialect.name == "postgresql"


def get_session() -> Session:
    global _SessionFactory
    if _SessionFactory is None:
        _SessionFactory = sessionmaker(bind=get_engine(), expire_on_commit=False)
    return _SessionFactory()


def reset_engine_cache() -> None:
    """Tests that change DATABASE_URL mid-process need a fresh engine/session
    factory rather than the module-level singleton above."""
    global _engine, _SessionFactory
    _engine = None
    _SessionFactory = None
