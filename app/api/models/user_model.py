from pydantic import BaseModel
from pydantic import field_validator


class User(BaseModel):
    username: str
    password: str
    is_admin: bool = False
    is_active: bool = True

    @field_validator("username")
    def validate_username(cls, username: str) -> str:
        if len(username) < 5:
            raise ValueError("Username must be at least 5 characters long")
        if not username.islower():
            raise ValueError("Username must be in lowercase")
        if not username.isalpha():
            raise ValueError("Username must contain only alphabetic characters")
        return username

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        if len(password) < 10:
            raise ValueError("Password must be at least 10 characters long")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        return password
