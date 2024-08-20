from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
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
