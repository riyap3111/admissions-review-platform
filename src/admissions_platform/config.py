"""Shared paths and constants for the Admissions Review Platform.

Centralized here so every module agrees on where things live, matching the
pattern used in the sibling Student Retention System project.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
HANDBOOKS_DIR = DATA_DIR / "handbooks"
CATALOG_FIXTURES_DIR = DATA_DIR / "catalog_fixtures"

STORAGE_DIR = PROJECT_ROOT / "storage"  # local-disk document storage (see storage/local.py)

DB_DIR = PROJECT_ROOT / "db"
DB_PATH = DB_DIR / "admissions.db"  # SQLite fallback for fast local tests only

RANDOM_SEED = 42

for _dir in (DATA_DIR, HANDBOOKS_DIR, CATALOG_FIXTURES_DIR, STORAGE_DIR, DB_DIR):
    _dir.mkdir(parents=True, exist_ok=True)
