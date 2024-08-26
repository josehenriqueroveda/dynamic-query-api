from typing import Any
from typing import List
from typing import Union

from pydantic import BaseModel


class FilterCondition(BaseModel):
    """
    Represents a single filter condition for a database query.
    """

    field: str
    operator: str  # "eq", "ne", "in"
    value: Union[str, int, float, List[Any]]


class QueryParameters(BaseModel):
    """
    Defines the dynamic query parameters for a database query.
    """

    select_fields: List[str]
    table_name: str
    db_schema: str | None = None
    sort_by: str | None = None
    sort_order: str | None = "asc"  # Default to "asc"
    filters: List[FilterCondition] | None = None
