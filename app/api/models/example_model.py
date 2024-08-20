from datetime import date
from typing import List

from pydantic import BaseModel


class ExampleModel(BaseModel):
    x_date: date
    x_mandatory_string: str
    x_optional_string: str | None = None
    x_optional_int: int | None = None
    x_optional_list: List[str] | None = None
