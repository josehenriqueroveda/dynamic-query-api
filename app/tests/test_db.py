import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text

load_dotenv(dotenv_path="../.env")

PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = quote_plus(os.getenv("PG_PASSWORD"))

database_url = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}"


def test_connection():
    try:
        engine = create_engine(database_url)
        connection = engine.connect()
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1
        connection.close()
        print("Connection successful")
    except Exception as e:
        print(e)


test_connection()
