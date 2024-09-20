import os
from datetime import datetime
from datetime import timedelta

from dotenv import find_dotenv
from dotenv import load_dotenv
from fastapi import status
from fastapi.exceptions import HTTPException
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.models.user_model import User
from app.core.database.tables.token_table import TokenTable
from app.core.database.tables.user_table import UserTable

load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
crypt_context = CryptContext(schemes=["sha256_crypt"])


class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def register(self, user: User):
        user_model = UserTable(
            username=user.username,
            password=crypt_context.hash(user.password),
            is_admin=user.is_admin,
            is_active=True,
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

    def user_login(self, user: User, expires_in: int = 3600):
        user_on_db = (
            self.db_session.query(UserTable).filter_by(username=user.username).first()
        )
        if not user_on_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        exp = datetime.now() + timedelta(minutes=expires_in)

        payload = {
            "sub": user.username,
            "exp": exp,
        }
        try:
            access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create access token",
            )

        return {
            "user_id": user_on_db.id,
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": str(exp),
        }

    def user_logout(self, user: User):
        token = self.db_session.query(TokenTable).filter_by(user_id=user.id).first()
        if token:
            self.db_session.delete(token)
            self.db_session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not logged in",
            )

    def verify_token(self, access_token: str):
        token_record = (
            self.db_session.query(TokenTable).filter_by(token=access_token).first()
        )
        if not token_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        user_on_db = (
            self.db_session.query(UserTable).filter_by(username=data["sub"]).first()
        )
        if not user_on_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return user_on_db

    def delete(self, username: str):
        user_model = (
            self.db_session.query(UserTable).filter_by(username=username).first()
        )
        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist"
            )
        else:
            user_model.is_active = False
            self.db_session.commit()

    def change_password(self, username: str, old_password: str, new_password: str):
        user_model = (
            self.db_session.query(UserTable).filter_by(username=username).first()
        )
        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist"
            )
        elif not crypt_context.verify(old_password, user_model.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect current password",
            )
        else:
            user_model.password = crypt_context.hash(new_password)
            self.db_session.commit()
