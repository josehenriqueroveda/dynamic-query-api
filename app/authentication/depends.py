from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session as SQLAlchemySession

from app.authentication.auth import UserUseCases
from app.core.database.db import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def token_is_valid(
    db_session: SQLAlchemySession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    uc = UserUseCases(db_session)
    return uc.verify_token(token)


def get_current_user(
    db_session: SQLAlchemySession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    uc = UserUseCases(db_session)
    user = uc.verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
