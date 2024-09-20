import os
import sys

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

Base = declarative_base()
metadata = MetaData()


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    pool_size=5,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
ScopedSession = scoped_session(SessionLocal)


def get_db():
    """
    Dependency that provides a SQLAlchemy session for a single request,
    closing it once the request is completed.
    """
    db = ScopedSession()
    try:
        yield db
    finally:
        db.close()


def get_table(table_name: str, db_schema: str | None = None):
    """
    Retrieve the SQLAlchemy Table object based on the table name and schema.
    """
    try:
        return Table(table_name, metadata, schema=db_schema, autoload_with=engine)
    except NoSuchTableError:
        raise HTTPException(status_code=500, detail="Table not found")
