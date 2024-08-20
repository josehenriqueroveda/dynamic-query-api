from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

import jwt
from core.config import settings
from passlib.context import CryptContext
from slowapi import Limiter
from slowapi.util import get_remote_address


class RequestLimiter:
    def __init__(self):
        self.limiter = Limiter(key_func=get_remote_address)

    def get_limiter(self):
        return self.limiter


request_limiter = RequestLimiter()


class AccessTools:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, subject: str | Any, expires_delta: timedelta) -> str:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
