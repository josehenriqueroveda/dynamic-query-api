import logging
import os
from urllib.parse import quote_plus

from dotenv import find_dotenv
from dotenv import load_dotenv


class Settings:
    load_dotenv(find_dotenv())
    # [Logging]
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )
    logger = logging.getLogger(__name__)

    # [Project]
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    DESCRIPTION: str = os.getenv("DESCRIPTION")
    API_V1_STR: str = "/api/v1"
    API_PORT: int = int(os.getenv("API_PORT"))
    VERSION: str = os.getenv("VERSION")

    # [Security]
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    BACKEND_CORS_ORIGINS: list = (
        ["*"]
        if os.getenv("BACKEND_CORS_ORIGINS") is None
        else os.getenv("BACKEND_CORS_ORIGINS").split(",")
    )

    # [Database]
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: int = (
        5432 if os.getenv("POSTGRES_PORT") is None else int(os.getenv("POSTGRES_PORT"))
    )
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = quote_plus(os.getenv("POSTGRES_PASSWORD"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")

    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"


settings = Settings()
