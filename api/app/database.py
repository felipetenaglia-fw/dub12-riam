from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import get_settings

settings = get_settings()

# Create engine with SQLite in-memory database
# Using check_same_thread=False for SQLite to work with FastAPI's async nature
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=settings.debug
)

# Disable foreign key enforcement at the database level (as requested)
# We'll handle consistency in the application code
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Disable foreign key enforcement for SQLite."""
    if "sqlite" in settings.database_url:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=OFF")
        cursor.close()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    # Import all models to ensure they're registered with Base.metadata
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
