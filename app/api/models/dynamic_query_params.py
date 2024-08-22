from typing import Any
from typing import List
from typing import Optional
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
    db_schema: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "asc"  # Default to "asc"
    filters: Optional[List[FilterCondition]] = None
