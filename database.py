from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Railway PostgreSQL URLs start with postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine - use SQLite for local dev if no DATABASE_URL
if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
else:
    # Local development fallback
    engine = create_engine("sqlite:///./local.db")
    print("⚠️  Using SQLite for local development. Set DATABASE_URL to use PostgreSQL.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()