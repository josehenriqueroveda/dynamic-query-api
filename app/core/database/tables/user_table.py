from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.core.database.db import Base


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column("username", String(50), unique=True, nullable=False)
    password = Column("password", String(50), nullable=False)
    is_admin = Column("is_admin", Boolean, nullable=False, server_default="0")
    is_active = Column("is_active", Boolean, nullable=False, server_default="1")
