"""Tests for the database engine factory: defaults to SQLite, switches to
PostgreSQL when DATABASE_URL is set."""
import importlib

import admissions_platform.db as db_module


def test_defaults_to_sqlite_when_database_url_unset(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    importlib.reload(db_module)
    try:
        engine = db_module.get_engine()
        assert engine.dialect.name == "sqlite"
        assert db_module.is_postgres(engine) is False
    finally:
        importlib.reload(db_module)


def test_uses_postgres_when_database_url_set(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg2://user:pass@localhost/dbname")
    importlib.reload(db_module)
    try:
        engine = db_module.get_engine()
        assert engine.dialect.name == "postgresql"
        assert db_module.is_postgres(engine) is True
    finally:
        monkeypatch.delenv("DATABASE_URL", raising=False)
        importlib.reload(db_module)


def test_get_session_returns_a_working_session(monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'session_test.db'}")
    importlib.reload(db_module)
    try:
        from admissions_platform.models import Base

        Base.metadata.create_all(db_module.get_engine())
        session = db_module.get_session()
        assert session.bind is not None
        session.close()
    finally:
        monkeypatch.delenv("DATABASE_URL", raising=False)
        importlib.reload(db_module)
