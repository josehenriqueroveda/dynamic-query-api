from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel


class FilterCondition(BaseModel):
    field: str
    operator: str  # "eq", "ne", "in"
    value: Union[str, int, float, List[Any]]


class DynamicQueryParams(BaseModel):
    select_fields: List[str]
    table: str
    schema: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = None  # "asc" or "desc"
    filters: Optional[List[FilterCondition]] = None
