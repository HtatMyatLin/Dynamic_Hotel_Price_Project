"""
SQLite database connection and session management.
Week 2: Database layer for Hotel Pricing Support System.
"""
import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Database configuration
DATABASE_URL = "sqlite:///hotel_pricing.db"
# For absolute path in development
_DB_FILE = os.path.join(os.path.dirname(__file__), "hotel_pricing.db")
DATABASE_URL_ABS = f"sqlite:///{_DB_FILE}"

# Create engine with echo=False for production; set to True for debugging
engine = create_engine(
    DATABASE_URL_ABS,
    connect_args={"check_same_thread": False},  # Required for SQLite
    echo=False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    Ensures proper cleanup after request completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database sessions (non-FastAPI contexts).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database tables.
    Call this once at application startup.
    """
    # Import all models to ensure they are registered with Base
    from backend import models  # noqa: F401
    Base.metadata.create_all(bind=engine)


def check_db_exists() -> bool:
    """Check if the database file exists."""
    return os.path.exists(_DB_FILE)